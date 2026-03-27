# “””
AΩ+ Reasoning Stability Field – Apple Silicon (MPS) Optimized

S = ΔΨ - λ·‖∇Ψ‖²  per sentence, using token embeddings.

Optimizations vs previous version:

- True batched Hutchinson with padding mask (no sentence-by-sentence loop)
- MPS-aware: autograd second-order ops run on CPU to avoid MPS limitations,
  embeddings and forward passes on MPS
- Async batch prefetch via threading
- Streaming CSV write (no full dataset in RAM)
- Reproducible Rademacher sampling with seeded generator
  “””

import torch
import heapq
import gc
import csv
import threading
import queue
import functools
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================================

# Configuration

# ============================================================================

INPUT_FILE      = “dataset.txt”
OUTPUT_CSV      = “stability_scores_mps.csv”
BATCH_SIZE      = 32          # larger batches for MPS throughput
LAMBDA_STAB     = 1.0
M_HUTCHINSON    = 20
MAX_SEQ_LENGTH  = 128
TOP_N_VISUAL    = 20
SAVE_PLOT       = “stability_top_mps.png”
RANDOM_SEED     = 42
PREFETCH_BATCHES = 2          # how many batches to prefetch ahead

# ============================================================================

# Device setup

# MPS is used for embedding inference.

# Hutchinson (second-order autograd) runs on CPU — MPS does not support

# create_graph=True reliably across all ops as of PyTorch 2.x.

# ============================================================================

if torch.backends.mps.is_available():
mps_device  = torch.device(“mps”)
grad_device = torch.device(“cpu”)   # second-order autograd
print(“Device: MPS (inference) + CPU (autograd second-order)”)
else:
mps_device  = torch.device(“cpu”)
grad_device = torch.device(“cpu”)
print(“MPS not available — running fully on CPU”)

torch.manual_seed(RANDOM_SEED)
rng = torch.Generator(device=“cpu”)
rng.manual_seed(RANDOM_SEED)

# ============================================================================

# Model

# ============================================================================

model = SentenceTransformer(‘all-MiniLM-L6-v2’, device=mps_device)
model.max_seq_length = MAX_SEQ_LENGTH

# ============================================================================

# Token embedding extraction → padded tensor on grad_device

# Returns:

# padded  [B, L_max, D]  float32 on grad_device

# lengths [B]            int64   on grad_device

# ============================================================================

def get_padded_embeddings(texts: list[str]):
raw = model.encode(
texts,
convert_to_tensor=False,
output_value=‘token_embeddings’,
show_progress_bar=False,
)
B   = len(raw)
D   = raw[0].shape[1]
lengths = torch.tensor([min(e.shape[0], MAX_SEQ_LENGTH) for e in raw],
dtype=torch.long, device=grad_device)
padded = torch.zeros(B, MAX_SEQ_LENGTH, D,
dtype=torch.float32, device=grad_device)
for i, emb in enumerate(raw):
L = lengths[i].item()
padded[i, :L] = torch.as_tensor(emb[:L], dtype=torch.float32,
device=grad_device)
return padded, lengths

# ============================================================================

# Padding mask  [B, L_max]  bool

# ============================================================================

def make_mask(lengths: torch.Tensor, L_max: int) -> torch.Tensor:
idx = torch.arange(L_max, device=lengths.device)          # [L_max]
return idx.unsqueeze(0) < lengths.unsqueeze(1)             # [B, L_max]

# ============================================================================

# Batched potential field  Ψ(x)

# x       : [B, L_max, D]  (requires_grad may be True)

# lengths : [B]

# returns : [B]  scalar potential per sentence

# ============================================================================

def potential_field_batch(x: torch.Tensor,
lengths: torch.Tensor) -> torch.Tensor:
B, L_max, D = x.shape
mask   = make_mask(lengths, L_max)                         # [B, L_max]

```
# L2-normalise along D, zero-out padding
norms  = x.norm(dim=-1, keepdim=True).clamp(min=1e-8)     # [B, L_max, 1]
x_norm = (x / norms) * mask.unsqueeze(-1).float()         # [B, L_max, D]

# Batched cosine similarity matrix  [B, L_max, L_max]
sim    = torch.bmm(x_norm, x_norm.transpose(1, 2))

# Zero diagonal
eye    = torch.eye(L_max, device=x.device).unsqueeze(0)   # [1, L_max, L_max]
sim    = sim * (1.0 - eye)

# Zero out padding rows/cols
pmask  = mask.unsqueeze(2).float() * mask.unsqueeze(1).float()  # [B, L, L]
sim    = sim * pmask

# Normalise by number of valid pairs
n_pairs = lengths.float() * (lengths.float() - 1)         # [B]
n_pairs = n_pairs.clamp(min=1.0)

return sim.sum(dim=(1, 2)) / n_pairs                       # [B]
```

# ============================================================================

# Batched gradient norm²

# Returns [B] — uses a fresh graph, safe to call independently

# ============================================================================

def batched_grad_norm_sq(padded: torch.Tensor,
lengths: torch.Tensor) -> torch.Tensor:
x = padded.clone().detach().requires_grad_(True)
psi = potential_field_batch(x, lengths)          # [B]
# Sum over batch → single scalar so grad flows to all sentences
psi.sum().backward()
mask  = make_mask(lengths, padded.shape[1])      # [B, L_max]
g     = x.grad * mask.unsqueeze(-1).float()      # zero padding grads
return g.pow(2).sum(dim=(1, 2)).detach()         # [B]

# ============================================================================

# Batched Hutchinson trace estimator

# ΔΨ ≈ (1/m) Σ_k  vᵏᵀ H vᵏ   where vᵏ ~ Rademacher

# Returns [B]

# ============================================================================

def batched_hutchinson(padded: torch.Tensor,
lengths: torch.Tensor,
m: int = M_HUTCHINSON) -> torch.Tensor:
B, L_max, D = padded.shape
mask   = make_mask(lengths, L_max).unsqueeze(-1).float()   # [B, L_max, 1]

```
x      = padded.clone().detach().requires_grad_(True)
psi    = potential_field_batch(x, lengths)                  # [B]

# First-order gradients with graph retained for Hessian-vector products
grads  = torch.autograd.grad(
    psi.sum(), x, create_graph=True
)[0]                                                        # [B, L_max, D]

trace  = torch.zeros(B, device=padded.device)

for _ in range(m):
    # Rademacher vector — respects padding mask
    v  = (torch.randint(0, 2, (B, L_max, D),
                        generator=rng, dtype=torch.float32)
          * 2 - 1) * mask                                  # [B, L_max, D]

    gv = (grads * v).sum()                                 # scalar
    hv = torch.autograd.grad(
        gv, x, retain_graph=True
    )[0]                                                    # [B, L_max, D]

    trace += (v * hv * mask).sum(dim=(1, 2))               # [B]

return (trace / m).detach()
```

# ============================================================================

# Async prefetch — loads next batch of embeddings while current batch computes

# ============================================================================

class EmbeddingPrefetcher:
def **init**(self, texts: list[str], batch_size: int, ahead: int = 2):
self.texts      = texts
self.batch_size = batch_size
self.q          = queue.Queue(maxsize=ahead)
self._stop      = threading.Event()
self._thread    = threading.Thread(target=self._worker, daemon=True)
self._thread.start()

```
def _worker(self):
    for start in range(0, len(self.texts), self.batch_size):
        if self._stop.is_set():
            break
        batch = self.texts[start:start + self.batch_size]
        item  = (start, batch, *get_padded_embeddings(batch))
        self.q.put(item)
    self.q.put(None)   # sentinel

def __iter__(self):
    while True:
        item = self.q.get()
        if item is None:
            break
        yield item

def stop(self):
    self._stop.set()
```

# ============================================================================

# Main

# ============================================================================

with open(INPUT_FILE, “r”, encoding=“utf-8”) as f:
all_texts = [ln.strip() for ln in f if ln.strip()]
print(f”Total sentences: {len(all_texts)}”)

top_heap = []   # max-heap of (-stability, text)

with open(OUTPUT_CSV, mode=‘w’, newline=’’, encoding=‘utf-8-sig’) as f_csv:
writer = csv.writer(f_csv)
writer.writerow([“text”, “grad_norm_sq”, “laplacian_est”, “stability_score”])

```
prefetcher = EmbeddingPrefetcher(all_texts, BATCH_SIZE, ahead=PREFETCH_BATCHES)
n_batches  = (len(all_texts) + BATCH_SIZE - 1) // BATCH_SIZE

with tqdm(total=n_batches, desc="Processing batches") as pbar:
    for start_idx, batch_texts, padded, lengths in prefetcher:

        # Skip trivial sentences (L < 2)
        valid = lengths >= 2                                # [B] bool

        grad_norms  = torch.zeros(len(batch_texts))
        laplacians  = torch.zeros(len(batch_texts))

        if valid.any():
            v_idx   = valid.nonzero(as_tuple=True)[0]
            p_v     = padded[v_idx]
            l_v     = lengths[v_idx]

            grad_norms[v_idx]  = batched_grad_norm_sq(p_v, l_v).cpu()
            laplacians[v_idx]  = batched_hutchinson(p_v, l_v, m=M_HUTCHINSON).cpu()

        stabilities = laplacians - LAMBDA_STAB * grad_norms

        for i, text in enumerate(batch_texts):
            gn  = grad_norms[i].item()
            lap = laplacians[i].item()
            s   = stabilities[i].item()
            writer.writerow([text, gn, lap, s])

            entry = (-s, text)
            if len(top_heap) < TOP_N_VISUAL:
                heapq.heappush(top_heap, entry)
            elif -s > top_heap[0][0]:
                heapq.heapreplace(top_heap, entry)

        # Free graph memory
        del padded, lengths, p_v, l_v, grad_norms, laplacians, stabilities
        gc.collect()
        pbar.update(1)
```

top_entries = sorted([(-s, t) for s, t in top_heap], key=lambda e: e[0])
print(f”Done. Results → {OUTPUT_CSV}”)

# ============================================================================

# Visualization

# ============================================================================

top_texts  = [e[1] for e in top_entries]
top_scores = [e[0] for e in top_entries]

plt.figure(figsize=(12, 6))
sns.barplot(
x=[t[:50] + (”…” if len(t) > 50 else “”) for t in top_texts],
y=top_scores,
palette=“coolwarm”,
)
plt.title(f”Top {len(top_entries)} Most Unstable Sentences  (S = ΔΨ − λ‖∇Ψ‖²)”)
plt.ylabel(“Stability score  (lower = more unstable)”)
plt.xticks(rotation=45, ha=‘right’, fontsize=8)
plt.tight_layout()
plt.savefig(SAVE_PLOT, dpi=150)
plt.show()
print(f”Plot saved → {SAVE_PLOT}”)

"""
AΩ+ Reasoning Stability Field – Production‑Ready

Computes stability score S = ΔΨ - λ·‖∇Ψ‖² for each sentence using token embeddings.
- Potential field Ψ with cosine similarity and uniform attention.
- Gradient via autograd.
- Laplacian via Hutchinson trace estimator with Rademacher vectors.
- Keeps top N most unstable sentences in a max‑heap.
- Reproducible, efficient for large datasets.
"""

import torch
import heapq
import functools
import gc
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import csv
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================================
# Configuration
# ============================================================================
INPUT_FILE = "dataset.txt"
OUTPUT_CSV = "stability_scores_per_sentence.csv"
BATCH_SIZE = 8
LAMBDA_STAB = 1.0
M_HUTCHINSON = 20
MAX_SEQ_LENGTH = 128
TOP_N_VISUAL = 20
SAVE_PLOT = "stability_top.png"
RANDOM_SEED = 42
CLEAR_CUDA_CACHE = True        # clear cache per batch (if OOM)

# ============================================================================
# Device & reproducibility
# ============================================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.manual_seed(RANDOM_SEED)
if device.type == 'cuda':
    torch.cuda.manual_seed_all(RANDOM_SEED)

print(f"Using device: {device}")

# ============================================================================
# Model (token embeddings)
# ============================================================================
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
model.max_seq_length = MAX_SEQ_LENGTH

def get_token_embeddings(texts):
    token_emb_np = model.encode(texts, convert_to_tensor=False, output_value='token_embeddings')
    return [torch.tensor(emb, device=device) for emb in token_emb_np]

# ============================================================================
# Potential field functions
# ============================================================================
def pairwise_cosine_similarity(embeddings):
    norms = torch.norm(embeddings, dim=1, keepdim=True)
    embeddings_norm = embeddings / norms.clamp(min=1e-8)
    return torch.mm(embeddings_norm, embeddings_norm.t())

def potential_field(embeddings, kernel='cosine'):
    L = embeddings.shape[0]
    if L < 2:
        return torch.tensor(0.0, device=embeddings.device, dtype=embeddings.dtype)
    if kernel == 'cosine':
        sim = pairwise_cosine_similarity(embeddings)
        sim = sim - torch.diag(torch.diag(sim))
        return sim.sum() / (L * (L - 1))
    else:
        raise NotImplementedError("Only cosine kernel is implemented.")

# ============================================================================
# Hutchinson trace estimator with Rademacher vectors
# ============================================================================
def hutchinson_trace_laplacian(func, inputs, m=20):
    x = inputs.clone().detach().requires_grad_(True)
    outputs = func(x)
    grads = torch.autograd.grad(outputs, x, create_graph=True)[0]

    trace_est = 0.0
    for _ in range(m):
        v = torch.randint(0, 2, x.shape, device=x.device, dtype=x.dtype).float() * 2 - 1
        gv = torch.sum(grads * v)
        hv = torch.autograd.grad(gv, x, retain_graph=True)[0]
        trace_est += torch.sum(v * hv).item()
    return trace_est / m

# ============================================================================
# Pre‑bind kernel
# ============================================================================
psi_func = functools.partial(potential_field, kernel='cosine')

# ============================================================================
# Main
# ============================================================================
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    all_texts = [line.strip() for line in f if line.strip()]
print(f"Total sentences: {len(all_texts)}")

with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8-sig') as f_csv:
    writer = csv.writer(f_csv)
    writer.writerow(["text", "grad_norm_sq", "laplacian_est", "stability_score"])

    top_heap = []  # max‑heap of (-stability, text)

    for start_idx in tqdm(range(0, len(all_texts), BATCH_SIZE), desc="Processing"):
        batch_texts = all_texts[start_idx:start_idx + BATCH_SIZE]
        batch_token_embs = get_token_embeddings(batch_texts)

        for idx, emb in enumerate(batch_token_embs):
            text = batch_texts[idx]
            L = emb.shape[0]

            if L < 2:
                grad_norm_sq = 0.0
                laplacian_est = 0.0
                stability = 0.0
            else:
                # Gradient norm squared
                x = emb.clone().detach().requires_grad_(True)
                psi = psi_func(x)
                psi.backward()
                grad_norm_sq = torch.sum(x.grad ** 2).item()

                # Laplacian estimate
                laplacian_est = hutchinson_trace_laplacian(psi_func, emb, m=M_HUTCHINSON)

                stability = laplacian_est - LAMBDA_STAB * grad_norm_sq

            writer.writerow([text, grad_norm_sq, laplacian_est, stability])

            # Keep top N most unstable (lowest stability)
            entry = (-stability, text)
            if len(top_heap) < TOP_N_VISUAL:
                heapq.heappush(top_heap, entry)
            else:
                if -stability > top_heap[0][0]:   # more unstable than the current worst
                    heapq.heapreplace(top_heap, entry)

        # Optional per‑batch cache clearing
        if CLEAR_CUDA_CACHE and device.type == 'cuda':
            torch.cuda.empty_cache()
            gc.collect()

    # Convert heap back to sorted list of (stability, text)
    top_entries = sorted([(-s, t) for s, t in top_heap], key=lambda x: x[0])

print(f"Computation finished. Results saved to {OUTPUT_CSV}")

# ============================================================================
# Visualization
# ============================================================================
top_texts = [entry[1] for entry in top_entries]
top_scores = [entry[0] for entry in top_entries]

plt.figure(figsize=(12, 6))
sns.barplot(x=[t[:50] + "..." for t in top_texts], y=top_scores, palette="coolwarm")
plt.title(f"Top {len(top_entries)} Lowest Stability Scores (most unstable sentences)")
plt.ylabel("Stability score (lower = more unstable)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(SAVE_PLOT, dpi=150)
plt.show()

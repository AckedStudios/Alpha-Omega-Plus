import torch
import torch.nn.functional as F

class AlphaOmegaRegulator(torch.nn.Module):
    def __init__(self, lambda_factor=0.1):
        super().__init__()
        self.lambda_factor = lambda_factor
        self.last_entropy = None  # Causal Cache for H(s_{t-1})

    def reset_cache(self):
        """Resets the causal entropy cache between sequences."""
        self.last_entropy = None

    def forward(self, logits):
        # 1. Calculate Softmax Entropy for the current step (H_t)
        # Numerical stability via 1e-9 to avoid log(0)
        probs = F.softmax(logits, dim=-1)
        current_entropy = -torch.sum(probs * torch.log(probs + 1e-9), dim=-1)
        
        # 2. Calculate the Field Gradient (Delta Entropy)
        if self.last_entropy is not None:
            # nabla_psi = H_t - H_{t-1}
            nabla_psi = current_entropy - self.last_entropy
        else:
            # First step initialization
            nabla_psi = torch.zeros_like(current_entropy)

        # 3. Update Cache (detached to prevent backprop through history)
        self.last_entropy = current_entropy.detach()

        # 4. Return the Penalty Mask formatted for Attention Broadcasting
        # Shape becomes [batch, 1, 1, seq_len] to match [batch, heads, seq, seq]
        penalty = self.lambda_factor * nabla_psi
        return penalty.unsqueeze(1).unsqueeze(-1)

# Example Integration:
# reg = AlphaOmegaRegulator()
# ... inside forward pass ...
# bias = reg(logits)
# attention_scores = (Q @ K.T) / sqrt_dk + bias 


"""
AΩ+ Truth Evaluation & Harmonic Scaling Integration
Part of the Alpha-Omega-Plus Research Framework
Version: 1.0 Final – Golden Ratio Harmonic Scaling Included
"""

from typing import List, Tuple

PHI = 1.618033988749895  # Golden Ratio

def evaluate_and_scale(
    dimensions: List[str],
    truth_values: List[float],
    weights: List[float],
    N_initial: float,
    threshold: float = 0.7,
    alpha: float = 2.08
) -> Tuple[float, float, float]:
    """
    Evaluates weighted truth, consistency, and adjusts computational difficulty N
    with Phi-based harmonic scaling.
    
    :param dimensions: Names of evaluation dimensions
    :param truth_values: Corresponding truth values [0,1]
    :param weights: Weight of each dimension
    :param N_initial: Initial computational budget / problem difficulty
    :param threshold: Truth score threshold for increasing difficulty
    :param alpha: Scaling exponent for harmonic adjustment
    :return: Tuple (truth_score, consistency, adjusted_N)
    """
    if len(dimensions) != len(truth_values) or len(truth_values) != len(weights):
        raise ValueError("Dimensions, truth values, and weights must match in length.")
    
    # Weighted truth score
    truth_score = sum(w * t for w, t in zip(weights, truth_values))
    
    # Consistency: inverse of standard deviation
    mean_val = sum(truth_values) / len(truth_values)
    variance = sum((t - mean_val) ** 2 for t in truth_values) / len(truth_values)
    consistency = max(0.0, 1.0 - variance ** 0.5)
    
    # Harmonic scaling adjustment based on truth score
    if truth_score < threshold:
        N_adjusted = N_initial * (1 + (threshold - truth_score))
    else:
        N_adjusted = N_initial
    
    # Apply Phi-based harmonic scaling
    N_harmonic = N_adjusted * (PHI ** (alpha * (1 - truth_score)))  # lower truth => stronger scaling
    
    return truth_score, consistency, N_harmonic


# --- Example Usage ---
if __name__ == "__main__":
    dimensions = ["conceptual", "verbal", "qualitative"]
    truth_values = [0.9, 0.8, 0.95]
    weights = [0.4, 0.3, 0.3]
    N_initial = 10
    
    score, consistency, N_final = evaluate_and_scale(dimensions, truth_values, weights, N_initial)
    
    print(f"--- AΩ+ Evaluation Results ---")
    print(f"Final Truth Score: {score:.4f}")
    print(f"Logical Consistency: {consistency:.4f}")
    print(f"Original Difficulty (N): {N_initial}")
    print(f"Harmonic-Scaled Difficulty (N): {N_final:.2f}")

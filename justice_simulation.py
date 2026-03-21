"""
AΩ+ Justice Evaluation Module
-----------------------------
Implements Golden Ratio-based stability for ethical reasoning.
Version: 1.0.0
"""

PHI = 1.618033  # Golden Ratio constant

def evaluate_justice(individual_rights, collective_good):
    """
    Computes a justice stability score using the Alpha-Omega Plus principle:
    Justice is maximized when the ratio of individual rights to collective good
    approaches the Golden Ratio (Φ).
    
    :param individual_rights: Value representing protection of individual rights (0..1)
    :param collective_good: Value representing collective welfare (0..1)
    :return: Justice Stability Score (0..1)
    """
    if collective_good <= 0:
        raise ValueError("collective_good must be greater than zero to avoid division error.")
    
    # Harmony ratio
    harmony_point = individual_rights / collective_good
    
    # Tension from Golden Ratio
    tension = abs(harmony_point - PHI)
    
    # Convert tension into a truth/stability score
    truth_score = 1 / (1 + tension)
    
    return round(truth_score, 4)

# ---------------------------------------------------------
# Example Usage
# ---------------------------------------------------------
if __name__ == "__main__":
    # Test cases
    scores = [
        (0.8, 0.494),
        (0.6, 0.37),
        (0.9, 0.55),
        (0.5, 0.31)
    ]
    
    print("--- AΩ+ Justice Evaluation ---")
    for ind_rights, col_good in scores:
        score = evaluate_justice(ind_rights, col_good)
        print(f"Individual: {ind_rights}, Collective: {col_good} → Justice Stability: {score}")

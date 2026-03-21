"""
AΩ+ Tetralectic Gate: Structural Symmetry Verification
-------------------------------------------------------
Implements the 'Fire of Truth' mechanism using Golden Ratio (Φ) scaling 
to ensure AI reasoning stability.

"""

# Golden Ratio constant for mathematical stability
PHI = 1.618033988749895

def tetralectic_gate(statement, evaluator):
    """
    Evaluates a statement through four logical poles to ensure structural harmony.
    
    Poles:
        θ (Thesis): The core assertion.
        / (Antithesis): The direct negation.
        § (Deviation): A distorted/similar but wrong version.
        ~ (Parallel): A harmonious alternative.
    
    Returns:
        dict: {
            'score': float, Φ-scaled truth score,
            'passed_fire': bool, symmetry validation across all poles,
            'pole_analysis': dict, scores of each pole
        }
    """
    
    # Evaluate the four poles
    poles = {
        'thesis': evaluator(statement),
        'antithesis': evaluator(f"NOT: {statement}"),
        'deviation': evaluator(f"SIMILAR BUT WRONG: {statement}"),
        'parallel': evaluator(f"HARMONIOUS ALT: {statement}")
    }
    
    # Positive Harmony Check: Thesis and Parallel alignment
    positive_symmetry = abs(poles['thesis'] - poles['parallel']) < 0.2
    
    # Negative Consistency Check: Antithesis and Deviation alignment
    negative_symmetry = abs(poles['antithesis'] - poles['deviation']) < 0.2
    
    # Φ-Scaling for truth stabilization
    truth_score = ((poles['thesis'] + poles['parallel']) / 2) / PHI
    truth_score = min(truth_score, 1.0)
    
    # Fire of Truth Validation
    passed_fire = positive_symmetry and negative_symmetry
    
    return {
        'score': round(truth_score, 3),
        'passed_fire': passed_fire,
        'pole_analysis': poles
    }

# ---------------------------------------------------------
# Example Evaluation Logic
# ---------------------------------------------------------
def logical_consistency_eval(statement):
    """
    Evaluates logical coherence and detects reasoning asymmetries.
    
    Penalizes dogmatic expressions and rewards nuanced, evidence-based language.
    """
    score = 0.8
    statement_lower = statement.lower()
    
    # Penalties for logic traps
    traps = {
        "always": 0.1, "never": 0.1, "everyone knows": 0.2,
        "obviously": 0.15, "because that's how": 0.3,
        "undoubtedly": 0.1, "impossible": 0.15, "must be": 0.1
    }
    
    # Rewards for logic boosters
    boosters = {
        "however": 0.05, "evidence": 0.07, "suggests": 0.05,
        "research shows": 0.1, "proportional": 0.05, "balance": 0.05
    }
    
    for trap, penalty in traps.items():
        if trap in statement_lower:
            score -= penalty
    for booster, reward in boosters.items():
        if booster in statement_lower:
            score = min(1.0, score + reward)
    
    # Reasoning length adjustment
    if len(statement) < 15 or len(statement) > 600:
        score -= 0.15
    
    return max(0.1, round(score, 2))

# ---------------------------------------------------------
# Example Usage
# ---------------------------------------------------------
if __name__ == "__main__":
    test_statement = "AI will enhance user experience on Apple devices."
    
    result = tetralectic_gate(test_statement, logical_consistency_eval)

    print(f"--- AΩ+ Tetralectic Analysis ---")
    print(f"Statement: '{test_statement}'")
    print(f"Final Truth Score (Φ-scaled): {result['score']:.3f}")
    print(f"Status: {'PASSED (Fire of Truth)' if result['passed_fire'] else 'REJECTED (Asymmetry Detected)'}")
    print(f"Detailed Poles: {result['pole_analysis']}")

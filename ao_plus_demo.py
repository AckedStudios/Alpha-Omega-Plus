#!/usr/bin/env python3
"""
AΩ+ Integrated Demo
Demonstrates the full reasoning pipeline:
- Tetralectic Gate (four-pole logic filter)
- Truth Evaluator (12-dimensional scoring with coupling)
- Justice & Ethical Stability Module
- Scalar Field Engine (optional, for advanced simulation)
"""

import numpy as np
from typing import Dict, Any

# Import the core modules
from tetralectic_gate import tetralectic_gate
from truth_evaluator import AO_TruthEvaluator
from justice_simulation import evaluate_justice
# Optional: from ao_engine import AOPlusEngine  # uncomment if you want field evolution


def simple_heuristic_evaluator(statement: str) -> float:
    """
    A simple heuristic to score a statement on a scale 0..1.
    Used as the evaluator for the Tetralectic Gate.
    Penalizes dogmatic terms, rewards moderate language.
    """
    statement_lower = statement.lower()
    score = 0.5  # neutral baseline

    # Penalize absolute terms (dogmatism)
    if any(word in statement_lower for word in ["always", "never", "every", "none", "impossible"]):
        score -= 0.2
    # Reward moderate terms (scientific caution)
    if any(word in statement_lower for word in ["evidence suggests", "likely", "may", "tends to"]):
        score += 0.2
    # Small boost for length (more nuance)
    if len(statement.split()) > 10:
        score += 0.05
    # Clamp to [0,1]
    return max(0.0, min(1.0, score))


def run_demo():
    print("=" * 60)
    print("AΩ+ Integrated Demo v2.4")
    print("=" * 60)

    # ------------------------------------------------------------
    # 1. Tetralectic Gate – verify a statement
    # ------------------------------------------------------------
    statement = "AI systems can never truly understand human emotions."
    print(f"\n[1] Tetralectic Gate – Statement: '{statement}'")
    gate_result = tetralectic_gate(statement, simple_heuristic_evaluator)
    print(f"    Gate Score: {gate_result['score']:.4f}")
    print(f"    Passed Fire: {gate_result['passed']}")
    print(f"    Poles: {gate_result['poles']}")

    # ------------------------------------------------------------
    # 2. Truth Evaluator – 12-dimensional scoring
    # ------------------------------------------------------------
    print("\n[2] Truth Evaluator – 12D analysis")
    # Sample raw scores for the same statement (mocked)
    # In a real scenario, these would come from a more sophisticated evaluator
    sample_input = {
        "D1_Nominal": 0.7,     # terminology ok but "never" is absolute
        "D2_Conceptual": 0.6,  # concept of "understanding" is vague
        "D3_Propositional": 0.4, # the implication is too strong
        "D4_Applicative": 0.5,   # applies to all AI systems – too broad
        "D5_Spatial": 1.0,       # no spatial restriction
        "D6_Modal": 0.3,         # presented as necessity, not possibility
        "D7_Temporal": 0.5,      # may change over time
        "D8_Quantitative": 0.2,  # no empirical evidence provided
        "D9_Qualitative": 0.4,   # human emotions are not well-defined here
        "D10_Causal": 0.3,       # no causal mechanism explained
        "D11_Intuitive": 0.6,    # some may find it plausible
        "D12_Logical": 0.4       # internally inconsistent with nuance
    }
    evaluator = AO_TruthEvaluator()
    result = evaluator.evaluate_12d(sample_input, domain="scientific")
    print(f"    ψₜ (Truth Coherence): {result['psi_t']}")
    print(f"    ψₑ (Field Entropy): {result['psi_e']}")
    print(f"    Final Truth Index (Φ‑scaled): {result['final_truth_index']}")
    print(f"    Stability Status: {result['stability_status']}")
    print(f"    Category Averages: {result['category_averages']}")

    # ------------------------------------------------------------
    # 3. Justice & Ethical Stability
    # ------------------------------------------------------------
    print("\n[3] Justice & Ethical Stability Module")
    # Example: individual rights vs collective good
    individual_rights = 0.8
    collective_good = 0.494  # tuned to approach Φ
    justice_score = evaluate_justice(individual_rights, collective_good)
    print(f"    Justice Score (Φ-harmony): {justice_score}")
    print(f"    Interpretation: Closer to 1 indicates better balance.")

    # ------------------------------------------------------------
    # 4. Optional: Scalar Field Engine (if available)
    # ------------------------------------------------------------
    try:
        from ao_engine import AOPlusEngine
        print("\n[4] Scalar Field Engine (ψ evolution)")
        engine = AOPlusEngine()
        # Example: evolve ψ over a few steps
        initial_psi = 0.5
        steps = 5
        psi_values = [initial_psi]
        for t in range(1, steps+1):
            # Simple evolution: here we would call engine.step() or similar
            # For demonstration, we just simulate a damping effect
            new_psi = psi_values[-1] * 0.95 + 0.05  # slow drift
            psi_values.append(new_psi)
        print(f"    ψ evolution: {[round(v,4) for v in psi_values]}")
    except ImportError:
        print("\n[4] Scalar Field Engine: not available (ao_engine.py not found)")

    print("\n" + "=" * 60)
    print("Demo completed. AΩ+ framework ready.")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()

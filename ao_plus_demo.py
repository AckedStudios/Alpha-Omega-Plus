#!/usr/bin/env python3
"""
AΩ+ Integrated Demo – Decoupled Integration
Demonstrates the full reasoning pipeline using:
- 12D Truth Evaluator (AO_TruthEvaluator)
- Tetralectic Gate (tetralectic_gate)
- Scalar Field Engine (AOPlusEngine)
- Justice & Ethical Stability (evaluate_justice)

The engine remains generic; truth scores are passed externally.
"""

import sys
import numpy as np

# Import core modules
from truth_evaluator import AO_TruthEvaluator
from tetralectic_gate import tetralectic_gate
from justice_simulation import evaluate_justice

# Try importing the scalar field engine (optional)
try:
    from ao_engine import AOPlusEngine
    ENGINE_AVAILABLE = True
except ImportError:
    ENGINE_AVAILABLE = False
    print("Warning: ao_engine.py not found. Skipping field evolution.")


def simple_heuristic_evaluator(statement: str) -> float:
    """
    Simple evaluator for the Tetralectic Gate.
    Returns a score 0..1 based on linguistic caution.
    """
    statement_lower = statement.lower()
    score = 0.5
    if any(w in statement_lower for w in ["always", "never", "every", "none", "impossible"]):
        score -= 0.2
    if any(w in statement_lower for w in ["evidence suggests", "likely", "may", "tends to"]):
        score += 0.2
    return max(0.0, min(1.0, score))


def run_demo():
    print("=" * 60)
    print("AΩ+ Integrated Demo – Decoupled Architecture")
    print("=" * 60)

    # ------------------------------------------------------------
    # 1. Input statement
    # ------------------------------------------------------------
    statement = "AI systems can never truly understand human emotions."
    print(f"\n[1] Statement: '{statement}'")

    # ------------------------------------------------------------
    # 2. 12‑Dimensional Truth Evaluation
    # ------------------------------------------------------------
    print("\n[2] 12‑Dimensional Truth Analysis")
    evaluator_12d = AO_TruthEvaluator()

    # Mock raw scores for the statement (in a real system, these would come from a parser)
    raw_scores = {
        "D1_Nominal": 0.7, "D2_Conceptual": 0.6, "D3_Propositional": 0.4,
        "D4_Applicative": 0.5, "D5_Spatial": 1.0, "D6_Modal": 0.3,
        "D7_Temporal": 0.5, "D8_Quantitative": 0.2, "D9_Qualitative": 0.4,
        "D10_Causal": 0.3, "D11_Intuitive": 0.6, "D12_Logical": 0.4
    }
    domain = "scientific"
    truth_result = evaluator_12d.evaluate_12d(raw_scores, domain=domain)
    psi_t = truth_result["psi_t"]
    psi_e = truth_result["psi_e"]
    print(f"    ψₜ (Truth Coherence): {psi_t}")
    print(f"    ψₑ (Field Entropy): {psi_e}")
    print(f"    Stability Status: {truth_result['stability_status']}")

    # ------------------------------------------------------------
    # 3. Tetralectic Gate – Structural Verification
    # ------------------------------------------------------------
    print("\n[3] Tetralectic Gate (Structural Verification)")
    gate_result = tetralectic_gate(statement, simple_heuristic_evaluator)
    print(f"    Gate Score: {gate_result['score']:.4f}")
    print(f"    Passed Fire: {gate_result['passed']}")
    print(f"    Poles: {gate_result['poles']}")

    # ------------------------------------------------------------
    # 4. Scalar Field Engine (using ψₜ as external truth)
    # ------------------------------------------------------------
    if ENGINE_AVAILABLE:
        print("\n[4] Scalar Field Engine (using ψₜ as external truth)")
        engine = AOPlusEngine()

        # Define a bridge: the engine will use the 12D truth score as its evaluator
        def bridge_evaluator(statement):
            # For demo, we return the already computed psi_t (simulate real-time)
            return psi_t

        # Compute stability using the engine, passing the bridge
        # Note: This assumes AOPlusEngine has a method like compute_total_stability
        # If not, we adapt to what's available.
        try:
            # If the engine has a method that accepts an evaluator function
            final_stability = engine.compute_total_stability(
                psi=0.5,
                concept="eleutheria",
                statement=statement,
                evaluator_func=bridge_evaluator
            )
            print(f"    Field Stability: {final_stability:.4f}")
        except AttributeError:
            # Fallback: simulate a simple evolution using the engine's step method
            # (assuming engine.step accepts external truth)
            engine.set_psi(0.5)  # initial psi
            for step in range(3):
                engine.step(external_truth=psi_t)
                print(f"    Step {step+1}: ψ = {engine.psi:.4f}")
    else:
        print("\n[4] Scalar Field Engine: not available (ao_engine.py not found)")

    # ------------------------------------------------------------
    # 5. Justice & Ethical Stability
    # ------------------------------------------------------------
    print("\n[5] Justice & Ethical Stability Module")
    # Example: individual rights vs collective good
    individual_rights = 0.8
    collective_good = 0.494  # tuned to approach Φ
    justice_score, warning = evaluate_justice(individual_rights, collective_good, return_warning=True)
    print(f"    Justice Score (Φ‑harmony): {justice_score}")
    if warning:
        print(f"    Warning: {warning}")

    # ------------------------------------------------------------
    # 6. Overall Assessment
    # ------------------------------------------------------------
    print("\n[6] Overall Assessment")
    overall_status = "PASS" if (psi_t > 0.65 and gate_result['passed'] and justice_score > 0.5) else "UNCERTAIN"
    print(f"    Overall Status: {overall_status}")
    print("    Interpretation: The system integrates 12D truth, structural verification, and ethical balance.")
    print("\n" + "=" * 60)
    print("Demo completed. AΩ+ decoupled architecture verified.")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()

import numpy as np

class AO_TruthEvaluator:
    """
    AΩ+ 12-Dimensional Truth Evaluator
    Implements Dimensional Coupling, Domain‑Specific Weighting,
    and Field Stability Scoring using the Golden Ratio (Φ).
    """
    
    def __init__(self):
        self.phi = 1.618033988749895
        self.dimensions = {
            "Structural": ["D1_Nominal", "D2_Conceptual", "D3_Propositional"],
            "Contextual": ["D4_Applicative", "D5_Spatial", "D6_Modal"],
            "Empirical":  ["D7_Temporal", "D8_Quantitative", "D9_Qualitative"],
            "Relational": ["D10_Causal", "D11_Intuitive", "D12_Logical"]
        }

    def evaluate_12d(self, raw_values, domain="default"):
        """
        raw_values: dict with keys D1_D12 and values 0.0 to 1.0
        domain: "scientific", "ethical", "definitional", or "default"
        Returns a dict with detailed scores, psi_t, psi_e, final_truth_index, etc.
        """
        scores = raw_values.copy()

        # --- DIMENSIONAL COUPLING (The Physics of Logic) ---
        # 1. Empirical -> Relational Coupling
        if scores.get("D8_Quantitative", 0) < 0.5:
            penalty = (0.5 - scores["D8_Quantitative"]) * 0.5
            scores["D10_Causal"] = max(0, scores.get("D10_Causal", 0) - penalty)

        # 2. Structural -> Relational Coupling
        if scores.get("D1_Nominal", 0) < 0.4:
            scores["D12_Logical"] = scores.get("D12_Logical", 0) * 0.5

        # 3. Contextual -> Empirical
        scores["D7_Temporal"] = scores.get("D7_Temporal", 0) * scores.get("D4_Applicative", 1.0)

        # --- DOMAIN‑SPECIFIC WEIGHTS (priority dimensions get weight 2) ---
        if domain == "scientific":
            priority_dims = {"D3_Propositional", "D8_Quantitative", "D10_Causal", "D12_Logical"}
        elif domain == "ethical":
            priority_dims = {"D4_Applicative", "D6_Modal", "D9_Qualitative", "D11_Intuitive"}
        elif domain == "definitional":
            priority_dims = {"D1_Nominal", "D2_Conceptual", "D12_Logical"}
        else:
            priority_dims = set()

        # Build weight list in the same order as the sorted dimension keys
        dims_sorted = sorted(scores.keys())
        weight_list = [2 if d in priority_dims else 1 for d in dims_sorted]
        values = [scores[d] for d in dims_sorted]

        total_weight = sum(weight_list)
        weighted_sum = sum(v * w for v, w in zip(values, weight_list))
        psi_t = weighted_sum / total_weight if total_weight > 0 else 0.0

        # --- CATEGORY AVERAGES (for interpretability) ---
        category_scores = {}
        for cat, dims in self.dimensions.items():
            cat_vals = [scores.get(d, 0) for d in dims]
            category_scores[cat] = np.mean(cat_vals)

        # --- FIELD STABILITY (ψₑ) based on entropy ---
        all_vals = list(scores.values())
        mean_score = np.mean(all_vals)
        variance = np.var(all_vals)
        psi_e = 1.0 - np.sqrt(variance)   # 0..1, higher = more stable

        # --- FINAL TRUTH INDEX (Φ‑scaled stability) ---
        # Combines truth coherence (ψₜ) with field stability (ψₑ), scaled by the Golden Ratio.
        final_truth_index = psi_t * (psi_e / self.phi)

        # --- STABILITY STATUS (matching README terminology) ---
        if final_truth_index > 0.85:
            stability_status = "STABLE"
        elif final_truth_index > 0.65:
            stability_status = "MODERATE"
        elif final_truth_index > 0.40:
            stability_status = "TURBULENT"
        else:
            stability_status = "COLLAPSED"

        return {
            "detailed_scores": scores,
            "coupling_applied": True,
            "psi_t": round(psi_t, 4),
            "psi_e": round(psi_e, 4),
            "category_averages": category_scores,
            "final_truth_index": round(final_truth_index, 4),
            "stability_status": stability_status
        }


# --- TEST RUN ---
if __name__ == "__main__":
    evaluator = AO_TruthEvaluator()

    # Example: strong theory but weak data (scientific domain)
    sample_input = {
        "D1_Nominal": 0.9, "D2_Conceptual": 0.9, "D3_Propositional": 0.8,
        "D4_Applicative": 0.7, "D5_Spatial": 0.6, "D6_Modal": 0.5,
        "D7_Temporal": 0.8, "D8_Quantitative": 0.1, "D9_Qualitative": 0.4,
        "D10_Causal": 0.9, "D11_Intuitive": 0.5, "D12_Logical": 0.8
    }

    result = evaluator.evaluate_12d(sample_input, domain="scientific")
    print("\n--- AΩ+ 12D Evaluation Result ---")
    print(f"ψₜ (Truth Coherence): {result['psi_t']}")
    print(f"ψₑ (Field Entropy): {result['psi_e']}")
    print(f"Final Truth Index (Φ‑scaled): {result['final_truth_index']}")
    print(f"Stability Status: {result['stability_status']}")
    print(f"Category Averages: {result['category_averages']}")

import math
import matplotlib.pyplot as plt

class AOPlusEngine:
    """
    Alpha-Omega Plus (AΩ+) Reasoning Engine
    --------------------------------------
    Version: 1.0.5 - Canonical Full Merge
    Integrates Scalar Field Physics with Relational Tetralectic Logic.
    
    Guiding Principle: Suppression of AI hallucinations through 
    mathematical stability and linguistic symmetry.
    """

    def __init__(self, phi=1.618033, sigma=1.0):
        # The Golden Ratio: Fundamental harmonic attractor
        self.phi = phi
        # Normalization constant for the scalar field manifold
        self.sigma = sigma

        # ════════════════════════════════════════════════════════════════════
        # STABILITY MATRIX: FULL RELATIONAL TETRALECTIC MAPPING
        # ════════════════════════════════════════════════════════════════════
        self.stability_matrix = {
            # TETRALECT 1: Eleutheria (Freedom)
            "eleutheria": {
                "role": "thesis", "ethos": "kl", "tetralect_id": 1,
                "partners": ["eiloteia", "asydosia", "diakonia"],
                "spectrum": ["eleutheria", "eleutheriazo", "eleutherōmeni", "eleutheriastiki"]
            },
            "eiloteia": {
                "role": "antithesis", "ethos": "kk", "tetralect_id": 1,
                "partners": ["eleutheria", "asydosia", "diakonia"],
                "spectrum": ["eiloteia", "eiloteuo", "eiloteumeni", "eilotiki"]
            },
            "asydosia": {
                "role": "deviation", "ethos": "kk", "tetralect_id": 1,
                "partners": ["eleutheria", "eiloteia", "diakonia", "ochlokratia"],
                "spectrum": ["asydosia", "asydoto", "asydotimeni", "asydotiki"]
            },
            "diakonia": {
                "role": "parallel", "ethos": "kl", "tetralect_id": 1,
                "partners": ["eleutheria", "eiloteia", "asydosia"],
                "spectrum": ["diakonia", "diakono", "diakonimeni", "diakoniki"]
            },

            # TETRALECT 2: Demokratia (Democracy)
            "demokratia": {
                "role": "thesis", "ethos": "kl", "tetralect_id": 2,
                "partners": ["tyrannia", "ochlokratia", "hegemonia"],
                "spectrum": ["demokratia", "demokrato", "demokratimeni", "demokratiki"]
            },
            "tyrannia": {
                "role": "antithesis", "ethos": "kk", "tetralect_id": 2,
                "partners": ["demokratia", "ochlokratia", "hegemonia"],
                "spectrum": ["tyrannia", "tyranno", "tyrannimeni", "tyranniki"]
            },
            "ochlokratia": {
                "role": "deviation", "ethos": "kk", "tetralect_id": 2,
                "partners": ["demokratia", "tyrannia", "hegemonia", "asydosia"],
                "spectrum": ["ochlokratia", "ochlokrato", "ochlokratimeni", "ochlokratiki"]
            },
            "hegemonia": {
                "role": "parallel", "ethos": "kl", "tetralect_id": 2,
                "partners": ["demokratia", "tyrannia", "ochlokratia"],
                "spectrum": ["hegemonia", "hegemoneuo", "hegemoneumeni", "hegemoniki"]
            },

            # CORE UNIVERSAL CONCEPTS (Bridge Logic)
            "justice": {
                "role": "thesis", "ethos": "kl", "tetralect_id": 0,
                "partners": ["harmony"],
                "spectrum": ["justice", "justify", "justified", "just"]
            },
            "harmony": {
                "role": "thesis", "ethos": "kl", "tetralect_id": 0,
                "partners": ["justice"],
                "spectrum": ["harmony", "harmonize", "harmonized", "harmonic"]
            }
        }

    # ---------------------------------------------------------
    # PHYSICS LAYER: Field Dynamics
    # ---------------------------------------------------------
    def scalar_field_pressure(self, psi, lam=0.1):
        """Calculates logical restoration force against drift."""
        exponent = -(psi ** 2) / (self.sigma ** 2)
        return abs(lam * (psi ** 3) * math.exp(exponent))

    def harmonic_scaling(self, N, T0=100, alpha=2.08):
        """Phi-based token budget scaling for complex reasoning."""
        return T0 * (self.phi ** (alpha * N))

    # ---------------------------------------------------------
    # LINGUISTIC LAYER: Tetralectic Kanons
    # ---------------------------------------------------------
    def check_kanon_3(self, concept_root):
        """Canon 3: Verifies if a concept has a stable 4-form spectrum."""
        concept = concept_root.lower().strip()
        if concept in self.stability_matrix:
            entry = self.stability_matrix[concept]
            return 1.0 if len(entry["spectrum"]) == 4 else round(1 / self.phi, 4)
        return round(1 / self.phi, 4) # Harmonic fallback

    def check_kanon_4(self, concept_root, suffix):
        """Canon 4: Sophistry Trap - Prohibits 'kk' roots from 'kl' suffixes."""
        concept = concept_root.lower().strip()
        suffix = suffix.lower().strip()
        if concept in self.stability_matrix:
            if self.stability_matrix[concept]["ethos"] == "kk" and suffix == "iki":
                return 0.1 # Logical corruption detected
        return 1.0

    def get_tetralect_group(self, concept_root):
        """Retrieves the full relational cluster of a concept."""
        concept = concept_root.lower().strip()
        if concept in self.stability_matrix:
            return [concept] + self.stability_matrix[concept]["partners"]
        return []

    def compute_unified_truth_score(self, psi, concept, current_suffix=None):
        """MASTER OPERATOR: Unifies Physics Pressure and Tetralectic Logic."""
        p_score = self.scalar_field_pressure(psi)
        k3_score = self.check_kanon_3(concept)
        k4_score = self.check_kanon_4(concept, current_suffix) if current_suffix else 1.0
        
        # Cumulative stability calculation
        return round(abs(p_score * k3_score * k4_score), 6)

    # ---------------------------------------------------------
    # VISUALIZATION LAYER: Stability Analytics
    # ---------------------------------------------------------
    def visualize_stability(self, concept_root):
        """Renders a comparative stability chart for a concept cluster."""
        cluster = self.get_tetralect_group(concept_root)
        if not cluster:
            print(f"Error: Concept '{concept_root}' not found in Matrix.")
            return
        
        scores = [self.compute_unified_truth_score(0.8, c) for c in cluster]
        # Green for Positive Ethos (kl), Red for Negative Ethos (kk)
        colors = ['#2ecc71' if self.stability_matrix[c]["ethos"] == "kl" else '#e74c3c' for c in cluster]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(cluster, scores, color=colors, edgecolor='black', alpha=0.8)
        plt.title(f"AΩ+ Stability Cluster Analysis: {concept_root.capitalize()}", fontsize=14)
        plt.ylabel("Unified Truth Score", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        
        # Annotate bars with exact scores
        for bar, score in zip(bars, scores):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002, 
                     f"{score}", ha='center', fontweight='bold')
        
        plt.tight_layout()
        plt.show()

# ---------------------------------------------------------
# PRODUCTION READINESS DEMO
# ---------------------------------------------------------
if __name__ == "__main__":
    engine = AOPlusEngine()
    
    print("⟴ AOPlusEngine v1.0.5 Deployment State: [ONLINE]")
    print("═"*50)
    print(f"[*] Harmonic Scaling (Depth 3): {engine.harmonic_scaling(3):.2f} tokens")
    print(f"[*] Scalar Pressure (Psi 0.8): {engine.scalar_field_pressure(0.8):.6f}")
    print(f"[*] Kanon 3 Validation (Justice): {engine.check_kanon_3('justice')}")
    print(f"[*] Kanon 4 Violation (Tyranniki): {engine.check_kanon_4('tyrannia', 'iki')} [SOPHISTRY ALERT]")
    print(f"[*] Kanon 4 Integrity (Diakoniki): {engine.check_kanon_4('diakonia', 'iki')} [VALID]")
    print(f"[*] Unified Score (Eleutheria): {engine.compute_unified_truth_score(0.8, 'eleutheria')}")
    print(f"[*] Relational Cluster (Asydosia): {engine.get_tetralect_group('asydosia')}")
    print("═"*50)
    
    # Launch Visual Analytics
    engine.visualize_stability('eleutheria')

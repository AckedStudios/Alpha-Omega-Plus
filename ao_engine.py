import math

class AOPlusEngine:
    """
    The Alpha-Omega Plus (AΩ+) Reasoning Engine.
    Unifies Physics (Scalar Field Pressure) with Relational Tetralectic Logic.
    
    This engine acts as a 'Truth Filter' for LLM outputs by verifying 
    mathematical stability and linguistic symmetry.
    """

    def __init__(self, phi=1.618033, sigma=1.0):
        # The Golden Ratio: Fundamental harmonic attractor
        self.phi = phi
        # Normalization constant for the scalar field manifold
        self.sigma = sigma

        # ════════════════════════════════════════════════════════════════════
        # STABILITY MATRIX: TETRALECTIC CONCEPT MAPPING
        # Each entry defines the role, ethos (kl/kk), and lexical spectrum.
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
                "partners": ["eleutheria", "eiloteia", "diakonia"],
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
                "partners": ["demokratia", "tyrannia", "hegemonia"],
                "spectrum": ["ochlokratia", "ochlokrato", "ochlokratimeni", "ochlokratiki"]
            },
            "hegemonia": {
                "role": "parallel", "ethos": "kl", "tetralect_id": 2,
                "partners": ["demokratia", "tyrannia", "ochlokratia"],
                "spectrum": ["hegemonia", "hegemoneuo", "hegemoneumeni", "hegemoniki"]
            },
            # ENGLISH TEST CONCEPTS
            "justice": {
                "role": "thesis", "ethos": "kl", "tetralect_id": 0,
                "partners": [],
                "spectrum": ["justice", "justify", "justified", "just"]
            },
            "harmony": {
                "role": "thesis", "ethos": "kl", "tetralect_id": 0,
                "partners": [],
                "spectrum": ["harmony", "harmonize", "harmonized", "harmonic"]
            }
        }

    def harmonic_scaling(self, N, T0=100, alpha=2.08):
        """Computes optimal token budget based on logical complexity N."""
        return T0 * (self.phi ** (alpha * N))

    def scalar_field_pressure(self, psi, lam=0.1):
        """
        Calculates Scalar Field Interaction (Physics-level).
        Acts as a restoring force against logical drift.
        """
        exponent = -(psi ** 2) / (self.sigma ** 2)
        return abs(lam * (psi ** 3) * math.exp(exponent))

    def check_kanon_3(self, concept_root):
        """
        Canon 3: Lexical Spectrum Validation.
        Verifies if a concept has a stable 4-form representation.
        """
        concept = concept_root.lower().strip()
        if concept in self.stability_matrix:
            entry = self.stability_matrix[concept]
            return 1.0 if len(entry["spectrum"]) == 4 else round(1 / self.phi, 4)
        # Fallback to harmonic constant for unknown concepts
        return round(1 / self.phi, 4)

    def check_kanon_4(self, concept_root, suffix):
        """
        Canon 4: Suffix Trap / Sophistry Detection.
        Prohibits negative (kk) ethos concepts from assuming positive (kl) suffixes.
        """
        concept = concept_root.lower().strip()
        suffix = suffix.lower().strip()
        
        if concept in self.stability_matrix:
            # Sophistry detection: A 'kk' root cannot logically yield an '-iki' adjective.
            if self.stability_matrix[concept]["ethos"] == "kk" and suffix == "iki":
                return 0.1  # Critical Failure
        return 1.0

    def compute_unified_truth_score(self, psi, concept, current_suffix=None):
        """
        MASTER OPERATOR: Integrates Field Physics and Tetralectic Symmetries.
        Returns the final stability probability (Truth Score).
        """
        p_score = self.scalar_field_pressure(psi)
        k3_score = self.check_kanon_3(concept)
        k4_score = self.check_kanon_4(concept, current_suffix) if current_suffix else 1.0
        
        final_stability = p_score * k3_score * k4_score
        return round(abs(final_stability), 6)

# ---------------------------------------------------------
# OPERATIONAL DEMONSTRATION
# ---------------------------------------------------------
if __name__ == "__main__":
    engine = AOPlusEngine()

    print("--- AΩ+ Engine Operational Test ---")
    
    # Test 1: Sophistry Trap (Tyrannia + -iki)
    # Expected: High penalty due to Kanon 4
    score_kk = engine.compute_unified_truth_score(0.8, "tyrannia", "iki")
    
    # Test 2: Harmonious Validation (Eleutheria)
    # Expected: Pass due to kl ethos
    score_kl = engine.compute_unified_truth_score(0.8, "eleutheria")

    # Test 3: Suffix check for kl concepts (Eleutheria + -iki)
    # Expected: Should return 1.0 for Kanon 4
    kanon4_pass = engine.check_kanon_4("eleutheria", "iki")

    print(f"Token Budget (N=3): {engine.harmonic_scaling(3):.2f}")
    print(f"Kanon 4 Test [Tyranniki]: {engine.check_kanon_4('tyrannia', 'iki')} (Penalty Applied)")
    print(f"Kanon 4 Test [Eleutheriastiki]: {kanon4_pass} (No Penalty)")
    print(f"Unified Score [Tyranniki]: {score_kk}")
    print(f"Unified Score [Eleutheria]: {score_kl}")

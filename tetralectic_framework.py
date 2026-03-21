import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PHI = 1.618033988749895

class AOPlusEngine:
    """
    Alpha-Omega Plus (AΩ+) Reasoning Engine v1.4.0
    ----------------------------------------------
    Adds pass/fail color-coded visualization for Total Stability.
    """

    def __init__(self, phi=PHI, sigma=1.0, stability_threshold=0.5):
        self.phi = phi
        self.sigma = sigma
        self.stability_threshold = stability_threshold

        # ---------------- STABILITY MATRIX ----------------
        self.stability_matrix = {
            "eleutheria": {"role":"thesis","ethos":"kl","tetralect_id":1,
                           "partners":["eiloteia","asydosia","diakonia"],
                           "spectrum":["eleutheria","eleutheriazo","eleutherōmeni","eleutheriastiki"]},
            "eiloteia": {"role":"antithesis","ethos":"kk","tetralect_id":1,
                         "partners":["eleutheria","asydosia","diakonia"],
                         "spectrum":["eiloteia","eiloteuo","eiloteumeni","eilotiki"]},
            "asydosia": {"role":"deviation","ethos":"kk","tetralect_id":1,
                         "partners":["eleutheria","eiloteia","diakonia","ochlokratia"],
                         "spectrum":["asydosia","asydoto","asydotimeni","asydotiki"]},
            "diakonia": {"role":"parallel","ethos":"kl","tetralect_id":1,
                         "partners":["eleutheria","eiloteia","asydosia"],
                         "spectrum":["diakonia","diakono","diakonimeni","diakoniki"]},
            "demokratia": {"role":"thesis","ethos":"kl","tetralect_id":2,
                           "partners":["tyrannia","ochlokratia","hegemonia"],
                           "spectrum":["demokratia","demokrato","demokratimeni","demokratiki"]},
            "tyrannia": {"role":"antithesis","ethos":"kk","tetralect_id":2,
                         "partners":["demokratia","ochlokratia","hegemonia"],
                         "spectrum":["tyrannia","tyranno","tyrannimeni","tyranniki"]},
            "ochlokratia": {"role":"deviation","ethos":"kk","tetralect_id":2,
                            "partners":["demokratia","tyrannia","hegemonia","asydosia"],
                            "spectrum":["ochlokratia","ochlokrato","ochlokratimeni","ochlokratiki"]},
            "hegemonia": {"role":"parallel","ethos":"kl","tetralect_id":2,
                          "partners":["demokratia","tyrannia","ochlokratia"],
                          "spectrum":["hegemonia","hegemoneuo","hegemoneumeni","hegemoniki"]},
            "justice": {"role":"thesis","ethos":"kl","tetralect_id":0,
                        "partners":["harmony"],
                        "spectrum":["justice","justify","justified","just"]},
            "harmony": {"role":"thesis","ethos":"kl","tetralect_id":0,
                        "partners":["justice"],
                        "spectrum":["harmony","harmonize","harmonized","harmonic"]}
        }

    # ---------------- PHYSICS LAYER ----------------
    def scalar_field_pressure(self, psi, lam=0.1):
        exponent = -(psi**2)/self.sigma**2
        return abs(lam*(psi**3)*math.exp(exponent))

    def harmonic_scaling(self, N, T0=100, alpha=2.08):
        return T0*(self.phi**(alpha*N))

    # ---------------- TETRALECTIC LAYER ----------------
    def check_kanon_3(self, concept_root):
        concept = concept_root.lower().strip()
        if concept in self.stability_matrix:
            return 1.0 if len(self.stability_matrix[concept]["spectrum"])==4 else round(1/self.phi,4)
        return round(1/self.phi,4)

    def check_kanon_4(self, concept_root, suffix):
        concept = concept_root.lower().strip()
        suffix = suffix.lower().strip()
        if concept in self.stability_matrix:
            if self.stability_matrix[concept]["ethos"]=="kk" and suffix=="iki":
                return 0.1
        return 1.0

    def get_tetralect_group(self, concept_root):
        concept = concept_root.lower().strip()
        if concept in self.stability_matrix:
            return [concept]+self.stability_matrix[concept]["partners"]
        return []

    # ---------------- UNIFIED TRUTH ----------------
    def compute_unified_truth_score(self, psi, concept, current_suffix=None):
        p = self.scalar_field_pressure(psi)
        k3 = self.check_kanon_3(concept)
        k4 = self.check_kanon_4(concept, current_suffix) if current_suffix else 1.0
        return round(abs(p*k3*k4),6)

    # ---------------- FIRE-OF-TRUTH ----------------
    def tetralectic_gate(self, statement, evaluator):
        poles = {
            'thesis': evaluator(statement),
            'antithesis': evaluator(f"NOT: {statement}"),
            'deviation': evaluator(f"SIMILAR BUT WRONG: {statement}"),
            'parallel': evaluator(f"HARMONIOUS ALT: {statement}")
        }
        positive_symmetry = abs(poles['thesis']-poles['parallel'])<0.2
        negative_symmetry = abs(poles['antithesis']-poles['deviation'])<0.2
        tetralectic_score = min(((poles['thesis']+poles['parallel'])/2)/self.phi,1.0)
        passed_validation = positive_symmetry and negative_symmetry
        return {'tetralectic_score':tetralectic_score,
                'passed_validation':passed_validation,
                'pole_values':poles}

    # ---------------- TOTAL STABILITY ----------------
    def compute_total_stability(self, psi, concept, statement, evaluator, current_suffix=None):
        unified_score = self.compute_unified_truth_score(psi, concept, current_suffix)
        gate_result = self.tetralectic_gate(statement, evaluator)
        total_score = round((unified_score + gate_result['tetralectic_score'])/2,6)
        status = 'PASS' if total_score>=self.stability_threshold else 'FAIL'
        return {'total_stability_score':total_score,
                'unified_score':unified_score,
                'tetralectic_score':gate_result['tetralectic_score'],
                'passed_validation':gate_result['passed_validation'],
                'pole_values':gate_result['pole_values'],
                'status':status}

    # ---------------- BATCH & VISUALIZATION ----------------
    def evaluate_statements(self, statements, psi, concept_map, evaluator, suffix_map=None):
        results=[]
        for i,s in enumerate(statements):
            concept = concept_map[i]
            suffix = suffix_map[i] if suffix_map else None
            r = self.compute_total_stability(psi, concept, s, evaluator, suffix)
            results.append({'Statement':s,**r})
        return pd.DataFrame(results)

    def visualize_statements(self, df):
        idx = np.arange(len(df))
        width=0.2
        plt.figure(figsize=(12,6))
        # Color-coded by PASS/FAIL
        colors = ['#2ecc71' if s=='PASS' else '#e74c3c' for s in df['status']]
        plt.bar(idx-width, df['unified_score'], width, label='Unified Score', color=colors, alpha=0.7)
        plt.bar(idx, df['tetralectic_score'], width, label='Tetralectic Score', color=colors, alpha=0.5)
        plt.bar(idx+width, df['total_stability_score'], width, label='Total Stability', color=colors, alpha=1.0)
        plt.xticks(idx, [f"S{i+1}" for i in range(len(df))], rotation=45)
        plt.ylabel("Score")
        plt.title("AΩ+ Total Stability Analysis (PASS=Green, FAIL=Red)")
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()
        return df

# ---------------- MOCK EVALUATOR ----------------
def mock_evaluator(statement):
    return np.clip(0.8 + 0.05*np.random.randn(),0,1)

# ---------------- DEMO ----------------
if __name__=="__main__":
    engine=AOPlusEngine(stability_threshold=0.6)
    psi=0.8
    statements=["AI must be transparent.","AI must avoid deception.","AI reasoning must be consistent.","AI hallucinations must be prevented."]
    concept_map=["eleutheria","tyrannia","demokratia","asydosia"]
    df=engine.evaluate_statements(statements,psi,concept_map,mock_evaluator)
    df = engine.visualize_statements(df)
    print(df[['Statement','total_stability_score','status']])

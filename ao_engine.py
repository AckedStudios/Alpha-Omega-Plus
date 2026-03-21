import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class AOPlusEngine:
    """
    Alpha-Omega Plus (AΩ+) Reasoning Engine
    --------------------------------------
    Version: 1.0.7 - Ultimate Production Edition
    Integrates Scalar Field Physics, Tetralectic Logic, 
    and full cluster analytics with DataFrame logging.
    """

    def __init__(self, phi=1.618033, sigma=1.0, verbose=False):
        self.phi = phi
        self.sigma = sigma
        self.verbose = verbose

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
    def scalar_field_pressure_vec(self, psi_arr, lam=0.1):
        psi_arr = np.array(psi_arr, dtype=float)
        return np.abs(lam * psi_arr**3 * np.exp(-psi_arr**2 / self.sigma**2))

    def harmonic_scaling(self, N, T0=100, alpha=2.08):
        return T0 * (self.phi ** (alpha * N))

    # ---------------- LINGUISTIC LAYER ----------------
    def check_kanon_3_vec(self, concept_arr):
        scores = []
        for concept in concept_arr:
            concept = concept.lower().strip()
            if concept in self.stability_matrix:
                entry = self.stability_matrix[concept]
                score = len(entry["spectrum"]) / 4
            else:
                score = 1 / self.phi
            scores.append(round(score,4))
        return np.array(scores)

    def check_kanon_4_vec(self, concept_arr, suffix_arr):
        scores = []
        for c, s in zip(concept_arr, suffix_arr):
            c = c.lower().strip()
            s = s.lower().strip()
            if c in self.stability_matrix:
                ethos = self.stability_matrix[c]["ethos"]
                score = 0.1 if (ethos=="kk" and s=="iki") else 1.0
            else:
                score = 1.0
            scores.append(score)
        return np.array(scores)

    # ---------------- VECTOR MASTER OPERATOR ----------------
    def compute_unified_truth_score_vec(self, psi_arr, concept_arr, suffix_arr=None):
        p_scores = self.scalar_field_pressure_vec(psi_arr)
        k3_scores = self.check_kanon_3_vec(concept_arr)
        if suffix_arr is not None:
            k4_scores = self.check_kanon_4_vec(concept_arr, suffix_arr)
        else:
            k4_scores = np.ones_like(p_scores)
        return np.round(np.abs(p_scores * k3_scores * k4_scores),6)

    # ---------------- TETRALECT ----------------
    def get_tetralect_group(self, concept_root):
        concept = concept_root.lower().strip()
        if concept in self.stability_matrix:
            return [concept] + self.stability_matrix[concept]["partners"]
        return []

    # ---------------- DATAFRAME LOGGING ----------------
    def generate_scores_dataframe(self, concept_root, psi_range=None, suffix=None):
        cluster = self.get_tetralect_group(concept_root)
        if not cluster:
            return pd.DataFrame()
        if psi_range is None:
            psi_range = [0.8]*len(cluster)
        psi_arr = np.array(psi_range[:len(cluster)])
        suffix_arr = [suffix]*len(cluster) if suffix else [None]*len(cluster)
        scores = self.compute_unified_truth_score_vec(psi_arr, cluster, suffix_arr)
        df = pd.DataFrame({
            "Concept": cluster,
            "Psi": psi_arr,
            "Suffix": suffix_arr,
            "UnifiedScore": scores,
            "Ethos": [self.stability_matrix[c]["ethos"] for c in cluster]
        })
        return df

    # ---------------- VISUALIZATION ----------------
    def visualize_stability_vec(self, concept_root, psi=0.8):
        df = self.generate_scores_dataframe(concept_root, [psi]*len(self.get_tetralect_group(concept_root)))
        colors = ['#2ecc71' if e=="kl" else '#e74c3c' for e in df["Ethos"]]
        plt.figure(figsize=(10,6))
        bars = plt.bar(df["Concept"], df["UnifiedScore"], color=colors, edgecolor='black', alpha=0.8)
        plt.title(f"AΩ+ Stability Cluster: {concept_root.capitalize()}")
        plt.ylabel("Unified Truth Score")
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        for bar, score in zip(bars, df["UnifiedScore"]):
            plt.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.002, f"{score}", ha='center', fontweight='bold')
        plt.show()
        return df

    # ---------------- FULL CLUSTER MULTI-Psi ANALYSIS ----------------
    def generate_full_cluster_matrix(self, psi_values=None, suffix=None):
        if psi_values is None:
            psi_values = np.linspace(0.1, 1.0, 10)
        dataframes = []
        for concept in self.stability_matrix.keys():
            df = self.generate_scores_dataframe(concept, psi_range=psi_values, suffix=suffix)
            dataframes.append(df)
        return pd.concat(dataframes, ignore_index=True)

# ---------------- DEMO ----------------
if __name__ == "__main__":
    engine = AOPlusEngine(verbose=True)

    print("⟴ AOPlusEngine v1.0.7 [FINAL EDIT]")
    print("-"*50)
    # Visual and DataFrame single-cluster
    df_vis = engine.visualize_stability_vec("eleutheria", psi=0.8)
    print(df_vis)

    # Multi-Psi full cluster analysis
    df_full = engine.generate_full_cluster_matrix(psi_values=np.linspace(0.2,1.0,5))
    print(df_full)

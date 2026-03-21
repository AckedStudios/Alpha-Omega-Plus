import math

class AOPlusEngine:
    """
    The Alpha-Omega Plus (ΑΩ+) Reasoning Engine.
    Unifies Physics (Scalar Fields) and Linguistics (Tetralectic Kanons).
    """
    def __init__(self, phi=1.618033, sigma=1.0):
        self.phi = phi  # Η Χρυσή Τομή (Ο Ελκυστής)
        self.sigma = sigma # Σταθερά κανονικοποίησης
        
        # Stability Matrix από το "Εγχειρίδιον Τετραλέκτων" (Κανών 3)
        # Εδώ ορίζεται αν μια λέξη έχει πλήρες "Φάσμα"
        self.stability_matrix = {
            "justice": ["justice", "justify", "justified", "just"],
            "harmony": ["harmony", "harmonize", "harmonized", "harmonic"],
            "diakonia": ["diakonia", "diakono", "diakonimeni", "diakoniki"],
            "hegemonia": ["hegemonia", "hegemoneuo", "hegemoneumeni", "hegemoniki"],
            "asydosia": ["asydosia", "asydoto", "asydotimeni", "asydotiki"],
            "tyrannia": ["tyrannia", "tyranno", "tyrannimeni", "tyranniki"]
        }

    def harmonic_scaling(self, N, T0=100, alpha=2.08):
        """Υπολογίζει το δυναμικό budget token βάσει της πολυπλοκότητας N."""
        return T0 * (self.phi ** (alpha * N))

    def scalar_field_pressure(self, psi, lam=0.1):
        """
        Υπολογίζει το 'φρένο' του βαθμωτού πεδίου (Επίπεδο Φυσικής).
        psi: η τιμή του πεδίου που αντιπροσωπεύει τη λογική ροή.
        """
        exponent = -(psi**2) / (self.sigma**2)
        return lam * (psi**3) * math.exp(exponent)

    def check_kanon_3(self, concept_root):
        """
        Εφαρμογή Κανόνα 3: Λεκτικό Φάσμα (Γλωσσικό επίπεδο).
        Επιστρέφει 1.0 για σταθερές έννοιες, 1/Phi για ασύμμετρες.
        """
        concept = concept_root.lower()
        if concept in self.stability_matrix:
            return 1.0
        return round(1 / self.phi, 4)

    def check_kanon_4(self, concept_root, suffix):
        """
        Εφαρμογή Κανόνα 4: Η Παγίδα της Κατάληξης.
        Μια 'κακή' (κκ) έννοια δεν μπορεί ΠΟΤΕ να φέρει επίθετο σε -ική.
        """
        # Οι "κκ" ρίζες από τη λίστα σου
        negative_roots = ["asydosia", "tyrannia"] 
        if concept_root.lower() in negative_roots and suffix == "iki":
            return 0.1  # Κρίσιμη Αποτυχία: Ανίχνευση Σοφιστείας
        return 1.0

    def compute_unified_truth_score(self, psi, concept, current_suffix=None):
        """
        Ο ΚΕΝΤΡΙΚΟΣ ΤΕΛΕΣΤΗΣ: Ενώνει Φυσική και Τετραλεκτική.
        Υπολογίζει την τελική πιθανότητα αλήθειας.
        """
        # 1. Σκορ Επιπέδου Φυσικής
        p_score = self.scalar_field_pressure(psi)
        
        # 2. Σκορ Γλωσσικού Επιπέδου (Κανόνες 3 & 4)
        k3_score = self.check_kanon_3(concept)
        k4_score = self.check_kanon_4(concept, current_suffix) if current_suffix else 1.0
        
        # 3. Ενοποιημένη Ολοκλήρωση
        # Το τελικό σκορ είναι το γινόμενο όλων των συμμετριών.
        final_stability = p_score * k3_score * k4_score
        
        return round(abs(final_stability), 6)

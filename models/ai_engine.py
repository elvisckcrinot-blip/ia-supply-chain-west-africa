import pandas as pd
import numpy as np
from scipy.stats import norm

# --- SECTION 1 : INTELLIGENCE TMS (PRÉDICTION) ---
def prediction_delai_eta(historique_trajets):
    """
    Prédit les retards sur l'axe Malanville.
    Emplacement pour modèle Random Forest ou XGBoost.
    """
    # Ici viendra ton code scikit-learn
    return "Estimation en cours..."

# --- SECTION 2 : INTELLIGENCE WMS (OPTIMISATION, QUALITÉ & ANOMALIES) ---

def predict_safety_stock(service_level, sigma_demand, lead_time):
    """
    Calcule le stock de sécurité optimal (Concept MIT SC0x).
    Formule : SS = Z * sigma_d * sqrt(L)
    """
    z_score = norm.ppf(service_level)
    safety_stock = z_score * sigma_demand * np.sqrt(lead_time)
    return round(safety_stock, 2)

def classify_abc(data_df):
    """
    Analyse de Pareto automatique pour l'entrepôt GDIZ.
    """
    if data_df.empty: return data_df
    data_df = data_df.sort_values(by='valeur_consommation', ascending=False)
    data_df['cum_perc'] = 100 * (data_df['valeur_consommation'].cumsum() / data_df['valeur_consommation'].sum())
    
    def category(perc):
        if perc <= 80: return 'A (Critique)'
        elif perc <= 95: return 'B (Modéré)'
        else: return 'C (Faible)'
        
    data_df['Categorie_ABC'] = data_df['cum_perc'].apply(category)
    return data_df

def analyse_six_sigma(unites_preparees, defauts_constates):
    """
    Calcule la performance qualité des opérations d'entrepôt (Lean Six Sigma).
    DPMO : Defects Per Million Opportunities.
    """
    if unites_preparees == 0: 
        return 0, 0
    
    # Calcul du DPMO
    dpmo = (defauts_constates / unites_preparees) * 1_000_000
    
    # Calcul du Niveau Sigma (avec le décalage conventionnel de 1.5 sigma)
    # On utilise max(dpmo, 1) pour éviter les erreurs log avec 0 défaut
    z_score = norm.ppf(1 - (max(dpmo, 1) / 1_000_000))
    niveau_sigma = z_score + 1.5
    
    return round(dpmo, 0), round(niveau_sigma, 2)

def detection_anomalies_stock(data_stock):
    """
    Identifie les vols ou erreurs de saisie via Isolation Forest.
    """
    # Ici viendra ton code de détection d'anomalies (Scikit-learn)
    return data_stock
        

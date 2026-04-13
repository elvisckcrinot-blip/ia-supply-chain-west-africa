import pandas as pd
import numpy as np
from scipy.stats import norm
from sklearn.ensemble import RandomForestRegressor, IsolationForest

# =================================================================
# SECTION 1 : INTELLIGENCE TMS (PRÉDICTION CORRIDOR)
# =================================================================

def prediction_delai_eta(features_trajet):
    """
    Moteur prédictif basé sur Random Forest.
    Analyse l'impact de la saisonnalité et du fret sur le temps de trajet.
    """
    # Note : Dans une version avancée, on chargerait un modèle joblib pré-entraîné
    # Ici, nous simulons l'inférence pour la démo
    # features : [mois, type_fret, poids, meteo]
    return "Calcul ETA via Random Forest..."

# =================================================================
# SECTION 2 : INTELLIGENCE WMS (STOCKS & SIX SIGMA)
# =================================================================

def predict_safety_stock(service_level, sigma_demand, lead_time):
    """
    Optimisation du Safety Stock (Référentiel MIT SC0x).
    Utilise la distribution normale pour garantir le taux de service.
    """
    try:
        # Calcul du coefficient de sécurité Z
        z_score = norm.ppf(service_level)
        
        # Formule robuste : Z * σ_demand * √LeadTime
        safety_stock = z_score * sigma_demand * np.sqrt(lead_time)
        
        return int(np.ceil(safety_stock))
    except Exception:
        return 0

def classify_abc(data_df):
    """
    Segmentation intelligente des stocks (GDIZ Center).
    Automatisation du Pareto pour la priorisation du réapprovisionnement.
    """
    if data_df.empty or 'valeur_consommation' not in data_df.columns:
        return data_df
        
    df = data_df.sort_values(by='valeur_consommation', ascending=False).copy()
    
    total = df['valeur_consommation'].sum()
    if total == 0:
        df['Categorie_ABC'] = 'C (Faible)'
        return df
        
    df['cum_perc'] = 100 * (df['valeur_consommation'].cumsum() / total)
    
    def category(perc):
        if perc <= 80: return 'A (Critique)'
        elif perc <= 95: return 'B (Modéré)'
        else: return 'C (Faible)'
        
    df['Categorie_ABC'] = df['cum_perc'].apply(category)
    return df

# =================================================================
# SECTION 3 : QUALITÉ & SÉCURITÉ (ANOMALIES SIX SIGMA)
# =================================================================

def detection_anomalies_stock(data_stock):
    """
    Identification des écarts d'inventaire via Isolation Forest (Machine Learning).
    Détecte les erreurs de saisie ou les pertes suspectes à la GDIZ.
    """
    if len(data_stock) < 5: # Besoin d'un minimum de données
        return data_stock
        
    # On isole les colonnes numériques pour le modèle
    model = IsolationForest(contamination=0.05, random_state=42)
    # Simulation sur la colonne Quantité
    data_stock['Anomalie_Score'] = model.fit_predict(data_stock[['Quantité']])
    
    # -1 indique une anomalie, 1 est normal
    return data_stock
    

import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm

st.set_page_config(page_title="WMS Expert - Inventory Dynamics", layout="wide")

st.title("📦 WMS : Gestion Stochastique (Modèles SC1x & SC2x)")
st.info("Focus : Service Level, Safety Stock & EOQ de Wilson")

# --- PARAMÈTRES EXPERTS (SC1x) ---
with st.sidebar:
    st.header("Configuration Inventaire")
    csl = st.slider("Cycle Service Level (CSL)", 0.80, 0.99, 0.95)
    cout_commande = st.number_input("Coût de Passation (K)", value=15000)
    taux_possession = st.slider("Taux de Possession (h)", 0.05, 0.30, 0.15)
    lead_time = st.number_input("Lead Time (Jours)", value=15)

# --- CALCULS LOGIQUES MIT ---
# Données simulées (ou importées)
data = {
    'SKU': ['REF-01', 'REF-02', 'REF-03'],
    'Demande_Moy_J': [10, 50, 100],
    'Sigma_Demande': [2, 8, 15], # Écart-type de la demande
    'Prix_Unit': [5000, 1200, 8000]
}
df = pd.DataFrame(data)

# 1. Calcul du Z-Score (Inverse de la loi normale)
z = norm.ppf(csl)

# 2. Stock de Sécurité (Safety Stock) stochastique
# Formule : Z * Sigma_D * sqrt(LeadTime)
df['Safety_Stock'] = (z * df['Sigma_Demande'] * np.sqrt(lead_time)).astype(int)

# 3. EOQ (Economic Order Quantity) - Modèle de Wilson
# Formule : sqrt( (2 * Demande_Annuelle * K) / (h * Prix_Unit) )
df['Demande_Annuelle'] = df['Demande_Moy_J'] * 365
df['EOQ'] = np.sqrt((2 * df['Demande_Annuelle'] * cout_commande) / (taux_possession * df['Prix_Unit'])).astype(int)

# 4. Point de Commande (ROP)
df['ROP'] = (df['Demande_Moy_J'] * lead_time) + df['Safety_Stock']

# --- DASHBOARD ---
st.subheader("🚀 Optimisation des Niveaux de Stock")
st.table(df[['SKU', 'Demande_Annuelle', 'Safety_Stock', 'EOQ', 'ROP']])

# Analyse ABC Financière (Pareto SC1x)
df['Valeur_Annuelle'] = df['Demande_Annuelle'] * df['Prix_Unit']
df = df.sort_values('Valeur_Annuelle', ascending=False)
df['Cum_Pct'] = 100 * df['Valeur_Annuelle'].cumsum() / df['Valeur_Annuelle'].sum()
df['Classe'] = df['Cum_Pct'].apply(lambda x: 'A' if x <= 80 else ('B' if x <= 95 else 'C'))

st.subheader("📊 Segmentation Stratégique ABC")
st.dataframe(df[['SKU', 'Classe', 'Valeur_Annuelle', 'Cum_Pct']], use_container_width=True)
    

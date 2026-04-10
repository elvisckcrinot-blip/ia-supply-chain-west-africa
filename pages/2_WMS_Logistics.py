import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. CONFIGURATION
st.set_page_config(page_title="WMS - Usine X", layout="wide")

st.title("📦 WMS : Gestion d'Entrepôt & Optimisation ABC")

with st.sidebar:
    st.header("🔍 Anticipation & Scénarios")
    hausse = st.slider("Augmentation demande (%)", 0, 100, 0) / 100
    retard = st.number_input("Retard logistique (Jours)", value=0)

# 2. DONNÉES D'INVENTAIRE (Données diversifiées pour forcer la segmentation ABC)
data_wms = {
    'SKU': ['REF-MAI-01', 'REF-COT-02', 'REF-SOJ-03', 'REF-CAJ-04', 'REF-CIM-05'],
    'Désignation': ['Maïs Grain', 'Coton Fibre', 'Soja Bio', 'Cajou Brut', 'Ciment Sac'],
    'Prix': [250, 450, 350, 600, 5000],
    'Stock_Physique': [500, 120, 800, 50, 2000],
    'Vente_Moy_J': [15, 10, 25, 5, 100]
}
df = pd.DataFrame(data_wms)

# --- 3. INTELLIGENCE ABC (CORRIGÉE) ---
df['Valeur_Stock_Total'] = df['Stock_Physique'] * df['Prix']

# TRI CRITIQUE : Du plus cher au moins cher pour respecter la loi de Pareto
df = df.sort_values(by='Valeur_Stock_Total', ascending=False).reset_index(drop=True)

df['Cumul_Valeur'] = df['Valeur_Stock_Total'].cumsum()
total_valeur = df['Valeur_Stock_Total'].sum()
df['Pct_Cumul'] = (df['Cumul_Valeur'] / total_valeur) * 100

# Fonction de classification stricte
def classifier_abc(pct):
    if pct <= 80: return 'A', 0.98  # Produits majeurs
    elif pct <= 95: return 'B', 0.90 # Produits intermédiaires
    else: return 'C', 0.85          # Produits mineurs

df[['Classe_ABC', 'Taux_Satisfaction']] = df['Pct_Cumul'].apply(lambda x: pd.Series(classifier_abc(x)))

# --- 4. CALCULS OPÉRATIONNELS ---
df['Besoin_J'] = df['Vente_Moy_J'] * (1 + hausse)
df['Seuil_Alerte'] = (df['Besoin_J'] * (14 + retard + (df['Taux_Satisfaction'] * 10))).astype(int)
df['Couverture_Jours'] = (df['Stock_Physique'] / df['Besoin_J']).astype(int)
df['Valeur_Risque'] = df.apply(lambda x: (x['Besoin_J'] * x['Prix'] * 7) if x['Stock_Physique'] <= x['Seuil_Alerte'] else 0, axis=1)

# Statut
def get_status(row):
    if row['Stock_Physique'] <= 0: return "🚫 RUPTURE"
    if row['Stock_Physique'] <= row['Seuil_Alerte']: return "🔴 CRITIQUE"
    return "🟢 OPTIMAL"
df['Statut'] = df.apply(get_status, axis=1)

# 5. DASHBOARD
k1, k2, k3 = st.columns(3)
k1.metric("Valeur Inventaire", f"{total_valeur:,.0f} FCFA")
k2.metric("Valeur en Risque", f"{df['Valeur_Risque'].sum():,.0f} FCFA", delta_color="inverse")
k3.metric("Besoin Réappro", len(df[df['Stock_Physique'] <= df['Seuil_Alerte']]))

# 6. TABLEAU DE BORD
st.subheader("📋 État Global de l'Inventaire & Analyse Stratégique")

def style_abc(val):
    color = '#ff4b4b' if val == 'A' else ('#ffa500' if val == 'B' else '#008000')
    return f'color: {color}; font-weight: bold'

st.dataframe(
    df[['Classe_ABC', 'SKU', 'Désignation', 'Stock_Physique', 'Couverture_Jours', 'Seuil_Alerte', 'Statut']]
    .style.map(style_abc, subset=['Classe_ABC']),
    use_container_width=True
)

# 7. PLAN DE RÉAPPROVISIONNEMENT
st.header("🛒 Plan de Réapprovisionnement")
df_reap = df[df['Stock_Physique'] <= df['Seuil_Alerte']].copy()
if not df_reap.empty:
    df_reap['Qte_Suggérée'] = (df_reap['Besoin_J'] * 30).astype(int)
    st.table(df_reap[['Classe_ABC', 'SKU', 'Désignation', 'Stock_Physique', 'Qte_Suggérée']])
    st.download_button("📥 Télécharger l'Ordre d'Achat", df_reap.to_csv(index=False).encode('utf-8'), "ordre_achat_abc.csv")
else:
    st.success("✅ Niveaux de stock optimaux.")

# 8. VISUALISATION (MULTI-COULEURS)
fig_pie = px.pie(df, values='Valeur_Stock_Total', names='Classe_ABC', 
                 title="Répartition de la Valeur (Pareto ABC)",
                 color='Classe_ABC',
                 color_discrete_map={'A':'#ff4b4b', 'B':'#ffa500', 'C':'#008000'})
st.plotly_chart(fig_pie, use_container_width=True)

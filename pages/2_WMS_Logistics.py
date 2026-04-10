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
    st.info("L'ajustement ABC optimise automatiquement le stock de sécurité selon l'importance du produit.")

# 2. DONNÉES D'INVENTAIRE (Version Unifiée)
data_wms = {
    'SKU': ['REF-MAI-01', 'REF-COT-02', 'REF-SOJ-03', 'REF-CAJ-04', 'REF-CIM-05'],
    'Désignation': ['Maïs Grain', 'Coton Fibre', 'Soja Bio', 'Cajou Brut', 'Ciment Sac'],
    'Prix': [250, 450, 350, 600, 5000],
    'Stock_Physique': [500, 120, 800, 50, 2000],
    'Vente_Moy_J': [15, 10, 25, 5, 100]
}
df = pd.DataFrame(data_wms)

# --- 3. LOGIQUE ABC & SATISFACTION CLIENT ---
df['Valeur_Stock_Total'] = df['Stock_Physique'] * df['Prix']
df = df.sort_values(by='Valeur_Stock_Total', ascending=False)
df['Cumul_Valeur'] = df['Valeur_Stock_Total'].cumsum()
total_valeur = df['Valeur_Stock_Total'].sum()
df['Pct_Cumul'] = (df['Cumul_Valeur'] / total_valeur) * 100

def classifier_abc(pct):
    if pct <= 80: return 'A', 0.98  # Produits A : 98% satisfaction (Hautement critique)
    elif pct <= 95: return 'B', 0.90 # Produits B : 90% satisfaction (Intermédiaire)
    else: return 'C', 0.85          # Produits C : 85% satisfaction (Faible impact financier)

df[['Classe_ABC', 'Taux_Satisfaction']] = df['Pct_Cumul'].apply(lambda x: pd.Series(classifier_abc(x)))

# --- 4. CALCULS OPÉRATIONNELS AVANCÉS ---
df['Besoin_J'] = df['Vente_Moy_J'] * (1 + hausse)

# Seuil d'alerte (ROP) dynamique : Délai de livraison + Marge de sécurité basée sur la classe ABC
# Plus le taux de satisfaction est haut, plus le seuil de commande s'élève pour éviter la rupture.
df['Seuil_Alerte'] = (df['Besoin_J'] * (14 + retard + (df['Taux_Satisfaction'] * 10))).astype(int)

df['Couverture_Jours'] = (df['Stock_Physique'] / df['Besoin_J']).astype(int)

# Valeur en risque (Manque à gagner sur 7 jours si rupture)
df['Valeur_Risque'] = df.apply(
    lambda x: (x['Besoin_J'] * x['Prix'] * 7) if x['Stock_Physique'] <= x['Seuil_Alerte'] else 0, 
    axis=1
)

# 5. DASHBOARD DE DIRECTION
k1, k2, k3 = st.columns(3)
k1.metric("Valeur Inventaire", f"{total_valeur:,.0f} FCFA")
k2.metric("Valeur en Risque", f"{df['Valeur_Risque'].sum():,.0f} FCFA", delta_color="inverse")
k3.metric("Besoin Réappro (Alertes)", len(df[df['Stock_Physique'] <= df['Seuil_Alerte']]))

# 6. TABLEAU DE BORD DÉTAILLÉ
st.subheader("📋 État Global de l'Inventaire & Analyse Stratégique")

def get_status(row):
    if row['Stock_Physique'] <= 0: return "🚫 RUPTURE"
    if row['Stock_Physique'] <= row['Seuil_Alerte']: return "🔴 CRITIQUE"
    return "🟢 OPTIMAL"
df['Statut'] = df.apply(get_status, axis=1)

# Mise en forme visuelle des classes ABC
def style_abc(val):
    color = '#ff4b4b' if val == 'A' else ('#ffa500' if val == 'B' else '#008000')
    return f'color: {color}; font-weight: bold'

st.dataframe(
    df[['Classe_ABC', 'SKU', 'Désignation', 'Stock_Physique', 'Couverture_Jours', 'Seuil_Alerte', 'Taux_Satisfaction', 'Statut']]
    .style.applymap(style_abc, subset=['Classe_ABC']),
    use_container_width=True
)

# 7. PLAN DE RÉAPPROVISIONNEMENT AUTOMATIQUE
st.header("🛒 3. Plan de Réapprovisionnement Automatique")
df_reap = df[df['Stock_Physique'] <= df['Seuil_Alerte']].copy()

if not df_reap.empty:
    # Quantité suggérée : Couverture pour 30 jours
    df_reap['Qte_Suggérée'] = (df_reap['Besoin_J'] * 30).astype(int)
    st.table(df_reap[['Classe_ABC', 'SKU', 'Désignation', 'Stock_Physique', 'Qte_Suggérée']])
    
    csv = df_reap.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Télécharger l'Ordre d'Achat", csv, "ordre_achat_abc.csv", "text/csv")
else:
    st.success("✅ Tous les niveaux de stock sont optimaux selon les objectifs de satisfaction client.")

# 8. VISUALISATION
c1, c2 = st.columns(2)
with c1:
    fig_pie = px.pie(df, values='Valeur_Stock_Total', names='Classe_ABC', 
                     title="Répartition de la Valeur (Pareto ABC)",
                     color='Classe_ABC',
                     color_discrete_map={'A':'#ff4b4b', 'B':'#ffa500', 'C':'#008000'})
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    fig_bar = px.bar(df, x='SKU', y='Valeur_Stock_Total', color='Classe_ABC',
                     title="Valeur par SKU et Importance Stratégique")
    st.plotly_chart(fig_bar, use_container_width=True)
    

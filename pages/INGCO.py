import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page pour le module INGCO
st.set_page_config(page_title="INGCO BENIN - Optimisation Stock", layout="wide")

st.title("📦 INGCO BÉNIN : Gestion de Stock 4.0")
st.markdown("---")

# 1. Moteur de simulation pour 500 articles
@st.cache_data
def charger_donnees_ingco():
    # Simulation d'un catalogue de 500 articles
    data = {
        'ref_sku': [f'ING-REF-{i}' for i in range(1, 501)],
        'designation': [f'Outil INGCO Professionnel {i}' for i in range(1, 501)],
        'prix_usine_fcfa': [150000 if i % 10 == 0 else 12500 for i in range(1, 501)],
        'vol_unitaire_cbm': [0.15 if i % 10 == 0 else 0.005 for i in range(1, 501)],
        'lead_time_jours': [60] * 500,
        'vente_moy_jour': [2 if i % 10 == 0 else 8 for i in range(1, 501)],
        'stock_physique': [145 if i % 10 == 0 else 350 for i in range(1, 501)],
        'stock_securite': [30] * 500
    }
    return pd.DataFrame(data)

df = charger_donnees_ingco()

# 2. Calculs Logistiques MIT (Étape 2 & 3)
df['ROP'] = (df['vente_moy_jour'] * df['lead_time_jours']) + df['stock_securite']
df['alerte'] = df.apply(lambda x: '🔴 RUPTURE' if x['stock_physique'] <= x['ROP'] else '🟢 OK', axis=1)
df['valeur_stock'] = df['stock_physique'] * df['prix_usine_fcfa']

# 3. Affichage des KPIs (Indicateurs Clés)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Taux de Service", "94.2%", "+1.2% vs mois dernier")
with col2:
    st.metric("Articles en Alerte", len(df[df['alerte'] == '🔴 RUPTURE']), "Sur 500 articles")
with col3:
    vol_total_cmd = (df[df['alerte'] == '🔴 RUPTURE']['vol_unitaire_cbm'] * 10).sum()
    remplissage = (vol_total_cmd / 33) * 100
    st.metric("Remplissage Conteneur", f"{remplissage:.1f}%", "Capacité 33m³")

# 4. Graphique Interactif
st.subheader("📊 État des stocks - Top 30 Articles")
fig = px.bar(df.head(30), x='ref_sku', y='stock_physique', color='alerte', 
             title="Stock Actuel vs Point de Commande (ROP)",
             labels={'stock_physique': 'Quantité en Stock', 'ref_sku': 'Référence Article'})
st.plotly_chart(fig, use_container_width=True)

# 5. Liste complète des 500 articles
st.subheader("🔍 Inventaire complet & Prévisions")
search = st.text_input("Filtrer par référence (ex: ING-REF-10)")
if search:
    df_display = df[df['ref_sku'].str.contains(search)]
else:
    df_display = df

st.dataframe(df_display[['ref_sku', 'designation', 'stock_physique', 'ROP', 'alerte', 'valeur_stock']], 
             use_container_width=True)

st.info("💡 Les calculs de Point de Commande (ROP) sont basés sur les modèles SC1x du MIT.")

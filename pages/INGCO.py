import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="INGCO - Import Réel", layout="wide")

st.title("📦 INGCO BÉNIN : Importation de Données")

# --- SYSTÈME D'IMPORTATION ---
st.sidebar.header("Configuration")
uploaded_file = st.sidebar.file_uploader("Charger le fichier Excel INGCO", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Lecture des données réelles
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.success("✅ Données réelles chargées avec succès !")
else:
    # Données par défaut si aucun fichier n'est chargé
    st.warning("⚠️ Utilisation des données de simulation (chargez un fichier pour actualiser)")
    data = {
        'ref_sku': [f'ING-REF-{i}' for i in range(1, 501)],
        'designation': [f'Outil Pro {i}' for i in range(1, 501)],
        'prix_usine_fcfa': [150000 if i % 10 == 0 else 12500 for i in range(1, 501)],
        'vol_unitaire_cbm': [0.15 if i % 10 == 0 else 0.005 for i in range(1, 501)],
        'lead_time_jours': [60] * 500,
        'vente_moy_jour': [2] * 500,
        'stock_physique': [145] * 500,
        'stock_securite': [30] * 500
    }
    df = pd.DataFrame(data)

# --- MOTEUR DE CALCUL MIT ---
df['ROP'] = (df['vente_moy_jour'] * df['lead_time_jours']) + df['stock_securite']
df['alerte'] = df.apply(lambda x: '🔴 RUPTURE' if x['stock_physique'] <= x['ROP'] else '🟢 OK', axis=1)

# --- AFFICHAGE DES RÉSULTATS ---
st.metric("Nombre d'articles analysés", len(df))

st.subheader("🔍 Aperçu de l'inventaire")
st.dataframe(df, use_container_width=True)

# Graphique de rupture
fig = px.pie(df, names='alerte', title="État global des stocks", color='alerte',
             color_discrete_map={'🔴 RUPTURE':'red', '🟢 OK':'green'})
st.plotly_chart(fig)
    

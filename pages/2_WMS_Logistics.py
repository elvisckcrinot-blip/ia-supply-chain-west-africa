import streamlit as st
import pandas as pd
# Importation corrigée pour correspondre à ton fichier models/mit_calculations.py
from models.mit_calculations import calcul_wilson_eoq, calcul_point_de_commande, analyse_pareto_abc
from utils.helpers import load_logistics_data
import io

# --- 1. CONFIGURATION ET STYLE ---
st.set_page_config(page_title="WMS Intelligence · MIT CTL", layout="wide")

st.markdown("""
<style>
    @import url('https://googleapis.com');
    .main-title { font-family: 'Syne', sans-serif; color: #ffad1f; font-size: 38px; font-weight: 800; }
    .wms-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; }
    .metric-val { font-family: 'Syne', sans-serif; font-size: 28px; color: #ffad1f; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# --- 2. INTERFACE ---
st.markdown('<h1 class="main-title">📦 WMS Intelligence : Stocks & Ruptures</h1>', unsafe_allow_html=True)
st.markdown("---")

# Navigation par onglets pour plus de clarté
tab1, tab2 = st.tabs(["📊 Analyse d'Inventaire", "⚙️ Simulateur Wilson (EOQ)"])

# --- ONGLET 1 : ANALYSE D'INVENTAIRE RÉEL ---
with tab1:
    st.sidebar.header("📁 Importation des données")
    uploaded_file = st.sidebar.file_uploader("Charger le stock (CSV/Excel)", type=["csv", "xlsx"])

    if uploaded_file:
        # Lecture du fichier
        df_stock = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        # Vérification des colonnes nécessaires pour Pareto
        if 'Valeur' in df_stock.columns:
            df_analyse = analyse_pareto_abc(df_stock, 'Valeur')
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="wms-card">Label: TOTAL RÉFÉRENCES<div class="metric-val">{len(df_analyse)}</div></div>', unsafe_allow_html=True)
            with c2:
                val_total = f"{df_analyse['Valeur'].sum():,.0f}".replace(",", " ")
                st.markdown(f'<div class="wms-card">VALEUR DU STOCK<div class="metric-val">{val_total} FCFA</div></div>', unsafe_allow_html=True)
            with c3:
                nb_a = len(df_analyse[df_analyse['Classe_ABC'] == 'A'])
                st.markdown(f'<div class="wms-card">ARTICLES CLASSE A (CRITIQUE)<div class="metric-val">{nb_a}</div></div>', unsafe_allow_html=True)

            st.write("### 📋 Tableau de classification ABC (Pareto)")
            st.dataframe(df_analyse[['Référence', 'Valeur', 'Classe_ABC']], use_container_width=True)
        else:
            st.error("Le fichier doit contenir une colonne nommée 'Valeur' pour l'analyse ABC.")
    else:
        st.info("💡 Veuillez charger un fichier dans la barre latérale pour démarrer l'analyse d'inventaire.")

# --- ONGLET 2 : SIMULATEUR WILSON ---
with tab2:
    st.write("### Optimisation du Réapprovisionnement")
    with st.expander("🛠️ Paramètres du Calculateur Wilson", expanded=True):
        col_w1, col_w2, col_w3 = st.columns(3)
        demande = col_w1.number_input("Demande annuelle prévue", value=1200)
        cout_c = col_w2.number_input("Coût de passation de commande (FCFA)", value=5000)
        cout_s = col_w3.number_input("Coût de possession par unité/an (FCFA)", value=250)

        if st.button("Calculer la Quantité Économique"):
            eoq = calcul_wilson_eoq(demande, cout_c, cout_s)
            st.success(f"La quantité idéale à commander (EOQ) est de **{eoq} unités**.")
            st.info("Ce modèle minimise le coût total (Stockage + Commandes) selon le référentiel MIT SC1x.")

st.sidebar.info("Référentiel : MIT CTL · Warehouse Intelligence")

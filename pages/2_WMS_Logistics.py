import streamlit as st
import pandas as pd
from models.mit_calculations import calcul_wilson_eoq, analyse_pareto_abc
import datetime

# --- 1. CONFIGURATION ET STYLE ---
st.set_page_config(page_title="WMS Intelligence · Bénin", layout="wide")

st.markdown("""
<style>
    @import url('https://googleapis.com');
    .main-title { font-family: 'Syne', sans-serif; color: #ffad1f; font-size: 38px; font-weight: 800; }
    .wms-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; text-align: center; }
    .wms-val { font-family: 'Syne', sans-serif; font-size: 32px; font-weight: 800; color: #ffad1f; }
    .status-alert { padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📦 WMS Intelligence : Stocks & Alertes</h1>', unsafe_allow_html=True)
st.markdown("---")

tab1, tab2 = st.tabs(["📊 Analyse & Alertes Ruptures", "⚙️ Simulateur Wilson (EOQ)"])

# --- ONGLET 1 : ANALYSE ET ALERTES ---
with tab1:
    st.sidebar.header("📁 Importation des données")
    uploaded_file = st.sidebar.file_uploader("Charger inventaire (Référence, Valeur, Quantité, ROP_Seuil)", type=["csv", "xlsx"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        # Vérification des colonnes critiques
        cols_requises = ['Référence', 'Valeur', 'Quantité', 'ROP_Seuil']
        if all(col in df.columns for col in cols_requises):
            
            # 1. Calcul des Analyses
            df_abc = analyse_pareto_abc(df, 'Valeur')
            
            def definir_statut(row):
                if row['Quantité'] <= row['ROP_Seuil']: return "🔴 RUPTURE"
                if row['Quantité'] <= row['ROP_Seuil'] * 1.2: return "🟠 STOCK FAIBLE"
                return "🟢 OPTIMAL"
            
            df_abc['Statut'] = df_abc.apply(definir_statut, axis=1)
            
            # 2. Tableau de Bord (KPIs)
            c1, c2, c3 = st.columns(3)
            nb_ruptures = len(df_abc[df_abc['Statut'] == "🔴 RUPTURE"])
            
            val_total = f"{df['Valeur'].sum():,.0f}".replace(",", " ")
            c1.markdown(f'<div class="wms-card"><div style="color:#7a92b0; font-size:12px;">VALEUR DU STOCK</div><div class="wms-val">{val_total} FCFA</div></div>', unsafe_allow_html=True)
            
            c2.markdown(f'<div class="wms-card"><div style="color:#7a92b0; font-size:12px;">ALERTES RUPTURES</div><div class="wms-val" style="color:#ff4b4b;">{nb_ruptures}</div></div>', unsafe_allow_html=True)
            
            nb_a = len(df_abc[df_abc['Classe_ABC'] == 'A'])
            c3.markdown(f'<div class="wms-card"><div style="color:#7a92b0; font-size:12px;">ARTICLES CLASSE A</div><div class="wms-val">{nb_a}</div></div>', unsafe_allow_html=True)

            # 3. Affichage des alertes prioritaires
            if nb_ruptures > 0:
                st.error(f"⚠️ {nb_ruptures} articles nécessitent une commande immédiate (Stock ≤ Seuil ROP).")
            
            st.write("### 📋 Rapport complet d'inventaire (Modèle MIT)")
            
            # Formatage visuel du tableau
            st.dataframe(df_abc[['Référence', 'Valeur', 'Classe_ABC', 'Quantité', 'ROP_Seuil', 'Statut']], use_container_width=True)
            
        else:
            st.warning(f"Format incorrect. Colonnes attendues : {', '.join(cols_requises)}")
    else:
        st.info("👋 Prêt pour l'analyse. Veuillez importer votre fichier incluant les colonnes 'Quantité' et 'ROP_Seuil' pour activer les alertes.")

# --- ONGLET 2 : OPTIMISATION WILSON ---
with tab2:
    st.write("### Calculateur Quantité Économique (EOQ)")
    col_w1, col_w2 = st.columns([1, 1.2])
    with col_w1:
        demande = st.number_input("Demande annuelle prévue", value=1200)
        cout_p = st.number_input("Coût de passation (FCFA)", value=5000)
        cout_s = st.number_input("Coût de stockage /unité /an (FCFA)", value=250)
    with col_w2:
        res_eoq = calcul_wilson_eoq(demande, cout_p, cout_s)
        st.markdown(f"""<div class="wms-card"><div style="color: #7a92b0; font-size: 14px;">EOQ MIT CTL</div><div class="wms-val">{res_eoq} Unités</div></div>""", unsafe_allow_html=True)

st.sidebar.info("Module WMS · Axe stratégique GDIZ")
        

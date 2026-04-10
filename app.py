import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
from scipy.stats import norm

# ==========================================
# 1. CONFIGURATION UNIFIÉE
# ==========================================
st.set_page_config(page_title="Hub Logistique Expert - Usine X", layout="wide", page_icon="🏢")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'accueil'
if 'db_tms' not in st.session_state:
    st.session_state.db_tms = pd.DataFrame([{'ID': 'EXP-UX-101', 'Camion': 'RB 1234', 'Position': 'Bohicon', 'Statut': 'En Transit'}])

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ==========================================
# 2. PAGE D'ACCUEIL (HUB)
# ==========================================
if st.session_state.page == 'accueil':
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏢 Hub Logistique Intégré - Usine X</h1>", unsafe_allow_html=True)
    st.write("##")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.info("### 🚛 Module TMS")
        st.write("Optimisation des flux transport & Métriques de performance Tonne-Kilomètre (MIT SC1x).")
        if st.button("ACCÉDER AU TMS"): go_to('tms')
    with col2:
        st.success("### 📦 Module WMS")
        st.write("Gestion stochastique des stocks, EOQ de Wilson & Analyse de risque financier.")
        if st.button("ACCÉDER AU WMS"): go_to('wms')

# ==========================================
# 3. MODULE TMS (Transport + MIT SC1x)
# ==========================================
elif st.session_state.page == 'tms':
    if st.sidebar.button("⬅️ Retour au Hub"): go_to('accueil')
    st.title("🚛 TMS Logistics : Pilotage & Ingénierie")

    # --- INPUTS EXPERTS MIT ---
    with st.sidebar:
        st.header("Paramètres Flotte")
        charge_utile = st.number_input("Charge utile (Tonnes)", value=25.0)
        taux_remp = st.slider("Taux de remplissage (%)", 10, 100, 85) / 100
        conso = st.number_input("Conso (L/100km)", value=32.0)

    # --- CALCULS ROI & MIT ---
    c1, c2, c3, c4 = st.columns(4)
    dist_annuelle = 45000 # km/an estimé
    economie_carburant = dist_annuelle * (conso/100) * 0.15 * 700 # 15% d'optimisation
    c1.metric("Économie Carburant", f"{economie_carburant:,.0f} FCFA")
    
    # Métrique MIT : Coût Tonne-Kilomètre
    charge_reelle = charge_utile * taux_remp
    cout_tkm = ((conso/100)*700) / charge_reelle
    c2.metric("Coût Tonne-Kilomètre", f"{cout_tkm:.2f} F/T.km")
    
    # Métrique SC0x : CO2
    c3.metric("CO2 Évité", "4.2 Tonnes/an")
    c4.metric("Charge Réelle", f"{charge_reelle} T")

    # --- TRACKING & DOCKING (FONCTIONNALITÉS INITIALES) ---
    st.header("📍 Suivi Territorial & Docking")
    villes = {"Usine X (Départ)": 0, "Cotonou": 25, "Bohicon": 105, "Parakou": 395, "Malanville": 720}
    
    col_f1, col_f2 = st.columns([1, 1.5])
    with col_f1:
        with st.form("dock_form"):
            camion = st.text_input("Immatriculation", "RB 0000")
            pos_actuelle = st.selectbox("Dernière Position", list(villes.keys()))
            if st.form_submit_button("Actualiser Position"):
                new_log = pd.DataFrame([{'ID': 'EXP-NEW', 'Camion': camion, 'Position': pos_actuelle, 'Statut': 'En Transit'}])
                st.session_state.db_tms = pd.concat([st.session_state.db_tms, new_log], ignore_index=True)
    
    with col_f2:
        st.dataframe(st.session_state.db_tms, use_container_width=True)
        km_faits = villes[pos_actuelle]
        st.progress(min(km_faits / 720, 1.0))
        st.caption(f"Progression : {km_faits} km parcourus depuis l'Usine X")

# ==========================================
# 4. MODULE WMS (Stocks + MIT SC1x/SC2x)
# ==========================================
elif st.session_state.page == 'wms':
    if st.sidebar.button("⬅️ Retour au Hub"): go_to('accueil')
    st.title("📦 WMS : Intelligence & Performance Stocks")

    # --- PARAMÈTRES STOCHASTIQUES (SC1x) ---
    with st.sidebar:
        st.header("Ingénierie Inventaire")
        csl = st.slider("Service Level Cible (Z)", 0.80, 0.99, 0.95)
        k_passation = st.number_input("Coût de Commande (K)", value=15000)
        h_possession = st.slider("Taux de Possession (h)", 0.05, 0.30, 0.15)
        lead_time = st.number_input("Lead Time (Jours)", value=14)

    # --- LOGIQUE DE CALCULS ---
    data = {
        'SKU': ['REF-01', 'REF-02', 'REF-03'],
        'Prix_Unit': [15000, 45000, 2500],
        'Vente_Moy_J': [12, 5, 45],
        'Sigma_Demande': [3, 1.5, 8], # Écart-type (Incertitude MIT)
        'Stock_Physique': [150, 40, 200]
    }
    df = pd.DataFrame(data)
    
    # 1. Stock de Sécurité Stochastique (Z * sigma * sqrt(L))
    z = norm.ppf(csl)
    df['Safety_Stock'] = (z * df['Sigma_Demande'] * np.sqrt(lead_time)).astype(int)
    
    # 2. EOQ Wilson (SC1x)
    df['Demande_Annuelle'] = df['Vente_Moy_J'] * 365
    df['EOQ'] = np.sqrt((2 * df['Demande_Annuelle'] * k_passation) / (h_possession * df['Prix_Unit'])).astype(int)
    
    # 3. ROP & Risque Financier (Fonctionnalités initiales)
    df['ROP'] = (df['Vente_Moy_J'] * lead_time) + df['Safety_Stock']
    df['Valeur_Stock'] = df['Stock_Physique'] * df['Prix_Unit']
    df['Risque_FCFA'] = df.apply(lambda x: (x['Vente_Moy_J'] * x['Prix_Unit'] * 7) if x['Stock_Physique'] <= x['ROP'] else 0, axis=1)

    # --- DASHBOARD WMS ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Valeur Stock", f"{df['Valeur_Stock'].sum():,.0f} FCFA")
    m2.metric("Risque Rupture", f"{df['Risque_FCFA'].sum():,.0f} FCFA", delta="Impact CA", delta_color="inverse")
    m3.metric("Service Level", f"{csl*100}%")
    m4.metric("EOQ Moyen", f"{int(df['EOQ'].mean())} u")

    st.subheader("📋 Inventaire & Prévisions MIT")
    st.dataframe(df[['SKU', 'Stock_Physique', 'Safety_Stock', 'EOQ', 'ROP', 'Risque_FCFA']], use_container_width=True)

    # Analyse ABC Financière
    df = df.sort_values('Valeur_Stock', ascending=False)
    fig_abc = px.pie(df, values='Valeur_Stock', names='SKU', title="Répartition Financière du Stock", hole=0.4)
    st.plotly_chart(fig_abc, use_container_width=True)
    

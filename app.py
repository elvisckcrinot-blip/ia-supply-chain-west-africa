import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import norm
from datetime import datetime

# 1. CONFIGURATION (Impérativement en première ligne)
st.set_page_config(page_title="Logistique Usine X", layout="wide", page_icon="🏢")

# Initialisation des états
if 'page' not in st.session_state:
    st.session_state.page = 'accueil'
if 'db_tms' not in st.session_state:
    st.session_state.db_tms = pd.DataFrame([{'ID': 'EXP-UX-101', 'Camion': 'RB 1234', 'Position': 'Bohicon', 'Statut': 'En Transit'}])

# --- NAVIGATION ---
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 2. PAGE D'ACCUEIL ---
if st.session_state.page == 'accueil':
    st.markdown("<h1 style='text-align: center;'>🏢 Hub Logistique Intégré - Usine X</h1>", unsafe_allow_html=True)
    st.write("##")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.info("### 🚛 Module TMS")
        st.write("Pilotage transport & Métriques Tonne-Kilomètre (MIT SC1x).")
        if st.button("ACCÉDER AU TMS"): go_to('tms')
    with col2:
        st.success("### 📦 Module WMS")
        st.write("Gestion stochastique & Analyse de risque financier.")
        if st.button("ACCÉDER AU WMS"): go_to('wms')

# --- 3. MODULE TMS (Bénin + MIT) ---
elif st.session_state.page == 'tms':
    if st.sidebar.button("⬅ Retour au Hub"): go_to('accueil')
    st.title("🚛 TMS Logistics : Pilotage & Ingénierie")

    # Calculs MIT
    with st.sidebar:
        st.header("Paramètres MIT SC1x")
        charge = st.number_input("Charge (Tonnes)", value=25.0)
        conso = st.number_input("Conso (L/100km)", value=32.0)
    
    charge_reelle = charge * 0.85
    cout_tkm = ((conso/100)*700) / charge_reelle
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Coût Tonne-Kilomètre", f"{cout_tkm:.2f} F/T.km")
    c2.metric("Économie Carburant", "15% Optimisé")
    c3.metric("Charge Réelle", f"{charge_reelle} T")

    # Suivi Bénin
    st.header("📍 Suivi Territorial")
    villes = {"Usine X": 0, "Cotonou": 25, "Bohicon": 105, "Parakou": 395, "Malanville": 720}
    pos_actuelle = st.selectbox("Position du Camion", list(villes.keys()))
    km = villes[pos_actuelle]
    st.progress(min(km / 720, 1.0))
    st.write(f"Trajet : {km} km parcourus depuis l'Usine X.")
    st.dataframe(st.session_state.db_tms, use_container_width=True)

# --- 4. MODULE WMS (Risque + MIT) ---
elif st.session_state.page == 'wms':
    if st.sidebar.button("⬅ Retour au Hub"): go_to('accueil')
    st.title("📦 WMS : Intelligence Stocks")

    with st.sidebar:
        st.header("Ingénierie MIT")
        csl = st.slider("Service Level (Z)", 0.80, 0.99, 0.95)
        lead_time = st.number_input("Lead Time (Jrs)", value=14)

    # Logique de calcul
    data = {
        'SKU': ['REF-01', 'REF-02', 'REF-03'],
        'Prix': [15000, 45000, 8000],
        'Vente_J': [10, 5, 25],
        'Sigma': [3, 1, 6],
        'Stock': [150, 40, 400]
    }
    df = pd.DataFrame(data)
    
    # Formules MIT CTL
    z = norm.ppf(csl)
    df['Safety_Stock'] = (z * df['Sigma'] * np.sqrt(lead_time)).astype(int)
    df['ROP'] = (df['Vente_J'] * lead_time) + df['Safety_Stock']
    df['Risque_FCFA'] = df.apply(lambda x: (x['Vente_J'] * x['Prix'] * 7) if x['Stock'] <= x['ROP'] else 0, axis=1)

    m1, m2 = st.columns(2)
    m1.metric("Risque Financier", f"{df['Risque_FCFA'].sum():,.0f} FCFA", delta_color="inverse")
    m2.metric("Z-Score", f"{z:.2f}")

    st.subheader("📋 Inventaire & Alertes")
    st.dataframe(df[['SKU', 'Stock', 'Safety_Stock', 'ROP', 'Risque_FCFA']], use_container_width=True)
    
    fig = px.pie(df, values='Stock', names='SKU', title="Répartition du Stock")
    st.plotly_chart(fig, use_container_width=True)
    

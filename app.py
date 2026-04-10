import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(page_title="Showcase Logistique - Usine X", layout="wide", page_icon="🏢")

# Style CSS pour une présentation élégante
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3em; transition: 0.3s; }
    .stButton>button:hover { border-color: #1E3A8A; color: #1E3A8A; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Navigation simplifiée (Sans mot de passe pour la démo public)
if 'page' not in st.session_state:
    st.session_state.page = 'accueil'

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ==========================================
# 2. PAGE D'ACCUEIL (HUB PUBLIC)
# ==========================================
if st.session_state.page == 'accueil':
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏢 Hub Logistique Intégré</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em;'>Démo opérationnelle : Pilotage Transport & Gestion d'Entrepôt</p>", unsafe_allow_html=True)
    st.write("##")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.info("### 🚛 Module TMS (Transport)")
        st.write("""
        - Optimisation énergétique & calcul ROI.
        - Suivi territorial (Bénin) depuis l'**Usine X**.
        - Gestion des flux et accès au Dock.
        """)
        if st.button("DÉCOUVRIR LE TMS"):
            go_to('tms')
            
    with col2:
        st.success("### 📦 Module WMS (Stock)")
        st.write("""
        - Analyse ABC (Pareto) financière.
        - Prévision de rupture & calcul du risque.
        - Plan d'achat suggéré par intelligence de flux.
        """)
        if st.button("DÉCOUVRIR LE WMS"):
            go_to('wms')

    st.markdown("---")
    st.caption("Projet Showcase - Usine X | Pilotage des flux en temps réel")

# ==========================================
# 3. MODULE TMS (VERSION DÉMO)
# ==========================================
elif st.session_state.page == 'tms':
    if st.sidebar.button("⬅️ Retour au Hub"):
        go_to('accueil')
    
    st.title("🚛 TMS Logistics : Pilotage Transport")
    
    # Données Démo
    villes_benin = {
        "Usine X (Départ)": 0, "Cotonou": 25, "Porto-Novo": 65, "Bohicon": 105, 
        "Parakou": 395, "Djougou": 450, "Malanville": 720
    }
    
    # KPI Énergie
    st.header("⛽ Optimisation de la Flotte")
    m1, m2, m3 = st.columns(3)
    dist_sav = 15.0 # km sauvés par jour par camion
    m1.metric("Distance Économisée", f"{dist_sav * 10 * 300:,.0f} km/an")
    m2.metric("Impact Carbone", "-4.5 Tonnes CO2")
    m3.metric("Gain ROI", "3,150,000 FCFA/an")

    # Suivi
    st.header("📍 Tracking des Expéditions")
    pos_actuelle = st.select_slider("Simuler la progression d'un camion", options=list(villes_benin.keys()))
    km = villes_benin[pos_actuelle]
    st.progress(min(km / 720, 1.0))
    st.write(f"Localisation : **{pos_actuelle}** ({km} km depuis Usine X)")

# ==========================================
# 4. MODULE WMS (VERSION DÉMO)
# ==========================================
elif st.session_state.page == 'wms':
    if st.sidebar.button("⬅️ Retour au Hub"):
        go_to('accueil')

    st.title("📦 WMS : Intelligence & Performance Stocks")
    
    # Simulation de données pour la démo
    data_demo = pd.DataFrame({
        'SKU': ['SKU-001', 'SKU-042', 'SKU-089', 'SKU-102'],
        'Désignation': ['Moteur Industriel', 'Pneus XL', 'Huile Synthétique', 'Batteries'],
        'Stock': [45, 12, 150, 0],
        'Statut': ['🟢 Optimal', '🟡 Préventif', '🔴 Critique', '🚫 Rupture'],
        'Risque_FCFA': [0, 150000, 850000, 2400000]
    })

    k1, k2, k3 = st.columns(3)
    k1.metric("Valeur Inventaire", "45,200,000 FCFA")
    k2.metric("Risque Financier", "3,400,000 FCFA", delta="Urgence")
    k3.metric("Taux de Service", "92%")

    st.subheader("📊 Analyse ABC & Alertes")
    st.dataframe(data_demo, use_container_width=True)
    
    fig = px.bar(data_demo, x='SKU', y='Risque_FCFA', color='Statut', title="Impact Financier des Ruptures")
    st.plotly_chart(fig, use_container_width=True)
    

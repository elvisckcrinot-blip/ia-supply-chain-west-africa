import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import norm
from datetime import datetime

# 1. CONFIGURATION (Doit être la toute première commande)
st.set_page_config(page_title="West Africa Logistics Hub", layout="wide")

# Initialisation sécurisée des données
if 'page' not in st.session_state:
    st.session_state.page = 'accueil'
if 'db_dock' not in st.session_state:
    st.session_state.db_dock = pd.DataFrame(columns=['Heure', 'Camion', 'Produit', 'Tonnage', 'Opération', 'Quai'])

# Fonctions de navigation
def go_to(p):
    st.session_state.page = p

# --- PAGE D'ACCUEIL ---
if st.session_state.page == 'accueil':
    st.title("🌍 West Africa Logistics Hub")
    st.write("Expertise MIT CTL – Pilotage Stratégique au Bénin")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚛 OUVRIR LE TMS", use_container_width=True):
            go_to('tms')
            st.rerun()
    with col2:
        if st.button("📦 OUVRIR LE WMS", use_container_width=True):
            go_to('wms')
            st.rerun()

# --- MODULE TMS ---
elif st.session_state.page == 'tms':
    if st.sidebar.button("⬅ Retour"):
        go_to('accueil')
        st.rerun()
    
    st.title("🚛 TMS : Pilotage & Tonnage")
    
    # Docking
    st.subheader("🏢 Gestion du Docking")
    with st.form("dock"):
        c1, c2, c3 = st.columns(3)
        imm = c1.text_input("Camion")
        prod = c2.selectbox("Marchandise", ["Maïs", "Noix", "Ananas", "Soja", "Coton", "Acajou", "Tourteau", "Ciment", "Gaz"])
        poids = c3.number_input("Tonnes", value=25.0)
        if st.form_submit_button("Valider"):
            new_log = pd.DataFrame([{'Heure': datetime.now().strftime("%H:%M"), 'Camion': imm, 'Produit': prod, 'Tonnage': poids}])
            st.session_state.db_dock = pd.concat([st.session_state.db_dock, new_log], ignore_index=True)
            st.success("Enregistré")

    st.dataframe(st.session_state.db_dock, use_container_width=True)

# --- MODULE WMS ---
elif st.session_state.page == 'wms':
    if st.sidebar.button("⬅ Retour"):
        go_to('accueil')
        st.rerun()
        
    st.title("📦 WMS : Intelligence Stocks")
    
    # Calcul MIT (Z-score)
    z = norm.ppf(0.95)
    st.metric("Z-Score de Sécurité (MIT)", f"{z:.2f}")
    
    # Données Démo
    df = pd.DataFrame({
        'SKU': ['SOJA-01', 'COTON-05'],
        'Stock': [150, 45],
        'Prix': [450000, 800000]
    })
    st.dataframe(df, use_container_width=True)
    
    fig = px.pie(df, values='Stock', names='SKU', title="Répartition")
    st.plotly_chart(fig)
    

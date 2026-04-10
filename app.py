import streamlit as st

st.set_page_config(page_title="West Africa Logistics Hub", layout="wide", page_icon="🌍")

# Style CSS pour le Hub
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 5em; font-size: 18px; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🌍 West Africa Logistics Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em;'>Pilotage Stratégique & Opérationnel au Bénin (Usine X)</p>", unsafe_allow_html=True)
st.write("---")

st.info("### Bienvenue sur la plateforme de gestion intégrée")
st.write("Utilisez le menu à gauche pour naviguer entre les modules ou cliquez sur les accès rapides ci-dessous.")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 🚛 TMS Logistics")
    st.write("Suivi des camions, Docking Usine X et Optimisation Carburant.")
    # Note : Le bouton ici est informatif car la navigation se fait par la sidebar
    st.caption("👈 Sélectionnez 'TMS Logistics' dans le menu de gauche.")

with col2:
    st.markdown("### 📦 WMS Logistics")
    st.write("Gestion des stocks, alertes ruptures et bons de commande.")
    st.caption("👈 Sélectionnez 'WMS Logistics' dans le menu de gauche.")

st.write("##")
st.caption("Développé par Elvis – Expertise Supply Chain West Africa")

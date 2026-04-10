import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="West Africa Logistics Hub", layout="wide", page_icon="🌍")

st.title("🌍 West Africa Logistics Hub")
st.markdown("---")

st.header("Bienvenue dans votre interface de pilotage")
st.write("Cette plateforme centralise vos solutions technologiques pour la Supply Chain au Bénin.")

# 2. PANNEAU DE NAVIGATION
col1, col2 = st.columns(2)

with col1:
    st.info("### 🚛 TMS Logistics")
    st.write("Transport Management System : Docking, Optimisation du carburant et Suivi en temps réel.")
    st.write("👈 *Cliquez sur 'TMS Logistics' dans le menu à gauche*")

with col2:
    st.success("### 📦 WMS Logistics")
    st.write("Warehouse Management System : Gestion d'entrepôt, Simulation de scénarios et Commandes auto.")
    st.write("👈 *Cliquez sur 'WMS Logistics' dans le menu à gauche*")

# 3. BARRE LATÉRALE
st.sidebar.success("Sélectionnez un module pour commencer")
st.sidebar.markdown("---")
st.sidebar.write("Expertise : Modèles MIT CTL")

import streamlit as st

# Configuration
st.set_page_config(page_title="Logistics Hub", layout="wide")

# Titre principal
st.title("🌍 West Africa Logistics Hub")
st.markdown("---")

st.header("Interface de Pilotage Stratégique")
st.write("Plateforme de gestion pour la GDIZ et INGCO BÉNIN.")

# Blocs de navigation
c1, c2 = st.columns(2)
with c1:
    st.info("### 🚛 TMS Logistics\nDocking, Optimisation & Suivi.")
with c2:
    st.success("### 📦 WMS Logistics\nStocks, Simulation & Commandes.")

st.sidebar.warning("Cliquez sur [ >> ] en haut à gauche pour naviguer.")

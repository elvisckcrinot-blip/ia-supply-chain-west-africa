import streamlit as st
import pandas as pd
from models.mit_calculations import calcul_wilson_eoq, calcul_point_de_commande

st.set_page_config(page_title="WMS Intelligence", layout="wide")

st.title("📦 Warehouse Management System")
st.subheader("Optimisation des stocks via modèles MIT CTL")

# --- Formulaire de simulation ---
with st.expander("🛠️ Paramètres d'optimisation (Calculateur Wilson)"):
    col1, col2, col3 = st.columns(3)
    demande = col1.number_input("Demande annuelle (unités)", value=1200)
    cout_c = col2.number_input("Coût par commande ($)", value=50)
    cout_s = col3.number_input("Coût de stockage par unité/an ($)", value=2)

    if st.button("Calculer l'EOQ"):
        resultat = calcul_wilson_eoq(demande, cout_c, cout_s)
        st.success(f"La quantité économique de commande (EOQ) est de : **{resultat} unités**")

st.info("Ce module utilise les données de `data/processed/` pour générer des alertes de rupture.")

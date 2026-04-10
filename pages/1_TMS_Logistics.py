import streamlit as st
import pandas as pd

st.set_page_config(page_title="TMS Expert - MIT CTL Metrics", layout="wide")

st.title("🚛 TMS : Ingénierie du Transport (Modèles SC1x)")
st.info("Focus : Efficacité Tonne-Kilomètre & Intensité Énergétique")

# --- INPUTS OPÉRATIONNELS ---
with st.sidebar:
    st.header("Paramètres de Flotte")
    charge_utile = st.number_input("Charge utile par camion (Tonnes)", value=25.0)
    taux_remplissage = st.slider("Taux de remplissage moyen (%)", 10, 100, 85) / 100
    conso_moyenne = st.number_input("Consommation (L/100km)", value=32.0)
    prix_diesel = 700 # FCFA

# --- CALCULS EXPERTS MIT (SC1x) ---
# 1. Analyse Tonne-Kilomètre (Le standard de mesure MIT)
charge_reelle = charge_utile * taux_remplissage
# Estimation du coût variable au km
cout_km = (conso_moyenne / 100) * prix_diesel
# Coût par Tonne-Kilomètre (Unit Revenue/Cost analysis)
cout_tkm = cout_km / charge_reelle

# 2. Intensité Émissions (SC0x - Supply Chain Sustainability)
# Facteur d'émission standard : 2.68 kg CO2 par litre de diesel
emissions_km = (conso_moyenne / 100) * 2.68
emissions_tkm = emissions_km / charge_reelle

# --- DASHBOARD ---
c1, c2, c3 = st.columns(3)
c1.metric("Coût Tonne-Kilomètre", f"{cout_tkm:.2f} FCFA", help="Indicateur clé de performance financière MIT")
c2.metric("Intensité CO2", f"{emissions_tkm:.4f} kg/T.km", help="Mesure de durabilité SC0x")
c3.metric("Charge Réelle", f"{charge_reelle:.1f} Tonnes")

st.markdown("---")
st.subheader("📍 Suivi Territorial & Logique de Proximité")
villes = {"Usine X": 0, "Cotonou": 25, "Bohicon": 105, "Parakou": 395, "Malanville": 720}
selection = st.select_slider("Position du Camion", options=list(villes.keys()))

# Calcul du "Ton-Mile" réalisé (Work done)
travail_realise = charge_reelle * villes[selection]
st.write(f"📊 **Travail Logistique Réalisé :** {travail_realise:,.0f} Tonnes-km")

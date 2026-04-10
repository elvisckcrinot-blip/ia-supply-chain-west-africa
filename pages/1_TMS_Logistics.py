import streamlit as st
from models.mit_calculations import calcul_cout_transport

st.set_page_config(page_title="TMS Logistics · GDIZ-Malanville", layout="wide")

# Style rapide pour le titre
st.markdown('<h1 style="font-family:Syne; color:#ffad1f;">🚛 TMS Logistics</h1>', unsafe_allow_html=True)
st.subheader("Pilotage du corridor GDIZ → Malanville")

# --- Interface de Pilotage ---
col1, col2 = st.columns([1, 2])

with col1:
    st.write("### ⚙️ Paramètres du trajet")
    distance = st.slider("Distance (km)", 0, 800, 720) # Par défaut axe Malanville
    conso = st.number_input("Consommation (L/100km)", value=35)
    prix_essence = st.number_input("Prix du Diesel ($/L)", value=1.2)
    frais_fixes = st.number_input("Frais de docking & péages ($)", value=150)

    cout_total, co2 = calcul_cout_transport(distance, conso, prix_essence, frais_fixes)

with col2:
    st.write("### 📊 Résultats de l'optimisation")
    kpi1, kpi2 = st.columns(2)
    kpi1.metric("Coût estimé du trajet", f"{cout_total} $")
    kpi2.metric("Empreinte Carbone", f"{co2} kg CO2", delta="-5% vs diesel standard")
    
    # Simulation de suivi
    st.info(f"📍 **Statut actuel :** Convoi en route vers Malanville (ETA: +14h)")
    st.progress(65) # Progression du trajet sur les 720km

st.divider()
st.caption("Données calculées selon le référentiel MIT SC0x - Supply Chain Analytics.")

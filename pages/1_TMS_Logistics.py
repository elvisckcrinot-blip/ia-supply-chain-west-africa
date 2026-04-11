import streamlit as st
from models.mit_calculations import calcul_cout_transport

st.set_page_config(page_title="TMS Logistics · GDIZ-Malanville", layout="wide")

st.markdown('<h1 style="font-family:Syne; color:#ffad1f;">🚛 TMS Logistics</h1>', unsafe_allow_html=True)
st.subheader("Pilotage du corridor GDIZ → Malanville")

# --- Interface de Pilotage ---
# Correction ici : on ajoute le chiffre 2 dans les parenthèses
col1, col2 = st.columns(2)

with col1:
    st.write("### ⚙️ Paramètres du trajet")
    distance = st.slider("Distance (km)", 0, 800, 720)
    conso = st.number_input("Consommation (L/100km)", value=35)
    
    # Paramètres en FCFA
    prix_diesel = st.number_input("Prix du Diesel (FCFA/L)", value=700)
    frais_fixes = st.number_input("Frais de docking & péages (FCFA)", value=85000)

    cout_total, co2 = calcul_cout_transport(distance, conso, prix_diesel, frais_fixes)

with col2:
    st.write("### 📊 Résultats de l'optimisation")
    kpi1, kpi2 = st.columns(2)
    
    # Formatage FCFA propre
    valeur_formatee = f"{cout_total:,}".replace(",", " ")
    kpi1.metric("Coût estimé du trajet", f"{valeur_formatee} FCFA")
    kpi2.metric("Empreinte Carbone", f"{co2} kg CO2", delta="-5% vs diesel standard")
    
    st.info(f"📍 **Statut actuel :** Convoi en route vers Malanville (ETA: +14h)")
    st.progress(65)

st.divider()
st.caption("Calculs basés sur le référentiel MIT SC0x · Devises en Francs CFA (XOF).")

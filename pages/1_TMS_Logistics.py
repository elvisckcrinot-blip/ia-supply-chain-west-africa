import streamlit as st
import pandas as pd

# 1. CONFIGURATION
st.set_page_config(page_title="TMS Logistics", layout="wide", page_icon="🚛")

st.title("🚛 Transport Management System (TMS)")
st.markdown("---")

# --- MODULE 1 : DOCKING ---
st.header("🏢 1. TMS - Gestion du Docking")
c1, c2 = st.columns([1, 1.5])
with c1:
    with st.form("dock_f"):
        cam = st.text_input("Immatriculation", "RB 0000")
        op = st.radio("Opération", ["Chargement", "Déchargement"])
        if st.form_submit_button("Valider"):
            st.success(f"Accès validé pour {cam}")
with c2:
    st.table(pd.DataFrame({'Quai': ['A1', 'A2'], 'Statut': ['🔴 Occupé', '🟢 Libre']}))

st.markdown("---")

# --- MODULE 2 : OPTIMISATION (CORRECTION ICI) ---
st.header("⛽ 2. TMS - Optimisation Carburant")
with st.expander("📊 Calculateur d'économies", expanded=True):
    col_a, col_b = st.columns(2)
    n = col_a.number_input("Nombre de véhicules", value=10)
    km_gain = col_b.number_input("Km sauvés / jour / véhicule", value=15)
    
    # Calcul simple
    economie = km_gain * n * 300 * (12/100) * 700
    st.metric("Gain Annuel Estimé", f"{economie:,.0f} FCFA")
    
    # Note Stratégique Propre (Sans bug d'affichage)
    st.info(f"**Note Stratégique :** Cette économie de {economie:,.0f} FCFA/an finance l'embauche d'un nouveau collaborateur.")

st.markdown("---")

# --- MODULE 3 : TRACKING ---
st.header("📦 3. TMS - Tracking")
if 'tms_db' not in st.session_state:
    st.session_state.tms_db = pd.DataFrame([{'ID': 'EXP-101', 'Statut': 'En Transit'}])

with st.form("track_f"):
    id_e = st.text_input("ID Expédition")
    stat = st.selectbox("Statut", ["En Transit", "Livré"])
    if st.form_submit_button("Mettre à jour"):
        new = pd.DataFrame([{'ID': id_e, 'Statut': stat}])
        st.session_state.tms_db = pd.concat([st.session_state.tms_db, new], ignore_index=True)

st.dataframe(st.session_state.tms_db, use_container_width=True)
    

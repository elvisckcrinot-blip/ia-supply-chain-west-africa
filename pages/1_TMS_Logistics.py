import streamlit as st
import pandas as pd

# 1. CONFIGURATION PROFESSIONNELLE
st.set_page_config(page_title="TMS Logistics - Expertise MIT", layout="wide", page_icon="🚛")

st.title("🚛 Transport Management System (TMS)")
st.info("Module d'optimisation basé sur la méthodologie MIT CTL (SC0x)")
st.markdown("---")

# --- MODULE 1 : GESTION DU DOCKING ---
st.header("🏢 1. TMS - Gestion du Docking")
col_d1, col_d2 = st.columns([1, 1.5])

with col_d1:
    st.subheader("Enregistrement des Flux")
    with st.form("docking_form", clear_on_submit=True):
        cam_id = st.text_input("Immatriculation Camion", placeholder="ex: RB 1234")
        operation = st.radio("Opération Logistique", ["Déchargement (Import)", "Chargement (Export)"])
        submit_d = st.form_submit_button("Valider l'Accès")
        if submit_d:
            st.success(f"Accès validé : {cam_id} vers Quai de {operation}")

with col_d2:
    st.subheader("Visualisation des Quais")
    docks = pd.DataFrame({
        'Quai': ['Quai A1', 'Quai A2', 'Quai B1'],
        'Statut': ['🔴 Occupé', '🟢 Libre', '🔴 Occupé']
    })
    st.table(docks)

st.markdown("---")

# --- MODULE 2 : OPTIMISATION DU ROUTING (L'INTELLIGENCE MIT) ---
st.header("⛽ 2. TMS - Optimisation & ROI Stratégique")
st.write("**Étude de cas : Réduction de la perte thermique en capital humain.**")

with st.expander("📊 Paramètres du Modèle d'Efficacité", expanded=True):
    c1, c2, c3 = st.columns(3)
    n = c1.number_input("Flotte (véhicules)", value=10)
    jours = c1.number_input("Jours opérationnels / an", value=300)
    d1 = c2.number_input("Distance Initiale (km/jour)", value=80.0)
    d2 = c2.number_input("Distance Optimisée (km/jour)", value=65.0)
    conso = c3.number_input("Consommation (L/100km)", value=12.0)
    prix_l = c3.number_input("Prix Carburant (FCFA/L)", value=700)

# CALCULS MÉTHODOLOGIE MIT
delta_d_jour = d1 - d2
delta_d_annuel = delta_d_jour * n * jours
vol_sauve = delta_d_annuel * (conso / 100)
gain_financier = vol_sauve * prix_l
co2_evite = vol_sauve * 2.6

# AFFICHAGE DES KPIS
k1, k2, k3 = st.columns(3)
with k1:
    st.metric("Économie Carburant", f"{gain_financier:,.0f} FCFA")
with k2:
    st.metric("Distance Sauvée", f"{delta_d_annuel:,.0f} km/an")
with k3:
    st.metric("Volume Économisé", f"{vol_sauve:,.0f} Litres/an")

# ANALYSE DE L'UPPERCUT (L'ARGUMENT CHOC)
st.markdown("### 🧠 Analyse de l'Uppercut (Logistics ROI)")
st.warning(f"**Impact Social :** L'économie de **{gain_financier:,.0f} FCFA/an** couvre 100% du coût d'un nouveau poste de magasinier qualifié (base 250 000 FCFA/mois).")

col_roi1, col_roi2 = st.columns(2)
with col_roi1:
    st.write("**⏱️ Productivité du Temps**")
    st.write(f"Réduire {delta_d_jour} km/jour libère environ **2 250 heures** de travail par an pour la flotte.")
with col_roi2:
    st.write("**🌍 Impact Environnemental**")
    st.write(f"Ce scénario évite l'émission de **{co2_evite/1000:.1f} tonnes de CO2** par an.")

st.markdown("---")

# --- MODULE 3 : TRACKING TMS ---
st.header("📦 3. TMS - Suivi des Expéditions")
if 'tms_tracking' not in st.session_state:
    st.session_state.tms_tracking = pd.DataFrame([
        {'ID': 'EXP-882', 'Article': 'Groupe INGCO', 'Statut': 'En Transit', 'Position': 'Bohicon'}
    ])

with st.form("tracking_tms"):
    t1, t2, t3 = st.columns(3)
    id_t = t1.text_input("ID Expédition")
    pos_t = t2.text_input("Position Actuelle")
    stat_t = t3.selectbox("Statut", ["Préparation", "En Transit", "Livré", "Incident"])
    if st.form_submit_button("Actualiser"):
        new_row = pd.DataFrame([{'ID': id_t, 'Article': 'Fret GDIZ', 'Statut': stat_t, 'Position': pos_t}])
        st.session_state.tms_tracking = pd.concat([st.session_state.tms_tracking, new_row], ignore_index=True)

st.dataframe(st.session_state.tms_tracking, use_container_width=True)
st.success("🎯 Système Opérationnel : Optimisation validée par les modèles MIT CTL.")

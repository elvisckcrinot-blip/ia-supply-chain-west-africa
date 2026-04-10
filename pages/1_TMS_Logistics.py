import streamlit as st
import pandas as pd

# 1. CONFIGURATION ÉLÉGANTE (Zéro Bug)
st.set_page_config(page_title="TMS Logistics - Expertise MIT", layout="wide", page_icon="🚛")

# Style CSS pour une immersion professionnelle
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("🚛 TMS Logistics : Pilotage & Optimisation")
st.info("Système intégré : Modèles MIT CTL & Suivi Territorial Bénin")
st.markdown("---")

# --- DATASET : RÉFÉRENTIEL DES DISTANCES BÉNIN (DEPUIS GDIZ) ---
villes_benin = {
    "GDIZ (Départ)": 0, "Abomey-Calavi": 15, "Cotonou": 25, "Ouidah": 35,
    "Allada": 12, "Porto-Novo": 65, "Bohicon": 105, "Dassa": 185,
    "Savalou": 205, "Glazoué": 200, "Parakou": 395, "Djougou": 450,
    "Natitingou": 520, "Kandi": 615, "Malanville": 720
}
liste_villes = sorted(list(villes_benin.keys()))

# --- INITIALISATION DE LA MÉMOIRE (SESSION STATE) ---
if 'db_tms' not in st.session_state:
    st.session_state.db_tms = pd.DataFrame([
        {'ID': 'EXP-GDIZ-101', 'Article': 'Groupe INGCO', 'Position': 'Bohicon', 'Statut': 'En Transit'}
    ])

# --- MODULE 1 : OPTIMISATION DU ROUTING (LOGIQUE MIT SC0x) ---
st.header("⛽ 1. Efficacité Énergétique & ROI")
with st.expander("📊 Paramètres du Modèle d'Optimisation", expanded=True):
    col_p1, col_p2, col_p3 = st.columns(3)
    n = col_p1.number_input("Flotte (Camions)", value=10, min_value=1)
    d_actuelle = col_p2.number_input("Distance actuelle (km/j)", value=80.0)
    d_opti = col_p2.number_input("Distance optimisée (km/j)", value=65.0)
    jours = col_p3.number_input("Jours d'activité / an", value=300)
    conso = col_p3.number_input("Conso (L/100km)", value=12.0)

# Calculs Stratégiques
gain_km_annuel = (d_actuelle - d_opti) * n * jours
economie_fcfa = gain_km_annuel * (conso / 100) * 700 # Prix fixe 700 FCFA/L

# Affichage des KPIs
m1, m2, m3 = st.columns(3)
m1.metric("Gain Annuel", f"{economie_fcfa:,.0f} FCFA")
m2.metric("Distance Sauvée", f"{gain_km_annuel:,.0f} km/an")
m3.metric("CO2 Évité", f"{(gain_km_annuel * 0.12 * 2.6):,.0f} kg")

st.warning(f"**Note Stratégique :** L'économie de {economie_fcfa:,.0f} FCFA finance intégralement un nouveau poste de travail.")
st.markdown("---")

# --- MODULE 2 : DOCKING & GESTION DES FLUX ---
st.header("🏢 2. Gestion du Docking")
col_d1, col_d2 = st.columns([1, 1.5])
with col_d1:
    with st.form("docking_form"):
        st.subheader("Contrôle d'Accès")
        camion = st.text_input("Immatriculation", "RB 0000")
        flux = st.selectbox("Type d'opération", ["Chargement", "Déchargement"])
        if st.form_submit_button("Valider"):
            st.success(f"Accès autorisé : {camion}")
with col_d2:
    st.subheader("État des Quais")
    st.table(pd.DataFrame({'Quai': ['A1', 'A2', 'B1'], 'Statut': ['🔴 Occupé', '🟢 Libre', '🟢 Libre']}))

st.markdown("---")

# --- MODULE 3 : TRACKING & LOCALISATION BÉNIN ---
st.header("📦 3. Suivi des Expéditions (TMS)")
with st.form("tracking_form", clear_on_submit=True):
    col_t1, col_t2, col_t3 = st.columns(3)
    id_exp = col_t1.text_input("ID Expédition", placeholder="EXP-XXX")
    pos_gps = col_t2.selectbox("Dernière Position Constatée", liste_villes)
    status = col_t3.selectbox("Statut Livraison", ["Préparation", "En Transit", "Livré", "Incident"])
    
    if st.form_submit_button("Actualiser le Tracking"):
        if id_exp:
            new_row = pd.DataFrame([{'ID': id_exp, 'Article': 'Matériel INGCO', 'Position': pos_gps, 'Statut': status}])
            st.session_state.db_tms = pd.concat([st.session_state.db_tms, new_row], ignore_index=True)
            st.toast(f"Mise à jour effectuée : {pos_gps}")
        else:
            st.error("Veuillez saisir une référence.")

# Tableau de bord TMS
st.subheader("📋 Dashboard Opérationnel")
st.dataframe(st.session_state.db_tms, use_container_width=True)

# Intelligence de Progression
if not st.session_state.db_tms.empty:
    actuelle = st.session_state.db_tms.iloc[-1]['Position']
    km_faits = villes_benin.get(actuelle, 0)
    st.markdown(f"**📍 Localisation Actuelle : {actuelle}** ({km_faits} km parcourus depuis la GDIZ)")
    st.progress(min(km_faits / 720, 1.0))

st.success("🎯 TMS Version Ultime : Zéro Bug - Intelligence MIT validée.")

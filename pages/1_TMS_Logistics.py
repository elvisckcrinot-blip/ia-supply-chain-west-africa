import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Transport Management System (TMS)", layout="wide", page_icon="🚛")

# Style CSS pour une interface professionnelle
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚛 Transport Management System (TMS)")
st.info("Plateforme de pilotage End-to-End : Flux d'usine, Optimisation et Suivi des expéditions.")
st.markdown("---")

# --- MODULE 1 : GESTION DU DOCKING (Entrée & Flux Usine) ---
st.header("🏢 1. TMS - Gestion du Docking")
col_d1, col_d2 = st.columns([1, 1.5])

with col_d1:
    st.subheader("Enregistrement des Flux")
    with st.form("tms_dock_form", clear_on_submit=True):
        cam_id = st.text_input("Immatriculation Camion", placeholder="ex: RB 1234")
        operation = st.radio("Opération Logistique", ["Déchargement (Import)", "Chargement (Export)"])
        quai_pref = st.selectbox("Assignation Quai de chargement", ["Quai A1", "Quai A2", "Quai B1"])
        submit_d = st.form_submit_button("Valider l'Accès au Dock")
        if submit_d:
            st.success(f"TMS : Accès validé pour {cam_id} vers {quai_pref}")

with col_d2:
    st.subheader("État des Quais (Visualisation TMS)")
    docks_data = pd.DataFrame({
        'Quai': ['Quai A1', 'Quai A2', 'Quai B1', 'Quai B2'],
        'Statut': ['🔴 Occupé', '🟢 Libre', '🔴 Occupé', '🟢 Libre'],
        'Temps d\'occupation restant': ['25 min', '-', '10 min', '-']
    })
    st.table(docks_data)

st.markdown("---")

# --- MODULE 2 : OPTIMISATION DU ROUTING (Moteur de Calcul MIT) ---
st.header("⛽ 2. TMS - Optimisation des Coûts de Transport")
st.write("Analyse prédictive de l'efficacité énergétique basée sur la réduction des distances (Modèles MIT CTL).")

with st.expander("📊 Calculateur de Rentabilité Transport", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        n_vehicules = st.number_input("Nombre de véhicules de la flotte", value=10, min_value=1)
        jours_an = st.number_input("Jours opérationnels annuels", value=300)
    with c2:
        km_avant = st.number_input("Distance actuelle (km/jour/véhicule)", value=80.0)
        km_apres = st.number_input("Distance optimisée via TMS (km/jour)", value=65.0)
    with c3:
        conso = st.number_input("Consommation moyenne (L/100km)", value=12.0)
        prix_l = st.number_input("Prix du Carburant (FCFA/L)", value=700)

# Calculs Mathématiques TMS (Logique MIT)
gain_km_jour = km_avant - km_apres
economie_annuelle = (gain_km_jour * n_vehicules * jours_an) * (conso / 100) * prix_l
co2_sauve = (gain_km_jour * n_vehicules * jours_an) * (conso / 100) * 2.6

# Affichage des KPIs Stratégiques
k1, k2, k3 = st.columns(3)
with k1:
    st.metric("Économie Budget Transport", f"{economie_annuelle:,.0f} FCFA", delta="Gain de rentabilité")
with k2:
    st.metric("Distance Totale Sauvée", f"{gain_km_jour * n_vehicules * jours_an:,.0f} km/an")
with k3:
    st.metric("Réduction Empreinte Carbone", f"{co2_sauve:,.0f} kg CO2", delta="Émissions évitées", delta_color="normal")

st.help(f"Note Stratégique TMS : Cette économie annuelle finance l'embauche d'un nouveau collaborateur (Base 3M FCFA/an).")
st.markdown("---")

# --- MODULE 3 : TRACKING & VISIBILITÉ (Suivi des Marchandises) ---
st.header("📦 3. TMS - Tracking & Visibilité (End-to-End)")

# Initialisation de la base de données de suivi dans la session
if 'tms_tracking_db' not in st.session_state:
    st.session_state.tms_tracking_db = pd.DataFrame([
        {'ID Expédition': 'EXP-882', 'Article': 'Groupe Électrogène INGCO', 'Destination': 'Calavi', 'Statut': 'En Transit', 'Localisation': 'Akassato'},
        {'ID Expédition': 'EXP-885', 'Article': 'Perceuse Pro', 'Destination': 'Cotonou', 'Statut': 'Livré', 'Localisation': 'Cadjehoun'}
    ])

# Formulaire de mise à jour TMS
with st.form("tms_track_form"):
    st.subheader("Mise à jour du statut d'expédition")
    t1, t2, t3, t4 = st.columns(4)
    new_id = t1.text_input("ID Expédition (Reference)")
    new_art = t2.text_input("Désignation de la marchandise")
    new_pos = t3.text_input("Dernière Position GPS")
    new_stat = t4.selectbox("Statut de livraison", ["Préparation", "En Transit", "Incident", "Livré"])
    
    if st.form_submit_button("Actualiser le TMS"):
        new_entry = pd.DataFrame([{'ID Expédition': new_id, 'Article': new_art, 'Destination': 'Bénin', 'Statut': new_stat, 'Localisation': new_pos}])
        st.session_state.tms_tracking_db = pd.concat([st.session_state.tms_tracking_db, new_entry], ignore_index=True)

# Affichage du tableau de bord de pilotage
st.subheader("📋 Dashboard Opérationnel des Livraisons")
st.dataframe(st.session_state.tms_tracking_db, use_container_width=True)

# Indicateur de performance (Service Level)
taux_livraison = len(st.session_state.tms_tracking_db[st.session_state.tms_tracking_db['Statut'] == 'Livré']) / len(st.session_state.tms_tracking_db)
st.write(f"**Taux d'exécution du réseau de transport : {int(taux_livraison*100)}%**")
st.progress(taux_livraison)

st.success("🎯 Transport Management System Opérationnel - West Africa Logistics")
    

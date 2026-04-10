import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="TMS - Usine X", layout="wide")

# Initialisation de la base de données de docking si inexistante
if 'db_dock' not in st.session_state:
    st.session_state.db_dock = pd.DataFrame(columns=['Heure', 'Camion', 'Marchandise', 'Tonnage', 'Opération', 'Quai'])

st.title("🚛 TMS : Pilotage Transport & Flux")

# --- OPTIMISATION CARBURANT ---
with st.expander("📊 Calculateur d'Économie Carburant", expanded=True):
    c1, c2, c3 = st.columns(3)
    n_cam = c1.number_input("Nombre de camions", value=10)
    d_act = c2.number_input("Km parcourus/jour actuel", value=80.0)
    d_opt = c2.number_input("Km parcourus/jour optimisé", value=65.0)
    gain_annuel = (d_act - d_opt) * n_cam * 300 * (32/100) * 700
    st.metric("Économie Budget Transport (Gain Annuel)", f"{gain_annuel:,.0f} FCFA")

# --- GESTION DU DOCKING ---
st.header("🏢 1. Gestion du Docking (Entrée/Sortie Usine X)")
liste_marchandises = ["Maïs", "Soja", "Coton", "Tourteau", "Cajou", "Ciment", "Gaz"]

col_d1, col_d2 = st.columns([1, 1.5])
with col_d1:
    with st.form("docking_form"):
        st.subheader("Contrôle d'Accès")
        imm = st.text_input("Immatriculation", "RB 1234")
        prod = st.selectbox("Nature de la marchandise", liste_marchandises)
        poids = st.number_input("Tonnage (Tonnes)", 0.1, 70.0, 25.0)
        ope = st.radio("Opération", ["Chargement", "Déchargement"], horizontal=True)
        quai = st.selectbox("Quai assigné", ["Quai A1", "Quai A2", "Quai B1", "Quai B2"])
        if st.form_submit_button("Valider l'opération"):
            new_entry = pd.DataFrame([{'Heure': datetime.now().strftime("%H:%M"), 'Camion': imm, 'Marchandise': prod, 'Tonnage': poids, 'Opération': ope, 'Quai': quai}])
            st.session_state.db_dock = pd.concat([st.session_state.db_dock, new_entry], ignore_index=True)
            st.success(f"Opération validée pour {prod}")

with col_d2:
    st.subheader("Performance & État des Quais")
    if not st.session_state.db_dock.empty:
        st.metric("Tonnage Journalier", f"{st.session_state.db_dock['Tonnage'].sum():,.1f} T")
        st.dataframe(st.session_state.db_dock.tail(5), use_container_width=True)

# --- TRACKING MIS À JOUR AVEC NOUVELLES VILLES ---
st.header("📍 3. Suivi des Expéditions (Tracking)")

# Référentiel des distances mis à jour (approximations depuis Usine X / GDIZ)
villes = {
    "Usine X (Départ)": 0,
    "Glo-Djigbé": 5,
    "Cotonou": 25,
    "Sèmè-Kpodji": 40,
    "Ouidah": 45,
    "Porto-Novo": 55,
    "Allada": 45,
    "Cana": 95,
    "Bohicon": 105,
    "Dassa": 185,
    "Glazoué": 205,
    "Savalou": 215,
    "Savè": 235,
    "Parakou": 395,
    "Djougou": 450,
    "Natitingou": 520,
    "Malanville": 720
}

# Tri alphabétique pour le menu déroulant (optionnel, mais plus propre)
liste_villes_triee = sorted(list(villes.keys()))

with st.form("tracking_form"):
    ref_track = st.text_input("Référence de l'expédition", placeholder="EXP-2024-XXXX")
    pos = st.selectbox("Position actuelle constatée", liste_villes_triee)
    if st.form_submit_button("Actualiser le suivi"):
        st.toast(f"Tracking mis à jour pour {ref_track}")

dist = villes[pos]
# Calcul de progression basé sur Malanville (point le plus loin : 720km)
st.progress(min(dist / 720, 1.0))
st.write(f"Position : **{pos}** | Distance parcourue depuis l'**Usine X** : **{dist} km**")
    

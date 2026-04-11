import streamlit as st
from models.mit_calculations import calcul_cout_transport, calcul_rentabilite_flotte
from fpdf import FPDF
import datetime
import pandas as pd
import io

# --- 1. CONFIGURATION ET STYLE ---
st.set_page_config(page_title="TMS Intelligence · Bénin", layout="wide")

st.markdown("""
<style>
    @import url('https://googleapis.com');
    .main-title { font-family: 'Syne', sans-serif; color: #ffad1f; font-size: 38px; font-weight: 800; }
    .roi-card { background: rgba(255,173,31,0.05); border: 1px solid rgba(255,173,31,0.2); border-radius: 12px; padding: 20px; text-align: center; margin-top: 20px; }
    .roi-val { font-family: 'Syne', sans-serif; font-size: 32px; font-weight: 800; color: #ffad1f; }
</style>
""", unsafe_allow_html=True)

# --- 2. INITIALISATION ---
if 'historique_docking' not in st.session_state:
    st.session_state.historique_docking = []

# --- 3. INTERFACE PRINCIPALE ---
st.markdown('<h1 class="main-title">🚛 Pilotage des Opérations TMS</h1>', unsafe_allow_html=True)
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["💰 Business Plan & ROI", "⚓ Docking GDIZ", "📍 Tracking Corridor"])

# --- ONGLET 1 : ROI (Format Image Configuration) ---
with tab1:
    st.write("### Analyse de Rentabilité Annuelle (360 jours)")
    col_input, col_result = st.columns([1, 1])

    with col_input:
        st.info("Configuration de la Flotte")
        tarif_client = st.number_input("Tarif facturé au client (FCFA/trajet)", value=650000, step=5000)
        nbre_camions = st.slider("Nombre de camions déployés par jour", 1, 50, 15)
        dist_axe = st.number_input("Distance Axe (km)", value=720)
        conso_moy = st.number_input("Consommation moyenne (L/100km)", value=35)
        prix_diesel = st.number_input("Prix Diesel (FCFA/L)", value=700)
        charges_fixes = st.number_input("Charges fixes/trajet (FCFA)", value=85000)

    with col_result:
        cout_u, co2 = calcul_cout_transport(dist_axe, conso_moy, prix_diesel, charges_fixes)
        gain_annuel = calcul_rentabilite_flotte(cout_u, tarif_client, nbre_camions)
        
        st.write("### Résultats Stratégiques")
        valeur_f = f"{gain_annuel:,}".replace(",", " ")
        st.markdown(f"""
            <div class="roi-card">
                <div style="color: #7a92b0; font-size: 14px;">PROFIT NET ANNUEL ESTIMÉ</div>
                <div class="roi-val">{valeur_f} FCFA</div>
                <div style="color: #5fc385; font-size: 12px; margin-top:5px;">✓ Basé sur 360 jours d'exploitation</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.metric("Coût de revient / Trajet", f"{cout_u:,} FCFA".replace(",", " "))
        st.metric("Empreinte CO2 / Trajet", f"{co2} kg")

# --- ONGLET 2 : DOCKING ---
with tab2:
    st.write("### Registre de Docking")
    with st.form("docking_form"):
        c1, c2, c3 = st.columns(3)
        immat = c1.text_input("Immatriculation", "RB 0001")
        marchandise = c2.selectbox("Marchandise", ["Maïs", "Coton", "Soja", "Cajou", "Tourteau", "Ciment", "Gaz"])
        quai = c3.selectbox("Affectation Quai", [f"Quai {l}" for l in "ABCDEFG"])
        op = st.radio("Opération", ["Chargement", "Déchargement"], horizontal=True)
        submit = st.form_submit_button("VALIDER L'AFFECTATION")

    if submit:
        st.session_state.historique_docking.insert(0, {
            "Heure": datetime.datetime.now().strftime("%H:%M"),
            "Immatriculation": immat, "Marchandise": marchandise, "Quai": quai, "Type": op
        })
        st.success("Affectation enregistrée.")

    if st.session_state.historique_docking:
        st.table(pd.DataFrame(st.session_state.historique_docking))

# --- ONGLET 3 : TRACKING (Version Visuelle Améliorée) ---
with tab3:
    st.write("### Suivi Temps Réel de l'Expédition")
    
    villes = ["Cotonou", "Porto-Novo", "Ouidah", "Seme-Kodji", "Abomey-Calavi", "Glo-Djigbé", 
              "Allada", "Houègbo", "Cana", "Zogbodomey", "Bohicon", "Abomey", "Dassa", 
              "Glazoue", "Savalou", "Savè", "Parakou", "Natitingou", "Djougou", "Malanville"]
    
    position_actuelle = st.selectbox("Position actuelle du convoi", villes, index=0)
    
    st.write("Statut de livraison")
    statut_exp = st.select_slider(
        "Statut_Slider",
        options=["En transit", "Incident", "Livré"],
        value="En transit",
        label_visibility="collapsed"
    )
    
    couleurs = {"En transit": "#ffad1f", "Incident": "#ff4b4b", "Livré": "#00cc66"}
    couleur_statut = couleurs.get(statut_exp, "#ffad1f")
    
    st.markdown(f"<span style='color:{couleur_statut}; font-weight:bold;'>{statut_exp}</span>", unsafe_allow_html=True)

    st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.05); 
            border-left: 5px solid {couleur_statut}; 
            border-radius: 15px; 
            padding: 30px; 
            margin-top: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        ">
            <h2 style="font-family:'Syne', sans-serif; color: #fff; margin-bottom: 15px;">
                Convoi {immat if 'immat' in locals() else 'RB 0001'}
            </h2>
            <p style="font-size: 18px; color: #e8edf5; margin: 5px 0;">
                📍 Localisation : <b style="color:#ffad1f;">{position_actuelle}</b>
            </p>
            <p style="font-size: 16px; color: #7a92b0; margin: 5px 0;">
                État : <span style="color:{couleur_statut}; font-weight:bold;">{statut_exp.upper()}</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.info("Axe stratégique : GDIZ → Malanville")

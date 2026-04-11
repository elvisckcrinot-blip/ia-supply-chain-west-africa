import streamlit as st
from models.mit_calculations import calcul_cout_transport, calcul_rentabilite_flotte

st.set_page_config(page_title="TMS Intelligence · Bénin", layout="wide")

st.markdown('<h1 style="font-family:Syne; color:#ffad1f;">🚛 Pilotage des Opérations TMS</h1>', unsafe_allow_html=True)
st.markdown("---")

# Navigation par onglets pour une interface propre
tab1, tab2, tab3 = st.tabs(["💰 Business Plan & ROI", "⚓ Docking GDIZ", "📍 Tracking Corridor"])

# --- ONGLET 1 : STRATÉGIE ET RENTABILITÉ ---
with tab1:
    st.write("### Analyse de Rentabilité Annuelle (360 jours)")
    c1, c2 = st.columns(2)
    
    with c1:
        st.info("Configuration de la Flotte")
        tarif_client = st.number_input("Tarif facturé au client (FCFA/trajet)", value=650000, step=5000)
        nbre_camions = st.slider("Nombre de camions déployés par jour", 1, 50, 15)
        dist = st.number_input("Distance Axe (km)", value=720)
        conso = st.number_input("Consommation moyenne (L/100km)", value=35)
        prix_d = st.number_input("Prix Diesel (FCFA/L)", value=700)
        fixes = st.number_input("Charges fixes/trajet (FCFA)", value=85000)

    # Calculs dynamiques
    cout_u, co2 = calcul_cout_transport(dist, conso, prix_d, fixes)
    gain_annuel = calcul_rentabilite_flotte(cout_u, tarif_client, nbre_camions)

    with c2:
        st.write("### Résultats Stratégiques")
        st.metric("Coût de revient / Trajet", f"{cout_u:,} FCFA".replace(",", " "))
        st.metric("Profit Net Annuel Estimé", f"{gain_annuel:,} FCFA".replace(",", " "), delta="ROI Optimisé")
        st.warning(f"Impact Environnemental : {co2:,} kg CO2 par trajet")

# --- ONGLET 2 : DOCKING OPÉRATIONNEL ---
with tab2:
    st.write("### Registre de Docking - Entrée/Sortie GDIZ")
    with st.form("docking_form"):
        col_d1, col_d2, col_d3 = st.columns(3)
        immat = col_d1.text_input("Immatriculation", "RB 0001")
        marchandise = col_d2.selectbox("Marchandise", ["Maïs", "Coton", "Soja", "Cajou", "Tourteau", "Ciment", "Gaz"])
        quai = col_d3.selectbox("Affectation Quai", [f"Quai {l}" for l in "ABCDEFG"])
        
        type_op = st.radio("Type d'opération", ["Chargement", "Déchargement"], horizontal=True)
        submitted = st.form_submit_button("Valider l'affectation")
        
        if submitted:
            st.success(f"ORDRE DE MISSION : Véhicule {immat} dirigé vers le **{quai}** pour {type_op} de **{marchandise}**.")

# --- ONGLET 3 : TRACKING DU CORRIDOR ---
with tab3:
    st.write("### Suivi Temps Réel de l'Expédition")
    villes = ["Cotonou", "Porto-Novo", "Ouidah", "Seme-Kodji", "Abomey-Calavi", "Glo-Djigbé", 
              "Allada", "Houègbo", "Cana", "Zogbodomey", "Bohicon", "Abomey", "Dassa", 
              "Glazoue", "Savalou", "Savè", "Parakou", "Natitingou", "Djougou", "Malanville"]
    
    ct1, ct2 = st.columns(2)
    position = ct1.selectbox("Position actuelle du convoi", villes)
    statut = ct2.select_slider("Statut de livraison", options=["En transit", "Incident", "Livré"])
    
    # Indicateur visuel de statut
    color = {"En transit": "#ffad1f", "Incident": "#ff4b4b", "Livré": "#00cc66"}[statut]
    
    st.markdown(f"""
        <div style="padding:25px; border-radius:15px; background:rgba(255,255,255,0.03); border-left: 8px solid {color};">
            <h3 style="margin:0;">Convoi {immat}</h3>
            <p style="font-size:18px;">📍 Localisation : <b>{position}</b></p>
            <p style="font-size:16px;">Statut : <span style="color:{color}; font-weight:bold;">{statut.upper()}</span></p>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info("Axe stratégique : GDIZ → Malanville")
        

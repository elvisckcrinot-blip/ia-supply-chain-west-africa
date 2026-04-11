import streamlit as st
from models.mit_calculations import calcul_cout_transport, calcul_rentabilite_flotte
from fpdf import FPDF
import datetime

st.set_page_config(page_title="TMS Intelligence · Bénin", layout="wide")

# --- FONCTION GÉNÉRATION PDF ---
def create_pdf(immat, marchandise, quai, type_op):
    pdf = FPDF()
    pdf.add_page()
    # En-tête
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "WEST AFRICA LOGISTICS HUB - GDIZ", ln=True, align="C")
    pdf.set_font("Arial", "I", 10)
    pdf.cell(190, 10, f"Généré le : {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
    pdf.ln(10)
    
    # Corps du bon
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, f"BON DE DOCKING N° : {datetime.datetime.now().strftime('%Y%m%d%H%M')}", ln=True, align="L")
    pdf.set_font("Arial", "", 12)
    pdf.cell(190, 10, f"Immatriculation : {immat}", ln=True)
    pdf.cell(190, 10, f"Marchandise : {marchandise}", ln=True)
    pdf.cell(190, 10, f"Affectation : {quai}", ln=True)
    pdf.cell(190, 10, f"Opération : {type_op}", ln=True)
    pdf.cell(190, 10, "Destination : Axe GDIZ - Malanville", ln=True)
    pdf.ln(20)
    pdf.cell(190, 10, "Signature Autorité GDIZ : _____________________", ln=True, align="R")
    
    return pdf.output(dest="S").encode("latin-1")

st.markdown('<h1 style="font-family:Syne; color:#ffad1f;">🚛 Pilotage des Opérations TMS</h1>', unsafe_allow_html=True)
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["💰 Business Plan & ROI", "⚓ Docking GDIZ", "📍 Tracking Corridor"])

# --- ONGLET 1 : STRATÉGIE ET RENTABILITÉ ---
with tab1:
    st.write("### Analyse de Rentabilité Annuelle (360 jours)")
    c1, c2 = st.columns(2)
    with c1:
        tarif_client = st.number_input("Tarif facturé au client (FCFA/trajet)", value=650000)
        nbre_camions = st.slider("Nombre de camions déployés par jour", 1, 50, 15)
        dist = st.number_input("Distance Axe (km)", value=720)
        conso = st.number_input("Consommation moyenne (L/100km)", value=35)
        prix_d = st.number_input("Prix Diesel (FCFA/L)", value=700)
        fixes = st.number_input("Charges fixes/trajet (FCFA)", value=85000)

    cout_u, co2 = calcul_cout_transport(dist, conso, prix_d, fixes)
    gain_annuel = calcul_rentabilite_flotte(cout_u, tarif_client, nbre_camions)

    with c2:
        st.metric("Coût de revient / Trajet", f"{cout_u:,} FCFA".replace(",", " "))
        st.metric("Profit Net Annuel Estimé", f"{gain_annuel:,} FCFA".replace(",", " "), delta="ROI Optimisé")

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
        st.success(f"ORDRE DE MISSION VALIDÉ pour {immat}")
        pdf_data = create_pdf(immat, marchandise, quai, type_op)
        st.download_button(
            label="📄 Télécharger le Bon de Docking (PDF)",
            data=pdf_data,
            file_name=f"Bon_Docking_{immat}.pdf",
            mime="application/pdf"
        )

# --- ONGLET 3 : TRACKING DU CORRIDOR ---
with tab3:
    st.write("### Suivi Temps Réel de l'Expédition")
    villes = ["Cotonou", "Porto-Novo", "Ouidah", "Seme-Kodji", "Abomey-Calavi", "Glo-Djigbé", "Allada", "Houègbo", "Cana", "Zogbodomey", "Bohicon", "Abomey", "Dassa", "Glazoue", "Savalou", "Savè", "Parakou", "Natitingou", "Djougou", "Malanville"]
    ct1, ct2 = st.columns(2)
    position = ct1.selectbox("Position actuelle", villes)
    statut = ct2.select_slider("Statut", options=["En transit", "Incident", "Livré"])
    color = {"En transit": "#ffad1f", "Incident": "#ff4b4b", "Livré": "#00cc66"}[statut]
    st.markdown(f'<div style="padding:20px; border-radius:15px; border-left: 8px solid {color}; background:rgba(255,255,255,0.03);"><h4>Convoi {immat}</h4><p>📍 Position : <b>{position}</b> | Statut : <b>{statut}</b></p></div>', unsafe_allow_html=True)

st.sidebar.info("Axe stratégique : GDIZ → Malanville")
    

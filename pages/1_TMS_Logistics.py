import streamlit as st
from models.mit_calculations import calcul_cout_transport, calcul_rentabilite_flotte
from fpdf import FPDF
import datetime
import pandas as pd
import io

st.set_page_config(page_title="TMS Intelligence · Bénin", layout="wide")

# --- INITIALISATION DE L'HISTORIQUE ---
if 'historique_docking' not in st.session_state:
    st.session_state.historique_docking = []

# --- FONCTION GÉNÉRATION PDF (Bon de Docking) ---
def create_pdf(immat, marchandise, quai, type_op):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "WEST AFRICA LOGISTICS HUB - GDIZ", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(190, 10, f"Bon généré le : {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.cell(190, 10, f"Immatriculation : {immat}", ln=True)
    pdf.cell(190, 10, f"Marchandise : {marchandise}", ln=True)
    pdf.cell(190, 10, f"Quai : {quai}", ln=True)
    pdf.cell(190, 10, f"Opération : {type_op}", ln=True)
    return pdf.output(dest="S").encode("latin-1")

# --- FONCTION EXPORT EXCEL (Récapitulatif) ---
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Docking_Journée')
    return output.getvalue()

st.markdown('<h1 style="font-family:Syne; color:#ffad1f;">🚛 Pilotage des Opérations TMS</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💰 Business Plan & ROI", "⚓ Docking GDIZ", "📍 Tracking Corridor"])

# --- ONGLET 1 : ROI ---
with tab1:
    st.write("### Rentabilité Flotte (360 jours)")
    c1, c2 = st.columns(2)
    with c1:
        tarif = st.number_input("Tarif Client (FCFA)", value=650000)
        nbre = st.slider("Camions / jour", 1, 50, 15)
        cout_u, co2 = calcul_cout_transport(720, 35, 700, 85000)
    with c2:
        gain = calcul_rentabilite_flotte(cout_u, tarif, nbre)
        st.metric("Profit Net Annuel", f"{gain:,} FCFA".replace(",", " "))

# --- ONGLET 2 : DOCKING & TABLEAU ---
with tab2:
    st.write("### Registre de Docking")
    with st.form("docking_form"):
        col_d1, col_d2, col_d3 = st.columns(3)
        immat = col_d1.text_input("Immatriculation", "RB 0001")
        marchandise = col_d2.selectbox("Marchandise", ["Maïs", "Coton", "Soja", "Cajou", "Tourteau", "Ciment", "Gaz"])
        quai = col_d3.selectbox("Quai", [f"Quai {l}" for l in "ABCDEFG"])
        type_op = st.radio("Opération", ["Chargement", "Déchargement"], horizontal=True)
        submitted = st.form_submit_button("Valider l'affectation")
        
    if submitted:
        # Enregistrement
        st.session_state.historique_docking.insert(0, {
            "Date": datetime.datetime.now().strftime("%d/%m/%Y"),
            "Heure": datetime.datetime.now().strftime("%H:%M"),
            "Immatriculation": immat,
            "Marchandise": marchandise,
            "Quai": quai,
            "Type": type_op
        })
        st.success("Camion enregistré avec succès.")

    # Affichage du tableau et Export Excel
    if st.session_state.historique_docking:
        df_hist = pd.DataFrame(st.session_state.historique_docking)
        st.write("### 📋 Historique de la session")
        st.dataframe(df_hist, use_container_width=True)
        
        # Boutons de téléchargement
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            pdf_data = create_pdf(immat, marchandise, quai, type_op)
            st.download_button("📄 Télécharger le DERNIER Bon (PDF)", data=pdf_data, file_name=f"Bon_{immat}.pdf")
        with btn_col2:
            excel_data = to_excel(df_hist)
            st.download_button("Excel 📥 Exporter tout l'historique (Excel)", data=excel_data, file_name="recap_docking_gdiz.xlsx")

# --- ONGLET 3 : TRACKING ---
with tab3:
    villes = ["Cotonou", "Porto-Novo", "Glo-Djigbé", "Bohicon", "Dassa", "Parakou", "Malanville"]
    c_t1, c_t2 = st.columns(2)
    pos = c_t1.selectbox("Position actuelle", villes)
    status = c_t2.select_slider("Statut", options=["En transit", "Incident", "Livré"])
    st.info(f"📍 Point de contrôle : {pos} | Statut : {status}")
    

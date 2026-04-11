import streamlit as st
import pandas as pd
from models.mit_calculations import calcul_wilson_eoq, calcul_point_de_commande, analyse_pareto_abc

st.set_page_config(page_title="WMS Intelligence", layout="wide")

st.markdown('<h1 style="font-family:Syne; color:#ffad1f;">📦 WMS Intelligence : Stocks</h1>', unsafe_allow_html=True)
st.markdown("---")

tab1, tab2 = st.tabs(["📊 Analyse ABC", "⚙️ Optimisation Wilson"])

with tab1:
    st.sidebar.header("📁 Importation")
    uploaded_file = st.sidebar.file_uploader("Charger fichier de stock", type=["csv", "xlsx"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        if 'Valeur' in df.columns:
            df_abc = analyse_pareto_abc(df, 'Valeur')
            st.write("### Résultat de la Classification ABC")
            st.dataframe(df_abc[['Référence', 'Valeur', 'Classe_ABC']], use_container_width=True)
        else:
            st.error("Colonne 'Valeur' manquante dans votre fichier.")

with tab2:
    st.write("### Simulateur de commande optimale")
    demande = st.number_input("Demande annuelle", value=1000)
    if st.button("Calculer EOQ"):
        res = calcul_wilson_eoq(demande, 5000, 250)
        st.success(f"Quantité optimale : {res} unités")
            

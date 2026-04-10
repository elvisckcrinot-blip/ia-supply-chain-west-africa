import streamlit as st
import pandas as pd
from models.mit_calculations import calcul_wilson_eoq, calcul_point_de_commande

st.set_page_config(page_title="WMS Intelligence", layout="wide")

st.title("📦 Warehouse Management System")
st.subheader("Optimisation des stocks via modèles MIT CTL")

# --- Formulaire de simulation ---
with st.expander("🛠️ Paramètres d'optimisation (Calculateur Wilson)"):
    col1, col2, col3 = st.columns(3)
    demande = col1.number_input("Demande annuelle (unités)", value=1200)
    cout_c = col2.number_input("Coût par commande ($)", value=50)
    cout_s = col3.number_input("Coût de stockage par unité/an ($)", value=2)

    if st.button("Calculer l'EOQ"):
        resultat = calcul_wilson_eoq(demande, cout_c, cout_s)
        st.success(f"La quantité économique de commande (EOQ) est de : **{resultat} unités**")

st.info("Ce module utilise les données de `data/processed/` pour générer des alertes de rupture.")
from utils.helpers import load_logistics_data
from models.mit_calculations import analyse_pareto_abc

st.sidebar.header("📁 Importation des données")
uploaded_file = st.sidebar.file_uploader("Charger votre fichier de stock (CSV/Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Lecture du fichier réel
    df_stock = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    st.write("### 📊 Analyse de l'Inventaire Réel")
    
    # Exécution automatique de l'analyse de Pareto (MIT)
    if 'Valeur' in df_stock.columns:
        df_analyse = analyse_pareto_abc(df_stock, 'Valeur')
        
        # Affichage des indicateurs stratégiques
        c1, c2, c3 = st.columns(3)
        c1.metric("Produits Classe A", len(df_analyse[df_analyse['Classe_ABC'] == 'A']))
        c2.metric("Valeur Totale Stock", f"{df_analyse['Valeur'].sum():,.2f} $")
        c3.info("La Classe A représente 80% de votre capital immobilisé.")
        
        st.dataframe(df_analyse[['Référence', 'Valeur', 'Classe_ABC']])
    else:
        st.warning("Pour l'analyse ABC, votre fichier doit contenir une colonne nommée 'Valeur'.")

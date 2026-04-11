import streamlit as st
import pandas as pd
from models.mit_calculations import calcul_wilson_eoq, analyse_pareto_abc

# --- 1. STYLE & CONFIG ---
st.set_page_config(page_title="WMS Intelligence · Bénin", layout="wide")

st.markdown("""
<style>
    @import url('https://googleapis.com');
    .main-title { font-family: 'Syne', sans-serif; color: #ffad1f; font-size: 38px; font-weight: 800; }
    .wms-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; text-align: center; }
    .wms-val { font-family: 'Syne', sans-serif; font-size: 32px; font-weight: 800; color: #ffad1f; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📦 WMS Intelligence : Stocks</h1>', unsafe_allow_html=True)
st.markdown("---")

tab1, tab2 = st.tabs(["📊 Analyse ABC (Pareto)", "⚙️ Optimisation Wilson (EOQ)"])

# --- ONGLET 1 : ANALYSE ABC ---
with tab1:
    st.sidebar.header("📁 Importation des données")
    uploaded_file = st.sidebar.file_uploader("Charger votre inventaire (CSV/Excel)", type=["csv", "xlsx"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        if 'Valeur' in df.columns and 'Référence' in df.columns:
            df_abc = analyse_pareto_abc(df, 'Valeur')
            
            # Affichage des KPIs en haut
            c1, c2, c3 = st.columns(3)
            val_total = f"{df['Valeur'].sum():,.0f}".replace(",", " ")
            c1.markdown(f'<div class="wms-card"><div style="color:#7a92b0; font-size:12px;">VALEUR TOTALE STOCK</div><div class="wms-val">{val_total} FCFA</div></div>', unsafe_allow_html=True)
            
            nb_a = len(df_abc[df_abc['Classe_ABC'] == 'A'])
            c2.markdown(f'<div class="wms-card"><div style="color:#7a92b0; font-size:12px;">ARTICLES CRITIQUES (A)</div><div class="wms-val">{nb_a}</div></div>', unsafe_allow_html=True)
            
            c3.markdown(f'<div class="wms-card"><div style="color:#7a92b0; font-size:12px;">RÉFÉRENCES GÉRÉES</div><div class="wms-val">{len(df)}</div></div>', unsafe_allow_html=True)

            st.write("### Classification de l'Inventaire")
            st.dataframe(df_abc[['Référence', 'Valeur', 'Classe_ABC']], use_container_width=True)
        else:
            st.error("Le fichier doit obligatoirement comporter les colonnes 'Référence' et 'Valeur' (en FCFA).")
    else:
        st.info("👋 Bienvenue. Veuillez charger un fichier Excel ou CSV dans la barre latérale pour analyser votre stock.")

# --- ONGLET 2 : OPTIMISATION WILSON ---
with tab2:
    st.write("### Calcul de la Quantité Économique de Commande")
    col_w1, col_w2 = st.columns([1, 1.2])
    
    with col_w1:
        st.info("Paramètres de Commande")
        demande = st.number_input("Demande annuelle prévue (Unités)", value=1200)
        cout_p = st.number_input("Coût de passation d'une commande (FCFA)", value=5000)
        cout_s = st.number_input("Coût de stockage /unité /an (FCFA)", value=250)

    with col_w2:
        res_eoq = calcul_wilson_eoq(demande, cout_p, cout_s)
        st.write("### Résultat MIT CTL")
        st.markdown(f"""
            <div class="wms-card">
                <div style="color: #7a92b0; font-size: 14px;">QUANTITÉ OPTIMALE À COMMANDER (EOQ)</div>
                <div class="wms-val">{res_eoq} Unités</div>
                <div style="color: #5fc385; font-size: 12px; margin-top:5px;">✓ Minimise le coût total selon Wilson</div>
            </div>
        """, unsafe_allow_html=True)

st.sidebar.info("Axe stratégique : Gestion d'entrepôt GDIZ")
    

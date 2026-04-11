import streamlit as st
import pandas as pd
from models.mit_calculations import calcul_wilson_eoq, analyse_pareto_abc
import io

# --- 1. CONFIGURATION ET STYLE ---
st.set_page_config(page_title="WMS Intelligence · Bénin", layout="wide")

st.markdown("""
<style>
    @import url('https://googleapis.com');
    .main-title { font-family: 'Syne', sans-serif; color: #ffad1f; font-size: 38px; font-weight: 800; }
    .wms-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; text-align: center; }
    .wms-val { font-family: 'Syne', sans-serif; font-size: 32px; font-weight: 800; color: #ffad1f; }
    /* Style pour l'en-tête bleu des paramètres */
    .param-header { background-color: #1a3a5a; color: #4a9eff; padding: 12px; border-radius: 8px; margin-bottom: 20px; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# --- 2. FONCTION EXPORT ---
def to_excel_plan_achat(df_alertes):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_alertes.to_excel(writer, index=False, sheet_name='Plan_Achat_Urgent')
    return output.getvalue()

st.markdown('<h1 class="main-title">📦 WMS Intelligence : Stocks</h1>', unsafe_allow_html=True)
st.markdown("---")

tab1, tab2 = st.tabs(["📊 Analyse & Plan d'Achat", "⚙️ Optimisation Wilson (EOQ)"])

# --- ONGLET 1 : ANALYSE ABC & ALERTES ---
with tab1:
    st.sidebar.header("📁 Importation")
    uploaded_file = st.sidebar.file_uploader("Fichier Stock (Référence, Valeur, Quantité, ROP_Seuil)", type=["csv", "xlsx"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        cols_requises = ['Référence', 'Valeur', 'Quantité', 'ROP_Seuil']
        
        if all(col in df.columns for col in cols_requises):
            df_abc = analyse_pareto_abc(df, 'Valeur')
            
            def definir_statut(row):
                if row['Quantité'] <= row['ROP_Seuil']: return "🔴 RUPTURE"
                if row['Quantité'] <= row['ROP_Seuil'] * 1.2: return "🟠 STOCK FAIBLE"
                return "🟢 OPTIMAL"
            
            df_abc['Statut'] = df_abc.apply(definir_statut, axis=1)
            
            # KPIs
            c1, c2, c3 = st.columns(3)
            nb_alertes = len(df_abc[df_abc['Statut'].str.contains("🔴|🟠")])
            val_total = f"{df['Valeur'].sum():,.0f}".replace(",", " ")
            
            c1.markdown(f'<div class="wms-card"><div style="color:#7a92b0; font-size:12px;">VALEUR DU STOCK</div><div class="wms-val">{val_total} FCFA</div></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="wms-card"><div style="color:#7a92b0; font-size:12px;">ARTICLES À COMMANDER</div><div class="wms-val" style="color:#ff4b4b;">{nb_alertes}</div></div>', unsafe_allow_html=True)
            c3.markdown(f'<div class="wms-card"><div style="color:#7a92b0; font-size:12px;">RÉFÉRENCES GÉRÉES</div><div class="wms-val">{len(df)}</div></div>', unsafe_allow_html=True)

            # Bouton Export
            df_achat = df_abc[df_abc['Statut'].str.contains("🔴|🟠")].copy()
            if not df_achat.empty:
                excel_data = to_excel_plan_achat(df_achat[['Référence', 'Quantité', 'ROP_Seuil', 'Statut']])
                st.download_button("📥 Télécharger le Plan d'Achat (Excel)", data=excel_data, file_name="plan_achat.xlsx")
            
            st.dataframe(df_abc[['Référence', 'Valeur', 'Classe_ABC', 'Quantité', 'Statut']], use_container_width=True)
    else:
        st.info("Veuillez charger votre fichier Excel pour activer l'analyse.")

# --- ONGLET 2 : OPTIMISATION WILSON (FORMAT IMAGE) ---
with tab2:
    st.markdown("## Calcul de la Quantité Économique de Commande")
    
    # Bloc de saisie
    with st.container():
        st.markdown('<div class="param-header">Paramètres de Commande</div>', unsafe_allow_html=True)
        
        # Champs de saisie conformes à l'image
        demande_annuelle = st.number_input("Demande annuelle prévue (Unités)", value=1200, step=100)
        cout_passation = st.number_input("Coût de passation d'une commande (FCFA)", value=5000, step=500)
        cout_stockage = st.number_input("Coût de stockage /unité /an (FCFA)", value=250, step=10)

    # Calcul et Affichage du résultat
    st.markdown("---")
    res_eoq = calcul_wilson_eoq(demande_annuelle, cout_passation, cout_stockage)
    
    st.markdown(f"""
        <div class="wms-card">
            <div style="color: #7a92b0; font-size: 14px;">QUANTITÉ OPTIMALE À COMMANDER (EOQ)</div>
            <div class="wms-val">{res_eoq} Unités</div>
            <div style="color: #5fc385; font-size: 12px; margin-top:5px;">✓ Modèle Wilson MIT CTL</div>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.info("WMS Intelligent · Axe GDIZ")
    

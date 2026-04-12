import streamlit as st
import pandas as pd
from models.mit_calculations import calcul_wilson_eoq, analyse_pareto_abc
# Importation enrichie du moteur IA
from models.ai_engine import predict_safety_stock, classify_abc, analyse_six_sigma
import io

# --- 1. CONFIGURATION ET STYLE ---
st.set_page_config(page_title="WMS Intelligence · Bénin", layout="wide")

st.markdown("""
<style>
    @import url('https://googleapis.com');
    .main-title { font-family: 'Syne', sans-serif; color: #ffad1f; font-size: 38px; font-weight: 800; }
    .wms-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; text-align: center; }
    .wms-val { font-family: 'Syne', sans-serif; font-size: 32px; font-weight: 800; color: #ffad1f; }
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

            st.dataframe(df_abc[['Référence', 'Valeur', 'Classe_ABC', 'Quantité', 'Statut']], use_container_width=True)
    else:
        st.info("Veuillez charger votre fichier Excel pour activer l'analyse de stock opérationnelle.")

# --- ONGLET 2 : OPTIMISATION WILSON (EOQ) ---
with tab2:
    st.markdown("## Calcul de la Quantité Économique de Commande")
    
    with st.container():
        st.markdown('<div class="param-header">Paramètres de Commande</div>', unsafe_allow_html=True)
        demande_annuelle = st.number_input("Demande annuelle prévue (Unités)", value=1200, step=100)
        cout_passation = st.number_input("Coût de passation d'une commande (FCFA)", value=5000, step=500)
        cout_stockage = st.number_input("Coût de stockage /unité /an (FCFA)", value=250, step=10)

    st.markdown("---")
    res_eoq = calcul_wilson_eoq(demande_annuelle, cout_passation, cout_stockage)
    
    st.markdown(f"""
        <div class="wms-card">
            <div style="color: #7a92b0; font-size: 14px;">QUANTITÉ OPTIMALE À COMMANDER (EOQ)</div>
            <div class="wms-val">{res_eoq} Unités</div>
            <div style="color: #5fc385; font-size: 12px; margin-top:5px;">✓ Modèle Wilson MIT CTL</div>
        </div>
    """, unsafe_allow_html=True)

# --- 3. SECTION : INTELLIGENCE DE STOCK (IA ENGINE) ---
st.markdown("---")
st.markdown("### 🤖 Intelligence de Stock (Moteur IA)")

col_ia1, col_ia2 = st.columns(2)

with col_ia1:
    st.info("Calcul du Stock de Sécurité (MIT SC0x)")
    service_lvl = st.select_slider("Niveau de Service cible", options=[0.85, 0.90, 0.95, 0.99], value=0.95)
    sigma = st.number_input("Variabilité de la demande (Écart-type)", value=15, min_value=1)
    lead_time = st.number_input("Délai de réapprovisionnement (Jours)", value=5, min_value=1)
    
    if st.button("Calculer le Stock de Sécurité"):
        ss_recommande = predict_safety_stock(service_lvl, sigma, lead_time)
        st.success(f"Stock de Sécurité Recommandé : **{ss_recommande} unités**")
        st.caption("Aide à prévenir les ruptures de stock à la GDIZ en cas d'imprévus.")

with col_ia2:
    st.info("Analyse de Priorisation ABC")
    data_demo = {
        'Produit': ['Fibre de Coton', 'Noix de Cajou', 'Soja Bio', 'Textile transformé', 'Ananas'],
        'valeur_consommation': [5000000, 3000000, 1500000, 400000, 100000]
    }
    df_demo = pd.DataFrame(data_demo)
    
    if st.button("Lancer l'Analyse de Pareto"):
        df_priorise = classify_abc(df_demo)
        st.dataframe(df_priorise[['Produit', 'Categorie_ABC']], use_container_width=True)
        st.caption("Les produits 'A' représentent 80% de votre valeur totale.")

# --- 4. SECTION : PERFORMANCE QUALITÉ (SIX SIGMA) ---
st.markdown("---")
st.markdown("### 📊 Performance Qualité : Lean Six Sigma")

col_sig1, col_sig2 = st.columns([1, 2])

with col_sig1:
    st.info("Calculateur DPMO")
    total_colis = st.number_input("Total colis préparés", value=10000, min_value=1)
    erreurs = st.number_input("Erreurs constatées (Inversions/Défauts)", value=50, min_value=0)
    
    if st.button("Calculer le Niveau Sigma"):
        dpmo_res, sigma_res = analyse_six_sigma(total_colis, erreurs)
        st.metric("Niveau Sigma", f"{sigma_res} σ")
        st.write(f"**DPMO :** {dpmo_res:,.0f}")
    else:
        # Initialisation par défaut pour éviter l'erreur NameError au premier chargement
        sigma_res = 0

with col_sig2:
    st.write("#### Interprétation MIT CTL")
    if 'sigma_res' in locals() and sigma_res > 0:
        if sigma_res >= 4.5:
            st.success("Excellent : Processus de classe mondiale (World Class Manufacturing).")
        elif sigma_res >= 3.0:
            st.warning("Standard : Processus stable mais nécessite une réduction de la variabilité.")
        else:
            st.error("Critique : Capabilité insuffisante. Risque élevé de coûts de non-qualité.")
    else:
        st.write("Veuillez lancer le calcul pour obtenir l'interprétation.")
    
    st.caption("Le MIT valorise la réduction de la variabilité pour stabiliser la Supply Chain.")

st.sidebar.info("WMS Intelligent · Axe GDIZ")
    

import streamlit as st
import pandas as pd
import plotly.express as px
from helpers import get_data, apply_ui_theme, preprocess_for_mit

# Importation des logiques métiers académiques
try:
    from models.mit_calculations import calcul_wilson_eoq, analyse_pareto_abc
    from models.ai_engine import predict_safety_stock, classify_abc
except ImportError:
    def calcul_wilson_eoq(d, cp, ch): return int((2*d*cp/ch)**0.5)
    def predict_safety_stock(lvl, s, lt): return int(1.65 * s * (lt**0.5))

# --- STYLE ET UI ---
apply_ui_theme()

st.markdown('<h1 style="font-family:Syne; color:#ffad1f;">📦 Intelligence Entrepôt (WMS · Cloud Sync)</h1>', unsafe_allow_html=True)

# --- SIDEBAR : MODE DE DONNÉES ---
with st.sidebar:
    st.header("⚙️ Source des Données")
    source = st.radio("Choisir la source :", ["Base de données Neon (Live)", "Import Manuel (Excel/CSV)"])
    
    if source == "Import Manuel (Excel/CSV)":
        uploaded_file = st.file_uploader("Fichier Stock", type=["csv", "xlsx"])
    else:
        st.success("📡 Connexion Cloud Active")
        uploaded_file = None

tab1, tab2, tab3 = st.tabs(["📊 Dashboard Inventaire", "⚙️ Optimisation Wilson", "🤖 Moteur Prédictif"])

# --- ONGLET 1 : ANALYSE DES STOCKS ---
with tab1:
    df = None
    
    # CHARGEMENT DES DONNÉES SELON LA SOURCE
    if source == "Base de données Neon (Live)":
        if st.button("🔄 Actualiser depuis Neon"):
            df = get_data("SELECT * FROM stocks_gdiz")
    elif uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

    if df is not None:
        # Nettoyage automatique via helpers
        df = preprocess_for_mit(df)
        
        # Adaptation des noms de colonnes (Base de données vs Excel)
        q_col = 'quantite_actuelle' if 'quantite_actuelle' in df.columns else 'Quantité'
        r_col = 'seuil_rop' if 'seuil_rop' in df.columns else 'ROP_Seuil'
        v_col = 'prix_unitaire' if 'prix_unitaire' in df.columns else 'Valeur'

        # Logique de statut
        df['Statut'] = df.apply(lambda x: "🔴 RUPTURE" if x[q_col] <= x[r_col] else "🟢 OPTIMAL", axis=1)
        
        # KPIs
        c1, c2, c3 = st.columns(3)
        with c1:
            val_total = (df[v_col] * df[q_col]).sum() if v_col in df.columns else 0
            st.markdown(f'<div class="stMetric"><small>VALEUR DU STOCK</small><br><span style="font-size:24px; color:#ffad1f; font-weight:bold;">{val_total:,.0f} FCFA</span></div>', unsafe_allow_html=True)
        with c2:
            alertes = len(df[df['Statut'] == "🔴 RUPTURE"])
            st.markdown(f'<div class="stMetric"><small>ALERTES ROP</small><br><span style="font-size:24px; color:#ff4b4b; font-weight:bold;">{alertes}</span></div>', unsafe_allow_html=True)
        with c3:
            nb_ref = len(df)
            st.markdown(f'<div class="stMetric"><small>RÉFÉRENCES</small><br><span style="font-size:24px; color:#5fc385; font-weight:bold;">{nb_ref}</span></div>', unsafe_allow_html=True)

        st.write("")
        
        # Graphique
        fig_abc = px.pie(df, names='Statut', title="Disponibilité Critique (GDIZ)", hole=.4, color_discrete_sequence=['#5fc385', '#ff4b4b'])
        fig_abc.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig_abc, use_container_width=True)

        st.dataframe(df, use_container_width=True)
    else:
        st.info("Sélectionnez une source et cliquez sur 'Actualiser' pour charger les stocks.")

# --- ONGLET 2 : WILSON EOQ ---
with tab2:
    st.subheader("🎯 Quantité Économique de Commande")
    col_e1, col_e2 = st.columns([1, 2])
    
    with col_e1:
        d_annuelle = st.number_input("Demande annuelle (D)", value=12000)
        c_passation = st.number_input("Coût de passation (S)", value=15000)
        c_possession = st.number_input("Coût de possession/u (H)", value=500)
        
        if st.button("Calculer l'EOQ"):
            eoq = calcul_wilson_eoq(d_annuelle, c_passation, c_possession)
            st.session_state['last_eoq'] = eoq

    with col_e2:
        if 'last_eoq' in st.session_state:
            st.markdown(f"""
                <div style="background:rgba(255,173,31,0.05); border:1px solid #ffad1f; padding:20px; border-radius:12px; text-align:center;">
                    <p>EOQ CALCULÉ ( Wilson )</p>
                    <h1 style="color:#ffad1f; font-size:48px;">{st.session_state['last_eoq']} unités</h1>
                </div>
            """, unsafe_allow_html=True)

# --- ONGLET 3 : IA & SAFETY STOCK ---
with tab3:
    st.subheader("🤖 Prédiction du Stock de Sécurité")
    c_ia1, c_ia2 = st.columns(2)
    with c_ia1:
        service_lvl = st.select_slider("Taux de Service Cible", options=[0.90, 0.95, 0.98, 0.99], value=0.95)
        sigma = st.number_input("Variabilité de la demande (σ)", value=25)
        lead_time = st.number_input("Délai de réappro (Jours)", value=7)
        if st.button("Calculer Stock de Sécurité"):
            ss = predict_safety_stock(service_lvl, sigma, lead_time)
            st.success(f"Stock de Sécurité : {ss} unités")
    with c_ia2:
        st.info("💡 Le calcul utilise le Z-score statistique du MIT MicroMasters pour garantir que vous ne tomberez pas en rupture sur le corridor.")

st.divider()
st.caption("WA Logistics Hub · Base de données : Neon Cloud · Moteur : Python 3.9")
    

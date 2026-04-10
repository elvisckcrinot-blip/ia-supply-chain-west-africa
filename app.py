import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import norm
from datetime import datetime

# ==========================================
# 1. CONFIGURATION ET STYLE
# ==========================================
st.set_page_config(page_title="West Africa Logistics Hub", layout="wide", page_icon="🌍")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #dee2e6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3em; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Initialisation des états de session
if 'page' not in st.session_state: st.session_state.page = 'accueil'
if 'db_tms' not in st.session_state:
    st.session_state.db_tms = pd.DataFrame(columns=['Date', 'Camion', 'Produit', 'Tonnage', 'Opération', 'Position', 'Statut'])
if 'db_dock' not in st.session_state:
    st.session_state.db_dock = pd.DataFrame(columns=['Heure', 'Camion', 'Produit', 'Tonnage', 'Opération', 'Quai'])

def go_to(page):
    st.session_state.page = page
    st.rerun()

# ==========================================
# 2. PAGE D'ACCUEIL (HUB)
# ==========================================
if st.session_state.page == 'accueil':
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🌍 West Africa Logistics Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em;'>Expertise MIT CTL – Pilotage Stratégique & Opérationnel au Bénin</p>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.info("### 🚛 MODULE 1 : TMS Logistics")
        st.write("**Gestion des flux transport :** Docking Usine X, Tonnage par filière (Coton, Soja, etc.) et Optimisation Énergétique SC0x.")
        if st.button("OUVRIR LE TMS"): go_to('tms')
    with col2:
        st.success("### 📦 MODULE 2 : WMS Logistics")
        st.write("**Intelligence des stocks :** Simulation de scénarios, Risque financier (FCFA) et Réapprovisionnement automatique EOQ.")
        if st.button("OUVRIR LE WMS"): go_to('wms')
    
    st.write("##")
    st.caption("Développé par Elvis – Expertise Supply Chain West Africa | Standards GDIZ & MIT")

# ==========================================
# 3. MODULE TMS (TRANSPORT & DOCKING)
# ==========================================
elif st.session_state.page == 'tms':
    if st.sidebar.button("⬅ Menu Principal"): go_to('accueil')
    st.title("🚛 TMS : Pilotage Transport & Tonnage")

    # --- 3.1 OPTIMISATION MIT SC0x ---
    with st.expander("📊 Optimisation Énergétique (Cerveau Financier)", expanded=True):
        c1, c2, c3 = st.columns(3)
        n_cam = c1.number_input("Nombre de camions", value=10)
        d_act = c2.number_input("Km/jour actuel", value=80.0)
        d_opt = c2.number_input("Km/jour optimisé", value=65.0)
        gain_annuel = (d_act - d_opt) * n_cam * 300 * (32/100) * 700
        st.metric("Économie Budget Transport (Annuel)", f"{gain_annuel:,.0f} FCFA", help="Basé sur une conso de 32L/100km")

    # --- 3.2 GESTION DU DOCKING (TONNAGE & MARCHANDISES) ---
    st.header("🏢 Gestion du Docking Usine X")
    liste_marchandises = ["Maïs", "Noix", "Ananas", "Soja", "Coton", "Acajou", "Tourteau", "Ciment", "Gaz"]
    
    col_d1, col_d2 = st.columns([1, 1.5])
    with col_d1:
        with st.form("docking_form"):
            st.subheader("Contrôle d'Accès")
            imm = st.text_input("Immatriculation", "RB XXXX")
            prod = st.selectbox("Marchandise", liste_marchandises)
            poids = st.number_input("Poids (Tonnes)", 0.1, 70.0, 25.0)
            ope = st.radio("Opération", ["Chargement", "Déchargement"], horizontal=True)
            quai = st.selectbox("Quai Assigné", ["Quai A1", "Quai A2", "Quai B1", "Quai B2"])
            if st.form_submit_button("Valider l'opération"):
                new_entry = pd.DataFrame([{'Heure': datetime.now().strftime("%H:%M"), 'Camion': imm, 'Produit': prod, 'Tonnage': poids, 'Opération': ope, 'Quai': quai}])
                st.session_state.db_dock = pd.concat([st.session_state.db_dock, new_entry], ignore_index=True)
                st.success("Opération validée au dock.")

    with col_d2:
        st.subheader("Performance du Jour")
        if not st.session_state.db_dock.empty:
            k1, k2 = st.columns(2)
            total_t = st.session_state.db_dock['Tonnage'].sum()
            k1.metric("Total Flux (Tonnes)", f"{total_t:,.1f} T")
            k2.metric("Camions Traités", len(st.session_state.db_dock))
            st.dataframe(st.session_state.db_dock.tail(5), use_container_width=True)
        else: st.info("Aucun mouvement enregistré ce jour.")

    # --- 3.3 TRACKING BÉNIN ---
    st.header("📍 Suivi des Expéditions (Tracking)")
    villes = {"GDIZ (Départ)": 0, "Cotonou": 25, "Allada": 45, "Bohicon": 105, "Dassa": 185, "Parakou": 395, "Djougou": 450, "Malanville": 720}
    with st.form("tracking_form"):
        ref = st.text_input("ID Expédition")
        pos = st.selectbox("Position Actuelle", list(villes.keys()))
        if st.form_submit_button("Actualiser Tracking"):
            st.toast(f"Tracking mis à jour : {pos}")
    
    dist = villes[pos]
    st.progress(min(dist / 720, 1.0))
    st.write(f"Dist. parcourue depuis GDIZ : **{dist} km**")

# ==========================================
# 4. MODULE WMS (STOCKS & INTELLIGENCE)
# ==========================================
elif st.session_state.page == 'wms':
    if st.sidebar.button("⬅ Menu Principal"): go_to('accueil')
    st.title("📦 WMS : Pilotage Stratégique")

    with st.sidebar:
        st.header("⚙️ Simulateur de Scénarios")
        hausse = st.slider("Pic de Demande (%)", 0, 100, 0) / 100
        retard = st.number_input("Retard Logistique (Jours)", value=0)
        st.markdown("---")
        up = st.file_uploader("1. Charger Inventaire Excel", type=["xlsx"])

    # Données simulées robustes
    data_wms = {
        'SKU': ['REF-MAI-01', 'REF-COT-02', 'REF-SOJ-03', 'REF-ACA-04', 'REF-CIM-05'],
        'Désignation': ['Maïs Grain', 'Coton Fibre', 'Soja Bio', 'Acajou Brut', 'Ciment Sac'],
        'Prix':, 'Stock':, 'Vente_J':, 'Sigma': [2.5, 1.2, 5.0, 0.5, 15.0]
    }
    df = pd.DataFrame(data_wms)

    # Logique MIT CTL (Z-Score & Stochastique)
    z = norm.ppf(0.95)
    lt_total = 14 + retard
    df['Vente_Sim'] = df['Vente_J'] * (1 + hausse)
    df['Safety_Stock'] = (z * df['Sigma'] * np.sqrt(lt_total)).astype(int)
    df['ROP'] = (df['Vente_Sim'] * lt_total) + df['Safety_Stock']
    df['Valeur_Stock'] = df['Stock'] * df['Prix']
    df['Couverture'] = (df['Stock'] / df['Vente_Sim']).replace([np.inf, -np.inf], 0).fillna(0).astype(int)
    df['Valeur_en_Risque'] = df.apply(lambda x: (x['Vente_Sim'] * x['Prix'] * 7) if x['Stock'] <= x['ROP'] else 0, axis=1)

    # Dashboard WMS
    k1, k2, k3 = st.columns(3)
    k1.metric("Valeur Totale", f"{df['Valeur_Stock'].sum():,.0f} FCFA")
    k2.metric("Valeur en Risque", f"{df['Valeur_en_Risque'].sum():,.0f} FCFA", delta="Impact CA", delta_color="inverse")
    k3.metric("Niveau de Service", "95%")

    st.subheader("📋 État de l'Inventaire & Analyse de Rupture")
    
    def color_status(val):
        if val <= 0: return 'background-color: #fee2e2'
        return ''
    
    st.dataframe(df[['SKU', 'Désignation', 'Stock', 'Couverture', 'ROP', 'Valeur_en_Risque']], use_container_width=True)

    # Plan de Réapprovisionnement EOQ (Wilson)
    st.header("🛒 Plan de Réapprovisionnement Automatique")
    df_reap = df[df['Stock'] <= df['ROP']].copy()
    if not df_reap.empty:
        df_reap['Qte_A_Commander'] = np.sqrt((2 * df_reap['Vente_Sim'] * 365 * 15000) / (0.15 * df_reap['Prix'])).astype(int)
        st.table(df_reap[['SKU', 'Désignation', 'Stock', 'ROP', 'Qte_A_Commander']])
        csv = df_reap.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger le Bon de Commande", csv, "bon_achat.csv", "text/csv")
    else: st.success("✅ Aucun réapprovisionnement nécessaire.")

    # Graphique ABC
    st.write("##")
    fig = px.pie(df, values='Valeur_Stock', names='SKU', title="Analyse ABC - Valeur Financière du Stock", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
        

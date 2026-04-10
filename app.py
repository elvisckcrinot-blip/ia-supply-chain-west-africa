import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
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

# Navigation
if 'page' not in st.session_state: 
    st.session_state.page = 'accueil'

# Mémoire des mouvements au Dock
if 'db_dock' not in st.session_state:
    st.session_state.db_dock = pd.DataFrame(columns=['Heure', 'Camion', 'Marchandise', 'Tonnage', 'Opération', 'Quai'])

def go_to(page):
    st.session_state.page = page
    st.rerun()

# ==========================================
# 2. PAGE D'ACCUEIL (HUB)
# ==========================================
if st.session_state.page == 'accueil':
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🌍 West Africa Logistics Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em;'>Pilotage Stratégique & Opérationnel au Bénin (Usine X)</p>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.info("### 🚛 MODULE 1 : TMS Logistics")
        st.write("**Gestion du Transport :** Entrées/Sorties Usine X, suivi des marchandises et économies de carburant.")
        if st.button("OUVRIR LE TMS"): 
            go_to('tms')
    with col2:
        st.success("### 📦 MODULE 2 : WMS Logistics")
        st.write("**Gestion d'Entrepôt :** Suivi d'inventaire, alertes de rupture et bons de commande automatiques.")
        if st.button("OUVRIR LE WMS"): 
            go_to('wms')
    
    st.write("##")
    st.caption("Développé par Elvis – Expertise Supply Chain West Africa")

# ==========================================
# 3. MODULE TMS (TRANSPORT & DOCKING)
# ==========================================
elif st.session_state.page == 'tms':
    if st.sidebar.button("⬅ Menu Principal"): 
        go_to('accueil')
    
    st.title("🚛 TMS : Pilotage Transport & Flux")

    # --- 3.1 OPTIMISATION CARBURANT ---
    with st.expander("📊 Calculateur d'Économie Carburant", expanded=True):
        c1, c2, c3 = st.columns(3)
        n_cam = c1.number_input("Nombre de camions", value=10)
        d_act = c2.number_input("Km parcourus/jour actuel", value=80.0)
        d_opt = c2.number_input("Km parcourus/jour optimisé", value=65.0)
        gain_annuel = (d_act - d_opt) * n_cam * 300 * (32/100) * 700
        st.metric("Économie Budget Transport (Gain Annuel)", f"{gain_annuel:,.0f} FCFA")

    # --- 3.2 GESTION DU DOCKING ---
    st.header("🏢 1. Gestion du Docking (Entrée/Sortie Usine X)")
    
    # Nature des marchandises
    liste_marchandises = ["Maïs", "Soja", "Coton", "Tourteau", "Cajou", "Ciment", "Gaz"]
    
    col_d1, col_d2 = st.columns([1, 1.5])
    with col_d1:
        with st.form("docking_form"):
            st.subheader("Contrôle d'Accès")
            imm = st.text_input("Immatriculation du véhicule", "RB 1234")
            prod = st.selectbox("Nature de la marchandise", liste_marchandises)
            poids = st.number_input("Tonnage chargé (Tonnes)", 0.1, 70.0, 25.0)
            ope = st.radio("Opération au quai", ["Chargement", "Déchargement"], horizontal=True)
            quai_assigne = st.selectbox("Quai assigné", ["Quai A1", "Quai A2", "Quai B1", "Quai B2"])
            
            if st.form_submit_button("Valider l'opération"):
                new_entry = pd.DataFrame([{
                    'Heure': datetime.now().strftime("%H:%M"), 
                    'Camion': imm, 
                    'Marchandise': prod, 
                    'Tonnage': poids, 
                    'Opération': ope, 
                    'Quai': quai_assigne
                }])
                st.session_state.db_dock = pd.concat([st.session_state.db_dock, new_entry], ignore_index=True)
                st.success(f"Opération validée pour {prod}")

    with col_d2:
        st.subheader("Performance & État des Quais")
        if not st.session_state.db_dock.empty:
            k1, k2 = st.columns(2)
            k1.metric("Tonnage Journalier", f"{st.session_state.db_dock['Tonnage'].sum():,.1f} T")
            k2.metric("Camions Traités", len(st.session_state.db_dock))
            st.dataframe(st.session_state.db_dock.tail(5), use_container_width=True)
        else: 
            st.info("Aucun mouvement enregistré pour le moment.")

    # --- 3.3 TRACKING BÉNIN (DÉPART USINE X) ---
    st.header("📍 3. Suivi des Expéditions (Tracking)")
    villes = {"Usine X (Départ)": 0, "Cotonou": 25, "Allada": 45, "Bohicon": 105, "Dassa": 185, "Parakou": 395, "Malanville": 720}
    with st.form("tracking_form"):
        ref = st.text_input("Référence de l'expédition")
        pos = st.selectbox("Position actuelle constatée", list(villes.keys()))
        if st.form_submit_button("Actualiser le suivi"):
            st.toast(f"Position mise à jour pour {ref}")
    
    dist = villes[pos]
    st.progress(min(dist / 720, 1.0))
    st.write(f"Distance parcourue depuis l'**Usine X** : **{dist} km**")

# ==========================================
# 4. MODULE WMS (STOCKS & INVENTAIRE)
# ==========================================
elif st.session_state.page == 'wms':
    if st.sidebar.button("⬅ Menu Principal"): 
        go_to('accueil')
    
    st.title("📦 WMS : Gestion d'Entrepôt")

    with st.sidebar:
        st.header("🔍 Anticipation")
        hausse = st.slider("Augmentation de la demande (%)", 0, 100, 0) / 100
        retard = st.number_input("Retard logistique port (Jours)", value=0)

    # Données simulées d'inventaire
    data_wms = {
        'SKU': ['REF-MAI-01', 'REF-COT-02', 'REF-SOJ-03', 'REF-CAJ-04', 'REF-CIM-05'],
        'Désignation': ['Maïs Grain', 'Coton Fibre', 'Soja Bio', 'Cajou Brut', 'Ciment Sac'],
        'Prix': [25000, 45000, 30000, 55000, 5000],
        'Stock_Physique': [450, 120, 800, 50, 2500],
        'Vente_Moy_J': [15, 5, 25, 2, 150]
    }
    df = pd.DataFrame(data_wms)

    # Calculs opérationnels
    df['Besoin_J'] = df['Vente_Moy_J'] * (1 + hausse)
    df['Seuil_Alerte'] = (df['Besoin_J'] * (14 + retard)) + 50
    df['Couverture_Jours'] = (df['Stock_Physique'] / df['Besoin_J']).astype(int)
    df['Valeur_Risque'] = df.apply(lambda x: (x['Besoin_J'] * x['Prix'] * 7) if x['Stock_Physique'] <= x['Seuil_Alerte'] else 0, axis=1)

    # Dashboard
    k1, k2, k3 = st.columns(3)
    k1.metric("Valeur de l'Inventaire", f"{(df['Stock_Physique']*df['Prix']).sum():,.0f} FCFA")
    k2.metric("Valeur en Risque", f"{df['Valeur_Risque'].sum():,.0f} FCFA", delta_color="inverse")
    k3.metric("Ruptures Identifiées", len(df[df['Stock_Physique'] <= df['Seuil_Alerte']]))

    st.subheader("📋 1. État Global de l'Inventaire")
    
    def get_status(row):
        if row['Stock_Physique'] <= 0: return "🚫 RUPTURE"
        if row['Stock_Physique'] <= row['Seuil_Alerte']: return "🔴 CRITIQUE"
        return "🟢 OPTIMAL"
    df['Statut'] = df.apply(get_status, axis=1)

    st.dataframe(df[['SKU', 'Désignation', 'Stock_Physique', 'Couverture_Jours', 'Seuil_Alerte', 'Statut']], use_container_width=True)

    # Plan de réapprovisionnement
    st.header("🛒 3. Plan de Réapprovisionnement Automatique")
    df_reap = df[df['Stock_Physique'] <= df['Seuil_Alerte']].copy()
    if not df_reap.empty:
        df_reap['Qte_Suggérée'] = (df_reap['Besoin_J'] * 30).astype(int)
        st.table(df_reap[['SKU', 'Désignation', 'Stock_Physique', 'Qte_Suggérée']])
        csv = df_reap.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger l'Ordre d'Achat", csv, "ordre_achat.csv", "text/csv")
    else:
        st.success("✅ Niveaux de stock optimaux.")

    # Graphique de répartition
    df['Valeur_Total'] = df['Stock_Physique'] * df['Prix']
    fig = px.pie(df, values='Valeur_Total', names='SKU', title="Répartition de la Valeur du Stock")
    st.plotly_chart(fig, use_container_width=True)
    

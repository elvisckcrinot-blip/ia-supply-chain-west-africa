import streamlit as st
import sys
import os

# --- FIX IMPORTATION : Permet de trouver helpers.py à la racine ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime
import pandas as pd
import plotly.express as px
from helpers import get_data, apply_ui_theme  # Importation des outils SQL et UI

# Vos fonctions académiques (MIT SC0x / SC1x)
try:
    from models.mit_calculations import calcul_cout_transport, calcul_rentabilite_flotte
except ImportError:
    def calcul_cout_transport(d, c, p, f): return int((d*(c/100)*p)+f), int(d*0.12)
    def calcul_rentabilite_flotte(cu, t, n): return (t - cu) * n * 360

# --- STYLE ET UI ---
apply_ui_theme()

st.markdown('<h1 style="font-family:Syne; color:#ffad1f; font-size:32px; font-weight:800;">🚛 Pilotage Transport (TMS · Live Sync)</h1>', unsafe_allow_html=True)

# --- INITIALISATION SESSION (Pour le docking local) ---
if 'historique_docking' not in st.session_state:
    st.session_state.historique_docking = []

tab1, tab2, tab3 = st.tabs(["💰 Business Plan & ROI", "⚓ Docking GDIZ", "📍 Tracking Corridor"])

# --- ONGLET 1 : STRATÉGIE & RENTABILITÉ ---
with tab1:
    st.subheader("📊 Modélisation du Centre de Profit")
    
    # RÉCUPÉRATION DE LA FLOTTE RÉELLE DEPUIS NEON
    df_flotte = get_data("SELECT * FROM flotte_vehicules")
    n_camions_db = len(df_flotte) if df_flotte is not None else 15
    
    c_in, c_res = st.columns([1, 1.2])

    with c_in:
        st.info("Variables de Flotte (Live)")
        tarif_client = st.number_input("Tarif Client (FCFA/Trajet)", value=650000)
        nbre_camions = st.slider("Flotte active / Jour", 1, 100, n_camions_db)
        dist_axe = st.number_input("Distance Moyenne (km)", value=720)
        conso = st.number_input("Conso (L/100km)", value=35)
        prix_gazole = st.number_input("Prix Gazole (FCFA/L)", value=700)
        fixes = st.number_input("Charges fixes / Trajet", value=85000)

    with c_res:
        cout_revient, co2 = calcul_cout_transport(dist_axe, conso, prix_gazole, fixes)
        profit_annuel = calcul_rentabilite_flotte(cout_revient, tarif_client, nbre_camions)
        
        st.markdown(f"""
            <div style="background: rgba(255,173,31,0.03); border: 1px solid rgba(255,173,31,0.15); border-radius: 12px; padding: 20px; text-align:center; margin-bottom:20px;">
                <small>PROFIT NET ANNUEL ESTIMÉ (360j)</small><br>
                <span style="font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; color: #ffad1f;">{profit_annuel:,.0f} FCFA</span>
            </div>
        """, unsafe_allow_html=True)
        
        k1, k2 = st.columns(2)
        k1.metric("Coût de Revient", f"{cout_revient:,.0f} FCFA")
        marge = tarif_client - cout_revient
        k2.metric("Marge / Trajet", f"{marge:,.0f} FCFA", delta=f"{(marge/tarif_client*100):.1f}%")
        
        df_costs = pd.DataFrame({
            'Poste': ['Diesel', 'Fixes', 'Marge'],
            'Valeur': [(dist_axe*conso/100*prix_gazole), fixes, marge]
        })
        fig = px.pie(df_costs, values='Valeur', names='Poste', hole=.3, title="Structure du Tarif")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=250)
        st.plotly_chart(fig, use_container_width=True)

# --- ONGLET 2 : DOCKING GDIZ ---
with tab2:
    st.subheader("⚓ Opérations en Zone Industrielle")
    with st.expander("➕ Enregistrer une nouvelle affectation"):
        with st.form("docking"):
            f1, f2, f3 = st.columns(3)
            liste_immat = df_flotte['immatriculation'].tolist() if df_flotte is not None else ["RB 0001"]
            immat = f1.selectbox("Camion", liste_immat)
            march = f2.selectbox("Fret", ["Fibre de Coton", "Noix de Cajou", "Soja", "Maïs", "Intrants"])
            quai_sel = f3.selectbox("Quai", [f"Quai {i}" for i in "ABCDEF"])
            op_type = st.radio("Mouvement", ["Chargement", "Déchargement"], horizontal=True)
            if st.form_submit_button("VALIDER"):
                new_entry = {"Heure": datetime.datetime.now().strftime("%H:%M"), "Camion": immat, "Marchandise": march, "Quai": quai_sel, "Opération": op_type}
                st.session_state.historique_docking.insert(0, new_entry)
                st.success(f"Affectation de {immat} enregistrée.")

    st.markdown("### Registre de Quai (Temps Réel)")
    st.dataframe(pd.DataFrame(st.session_state.historique_docking), use_container_width=True)

# --- ONGLET 3 : TRACKING & HISTORIQUE DES MISSIONS ---
with tab3:
    st.subheader("📍 Monitoring du Corridor & Missions")
    
    df_missions = get_data("SELECT * FROM historique_trajets ORDER BY date_depart DESC LIMIT 10")
    
    if df_missions is not None and not df_missions.empty:
        st.write("**Dernières missions planifiées par l'Optimizer :**")
        st.dataframe(df_missions[['destination', 'cout_estime', 'statut_livraison', 'date_depart']], use_container_width=True)
    
    st.divider()
    villes_corridor = ["Cotonou", "GDIZ", "Bohicon", "Dassa", "Parakou", "Kandi", "Malanville"]
    c_track1, c_track2 = st.columns(2)
    pos = c_track1.select_slider("Position du convoi test", options=villes_corridor, value="GDIZ")
    statut = c_track2.selectbox("Statut", ["En Transit", "Alerte Incident", "Livraison Effectuée"])

    color_map = {"En Transit": "#ffad1f", "Alerte Incident": "#ff4b4b", "Livraison Effectuée": "#5fc385"}
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border-left: 5px solid {color_map[statut]}; border-radius: 12px; padding: 25px;">
            <p style="margin:0; font-size:12px; color:#7a92b0;">SUIVI TEMPS RÉEL</p>
            <h3 style="margin:5px 0;">📍 {pos.upper()}</h3>
            <span style="padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; background:{color_map[statut]}; color:#0a1628;">{statut.upper()}</span>
        </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("WA Logistics Hub · Base de données : Neon PostgreSQL · Référentiel MIT CTL")
    

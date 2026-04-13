import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
# Vos fonctions académiques (MIT SC0x / SC1x)
try:
    from models.mit_calculations import calcul_cout_transport, calcul_rentabilite_flotte
except ImportError:
    # Fallback pour démonstration
    def calcul_cout_transport(d, c, p, f): return int((d*(c/100)*p)+f), int(d*0.12)
    def calcul_rentabilite_flotte(cu, t, n): return (t - cu) * n * 360

# --- STYLE ET UI ---
st.markdown("""
<style>
    .main-title { font-family: 'Syne', sans-serif; color: #ffad1f; font-size: 32px; font-weight: 800; }
    .tms-card { background: rgba(255,173,31,0.03); border: 1px solid rgba(255,173,31,0.15); border-radius: 12px; padding: 20px; }
    .tms-val { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; color: #ffad1f; }
    .status-badge { padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🚛 Pilotage Transport (TMS)</h1>', unsafe_allow_html=True)

# --- INITIALISATION SESSION ---
if 'historique_docking' not in st.session_state:
    st.session_state.historique_docking = [
        {"Heure": "08:30", "Camion": "RB 1245", "Marchandise": "Coton", "Quai": "Quai A", "Opération": "Chargement"},
        {"Heure": "09:15", "Camion": "RB 8892", "Marchandise": "Soja", "Quai": "Quai C", "Opération": "Déchargement"}
    ]

tab1, tab2, tab3 = st.tabs(["💰 Business Plan & ROI", "⚓ Docking GDIZ", "📍 Tracking Corridor"])

# --- ONGLET 1 : STRATÉGIE & RENTABILITÉ ---
with tab1:
    st.subheader("📊 Modélisation du Centre de Profit")
    c_in, c_res = st.columns([1, 1.2])

    with c_in:
        st.info("Variables de Flotte")
        tarif_client = st.number_input("Tarif Client (FCFA/Trajet)", value=650000)
        nbre_camions = st.slider("Flotte active / Jour", 1, 50, 15)
        dist_axe = st.number_input("Distance Moyenne (km)", value=720)
        conso = st.number_input("Conso (L/100km)", value=35)
        prix_gazole = st.number_input("Prix Gazole (FCFA/L)", value=700)
        fixes = st.number_input("Charges fixes / Trajet", value=85000)

    with c_res:
        cout_revient, co2 = calcul_cout_transport(dist_axe, conso, prix_gazole, fixes)
        profit_annuel = calcul_rentabilite_flotte(cout_revient, tarif_client, nbre_camions)
        
        st.markdown(f"""
            <div class="tms-card" style="text-align:center; margin-bottom:20px;">
                <small>PROFIT NET ANNUEL ESTIMÉ</small><br>
                <span class="tms-val">{profit_annuel:,.0f} FCFA</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Dashboard de KPIs
        k1, k2 = st.columns(2)
        k1.metric("Coût de Revient", f"{cout_revient:,.0f} FCFA")
        k2.metric("Marge / Trajet", f"{(tarif_client - cout_revient):,.0f} FCFA", delta=f"{((tarif_client-cout_revient)/tarif_client*100):.1f}%")
        
        # Petit graphique de structure de coût
        df_costs = pd.DataFrame({
            'Poste': ['Diesel', 'Fixes', 'Marge'],
            'Valeur': [(dist_axe*conso/100*prix_gazole), fixes, (tarif_client-cout_revient)]
        })
        fig = px.pie(df_costs, values='Valeur', names='Poste', hole=.3, title="Structure du Tarif Client")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=250)
        st.plotly_chart(fig, use_container_width=True)

# --- ONGLET 2 : DOCKING GDIZ ---
with tab2:
    st.subheader("⚓ Opérations en Zone Industrielle")
    with st.expander("➕ Enregistrer une nouvelle affectation"):
        with st.form("docking"):
            f1, f2, f3 = st.columns(3)
            immat = f1.text_input("Immatriculation", "RB ")
            march = f2.selectbox("Fret", ["Fibre de Coton", "Noix de Cajou", "Soja", "Maïs", "Intrants"])
            quai_sel = f3.selectbox("Quai", [f"Quai {i}" for i in "ABCDEF"])
            op_type = st.radio("Mouvement", ["Chargement", "Déchargement"], horizontal=True)
            if st.form_submit_button("VALIDER"):
                new_entry = {
                    "Heure": datetime.datetime.now().strftime("%H:%M"),
                    "Camion": immat, "Marchandise": march, "Quai": quai_sel, "Opération": op_type
                }
                st.session_state.historique_docking.insert(0, new_entry)
                st.rerun()

    st.markdown("### Registre de Quai (Temps Réel)")
    df_dock = pd.DataFrame(st.session_state.historique_docking)
    st.dataframe(df_dock, use_container_width=True)

# --- ONGLET 3 : TRACKING & CORRIDOR ---
with tab3:
    st.subheader("📍 Monitoring de l'Axe Nord")
    
    villes_corridor = ["Cotonou (Port)", "GDIZ (Glo-Djigbé)", "Bohicon", "Dassa", "Parakou", "Kandi", "Malanville"]
    
    c_track1, c_track2 = st.columns(2)
    pos = c_track1.select_slider("Position actuelle du convoi", options=villes_corridor, value="Bohicon")
    statut = c_track2.selectbox("Statut Opérationnel", ["En Transit", "Alerte Incident", "Livraison Effectuée"])

    color_map = {"En Transit": "#ffad1f", "Alerte Incident": "#ff4b4b", "Livraison Effectuée": "#5fc385"}
    
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border-left: 5px solid {color_map[statut]}; border-radius: 12px; padding: 25px; margin-top:10px;">
            <p style="margin:0; font-size:12px; color:#7a92b0;">SUIVI CONVOI STRATÉGIQUE</p>
            <h3 style="margin:5px 0;">📍 {pos.upper()}</h3>
            <span class="status-badge" style="background:{color_map[statut]}; color:#0a1628;">{statut.upper()}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Simulation de barre de progression
    idx = villes_corridor.index(pos)
    progress = (idx / (len(villes_corridor)-1))
    st.write("")
    st.progress(progress)
    st.caption(f"Progression sur le corridor : {int(progress*100)}%")

# FOOTER
st.divider()
st.caption("WA Logistics Hub · TMS Core · Powered by PuLP & MIT MicroMasters Metrics")
         

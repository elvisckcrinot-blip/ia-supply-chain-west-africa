import streamlit as st
import pulp
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from helpers import save_optimization_result, apply_ui_theme  # Import de la fonction de sauvegarde

# --- CONFIGURATION ET STYLE ---
apply_ui_theme()

st.markdown("""
<style>
    .main-title { font-family: 'Syne', sans-serif; color: #5fc385; font-size: 32px; font-weight: 800; }
    .opti-card { background: rgba(95,195,133,0.05); border: 1px solid rgba(95,195,133,0.2); border-radius: 12px; padding: 20px; }
    .six-sigma-badge { background: #5fc385; color: #0a1628; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-bottom: 10px; display: inline-block;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🎯 Network Optimizer (SC1x + Six Sigma)</h1>', unsafe_allow_html=True)
st.markdown('<span class="six-sigma-badge">MOTEUR CBC AVEC PÉNALITÉ DE VARIABILITÉ</span>', unsafe_allow_html=True)

# --- 1. BASE DE DONNÉES AVEC INDICE SIGMA ---
database_villes = {
    "Parakou": {"dist": 410, "sigma": 1.2}, 
    "Malanville": {"dist": 730, "sigma": 2.8}, 
    "Bohicon": {"dist": 110, "sigma": 1.0}, 
    "Dassa": {"dist": 190, "sigma": 1.5}, 
    "Natitingou": {"dist": 480, "sigma": 2.1},
    "Djougou": {"dist": 440, "sigma": 1.9}
}

col_param1, col_param2 = st.columns(2)

with col_param1:
    st.info("⛽ Paramètres Financiers")
    prix_diesel = st.number_input("Prix Diesel (FCFA/L)", value=700)
    conso_moy = st.number_input("Consommation (L/100km)", value=35)
    charges_fixes = st.number_input("Charges fixes/trajet (FCFA)", value=85000)

with col_param2:
    st.info("📊 Stratégie Qualité (Six Sigma)")
    poids_sigma = st.slider("Poids de la variabilité (Impact Risque)", 0, 100000, 25000)
    produit_select = st.selectbox("Type de fret", ["Fibre de Coton", "Noix de Cajou transformée", "Soja Bio"])
    tonnage_unitaire = {"Fibre de Coton": 22, "Noix de Cajou transformée": 28, "Soja Bio": 30}[produit_select]

st.divider()

# --- 2. SÉLECTION ET DEMANDE ---
villes_selectionnees = st.multiselect("Destinations à optimiser", options=list(database_villes.keys()), default=["Parakou", "Malanville"])

demandes = {}
if villes_selectionnees:
    cols = st.columns(len(villes_selectionnees))
    for i, ville in enumerate(villes_selectionnees):
        demandes[ville] = cols[i].number_input(f"Demande {ville} (T)", value=100, step=10)

    total_camions_dispo = st.slider("Flotte totale disponible (GDIZ)", 1, 100, 30)

    # --- 3. LOGIQUE D'OPTIMISATION ---
    if st.button("🚀 LANCER L'OPTIMISATION ROBUSTE"):
        model = pulp.LpProblem("Optimization_Fret_Robust", pulp.LpMinimize)
        vars_camions = {v: pulp.LpVariable(f"Cam_{v}", lowBound=0, cat='Integer') for v in villes_selectionnees}

        couts_trajets_réels = {}
        couts_robustes = {}
        for v in villes_selectionnees:
            dist = database_villes[v]["dist"]
            sigma = database_villes[v]["sigma"]
            cout_standard = (dist * (conso_moy / 100) * prix_diesel) + charges_fixes
            couts_trajets_réels[v] = cout_standard
            couts_robustes[v] = cout_standard + (sigma * poids_sigma)

        model += pulp.lpSum([vars_camions[v] * couts_robustes[v] for v in villes_selectionnees])
        model += pulp.lpSum([vars_camions[v] for v in villes_selectionnees]) <= total_camions_dispo
        for v in villes_selectionnees:
            model += vars_camions[v] * tonnage_unitaire >= demandes[v]

        model.solve(pulp.PULP_CBC_CMD(msg=0))

        # --- 4. RÉSULTATS & SAUVEGARDE ---
        if pulp.LpStatus[model.status] == 'Optimal':
            st.success("✅ Solution optimale trouvée et sauvegardée en base de données.")
            
            # --- LOGIQUE DE SAUVEGARDE POSTGRESQL ---
            for v in villes_selectionnees:
                n_camions = int(vars_camions[v].varValue)
                if n_camions > 0:
                    # Enregistrement dans la table historique_trajets
                    save_optimization_result(
                        camion_id=1, 
                        destination=v,
                        cout_estime=couts_trajets_réels[v] * n_camions,
                        statut="Planifié (Optimisé)"
                    )
            
            # --- AFFICHAGE DASHBOARD ---
            res_col1, res_col2 = st.columns([1, 2])
            with res_col1:
                st.markdown("### 🚛 Allocation Flotte")
                for v in villes_selectionnees:
                    val = int(vars_camions[v].varValue)
                    if val > 0: st.write(f"**{v}** : {val} camions")
                
                total_cout_reel = sum([vars_camions[v].varValue * couts_trajets_réels[v] for v in villes_selectionnees])
                st.markdown(f'<div class="opti-card"><b>Coût Opérationnel Total :</b><br><span style="font-size:20px; color:#5fc385;">{total_cout_reel:,.0f} FCFA</span></div>', unsafe_allow_html=True)

            with res_col2:
                fig = go.Figure(data=[
                    go.Bar(name='Capacité Allouée', x=villes_selectionnees, y=[vars_camions[v].varValue * tonnage_unitaire for v in villes_selectionnees], marker_color='#5fc385'),
                    go.Bar(name='Demande Client', x=villes_selectionnees, y=[demandes[v] for v in villes_selectionnees], marker_color='#3e4451')
                ])
                fig.update_layout(title="Adéquation Capacité / Demande", barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("❌ Échec de l'optimisation : Ressources insuffisantes.")
else:
    st.warning("Sélectionnez des destinations pour activer le moteur CBC.")

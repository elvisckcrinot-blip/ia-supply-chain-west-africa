import streamlit as st
import pulp
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURATION ET STYLE ---
st.set_page_config(page_title="Smart Network Optimizer", layout="wide")

st.markdown("""
<style>
    .main-title { font-family: 'Syne', sans-serif; color: #5fc385; font-size: 32px; font-weight: 800; }
    .opti-card { background: rgba(95,195,133,0.05); border: 1px solid rgba(95,195,133,0.2); border-radius: 12px; padding: 20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🎯 Optimisation du Réseau (Dynamique)</h1>', unsafe_allow_html=True)

# --- 1. PARAMÈTRES ET RÉFÉRENTIEL VILLES ---
# Base de données des distances depuis GDIZ
database_villes = {
    "Parakou": 410, 
    "Malanville": 730, 
    "Bohicon": 110, 
    "Dassa": 190, 
    "Natitingou": 480,
    "Djougou": 440
}

col_param1, col_param2 = st.columns(2)

with col_param1:
    st.info("⛽ Données de Coûts")
    prix_diesel = st.number_input("Prix Diesel (FCFA/L)", value=700, min_value=1)
    conso_moy = st.number_input("Consommation (L/100km)", value=35, min_value=1)
    charges_fixes = st.number_input("Charges fixes/trajet (FCFA)", value=85000)

with col_param2:
    st.info("📦 Marchandise GDIZ")
    produit_select = st.selectbox("Type de fret", ["Fibre de Coton", "Noix de Cajou transformée", "Soja Bio"])
    dict_tonnage = {"Fibre de Coton": 22, "Noix de Cajou transformée": 28, "Soja Bio": 30}
    tonnage_unitaire = dict_tonnage[produit_select]
    st.write(f"Capacité : **{tonnage_unitaire} T / Camion**")

st.divider()

# --- 2. SÉLECTION DYNAMIQUE DES DESTINATIONS ---
st.subheader("📍 Planification des Destinations")
villes_selectionnees = st.multiselect(
    "Choisir les villes de destination", 
    options=list(database_villes.keys()),
    default=["Parakou", "Malanville"]
)

demandes = {}
if villes_selectionnees:
    cols = st.columns(len(villes_selectionnees))
    for i, ville in enumerate(villes_selectionnees):
        demandes[ville] = cols[i].number_input(f"Demande {ville} (T)", value=100, min_value=0)

    total_camions_dispo = st.slider("Flotte disponible (Camions)", 1, 100, 30)

    # --- 3. LOGIQUE D'OPTIMISATION (PuLP Dynamique) ---
    if st.button("🚀 EXÉCUTER L'ALGORITHME"):
        if prix_diesel > 0 and conso_moy > 0:
            model = pulp.LpProblem("Minimisation_Couts_Dynamique", pulp.LpMinimize)
            
            # Variables de décision créées dynamiquement
            vars_camions = {v: pulp.LpVariable(f"Camions_{v}", lowBound=0, cat='Integer') for v in villes_selectionnees}

            # Fonction Objectif : Somme (Camions * Coût par trajet)
            couts_trajets = {}
            for v in villes_selectionnees:
                dist = database_villes[v]
                couts_trajets[v] = (dist * (conso_moy / 100) * prix_diesel) + charges_fixes
            
            model += pulp.lpSum([vars_camions[v] * couts_trajets[v] for v in villes_selectionnees])

            # Contraintes
            model += pulp.lpSum([vars_camions[v] for v in villes_selectionnees]) <= total_camions_dispo, "Capacite_Totale"
            for v in villes_selectionnees:
                model += vars_camions[v] * tonnage_unitaire >= demandes[v], f"Satisfaction_{v}"

            model.solve()

            # --- 4. AFFICHAGE DES RÉSULTATS ---
            st.success(f"Optimisation terminée (Statut : {pulp.LpStatus[model.status]})")
            
            res_col1, res_col2 = st.columns([1, 2])
            with res_col1:
                for v in villes_selectionnees:
                    st.metric(f"Vers {v}", f"{int(vars_camions[v].varValue)} Camions")
                
                total_final = pulp.value(model.objective)
                st.markdown(f'<div class="opti-card"><b>Coût Total :</b> {total_final:,.0f} FCFA</div>', unsafe_allow_html=True)

            with res_col2:
                fig = go.Figure(data=[
                    go.Bar(name='Alloué (T)', x=villes_selectionnees, y=[vars_camions[v].varValue * tonnage_unitaire for v in villes_selectionnees], marker_color='#5fc385'),
                    go.Bar(name='Requis (T)', x=villes_selectionnees, y=[demandes[v] for v in villes_selectionnees], marker_color='#7a92b0')
                ])
                st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Veuillez sélectionner au moins une ville de destination.")
    

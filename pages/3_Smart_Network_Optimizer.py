import streamlit as st
import pulp
import pandas as pd
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Smart Network Optimizer", layout="wide")

st.markdown("""
<style>
    .main-title { font-family: 'Syne', sans-serif; color: #5fc385; font-size: 32px; font-weight: 800; }
    .opti-card { background: rgba(95,195,133,0.05); border: 1px solid rgba(95,195,133,0.2); border-radius: 12px; padding: 20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Optimisation du Réseau (MIT SCM Model)</h1>', unsafe_allow_html=True)
st.write("Ce module utilise la **Programmation Linéaire** pour minimiser les coûts de transport GDIZ vers le Nord.")

# --- 1. PARAMÈTRES RÉCUPÉRÉS ET SÉLECTION PRODUIT ---
col_param1, col_param2 = st.columns(2)

with col_param1:
    st.info("Données de Coûts (GDIZ)")
    prix_diesel = st.number_input("Prix Diesel (FCFA/L)", value=700)
    conso_moy = st.number_input("Consommation moyenne (L/100km)", value=35)
    charges_fixes = st.number_input("Charges fixes/trajet (FCFA)", value=85000)

with col_param2:
    st.info("Stratégie de Chargement GDIZ")
    # Ajout de la dimension produit pour le dossier MIT
    produit_select = st.selectbox("Type de marchandise stratégique", 
                                  ["Fibre de Coton", "Noix de Cajou transformée", "Soja Bio"])
    
    # Facteurs de conversion Tonnes/Camion (Logique de densité de fret)
    dict_tonnage = {"Fibre de Coton": 22, "Noix de Cajou transformée": 28, "Soja Bio": 30}
    tonnage_unitaire = dict_tonnage[produit_select]
    
    st.write(f"Capacité estimée : **{tonnage_unitaire} Tonnes / Camion**")

st.divider()

# --- 2. CAPACITÉS ET DEMANDE EN TONNES ---
col_input1, col_input2 = st.columns(2)

with col_input1:
    total_camions_dispo = st.slider("Flotte totale disponible à la GDIZ (Camions)", 1, 100, 30)
    capacite_totale_tonnes = total_camions_dispo * tonnage_unitaire
    st.write(f"Capacité totale de transport : {capacite_totale_tonnes} Tonnes")

with col_input2:
    demande_pko_t = st.number_input("Demande Parakou (Tonnes)", value=200)
    demande_mln_t = st.number_input("Demande Malanville (Tonnes)", value=400)

# --- 3. LOGIQUE D'OPTIMISATION ---
dist_parakou = 410
dist_malanville = 730

def estimer_cout(distance):
    cout_diesel = (distance * (conso_moy / 100)) * prix_diesel
    return cout_diesel + charges_fixes

cost_pko = estimer_cout(dist_parakou)
cost_mln = estimer_cout(dist_malanville)

if st.button("EXECUTER L'ALGORITHME D'OPTIMISATION"):
    # Initialisation
    model = pulp.LpProblem("Minimisation_Couts_Transport", pulp.LpMinimize)

    # Variables : Nombre de camions (Entiers car on ne divise pas un camion)
    x_pko = pulp.LpVariable("Camions_Parakou", lowBound=0, cat='Integer')
    x_mln = pulp.LpVariable("Camions_Malanville", lowBound=0, cat='Integer')

    # Objectif
    model += (x_pko * cost_pko) + (x_mln * cost_mln), "Cout_Total"

    # Contraintes (Conversion Tonnes vers Camions)
    model += x_pko + x_mln <= total_camions_dispo, "Capacite_Flotte_GDIZ"
    model += x_pko * tonnage_unitaire >= demande_pko_t, "Satisfaction_Parakou"
    model += x_mln * tonnage_unitaire >= demande_mln_t, "Satisfaction_Malanville"

    model.solve()

    # --- 4. AFFICHAGE DES RÉSULTATS ---
    st.markdown("---")
    res_col1, res_col2 = st.columns([1, 2])

    with res_col1:
        st.write("### Plan d'Allocation")
        st.success(f"Statut : {pulp.LpStatus[model.status]}")
        st.metric(f"Camions {produit_select} -> Parakou", int(x_pko.varValue))
        st.metric(f"Camions {produit_select} -> Malanville", int(x_mln.varValue))
        
        total_final = pulp.value(model.objective)
        st.markdown(f"""
            <div class="opti-card">
                <div style="color: #7a92b0; font-size: 14px;">COUT OPERATIONNEL OPTIMISE</div>
                <div style="font-size: 24px; font-weight: 800; color: #5fc385;">{total_final:,.0f} FCFA</div>
                <div style="font-size: 11px; color: #7a92b0; margin-top:5px;">Algorithme : Mixed-Integer Linear Programming</div>
            </div>
        """, unsafe_allow_html=True)

    with res_col2:
        st.write("### Comparaison des Flux (Tonnes)")
        fig = go.Figure(data=[
            go.Bar(name='Capacité Allouée (T)', x=['Parakou', 'Malanville'], 
                   y=[x_pko.varValue * tonnage_unitaire, x_mln.varValue * tonnage_unitaire], marker_color='#5fc385'),
            go.Bar(name='Demande Requise (T)', x=['Parakou', 'Malanville'], 
                   y=[demande_pko_t, demande_mln_t], marker_color='#7a92b0')
        ])
        fig.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

st.sidebar.warning("Ce module utilise le solveur CBC intégré à PuLP pour résoudre un problème de transport à variables entières.")
    

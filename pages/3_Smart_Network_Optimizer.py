import streamlit as st
import pulp
import pandas as pd
import plotly.graph_objects as go

# Configuration identique à ton style
st.set_page_config(page_title="Smart Network Optimizer", layout="wide")

st.markdown("""
<style>
    .main-title { font-family: 'Syne', sans-serif; color: #5fc385; font-size: 32px; font-weight: 800; }
    .opti-card { background: rgba(95,195,133,0.05); border: 1px solid rgba(95,195,133,0.2); border-radius: 12px; padding: 20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🎯 Optimisation du Réseau (MIT SCM Model)</h1>', unsafe_allow_html=True)
st.write("Ce module utilise la **Programmation Linéaire** pour minimiser les coûts de transport GDIZ vers le Nord.")

# --- 1. PARAMÈTRES RÉCUPÉRÉS DE TON TMS ---
col_param1, col_param2 = st.columns(2)

with col_param1:
    st.info("Données de Coûts (GDIZ)")
    prix_diesel = st.number_input("Prix Diesel (FCFA/L)", value=700)
    conso_moy = st.number_input("Consommation moyenne (L/100km)", value=35)
    charges_fixes = st.number_input("Charges fixes/trajet (FCFA)", value=85000)

with col_param2:
    st.info("Capacités et Demande")
    total_camions_dispo = st.slider("Total camions disponibles à la GDIZ", 1, 100, 30)
    # Simulation de demande pour deux hubs majeurs
    demande_parakou = st.number_input("Besoin à Parakou (Camions)", value=10)
    demande_malanville = st.number_input("Besoin à Malanville (Camions)", value=15)

# --- 2. LOGIQUE D'OPTIMISATION (Cœur du projet) ---
# Calcul du coût par trajet basé sur ton modèle initial
dist_parakou = 410
dist_malanville = 730

def estimer_cout(distance):
    cout_diesel = (distance * (conso_moy / 100)) * prix_diesel
    return cout_diesel + charges_fixes

cost_pko = estimer_cout(dist_parakou)
cost_mln = estimer_cout(dist_malanville)

if st.button("🚀 EXÉCUTER L'ALGORITHME D'OPTIMISATION"):
    # Initialisation du Problème PuLP
    model = pulp.LpProblem("Minimisation_Couts_Transport", pulp.LpMinimize)

    # Variables de décision (Nombre de camions à envoyer)
    x_pko = pulp.LpVariable("Camions_Parakou", lowBound=0, cat='Integer')
    x_mln = pulp.LpVariable("Camions_Malanville", lowBound=0, cat='Integer')

    # Fonction Objectif
    model += (x_pko * cost_pko) + (x_mln * cost_mln), "Cout_Total"

    # Contraintes
    model += x_pko + x_mln <= total_camions_dispo, "Capacite_GDIZ"
    model += x_pko >= demande_parakou, "Satisfaction_Parakou"
    model += x_mln >= demande_malanville, "Satisfaction_Malanville"

    model.solve()

    # --- 3. AFFICHAGE DES RÉSULTATS ---
    st.markdown("---")
    res_col1, res_col2 = st.columns([1, 2])

    with res_col1:
        st.write("### Plan d'Allocation")
        st.success(f"Statut : {pulp.LpStatus[model.status]}")
        st.metric("Camions vers Parakou", int(x_pko.varValue))
        st.metric("Camions vers Malanville", int(x_mln.varValue))
        
        total_final = pulp.value(model.objective)
        st.markdown(f"""
            <div class="opti-card">
                <div style="color: #7a92b0; font-size: 14px;">COÛT OPÉRATIONNEL OPTIMISÉ</div>
                <div style="font-size: 24px; font-weight: 800; color: #5fc385;">{total_final:,.0f} FCFA</div>
            </div>
        """, unsafe_allow_html=True)

    with res_col2:
        st.write("### Comparaison des Flux")
        fig = go.Figure(data=[
            go.Bar(name='Allocation Optimale', x=['Parakou', 'Malanville'], y=[x_pko.varValue, x_mln.varValue], marker_color='#5fc385'),
            go.Bar(name='Demande Minimale', x=['Parakou', 'Malanville'], y=[demande_parakou, demande_malanville], marker_color='#7a92b0')
        ])
        fig.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

st.sidebar.warning("🔬 Ce module utilise le solveur CBC intégré à PuLP pour résoudre un problème de transport à variables entières.")


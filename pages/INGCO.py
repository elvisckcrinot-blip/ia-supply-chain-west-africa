import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURATION
st.set_page_config(page_title="INGCO - Stratégie MIT", layout="wide")
st.title("📦 INGCO BÉNIN : Pilotage & Simulation")

# 2. IMPORTATION & DONNÉES
st.sidebar.header("📂 Données Réelles")
uploaded_file = st.sidebar.file_uploader("Charger Excel INGCO", type=["xlsx", "csv"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
else:
    # Simulation par défaut (500 articles)
    data = {
        'ref_sku': [f'ING-REF-{i}' for i in range(1, 501)],
        'designation': [f'Outil {i}' for i in range(1, 501)],
        'prix_usine': [150000 if i % 10 == 0 else 12000 for i in range(1, 501)],
        'vente_moy_jour': [2 if i % 10 == 0 else 5 for i in range(1, 501)],
        'lead_time_jours': [60] * 500,
        'stock_physique': [140 if i % 10 == 0 else 300 for i in range(1, 501)],
        'stock_securite': [30] * 500
    }
    df = pd.DataFrame(data)

# 3. 🕹️ MODULE DE SIMULATION (L'intelligence ajoutée)
st.sidebar.markdown("---")
st.sidebar.header("🕹️ Simulateur de Scénarios")
facteur_demande = st.sidebar.slider("Hausse de la demande (%)", 0, 100, 0) / 100
retard_port = st.sidebar.number_input("Retard au Port de Cotonou (jours)", 0, 60, 0)

# Calcul des impacts
df['ROP_Actuel'] = (df['vente_moy_jour'] * df['lead_time_jours']) + df['stock_securite']
df['ROP_Simule'] = ((df['vente_moy_jour'] * (1 + facteur_demande)) * (df['lead_time_jours'] + retard_port)) + df['stock_securite']

df['Statut_Simule'] = df.apply(lambda x: '🔴 RISQUE' if x['stock_physique'] <= x['ROP_Simule'] else '🟢 OK', axis=1)

# 4. DASHBOARD VISUEL
col1, col2 = st.columns(2)
with col1:
    ruptures_simulees = len(df[df['Statut_Simule'] == '🔴 RISQUE'])
    st.metric("Alertes Scénario", ruptures_simulees, delta=f"{ruptures_simulees - len(df[df['stock_physique'] <= df['ROP_Actuel']])} nouvelles", delta_color="inverse")

with col2:
    valeur_risque = df[df['Statut_Simule'] == '🔴 RISQUE']['prix_usine'].sum()
    st.metric("Valeur CA en Risque", f"{valeur_risque:,.0f} FCFA")

st.subheader("📊 Comparaison : Stock Réel vs Besoin Simulé")
fig = px.scatter(df.head(50), x='ref_sku', y=['stock_physique', 'ROP_Simule'], 
                 title="Capacité de résistance du stock par article",
                 labels={'value': 'Quantité', 'variable': 'Indicateur'})
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df[['ref_sku', 'stock_physique', 'ROP_Actuel', 'ROP_Simule', 'Statut_Simule']], use_container_width=True)
        

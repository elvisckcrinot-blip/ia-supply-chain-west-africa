import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURATION
st.set_page_config(page_title="INGCO - Décisionnel MIT", layout="wide")
st.title("📦 INGCO BÉNIN : Pilotage & Commandes")

# 2. IMPORTATION & DONNÉES
st.sidebar.header("📂 Données Réelles")
uploaded_file = st.sidebar.file_uploader("Charger Excel INGCO", type=["xlsx", "csv"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
else:
    # Simulation automatique de 500 articles
    data = {
        'ref_sku': [f'ING-REF-{i}' for i in range(1, 501)],
        'designation': [f'Outil Pro {i}' for i in range(1, 501)],
        'prix_usine': [150000 if i % 10 == 0 else 12000 for i in range(1, 501)],
        'vol_unitaire_cbm': [0.15 if i % 10 == 0 else 0.01 for i in range(1, 501)],
        'vente_moy_jour': [2 if i % 10 == 0 else 5 for i in range(1, 501)],
        'lead_time_jours': [60] * 500,
        'stock_physique': [140 if i % 10 == 0 else 300 for i in range(1, 501)],
        'stock_securite': [30] * 500
    }
    df = pd.DataFrame(data)

# 3. 🕹️ MODULE DE SIMULATION
st.sidebar.markdown("---")
st.sidebar.header("🕹️ Simulateur de Scénarios")
facteur_demande = st.sidebar.slider("Hausse de la demande (%)", 0, 100, 0) / 100
retard_port = st.sidebar.number_input("Retard au Port de Cotonou (jours)", 0, 60, 0)

# Calculs MIT (SC1x)
df['ROP_Actuel'] = (df['vente_moy_jour'] * df['lead_time_jours']) + df['stock_securite']
df['ROP_Simule'] = ((df['vente_moy_jour'] * (1 + facteur_demande)) * (df['lead_time_jours'] + retard_port)) + df['stock_securite']
df['Statut_Simule'] = df.apply(lambda x: '🔴 RISQUE' if x['stock_physique'] <= x['ROP_Simule'] else '🟢 OK', axis=1)

# 4. DASHBOARD VISUEL
col1, col2 = st.columns(2)
with col1:
    ruptures = len(df[df['Statut_Simule'] == '🔴 RISQUE'])
    st.metric("Articles en Danger", ruptures, delta=f"{ruptures} alertes", delta_color="inverse")
with col2:
    val_risque = df[df['Statut_Simule'] == '🔴 RISQUE']['prix_usine'].sum()
    st.metric("CA Menacé (FCFA)", f"{val_risque:,.0f}")

st.subheader("📊 Résistance des stocks face au scénario")
fig = px.scatter(df.head(50), x='ref_sku', y=['stock_physique', 'ROP_Simule'], 
                 color_discrete_sequence=['#1f77b4', '#ff7f0e'])
st.plotly_chart(fig, use_container_width=True)

# 5. 📝 BON DE COMMANDE AUTOMATIQUE (Nouveau !)
st.markdown("---")
st.subheader("📝 Bon de Commande Suggéré")

# Calcul de la quantité nécessaire pour combler le risque + 30 jours de stock
df['Qte_a_Commander'] = df.apply(
    lambda x: max(0, int(x['ROP_Simule'] - x['stock_physique'] + (x['vente_moy_jour'] * 30))) 
    if x['Statut_Simule'] == '🔴 RISQUE' else 0, axis=1
)

bon_commande = df[df['Qte_a_Commander'] > 0][['ref_sku', 'designation', 'Qte_a_Commander', 'prix_usine', 'vol_unitaire_cbm']]

if not bon_commande.empty:
    # Calcul du volume total (Conteneur)
    vol_total = (bon_commande['Qte_a_Commander'] * bon_commande['vol_unitaire_cbm']).sum()
    st.info(f"🚢 Volume total de la commande : **{vol_total:.2f} m³** (Remplissage : {int((vol_total/33)*100)}% d'un conteneur 20ft)")
    
    csv = bon_commande.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Télécharger le Bon de Commande (CSV)", csv, "bon_commande_ingco.csv", "text/csv")
    st.table(bon_commande)
else:
    st.success("✅ Aucun besoin d'achat pour ce scénario.")
                       

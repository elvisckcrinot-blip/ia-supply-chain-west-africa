import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURATION
st.set_page_config(page_title="WMS Logistics - Warehouse Management System", layout="wide")
st.title("📦 WMS Logistics : Gestion d'Entrepôt & Optimisation")

# 2. IMPORTATION & DONNÉES (WMS Input)
st.sidebar.header("📂 WMS - Données Réelles")
uploaded_file = st.sidebar.file_uploader("Charger l'inventaire Excel", type=["xlsx", "csv"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
else:
    # Simulation automatique du stock (500 articles)
    data = {
        'ref_sku': [f'SKU-REF-{i}' for i in range(1, 501)],
        'designation': [f'Article Logistique {i}' for i in range(1, 501)],
        'prix_usine': [150000 if i % 10 == 0 else 12000 for i in range(1, 501)],
        'vol_unitaire_cbm': [0.15 if i % 10 == 0 else 0.01 for i in range(1, 501)],
        'vente_moy_jour': [2 if i % 10 == 0 else 5 for i in range(1, 501)],
        'lead_time_jours': [60] * 500,
        'stock_physique': [140 if i % 10 == 0 else 300 for i in range(1, 501)],
        'stock_securite': [30] * 500
    }
    df = pd.DataFrame(data)

# 3. 🕹️ WMS - MODULE DE SIMULATION STRATÉGIQUE
st.sidebar.markdown("---")
st.sidebar.header("🕹️ Simulateur de Scénarios")
facteur_demande = st.sidebar.slider("Hausse de la demande (%)", 0, 100, 0) / 100
retard_port = st.sidebar.number_input("Retard Logistique (jours)", 0, 60, 0)

# Calculs MIT (SC1x - Supply Chain Fundamentals)
df['ROP_Actuel'] = (df['vente_moy_jour'] * df['lead_time_jours']) + df['stock_securite']
df['ROP_Simule'] = ((df['vente_moy_jour'] * (1 + facteur_demande)) * (df['lead_time_jours'] + retard_port)) + df['stock_securite']
df['Statut_WMS'] = df.apply(lambda x: '🔴 RISQUE' if x['stock_physique'] <= x['ROP_Simule'] else '🟢 OK', axis=1)

# 4. WMS DASHBOARD VISUEL
col1, col2 = st.columns(2)
with col1:
    ruptures = len(df[df['Statut_WMS'] == '🔴 RISQUE'])
    st.metric("Alertes Stock (WMS)", ruptures, delta=f"{ruptures} critiques", delta_color="inverse")
with col2:
    val_risque = df[df['Statut_WMS'] == '🔴 RISQUE']['prix_usine'].sum()
    st.metric("Valeur du Stock en Risque (FCFA)", f"{val_risque:,.0f}")

st.subheader("📊 WMS - Analyse de Résistance du Stock")
fig = px.scatter(df.head(50), x='ref_sku', y=['stock_physique', 'ROP_Simule'], 
                 color_discrete_sequence=['#1f77b4', '#ff7f0e'],
                 labels={'value': 'Quantité', 'variable': 'Indicateurs'})
st.plotly_chart(fig, use_container_width=True)

# 5. 📝 WMS - PLAN DE RÉAPPROVISIONNEMENT AUTOMATIQUE
st.markdown("---")
st.subheader("📝 WMS - Bon de Commande Suggéré")

# Calcul de la quantité optimale (Q)
df['Qte_a_Commander'] = df.apply(
    lambda x: max(0, int(x['ROP_Simule'] - x['stock_physique'] + (x['vente_moy_jour'] * 30))) 
    if x['Statut_WMS'] == '🔴 RISQUE' else 0, axis=1
)

bon_commande = df[df['Qte_a_Commander'] > 0][['ref_sku', 'designation', 'Qte_a_Commander', 'prix_usine', 'vol_unitaire_cbm']]

if not bon_commande.empty:
    # Optimisation du transport (SC0x)
    vol_total = (bon_commande['Qte_a_Commander'] * bon_commande['vol_unitaire_cbm']).sum()
    st.info(f"🚢 WMS - Analyse Transport : Volume total **{vol_total:.2f} m³** (Remplissage : {int((vol_total/33)*100)}% d'un conteneur 20ft)")
    
    csv = bon_commande.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Télécharger l'Ordre d'Achat (WMS)", csv, "wms_purchase_order.csv", "text/csv")
    st.table(bon_commande)
else:
    st.success("✅ WMS : Les niveaux de stock sont optimaux pour ce scénario.")

st.success("🎯 Warehouse Management System Opérationnel - West Africa Logistics")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="WMS Logistics - Pilotage Flux", layout="wide", page_icon="📦")

st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #f1f3f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIQUE MÉTIER ET CALCULS DU RISQUE
def calculer_logistique(df, hausse_dem, ret_log, cout_com, taux_stock):
    df = df.copy()
    df['vente_moy_jour'] = df['vente_moy_jour'].replace(0, 0.001) 
    
    # Simulations de demande et délais
    df['Vente_Simulee'] = df['vente_moy_jour'] * (1 + hausse_dem)
    df['LeadTime_Total'] = df['lead_time_jours'] + ret_log
    
    # ROP & EOQ (Wilson)
    df['ROP_Calculé'] = (df['Vente_Simulee'] * df['LeadTime_Total']) + df['stock_securite']
    demande_annuelle = df['Vente_Simulee'] * 365
    df['EOQ_Wilson'] = np.sqrt((2 * demande_annuelle * cout_com) / (df['prix_usine'] * taux_stock)).replace([np.inf, -np.inf], 0).fillna(0).astype(int)
    
    # Analyse de Rupture
    df['Jours_Restants'] = (df['stock_physique'] / df['Vente_Simulee']).fillna(0).astype(int)
    df['Date_Rupture'] = [datetime.now() + timedelta(days=int(x)) if x < 1000 else datetime.now() + timedelta(days=1000) for x in df['Jours_Restants']]
    
    # VALORISATION DU RISQUE (NOUVEAU)
    df['Perte_CA_Jour'] = df['Vente_Simulee'] * df['prix_usine']
    # Si le stock est inférieur au ROP, on calcule le manque à gagner potentiel sur la période de retard
    df['Risque_Financier'] = df.apply(
        lambda x: x['Perte_CA_Jour'] * ret_log if x['stock_physique'] <= x['ROP_Calculé'] else 0, 
        axis=1
    )
    
    # Analyse ABC
    df['Valeur_Stock'] = df['stock_physique'] * df['prix_usine']
    df = df.sort_values(by='Valeur_Stock', ascending=False)
    df['Cumsum_Val'] = df['Valeur_Stock'].cumsum()
    total_val = df['Valeur_Stock'].sum() if df['Valeur_Stock'].sum() > 0 else 1
    df['Pct_Cumul'] = (df['Cumsum_Val'] / total_val) * 100
    df['Classe_ABC'] = df['Pct_Cumul'].apply(lambda x: 'A' if x <= 80 else ('B' if x <= 95 else 'C'))
    
    # Statuts
    def get_status(row):
        if row['stock_physique'] <= 0: return "🚫 RUPTURE"
        if row['stock_physique'] <= row['ROP_Calculé']: return "🔴 CRITIQUE"
        if row['stock_physique'] <= row['ROP_Calculé'] * 1.2: return "🟡 PRÉVENTIF"
        return "🟢 OPTIMAL"
    
    df['Statut'] = df.apply(get_status, axis=1)
    return df

# 3. INTERFACE (SIDEBAR)
st.sidebar.header("⚙️ Paramètres de Simulation")
uploaded_file = st.sidebar.file_uploader("Importer Inventaire", type=["xlsx", "csv"])

hausse_dem = st.sidebar.slider("Pic de Demande (%)", 0, 100, 0) / 100
ret_log = st.sidebar.number_input("Retard de Livraison (Jours)", 0, 90, 0)
c_com = st.sidebar.number_input("Coût de Commande (FCFA)", 1000, 100000, 15000)
t_pos = st.sidebar.slider("Taux de Possession Stock (%)", 5, 50, 15) / 100

if uploaded_file:
    df_input = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
else:
    data = {
        'ref_sku': [f'SKU-{i:03d}' for i in range(1, 101)],
        'designation': [f'Produit {i}' for i in range(1, 101)],
        'prix_usine': np.random.randint(1000, 50000, 100),
        'vol_unitaire_cbm': np.random.uniform(0.01, 0.3, 100),
        'vente_moy_jour': np.random.randint(1, 15, 100),
        'lead_time_jours': [45] * 100,
        'stock_physique': np.random.randint(0, 800, 100),
        'stock_securite': [50] * 100
    }
    df_input = pd.DataFrame(data)

df = calculer_logistique(df_input, hausse_dem, ret_log, c_com, t_pos)

# 4. DASHBOARD
st.title("📦 WMS : Pilotage & Performance Stocks")
st.markdown("---")

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Valeur Stock", f"{df['Valeur_Stock'].sum():,.0f} FCFA")
m2.metric("Ruptures (<7j)", len(df[df['Jours_Restants'] < 7]))
m3.metric("Commandes Critiques", len(df[df['Statut'] == "🔴 CRITIQUE"]))
m4.metric("Rotation Stock", f"{(df['Vente_Simulee'].sum()*365 / (df['stock_physique'].sum() if df['stock_physique'].sum() > 0 else 1)):.1f}x")
m5.metric("Risque Financier", f"{df['Risque_Financier'].sum():,.0f} FCFA", delta="Perte potentielle", delta_color="inverse")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Structure du Stock (ABC)")
    fig_abc = px.pie(df, names='Classe_ABC', values='Valeur_Stock', color='Classe_ABC',
                    color_discrete_map={'A':'#ef4444', 'B':'#f59e0b', 'C':'#10b981'}, hole=0.5)
    st.plotly_chart(fig_abc, use_container_width=True)

with c2:
    st.subheader("Top 15 Risques de Rupture (Jours)")
    fig_rupture = px.bar(df.sort_values('Jours_Restants').head(15), x='Jours_Restants', y='ref_sku', 
                         orientation='h', color='Jours_Restants', color_continuous_scale='Reds_r')
    st.plotly_chart(fig_rupture, use_container_width=True)

# 5. DÉTAILS
st.subheader("📋 État Global de l'Inventaire")
def highlight_status(val):
    if "🚫" in str(val): return 'background-color: #fee2e2; color: #991b1b'
    if "🔴" in str(val): return 'background-color: #fef3c7; color: #92400e'
    if "🟢" in str(val): return 'background-color: #dcfce7; color: #166534'
    return ''

st.dataframe(
    df[['ref_sku', 'designation', 'Classe_ABC', 'stock_physique', 'Vente_Simulee', 'Date_Rupture', 'Risque_Financier', 'Statut']]
    .style.map(highlight_status, subset=['Statut']), 
    use_container_width=True
)

# 6. PLAN D'APPROVISIONNEMENT
st.markdown("---")
st.subheader("🛒 Suggestions de Réapprovisionnement")
df_reap = df[df['Statut'].str.contains("🔴|🚫")].copy()

if not df_reap.empty:
    df_reap['Qte_A_Commander'] = df_reap.apply(lambda x: max(int(x['EOQ_Wilson']), int(x['ROP_Calculé'] - x['stock_physique'] + (x['Vente_Simulee']*30))), axis=1)
    
    vol = (df_reap['Qte_A_Commander'] * df_reap['vol_unitaire_cbm']).sum()
    st.info(f"🚢 Besoins identifiés : **{vol:.2f} m³** soit environ **{int((vol/33)*100)}%** d'un conteneur 20ft.")
    
    st.table(df_reap[['ref_sku', 'designation', 'Qte_A_Commander', 'Risque_Financier', 'Statut']])
    
    csv = df_reap.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Exporter l'Ordre d'Achat", csv, "ordre_achat.csv", "text/csv")
else:
    st.success("✅ Niveaux de stock optimaux.")
    

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="WMS MIT CTL - Ultimate Edition", layout="wide", page_icon="📦")

# Style CSS personnalisé
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #f1f3f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. FONCTIONS LOGIQUES SANS BUG
def calculer_logistique(df, hausse_dem, ret_log, cout_com, taux_stock):
    # Sécurité : Éviter les valeurs nulles ou négatives
    df = df.copy()
    df['vente_moy_jour'] = df['vente_moy_jour'].replace(0, 0.001) 
    
    # Simulations MIT
    df['Vente_Simulee'] = df['vente_moy_jour'] * (1 + hausse_dem)
    df['LeadTime_Total'] = df['lead_time_jours'] + ret_log
    
    # ROP & EOQ (Wilson)
    df['ROP_MIT'] = (df['Vente_Simulee'] * df['LeadTime_Total']) + df['stock_securite']
    demande_annuelle = df['Vente_Simulee'] * 365
    # Formule de Wilson sécurisée
    df['EOQ_Wilson'] = np.sqrt((2 * demande_annuelle * cout_com) / (df['prix_usine'] * taux_stock)).replace([np.inf, -np.inf], 0).fillna(0).astype(int)
    
    # Date de Rupture (Run-out Date)
    df['Jours_Restants'] = (df['stock_physique'] / df['Vente_Simulee']).fillna(0).astype(int)
    df['Date_Rupture'] = [datetime.now() + timedelta(days=int(x)) if x < 1000 else datetime.now() + timedelta(days=1000) for x in df['Jours_Restants']]
    
    # Analyse ABC (Pareto)
    df['Valeur_Stock'] = df['stock_physique'] * df['prix_usine']
    df = df.sort_values(by='Valeur_Stock', ascending=False)
    df['Cumsum_Val'] = df['Valeur_Stock'].cumsum()
    total_val = df['Valeur_Stock'].sum() if df['Valeur_Stock'].sum() > 0 else 1
    df['Pct_Cumul'] = (df['Cumsum_Val'] / total_val) * 100
    
    df['Classe_ABC'] = df['Pct_Cumul'].apply(lambda x: 'A' if x <= 80 else ('B' if x <= 95 else 'C'))
    
    # Statut Visuel
    def get_status(row):
        if row['stock_physique'] <= 0: return "🚫 RUPTURE"
        if row['stock_physique'] <= row['ROP_MIT']: return "🔴 CRITIQUE"
        if row['stock_physique'] <= row['ROP_MIT'] * 1.2: return "🟡 PRÉVENTIF"
        return "🟢 OPTIMAL"
    
    df['Statut'] = df.apply(get_status, axis=1)
    return df

# 3. INTERFACE UTILISATEUR (SIDEBAR)
st.sidebar.header("⚙️ Paramètres Expert")
uploaded_file = st.sidebar.file_uploader("Fichier Inventaire", type=["xlsx", "csv"])

hausse_dem = st.sidebar.slider("Pic Demande (%)", 0, 100, 0) / 100
ret_log = st.sidebar.number_input("Retard Logistique (Jrs)", 0, 90, 0)
c_com = st.sidebar.number_input("Coût de Commande (FCFA)", 1000, 100000, 15000)
t_pos = st.sidebar.slider("Taux de Stockage (%)", 5, 50, 15) / 100

# Chargement / Simulation de données
if uploaded_file:
    try:
        df_input = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
        st.stop()
else:
    # Dataset de test robuste
    data = {
        'ref_sku': [f'SKU-{i:03d}' for i in range(1, 101)],
        'designation': [f'Produit Logistique {i}' for i in range(1, 101)],
        'prix_usine': np.random.randint(1000, 50000, 100),
        'vol_unitaire_cbm': np.random.uniform(0.01, 0.3, 100),
        'vente_moy_jour': np.random.randint(1, 15, 100),
        'lead_time_jours': [45] * 100,
        'stock_physique': np.random.randint(0, 800, 100),
        'stock_securite': [50] * 100
    }
    df_input = pd.DataFrame(data)

# Calculs
df = calculer_logistique(df_input, hausse_dem, ret_log, c_com, t_pos)

# 4. DASHBOARD
st.title("📦 WMS Intelligence : Pilotage MIT CTL")
st.markdown("---")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Valeur Stock", f"{df['Valeur_Stock'].sum():,.0f} FCFA")
m2.metric("Ruptures Imminentes", len(df[df['Jours_Restants'] < 7]))
m3.metric("Besoin Commande (🔴)", len(df[df['Statut'] == "🔴 CRITIQUE"]))
m4.metric("Rotation Stock", f"{(df['Vente_Simulee'].sum()*365 / (df['stock_physique'].sum() if df['stock_physique'].sum() > 0 else 1)):.1f}x")

# Graphiques
c1, c2 = st.columns(2)
with c1:
    st.subheader("Analyse ABC (Valeur Financière)")
    fig_abc = px.pie(df, names='Classe_ABC', values='Valeur_Stock', color='Classe_ABC',
                     color_discrete_map={'A':'#ef4444', 'B':'#f59e0b', 'C':'#10b981'}, hole=0.5)
    st.plotly_chart(fig_abc, use_container_width=True)

with c2:
    st.subheader("Alerte Rupture (Top 15 les plus proches)")
    fig_rupture = px.bar(df.sort_values('Jours_Restants').head(15), x='Jours_Restants', y='ref_sku', 
                         orientation='h', color='Jours_Restants', color_continuous_scale='Reds_r')
    st.plotly_chart(fig_rupture, use_container_width=True)

# 5. TABLEAU DE BORD DÉTAILLÉ
st.subheader("📋 Inventaire & Prévisions de Rupture")
search = st.text_input("🔍 Rechercher une référence...")
df_disp = df[df['ref_sku'].str.contains(search, case=False)] if search else df

# Application du style au tableau (Correction .map pour Streamlit)
def highlight_status(val):
    if "🚫" in str(val): return 'background-color: #fee2e2; color: #991b1b'
    if "🔴" in str(val): return 'background-color: #fef3c7; color: #92400e'
    if "🟢" in str(val): return 'background-color: #dcfce7; color: #166534'
    return ''

st.dataframe(
    df_disp[['ref_sku', 'designation', 'Classe_ABC', 'stock_physique', 'Vente_Simulee', 'Date_Rupture', 'Statut']]
    .style.map(highlight_status, subset=['Statut']), 
    use_container_width=True
)

# 6. PLAN DE RÉAPPROVISIONNEMENT (Wilson + MIT)
st.markdown("---")
st.subheader("🛒 Plan d'Achat Suggéré")
df_reap = df[df['Statut'].str.contains("🔴|🚫")].copy()

if not df_reap.empty:
    # Calcul quantité : EOQ ou Besoin pour couvrir 30 jours (le plus grand des deux)
    df_reap['Qte_A_Commander'] = df_reap.apply(lambda x: max(int(x['EOQ_Wilson']), int(x['ROP_MIT'] - x['stock_physique'] + (x['Vente_Simulee']*30))), axis=1)
    
    vol = (df_reap['Qte_A_Commander'] * df_reap['vol_unitaire_cbm']).sum()
    st.info(f"🚢 Volume total estimé : **{vol:.2f} m³** | Soit environ **{int((vol/33)*100)}%** d'un conteneur 20ft.")
    
    st.table(df_reap[['ref_sku', 'designation', 'Classe_ABC', 'Qte_A_Commander', 'Date_Rupture']])
    
    csv = df_reap.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Télécharger l'Ordre d'Achat", csv, "ordre_achat.csv", "text/csv")
else:
    st.success("✅ Tous les niveaux de stock sont optimaux selon les critères MIT.")
  

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ─────────────────────────────────────────────────────────────────────────────
# 1. CONFIGURATION DE LA PAGE
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WMS MIT CTL - Ultimate Edition",
    layout="wide",
    page_icon="📦"
)

st.markdown("""
<style>
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #f1f3f6; }

    /* Métriques */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }

    /* Titres de section */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e3a5f;
        margin-bottom: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 2. COLONNES REQUISES & VALIDATION
# ─────────────────────────────────────────────────────────────────────────────
COLONNES_REQUISES = [
    'ref_sku', 'designation', 'prix_usine',
    'vol_unitaire_cbm', 'vente_moy_jour',
    'lead_time_jours', 'stock_physique', 'stock_securite'
]

def valider_dataframe(df: pd.DataFrame) -> tuple[bool, str]:
    """Vérifie que toutes les colonnes requises sont présentes."""
    manquantes = [c for c in COLONNES_REQUISES if c not in df.columns]
    if manquantes:
        return False, f"Colonnes manquantes : {', '.join(manquantes)}"
    return True, ""


# ─────────────────────────────────────────────────────────────────────────────
# 3. LOGIQUE MÉTIER — CALCULS WMS
# ─────────────────────────────────────────────────────────────────────────────
def calculer_logistique(
    df: pd.DataFrame,
    hausse_dem: float,
    ret_log: int,
    cout_com: float,
    taux_stock: float
) -> pd.DataFrame:
    """
    Calcule tous les indicateurs logistiques (ROP, EOQ, ABC, statuts).
    Robuste face aux valeurs nulles, infinies ou manquantes.
    """
    df = df.copy()

    # --- Nettoyage préventif des colonnes numériques ---
    for col in ['vente_moy_jour', 'lead_time_jours', 'stock_physique',
                'stock_securite', 'prix_usine', 'vol_unitaire_cbm']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Éviter la division par zéro sur vente_moy_jour
    df['vente_moy_jour'] = df['vente_moy_jour'].clip(lower=0.001)

    # --- Simulation MIT ---
    df['Vente_Simulee'] = df['vente_moy_jour'] * (1 + hausse_dem)
    df['LeadTime_Total'] = (df['lead_time_jours'] + ret_log).clip(lower=0)

    # --- ROP (Reorder Point) ---
    df['ROP_MIT'] = (df['Vente_Simulee'] * df['LeadTime_Total']) + df['stock_securite']

    # --- EOQ (Formule de Wilson) ---
    demande_annuelle = df['Vente_Simulee'] * 365
    prix_pos = df['prix_usine'].clip(lower=0.01)       # Évite division par zéro
    taux_pos = max(taux_stock, 0.001)                   # Évite division par zéro
    eoq_raw = (2 * demande_annuelle * cout_com) / (prix_pos * taux_pos)
    df['EOQ_Wilson'] = (
        np.sqrt(eoq_raw.replace([np.inf, -np.inf], 0))
        .fillna(0)
        .clip(lower=0)
        .round()
        .astype(int)
    )

    # --- Jours avant rupture & date estimée ---
    df['Jours_Restants'] = (
        (df['stock_physique'] / df['Vente_Simulee'])
        .replace([np.inf, -np.inf], 9999)
        .fillna(9999)
        .clip(lower=0, upper=9999)
        .round()
        .astype(int)
    )
    today = datetime.now()
    df['Date_Rupture'] = df['Jours_Restants'].apply(
        lambda j: today + timedelta(days=min(int(j), 3650))
    )

    # --- Valeur du stock ---
    df['Valeur_Stock'] = (df['stock_physique'] * df['prix_usine']).clip(lower=0)

    # --- Analyse ABC (Pareto) ---
    df = df.sort_values('Valeur_Stock', ascending=False).reset_index(drop=True)
    total_val = df['Valeur_Stock'].sum()
    if total_val > 0:
        df['Cumsum_Val'] = df['Valeur_Stock'].cumsum()
        df['Pct_Cumul'] = (df['Cumsum_Val'] / total_val) * 100
    else:
        df['Cumsum_Val'] = 0
        df['Pct_Cumul'] = 0

    df['Classe_ABC'] = df['Pct_Cumul'].apply(
        lambda x: 'A' if x <= 80 else ('B' if x <= 95 else 'C')
    )

    # --- Statut visuel ---
    def get_status(row):
        if row['stock_physique'] <= 0:
            return "🚫 RUPTURE"
        if row['stock_physique'] <= row['ROP_MIT']:
            return "🔴 CRITIQUE"
        if row['stock_physique'] <= row['ROP_MIT'] * 1.2:
            return "🟡 PRÉVENTIF"
        return "🟢 OPTIMAL"

    df['Statut'] = df.apply(get_status, axis=1)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# 4. GÉNÉRATION DU DATASET DE DÉMONSTRATION
# ─────────────────────────────────────────────────────────────────────────────
def generer_dataset_demo() -> pd.DataFrame:
    np.random.seed(42)
    n = 100
    return pd.DataFrame({
        'ref_sku':          [f'SKU-{i:03d}' for i in range(1, n + 1)],
        'designation':      [f'Produit Logistique {i}' for i in range(1, n + 1)],
        'prix_usine':       np.random.randint(1_000, 50_000, n),
        'vol_unitaire_cbm': np.round(np.random.uniform(0.01, 0.30, n), 3),
        'vente_moy_jour':   np.random.randint(1, 15, n).astype(float),
        'lead_time_jours':  np.full(n, 45),
        'stock_physique':   np.random.randint(0, 800, n),
        'stock_securite':   np.full(n, 50),
    })


# ─────────────────────────────────────────────────────────────────────────────
# 5. SIDEBAR — PARAMÈTRES
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Paramètres Expert")

uploaded_file = st.sidebar.file_uploader(
    "📂 Fichier Inventaire", type=["xlsx", "csv"],
    help="Colonnes requises : " + ", ".join(COLONNES_REQUISES)
)

st.sidebar.markdown("---")
hausse_dem = st.sidebar.slider("📈 Pic Demande (%)", 0, 100, 0) / 100
ret_log    = st.sidebar.number_input("⏱ Retard Logistique (jours)", 0, 90, 0, step=1)
c_com      = st.sidebar.number_input("💰 Coût de Commande (FCFA)", 1_000, 100_000, 15_000, step=500)
t_pos      = st.sidebar.slider("📦 Taux de Stockage (%)", 5, 50, 15) / 100

st.sidebar.markdown("---")
st.sidebar.caption("🎓 MIT CTL – Centre for Transportation & Logistics")


# ─────────────────────────────────────────────────────────────────────────────
# 6. CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────────────────────────────────────────
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df_input = pd.read_excel(uploaded_file)
        else:
            df_input = pd.read_csv(uploaded_file)

        ok, msg = valider_dataframe(df_input)
        if not ok:
            st.error(f"❌ Fichier invalide — {msg}")
            st.stop()

        st.sidebar.success(f"✅ {len(df_input)} articles chargés")

    except Exception as e:
        st.error(f"❌ Erreur de lecture du fichier : {e}")
        st.stop()
else:
    df_input = generer_dataset_demo()
    st.sidebar.info("ℹ️ Données de démonstration (100 SKU)")


# ─────────────────────────────────────────────────────────────────────────────
# 7. CALCULS
# ─────────────────────────────────────────────────────────────────────────────
df = calculer_logistique(df_input, hausse_dem, ret_log, c_com, t_pos)


# ─────────────────────────────────────────────────────────────────────────────
# 8. EN-TÊTE DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
st.title("📦 WMS Intelligence — Pilotage MIT CTL")
st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# 9. MÉTRIQUES CLÉS
# ─────────────────────────────────────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)

total_stock = df['stock_physique'].sum()
rotation    = (df['Vente_Simulee'].sum() * 365) / max(total_stock, 1)

m1.metric("💰 Valeur Stock",         f"{df['Valeur_Stock'].sum():,.0f} FCFA")
m2.metric("🚫 Ruptures actives",     len(df[df['Statut'] == "🚫 RUPTURE"]))
m3.metric("🔴 Critiques (< ROP)",    len(df[df['Statut'] == "🔴 CRITIQUE"]))
m4.metric("⚠️ Ruptures < 7 jours",  len(df[df['Jours_Restants'] < 7]))
m5.metric("🔄 Rotation Stock",       f"{rotation:.1f}x / an")


# ─────────────────────────────────────────────────────────────────────────────
# 10. GRAPHIQUES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
c1, c2 = st.columns(2)

with c1:
    st.markdown('<p class="section-title">📊 Analyse ABC — Valeur Financière</p>', unsafe_allow_html=True)
    abc_counts = df.groupby('Classe_ABC').agg(
        Valeur=('Valeur_Stock', 'sum'),
        Nb_SKU=('ref_sku', 'count')
    ).reset_index()

    fig_abc = px.pie(
        abc_counts,
        names='Classe_ABC',
        values='Valeur',
        color='Classe_ABC',
        color_discrete_map={'A': '#ef4444', 'B': '#f59e0b', 'C': '#10b981'},
        hole=0.5,
        custom_data=['Nb_SKU']
    )
    fig_abc.update_traces(
        hovertemplate="<b>Classe %{label}</b><br>Valeur : %{value:,.0f} FCFA<br>SKU : %{customdata[0]}<extra></extra>"
    )
    fig_abc.update_layout(margin=dict(t=10, b=10), legend_title="Classe")
    st.plotly_chart(fig_abc, use_container_width=True)

with c2:
    st.markdown('<p class="section-title">🚨 Top 15 — Ruptures les plus imminentes</p>', unsafe_allow_html=True)
    df_top15 = df.sort_values('Jours_Restants').head(15)
    fig_rupture = px.bar(
        df_top15,
        x='Jours_Restants',
        y='ref_sku',
        orientation='h',
        color='Jours_Restants',
        color_continuous_scale='Reds_r',
        labels={'Jours_Restants': 'Jours restants', 'ref_sku': 'Référence'}
    )
    fig_rupture.update_layout(
        margin=dict(t=10, b=10),
        coloraxis_showscale=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig_rupture, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# 11. TABLEAU INVENTAIRE DÉTAILLÉ
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📋 Inventaire & Prévisions de Rupture")

col_search, col_filtre = st.columns([3, 1])
with col_search:
    search = st.text_input("🔍 Rechercher une référence ou désignation...")
with col_filtre:
    filtre_statut = st.selectbox(
        "Filtrer par statut",
        ["Tous", "🚫 RUPTURE", "🔴 CRITIQUE", "🟡 PRÉVENTIF", "🟢 OPTIMAL"]
    )

df_disp = df.copy()
if search:
    mask = (
        df_disp['ref_sku'].str.contains(search, case=False, na=False) |
        df_disp['designation'].str.contains(search, case=False, na=False)
    )
    df_disp = df_disp[mask]

if filtre_statut != "Tous":
    df_disp = df_disp[df_disp['Statut'] == filtre_statut]

st.caption(f"Affichage : {len(df_disp)} / {len(df)} articles")

def highlight_status(val):
    val = str(val)
    if "🚫" in val: return 'background-color:#fee2e2; color:#991b1b; font-weight:bold'
    if "🔴" in val: return 'background-color:#fef3c7; color:#92400e; font-weight:bold'
    if "🟡" in val: return 'background-color:#fefce8; color:#854d0e'
    if "🟢" in val: return 'background-color:#dcfce7; color:#166534'
    return ''

cols_affichage = ['ref_sku', 'designation', 'Classe_ABC', 'stock_physique',
                  'ROP_MIT', 'EOQ_Wilson', 'Vente_Simulee', 'Jours_Restants',
                  'Date_Rupture', 'Statut']

st.dataframe(
    df_disp[cols_affichage]
    .rename(columns={
        'ref_sku': 'Référence', 'designation': 'Désignation',
        'stock_physique': 'Stock Phys.', 'Vente_Simulee': 'Vente/J Simulée',
        'Jours_Restants': 'Jours restants', 'Date_Rupture': 'Date rupture estimée'
    })
    .style.map(highlight_status, subset=['Statut']),
    use_container_width=True,
    height=420
)


# ─────────────────────────────────────────────────────────────────────────────
# 12. PLAN DE RÉAPPROVISIONNEMENT
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🛒 Plan d'Achat Suggéré (🚫 Rupture + 🔴 Critique)")

df_reap = df[df['Statut'].isin(["🚫 RUPTURE", "🔴 CRITIQUE"])].copy()

if not df_reap.empty:
    def calc_qte(row):
        besoin_30j    = int(row['Vente_Simulee'] * 30)
        besoin_rop    = max(int(row['ROP_MIT'] - row['stock_physique']), 0)
        eoq           = int(row['EOQ_Wilson'])
        return max(eoq, besoin_rop + besoin_30j)

    df_reap['Qte_A_Commander'] = df_reap.apply(calc_qte, axis=1)
    df_reap['Valeur_Commande']  = (df_reap['Qte_A_Commander'] * df_reap['prix_usine']).round(0).astype(int)
    df_reap['Volume_CBM']       = (df_reap['Qte_A_Commander'] * df_reap['vol_unitaire_cbm']).round(3)

    vol_total    = df_reap['Volume_CBM'].sum()
    val_totale   = df_reap['Valeur_Commande'].sum()
    pct_20ft     = min((vol_total / 33) * 100, 100)
    pct_40ft     = min((vol_total / 67) * 100, 100)

    ki1, ki2, ki3 = st.columns(3)
    ki1.metric("🚢 Volume total", f"{vol_total:.2f} m³")
    ki2.metric("📦 Conteneur 20ft",  f"{pct_20ft:.1f}% rempli")
    ki3.metric("💵 Valeur commande", f"{val_totale:,.0f} FCFA")

    st.table(
        df_reap[['ref_sku', 'designation', 'Classe_ABC', 'stock_physique',
                 'Qte_A_Commander', 'Volume_CBM', 'Valeur_Commande', 'Date_Rupture', 'Statut']]
        .rename(columns={
            'ref_sku': 'Référence', 'designation': 'Désignation',
            'stock_physique': 'Stock actuel', 'Qte_A_Commander': 'Qté à commander',
            'Valeur_Commande': 'Valeur (FCFA)', 'Volume_CBM': 'Volume (m³)',
            'Date_Rupture': 'Date rupture'
        })
    )

    csv_bytes = df_reap.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger l'Ordre d'Achat (.csv)",
        data=csv_bytes,
        file_name=f"ordre_achat_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )
else:
    st.success("✅ Tous les niveaux de stock sont optimaux selon les critères MIT CTL.")


# ─────────────────────────────────────────────────────────────────────────────
# 13. PIED DE PAGE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    f"🎓 WMS MIT CTL — Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M')} "
    f"| {len(df)} SKU analysés | Modèle Wilson + ROP"
    )
    

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="WMS Logistics · MIT CTL", page_icon="📦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
.stApp{background:linear-gradient(135deg,#0a1628 0%,#0d2240 50%,#0a1628 100%);color:#e8edf5;}
.page-header{background:linear-gradient(120deg,rgba(0,196,167,.10) 0%,rgba(0,114,255,.04) 100%);border:1px solid rgba(0,196,167,.25);border-radius:16px;padding:32px 40px;margin-bottom:32px;position:relative;overflow:hidden;}
.page-tag{display:inline-block;background:rgba(0,196,167,.15);color:#00c4a7;font-size:10px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;padding:5px 14px;border-radius:20px;border:1px solid rgba(0,196,167,.3);margin-bottom:14px;}
.page-title{font-family:'Syne',sans-serif;font-size:38px;font-weight:800;color:#fff;margin:0 0 8px 0;line-height:1.1;}
.page-title span{color:#00c4a7;}.page-sub{font-size:15px;color:#7a92b0;font-weight:300;}
.section-title{font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:#fff;margin:0 0 4px 0;}
.section-bar{width:36px;height:3px;background:linear-gradient(90deg,#00c4a7,#0072ff);border-radius:2px;margin-bottom:20px;}
.divider{height:1px;background:rgba(255,255,255,.07);margin:32px 0;}
[data-testid="metric-container"]{background:rgba(255,255,255,.04)!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:12px!important;padding:18px 20px!important;}
[data-testid="metric-container"] label{color:#5a7090!important;font-size:12px!important;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:#00c4a7!important;font-family:'Syne',sans-serif!important;font-size:24px!important;font-weight:800!important;}
[data-testid="stDataFrame"]{border:1px solid rgba(255,255,255,.08)!important;border-radius:12px!important;overflow:hidden!important;}
.stButton>button{background:linear-gradient(135deg,#00c4a7,#0072ff)!important;color:#0a1628!important;font-weight:700!important;border:none!important;border-radius:8px!important;padding:10px 24px!important;}
#MainMenu,footer,header{visibility:hidden;}
</style>""", unsafe_allow_html=True)

# ── COLONNES REQUISES ──
COLS = ['ref_sku','designation','prix_usine','vol_unitaire_cbm','vente_moy_jour','lead_time_jours','stock_physique','stock_securite']

def valider(df):
    m = [c for c in COLS if c not in df.columns]
    return (False, f"Colonnes manquantes : {', '.join(m)}") if m else (True, "")

# ── LOGIQUE MÉTIER ──
def calculer(df, hausse, retard, cout_com, taux):
    df = df.copy()
    for c in ['vente_moy_jour','lead_time_jours','stock_physique','stock_securite','prix_usine','vol_unitaire_cbm']:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
    df['vente_moy_jour'] = df['vente_moy_jour'].clip(lower=0.001)
    df['Vente_Simulee']  = df['vente_moy_jour'] * (1 + hausse)
    df['LeadTime_Total'] = (df['lead_time_jours'] + retard).clip(lower=0)
    df['ROP_MIT']        = (df['Vente_Simulee'] * df['LeadTime_Total']) + df['stock_securite']
    eoq_raw = (2 * df['Vente_Simulee'] * 365 * cout_com) / (df['prix_usine'].clip(lower=0.01) * max(taux, 0.001))
    df['EOQ_Wilson']     = np.sqrt(eoq_raw.replace([np.inf,-np.inf],0)).fillna(0).clip(lower=0).round().astype(int)
    df['Jours_Restants'] = ((df['stock_physique']/df['Vente_Simulee']).replace([np.inf,-np.inf],9999).fillna(9999).clip(0,9999).round().astype(int))
    today = datetime.now()
    df['Date_Rupture']   = df['Jours_Restants'].apply(lambda j: today + timedelta(days=min(int(j),3650)))
    df['Valeur_Stock']   = (df['stock_physique'] * df['prix_usine']).clip(lower=0)
    df = df.sort_values('Valeur_Stock', ascending=False).reset_index(drop=True)
    total = df['Valeur_Stock'].sum()
    df['Pct_Cumul']  = (df['Valeur_Stock'].cumsum() / total * 100) if total > 0 else 0
    df['Classe_ABC'] = df['Pct_Cumul'].apply(lambda x: 'A' if x<=80 else ('B' if x<=95 else 'C'))
    df['Statut'] = df.apply(lambda r: "🚫 RUPTURE" if r['stock_physique']<=0 else ("🔴 CRITIQUE" if r['stock_physique']<=r['ROP_MIT'] else ("🟡 PRÉVENTIF" if r['stock_physique']<=r['ROP_MIT']*1.2 else "🟢 OPTIMAL")), axis=1)
    return df

def demo():
    np.random.seed(42); n=100
    return pd.DataFrame({'ref_sku':[f'SKU-{i:03d}' for i in range(1,n+1)],'designation':[f'Produit Logistique {i}' for i in range(1,n+1)],
        'prix_usine':np.random.randint(1_000,50_000,n),'vol_unitaire_cbm':np.round(np.random.uniform(.01,.30,n),3),
        'vente_moy_jour':np.random.randint(1,15,n).astype(float),'lead_time_jours':np.full(n,45),
        'stock_physique':np.random.randint(0,800,n),'stock_securite':np.full(n,50)})

# ── SIDEBAR ──
with st.sidebar:
    st.markdown('<div style="text-align:center;padding:20px 0 10px;"><div style="font-size:36px;">🏭</div><div style="font-family:Syne,sans-serif;font-size:15px;font-weight:700;color:#fff;margin-top:8px;">WMS Logistics</div><div style="font-size:10px;color:#5a7090;letter-spacing:2px;text-transform:uppercase;">Warehouse Management</div></div><hr style="border-color:rgba(255,255,255,.07);margin:12px 0;">', unsafe_allow_html=True)
    st.markdown("**Navigation**")
    st.page_link("home.py",                  label="🏠 Accueil Hub")
    st.page_link("pages/1_TMS_Logistics.py", label="🚛 TMS Logistics")
    st.page_link("pages/2_WMS_Logistics.py", label="🏭 WMS Logistics", disabled=True)
    st.markdown("<hr style='border-color:rgba(255,255,255,.07);margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("**⚙️ Paramètres Expert**")
    uploaded = st.file_uploader("📂 Fichier Inventaire (.xlsx / .csv)", type=["xlsx","csv"], help="Colonnes requises : " + ", ".join(COLS))
    st.markdown("---")
    hausse = st.slider("📈 Pic Demande (%)", 0, 100, 0) / 100
    retard = st.number_input("⏱ Retard Logistique (jours)", 0, 90, 0, step=1)
    c_com  = st.number_input("💰 Coût de Commande (FCFA)", 1_000, 100_000, 15_000, step=500)
    taux   = st.slider("📦 Taux de Stockage (%)", 5, 50, 15) / 100
    st.markdown('<hr style="border-color:rgba(255,255,255,.07);margin:14px 0;"><div style="font-size:11px;color:#3d5570;text-align:center;">Référentiel<br><span style="color:#00c4a7;">MIT Center for Transportation & Logistics</span></div>', unsafe_allow_html=True)

# ── CHARGEMENT DONNÉES ──
if uploaded:
    try:
        df_input = pd.read_excel(uploaded) if uploaded.name.endswith('.xlsx') else pd.read_csv(uploaded)
        ok, msg = valider(df_input)
        if not ok: st.error(f"❌ {msg}"); st.stop()
        st.sidebar.success(f"✅ {len(df_input)} articles chargés")
    except Exception as e:
        st.error(f"❌ Erreur lecture fichier : {e}"); st.stop()
else:
    df_input = demo()
    st.sidebar.info("ℹ️ Données de démonstration (100 SKU)")

df = calculer(df_input, hausse, retard, c_com, taux)

# ── EN-TÊTE ──
st.markdown('<div class="page-header"><div class="page-tag">🏭 Warehouse Management System · MIT CTL</div><h1 class="page-title">WMS <span>Logistics</span></h1><p class="page-sub">Pilotage des stocks · ROP · EOQ Wilson · Analyse ABC · Plan de réapprovisionnement</p></div>', unsafe_allow_html=True)

# ── KPIs ──
total_stock = df['stock_physique'].sum()
rotation    = (df['Vente_Simulee'].sum() * 365) / max(total_stock, 1)
k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("💰 Valeur Stock",        f"{df['Valeur_Stock'].sum():,.0f} FCFA")
k2.metric("🚫 Ruptures actives",    len(df[df['Statut']=="🚫 RUPTURE"]))
k3.metric("🔴 Critiques (< ROP)",   len(df[df['Statut']=="🔴 CRITIQUE"]))
k4.metric("⚠️ Ruptures < 7 j",     len(df[df['Jours_Restants']<7]))
k5.metric("🔄 Rotation Stock",      f"{rotation:.1f}x / an")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── GRAPHIQUES ──
c1, c2 = st.columns(2)
with c1:
    st.markdown('<p class="section-title">📊 Analyse ABC — Valeur Financière</p><div class="section-bar"></div>', unsafe_allow_html=True)
    abc = df.groupby('Classe_ABC').agg(Valeur=('Valeur_Stock','sum'), Nb_SKU=('ref_sku','count')).reset_index()
    fig = px.pie(abc, names='Classe_ABC', values='Valeur', color='Classe_ABC',
                 color_discrete_map={'A':'#ef4444','B':'#f59e0b','C':'#10b981'}, hole=0.5, custom_data=['Nb_SKU'])
    fig.update_traces(hovertemplate="<b>Classe %{label}</b><br>Valeur : %{value:,.0f} FCFA<br>SKU : %{customdata[0]}<extra></extra>")
    fig.update_layout(margin=dict(t=10,b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c8d8ec')
    st.plotly_chart(fig, use_container_width=True)
with c2:
    st.markdown('<p class="section-title">🚨 Top 15 — Ruptures imminentes</p><div class="section-bar"></div>', unsafe_allow_html=True)
    fig2 = px.bar(df.sort_values('Jours_Restants').head(15), x='Jours_Restants', y='ref_sku', orientation='h',
                  color='Jours_Restants', color_continuous_scale='Reds_r', labels={'Jours_Restants':'Jours restants','ref_sku':'Référence'})
    fig2.update_layout(margin=dict(t=10,b=10), coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'},
                       paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c8d8ec')
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── TABLEAU INVENTAIRE ──
st.markdown('<p class="section-title">📋 Inventaire & Prévisions de Rupture</p><div class="section-bar"></div>', unsafe_allow_html=True)
cs, cf = st.columns([3,1])
search = cs.text_input("🔍 Rechercher une référence ou désignation...")
filtre = cf.selectbox("Filtrer par statut", ["Tous","🚫 RUPTURE","🔴 CRITIQUE","🟡 PRÉVENTIF","🟢 OPTIMAL"])
df_disp = df.copy()
if search:
    df_disp = df_disp[df_disp['ref_sku'].str.contains(search,case=False,na=False)|df_disp['designation'].str.contains(search,case=False,na=False)]
if filtre != "Tous":
    df_disp = df_disp[df_disp['Statut']==filtre]
st.caption(f"Affichage : {len(df_disp)} / {len(df)} articles")

def highlight(val):
    v = str(val)
    if "🚫" in v: return 'background-color:#fee2e2;color:#991b1b;font-weight:bold'
    if "🔴" in v: return 'background-color:#fef3c7;color:#92400e;font-weight:bold'
    if "🟡" in v: return 'background-color:#fefce8;color:#854d0e'
    if "🟢" in v: return 'background-color:#dcfce7;color:#166534'
    return ''

COLS_AFF = ['ref_sku','designation','Classe_ABC','stock_physique','ROP_MIT','EOQ_Wilson','Vente_Simulee','Jours_Restants','Date_Rupture','Statut']
st.dataframe(df_disp[COLS_AFF].rename(columns={'ref_sku':'Référence','designation':'Désignation','stock_physique':'Stock Phys.',
    'Vente_Simulee':'Vente/J Simulée','Jours_Restants':'Jours restants','Date_Rupture':'Date rupture estimée'}).style.map(highlight,subset=['Statut']),
    use_container_width=True, height=420)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── PLAN DE RÉAPPROVISIONNEMENT ──
st.markdown('<p class="section-title">🛒 Plan d\'Achat (🚫 Rupture + 🔴 Critique)</p><div class="section-bar"></div>', unsafe_allow_html=True)
df_reap = df[df['Statut'].isin(["🚫 RUPTURE","🔴 CRITIQUE"])].copy()
if not df_reap.empty:
    df_reap['Qte_A_Commander'] = df_reap.apply(lambda r: max(int(r['EOQ_Wilson']), max(int(r['ROP_MIT']-r['stock_physique']),0)+int(r['Vente_Simulee']*30)), axis=1)
    df_reap['Valeur_Commande']  = (df_reap['Qte_A_Commander'] * df_reap['prix_usine']).round(0).astype(int)
    df_reap['Volume_CBM']       = (df_reap['Qte_A_Commander'] * df_reap['vol_unitaire_cbm']).round(3)
    vol, val = df_reap['Volume_CBM'].sum(), df_reap['Valeur_Commande'].sum()
    r1,r2,r3 = st.columns(3)
    r1.metric("🚢 Volume total",      f"{vol:.2f} m³")
    r2.metric("📦 Conteneur 20ft",    f"{min(vol/33*100,100):.1f}% rempli")
    r3.metric("💵 Valeur commande",   f"{val:,.0f} FCFA")
    st.table(df_reap[['ref_sku','designation','Classe_ABC','stock_physique','Qte_A_Commander','Volume_CBM','Valeur_Commande','Date_Rupture','Statut']].rename(columns={
        'ref_sku':'Référence','designation':'Désignation','stock_physique':'Stock actuel',
        'Qte_A_Commander':'Qté à commander','Valeur_Commande':'Valeur (FCFA)','Volume_CBM':'Volume (m³)','Date_Rupture':'Date rupture'}))
    st.download_button("📥 Télécharger l'Ordre d'Achat (.csv)", df_reap.to_csv(index=False).encode('utf-8'),
        f"ordre_achat_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", "text/csv")
else:
    st.success("✅ Tous les niveaux de stock sont optimaux selon les critères MIT CTL.")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.caption(f"🎓 WMS MIT CTL · {datetime.now().strftime('%d/%m/%Y %H:%M')} · {len(df)} SKU analysés · Modèle Wilson + ROP")
    

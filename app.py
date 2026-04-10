import streamlit as st

# 1. CONFIGURATION DE LA PAGE (Identité visuelle forcée)
st.set_page_config(
    page_title="West Africa Logistics Hub · MIT CTL", 
    page_icon="🌍", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. INJECTION DU STYLE CSS (Ton design personnalisé)
st.markdown("""
<style>
    @import url('https://googleapis.com');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0a1628 0%, #0d2240 50%, #0a1628 100%); color: #e8edf5; }
    .hero { background: linear-gradient(120deg, rgba(255,140,0,0.08) 0%, rgba(13,34,64,0.60) 60%, rgba(10,18,40,0.80) 100%); 
            border: 1px solid rgba(255,160,30,0.20); border-radius: 20px; padding: 50px; margin-bottom: 40px; }
    .hero-title { font-family: 'Syne', sans-serif; font-size: 52px; font-weight: 800; color: #fff; line-height: 1.1; }
    .hero-title span { color: #ffad1f; }
    .stat-strip { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); 
                  border-radius: 12px; padding: 20px; display: flex; justify-content: space-around; margin-bottom: 40px; }
    .stat-val { font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 800; color: #ffad1f; }
    .card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); 
             border-radius: 16px; padding: 25px; transition: 0.3s; }
    .stButton>button { background: linear-gradient(135deg, #ffad1f, #ff6b35)!important; color: #0a1628!important; 
                       font-weight: 700!important; border: none!important; border-radius: 10px!important; width: 100%!important; }
</style>
""", unsafe_allow_html=True)

# 3. BARRE LATÉRALE (Navigation intelligente)
with st.sidebar:
    st.markdown('<div style="text-align:center;"><div style="font-size:40px;">🌍</div><h3 style="color:#fff;font-family:Syne;">WA Logistics Hub</h3></div>', unsafe_allow_html=True)
    st.divider()
    st.page_link("app.py", label="🏠 Accueil Cockpit", icon="📊")
    st.page_link("pages/1_TMS_Logistics.py", label="🚛 Pilotage Transport (TMS)", icon="🛣️")
    st.page_link("pages/2_WMS_Logistics.py", label="📦 Gestion Entrepôt (WMS)", icon="🏗️")
    st.divider()
    st.info("Référentiel académique MIT CTL (SC0x & SC1x)")

# 4. SECTION HERO (Vision)
st.markdown("""
<div class="hero">
    <div style="text-transform: uppercase; letter-spacing: 2px; color: #ffad1f; font-size: 12px; font-weight: 700; margin-bottom: 10px;">Plateforme Intégrée IA</div>
    <h1 class="hero-title">Logistics <span>Hub</span></h1>
    <p style="color: #7a92b0; max-width: 600px; font-size: 16px;">
        Pilotage intelligent de l'axe <b>GDIZ – Malanville</b>. 
        Optimisation des flux et des stocks via les modèles mathématiques du MIT.
    </p>
</div>
""", unsafe_allow_html=True)

# 5. STATISTIQUES EN TEMPS RÉEL (Simulation de données IA)
st.markdown('<div class="stat-strip">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown('<div style="text-align:center;"><div class="stat-val">720 km</div><div style="font-size:11px;color:#5a7090;">Axe Principal</div></div>', unsafe_allow_html=True)
with col2: st.markdown('<div style="text-align:center;"><div class="stat-val">94%</div><div style="font-size:11px;color:#5a7090;">Taux de Service</div></div>', unsafe_allow_html=True)
with col3: st.markdown('<div style="text-align:center;"><div class="stat-val">12.4t</div><div style="font-size:11px;color:#5a7090;">CO2 Évité</div></div>', unsafe_allow_html=True)
with col4: st.markdown('<div style="text-align:center;"><div class="stat-val">MIT</div><div style="font-size:11px;color:#5a7090;">Algorithmes ROP/EOQ</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 6. ACCÈS AUX MODULES
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("""<div class="card">
        <h3 style="font-family:Syne; color:#fff;">🚛 TMS Intelligent</h3>
        <p style="font-size:13px; color:#7a92b0;">Optimisation des tournées et tracking temps réel vers Malanville.</p>
    </div>""", unsafe_allow_html=True)
    if st.button("Ouvrir le Pilotage Transport", key="btn_tms"):
        st.switch_page("pages/1_TMS_Logistics.py")

with c2:
    st.markdown("""<div class="card">
        <h3 style="font-family:Syne; color:#fff;">📦 WMS Analytique</h3>
        <p style="font-size:13px; color:#7a92b0;">Intelligence de stock basée sur l'analyse de Pareto et Wilson.</p>
    </div>""", unsafe_allow_html=True)
    if st.button("Ouvrir la Gestion Entrepôt", key="btn_wms"):
        st.switch_page("pages/2_WMS_Logistics.py")

# 7. BANNIÈRE ACADÉMIQUE (Footer)
st.markdown("""
<div style="margin-top: 50px; padding: 20px; border-top: 1px solid rgba(255,255,255,0.1); text-align: center;">
    <p style="font-size:12px; color: #5a7090;">Propulsé par <b>Streamlit</b> | Référentiel <b>MIT Center for Transportation & Logistics</b></p>
</div>
""", unsafe_allow_html=True)
    

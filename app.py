import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="West Africa Logistics Hub · MIT CTL", 
    page_icon="🌍", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. STYLE CSS (Mis à jour pour inclure la couleur de l'optimisation)
st.markdown("""
<style>
    @import url('https://googleapis.com');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0a1628 0%, #0d2240 50%, #0a1628 100%); color: #e8edf5; }
    .hero { background: linear-gradient(120deg, rgba(255,140,0,0.08) 0%, rgba(13,34,64,0.60) 60%, rgba(10,18,40,0.80) 100%); 
            border: 1px solid rgba(255,160,30,0.20); border-radius: 20px; padding: 50px; margin-bottom: 40px; }
    .hero-title { font-family: 'Syne', sans-serif; font-size: 52px; font-weight: 800; color: #fff; line-height: 1.1; }
    .hero-title span { color: #ffad1f; }
    .stat-val { font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 800; color: #ffad1f; }
    .card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); 
             border-radius: 16px; padding: 25px; transition: 0.3s; height: 100%; }
    .opti-card { border: 1px solid rgba(95,195,133,0.3); background: rgba(95,195,133,0.02); }
</style>
""", unsafe_allow_html=True)

# 3. BARRE LATÉRALE (Mise à jour avec le nouveau lien)
with st.sidebar:
    st.markdown('<div style="text-align:center;"><div style="font-size:40px;">🌍</div><h3 style="color:#fff;font-family:Syne;">WA Logistics Hub</h3></div>', unsafe_allow_html=True)
    st.divider()
    st.page_link("app.py", label="🏠 Accueil Cockpit", icon="📊")
    st.page_link("pages/1_TMS_Logistics.py", label="🚛 Pilotage Transport (TMS)", icon="🛣️")
    st.page_link("pages/2_WMS_Logistics.py", label="📦 Gestion Entrepôt (WMS)", icon="🏗️")
    st.page_link("pages/3_Smart_Network_Optimizer.py", label="🎯 Network Optimizer (SC1x)", icon="🧠")
    st.divider()
    st.info("Référentiel académique MIT CTL (SC0x, SC1x, SC2x)")

# 4. SECTION HERO
st.markdown("""
<div class="hero">
    <div style="text-transform: uppercase; letter-spacing: 2px; color: #ffad1f; font-size: 12px; font-weight: 700; margin-bottom: 10px;">Plateforme Intégrée IA & Recherche Opérationnelle</div>
    <h1 class="hero-title">Logistics <span>Hub</span></h1>
    <p style="color: #7a92b0; max-width: 600px; font-size: 16px;">
        Optimisation du corridor <b>GDIZ – Malanville – Hinterland</b>. 
        Application des modèles de programmation linéaire et de gestion des stocks du MIT MicroMasters.
    </p>
</div>
""", unsafe_allow_html=True)

# 5. STATISTIQUES (Modifiées pour inclure l'optimisation)
st.markdown('<div style="background: rgba(255,255,255,0.03); border-radius: 12px; padding: 20px; display: flex; justify-content: space-around; margin-bottom: 40px; border: 1px solid rgba(255,255,255,0.07);">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown('<div style="text-align:center;"><div class="stat-val">720 km</div><div style="font-size:11px;color:#5a7090;">Axe Stratégique</div></div>', unsafe_allow_html=True)
with col2: st.markdown('<div style="text-align:center;"><div class="stat-val">PuLP</div><div style="font-size:11px;color:#5a7090;">Moteur d\'Optimisation</div></div>', unsafe_allow_html=True)
with col3: st.markdown('<div style="text-align:center;"><div class="stat-val">CBC</div><div style="font-size:11px;color:#5a7090;">Solveur Mathématique</div></div>', unsafe_allow_html=True)
with col4: st.markdown('<div style="text-align:center;"><div class="stat-val">Linear</div><div style="font-size:11px;color:#5a7090;">Programming (SC1x)</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 6. ACCÈS AUX MODULES (3 colonnes maintenant)
c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🚛 TMS")
    st.caption("Pilotage opérationnel, rentabilité de flotte et tracking corridor.")
    if st.button("Ouvrir TMS", key="btn_tms"):
        st.switch_page("pages/1_TMS_Logistics.py")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📦 WMS")
    st.caption("Gestion analytique des stocks, modèles EOQ et Safety Stock.")
    if st.button("Ouvrir WMS", key="btn_wms"):
        st.switch_page("pages/2_WMS_Logistics.py")
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card opti-card">', unsafe_allow_html=True)
    st.subheader("🎯 Optimizer")
    st.markdown('<span style="color:#5fc385; font-size:12px; font-weight:bold;">NEW - SMART ENGINE</span>', unsafe_allow_html=True)
    st.caption("Programmation linéaire pour minimiser les coûts de distribution.")
    if st.button("Lancer l'Optimiseur", key="btn_opti"):
        st.switch_page("pages/3_Smart_Network_Optimizer.py")
    st.markdown('</div>', unsafe_allow_html=True)

# 7. BANNIÈRE ACADÉMIQUE
st.markdown("""
<div style="margin-top: 50px; padding: 20px; border-top: 1px solid rgba(255,255,255,0.1); text-align: center;">
    <p style="font-size:12px; color: #5a7090;">Projet Portfolio pour le <b>MIT SCM Blended Pathway</b> | Candidat : Bénin 🌍</p>
</div>
""", unsafe_allow_html=True)
                       

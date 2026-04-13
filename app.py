import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="West Africa Logistics Hub · MIT CTL", 
    page_icon="🌍", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- NOUVEAU : GESTION DE L'AUTHENTIFICATION ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False
    st.session_state['role'] = None

# 2. STYLE CSS (Optimisé pour la lisibilité et les nouveaux indicateurs)
st.markdown("""
<style>
    @import url('https://googleapis.com');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0a1628 0%, #0d2240 50%, #0a1628 100%); color: #e8edf5; }
    .hero { background: linear-gradient(120deg, rgba(255,140,0,0.08) 0%, rgba(13,34,64,0.60) 60%, rgba(10,18,40,0.80) 100%); 
            border: 1px solid rgba(255,160,30,0.20); border-radius: 20px; padding: 40px; margin-bottom: 30px; }
    .hero-title { font-family: 'Syne', sans-serif; font-size: 48px; font-weight: 800; color: #fff; line-height: 1.1; margin:0; }
    .hero-title span { color: #ffad1f; }
    .stat-val { font-family: 'Syne', sans-serif; font-size: 26px; font-weight: 800; color: #ffad1f; }
    .card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); 
             border-radius: 16px; padding: 25px; transition: 0.3s; height: 100%; }
    .card:hover { border: 1px solid rgba(255,173,31,0.4); background: rgba(255,255,255,0.05); }
    .opti-card { border: 1px solid rgba(95,195,133,0.3); background: rgba(95,195,133,0.02); }
    .six-sigma-badge { background: #5fc385; color: #0a1628; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- FONCTION DE LOGIN ---
def login():
    st.markdown('<div class="hero" style="text-align:center;">', unsafe_allow_html=True)
    st.image("https://wikimedia.org", width=60)
    st.subheader("Accès Sécurisé WA Logistics Hub")
    user = st.text_input("Identifiant", placeholder="Admin / Manager")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Entrer dans le Cockpit"):
        if user.lower() in ["admin", "mit"] and pwd == "benin2026": # À sécuriser via secrets.toml
            st.session_state['auth'] = True
            st.session_state['role'] = user
            st.rerun()
        else:
            st.error("Identifiants non autorisés.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- APPLICATION PRINCIPALE ---
if not st.session_state['auth']:
    login()
else:
    # 3. BARRE LATÉRALE
    with st.sidebar:
        st.markdown('<div style="text-align:center;"><div style="font-size:40px;">🌍</div><h3 style="color:#fff;font-family:Syne;">WA Logistics Hub</h3></div>', unsafe_allow_html=True)
        st.caption(f"Connecté en tant que : {st.session_state['role'].upper()}")
        st.divider()
        st.page_link("app.py", label="🏠 Accueil Cockpit", icon="📊")
        st.page_link("pages/1_TMS_Logistics.py", label="🚛 Pilotage Transport", icon="🛣️")
        st.page_link("pages/2_WMS_Logistics.py", label="📦 Gestion Entrepôt", icon="🏗️")
        st.page_link("pages/3_Smart_Network_Optimizer.py", label="🎯 Smart Optimizer", icon="🧠")
        st.divider()
        if st.button("Se déconnecter"):
            st.session_state['auth'] = False
            st.rerun()

    # 4. SECTION HERO
    st.markdown(f"""
    <div class="hero">
        <div style="text-transform: uppercase; letter-spacing: 2px; color: #ffad1f; font-size: 11px; font-weight: 700; margin-bottom: 5px;">Data-Driven Supply Chain · GDIZ Corridor</div>
        <h1 class="hero-title">Logistics <span>Cockpit</span></h1>
        <p style="color: #7a92b0; max-width: 650px; font-size: 15px; margin-top:10px;">
            Optimisation temps réel <b>GDIZ – Hinterland</b>. Intégration des modèles <b>SC1x (Optimization)</b> et <b>Six Sigma</b> pour la réduction de la variabilité.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 5. KPIS DYNAMIQUES (TMS & WMS & QUALITY)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown('<div class="card"><div style="font-size:11px;color:#5a7090;">DIST. MOYENNE</div><div class="stat-val">720 km</div></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="card"><div style="font-size:11px;color:#5a7090;">SOLVEUR ACTIF</div><div class="stat-val">PuLP/CBC</div></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="card"><div style="font-size:11px;color:#5a7090;">PRÉCISION IA (RF)</div><div class="stat-val">94.2%</div></div>', unsafe_allow_html=True)
    with col4: st.markdown('<div class="card"><div style="font-size:11px;color:#5a7090;">QUALITÉ PROCESS</div><div class="stat-val">3.4 <small>σ</small></div></div>', unsafe_allow_html=True)

    st.write("") # Spacer

    # 6. ACCÈS AUX MODULES
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🚛 Pilotage TMS")
        st.caption("ROI de flotte, analyse des coûts de carburant et tracking Corridor.")
        if st.button("Accéder au TMS", use_container_width=True):
            st.switch_page("pages/1_TMS_Logistics.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📦 Intelligence WMS")
        st.caption("Modèles MIT SC0x : EOQ, ROP et gestion par méthode ABC.")
        if st.button("Accéder au WMS", use_container_width=True):
            st.switch_page("pages/2_WMS_Logistics.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="card opti-card">', unsafe_allow_html=True)
        st.subheader("🎯 Smart Optimizer")
        st.markdown('<span class="six-sigma-badge">SIX SIGMA INTEGRATED</span>', unsafe_allow_html=True)
        st.caption("Recherche opérationnelle pour la minimisation du risque et des coûts.")
        if st.button("Lancer l'Optimizer", use_container_width=True):
            st.switch_page("pages/3_Smart_Network_Optimizer.py")
        st.markdown('</div>', unsafe_allow_html=True)

    # 7. FOOTER
    st.markdown('<p style="text-align:center; color:#5a7090; font-size:11px; margin-top:40px;">Bénin Logistics Hub | MIT MicroMasters SCx Case Study | Powered by Random Forest & PuLP</p>', unsafe_allow_html=True)

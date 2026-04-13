import streamlit as st
from helpers import get_data, apply_ui_theme  # Importation des outils SQL et UI

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="West Africa Logistics Hub · MIT CTL", 
    page_icon="🌍", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- GESTION DE L'AUTHENTIFICATION ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False
    st.session_state['role'] = None

# 2. APPLICATION DU THÈME VISUEL
apply_ui_theme()

# 3. FONCTION DE LOGIN
def login():
    st.markdown('<div class="hero" style="text-align:center;">', unsafe_allow_html=True)
    st.subheader("🌍 Accès Sécurisé WA Logistics Hub")
    user = st.text_input("Identifiant", placeholder="Admin / Manager")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Entrer dans le Cockpit"):
        if user.lower() in ["admin", "mit"] and pwd == "benin2026":
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
    # 4. BARRE LATÉRALE
    with st.sidebar:
        st.markdown('<div style="text-align:center;"><div style="font-size:40px;">🌍</div><h3 style="color:#fff;font-family:Syne;">WA Logistics Hub</h3></div>', unsafe_allow_html=True)
        st.caption(f"Connecté : {st.session_state['role'].upper()}")
        st.divider()
        st.page_link("app.py", label="🏠 Accueil Cockpit", icon="📊")
        st.page_link("pages/1_TMS_Logistics.py", label="🚛 Pilotage Transport", icon="🛣️")
        st.page_link("pages/2_WMS_Logistics.py", label="📦 Gestion Entrepôt", icon="🏗️")
        st.page_link("pages/3_Smart_Network_Optimizer.py", label="🎯 Smart Optimizer", icon="🧠")
        st.divider()
        if st.button("Se déconnecter"):
            st.session_state['auth'] = False
            st.rerun()

    # 5. SECTION HERO
    st.markdown(f"""
    <div class="hero">
        <div style="text-transform: uppercase; letter-spacing: 2px; color: #ffad1f; font-size: 11px; font-weight: 700; margin-bottom: 5px;">Data-Driven Supply Chain · GDIZ Corridor</div>
        <h1 class="hero-title">Logistics <span>Cockpit</span></h1>
        <p style="color: #7a92b0; max-width: 650px; font-size: 15px; margin-top:10px;">
            Optimisation temps réel <b>GDIZ – Hinterland</b>. Intégration des modèles <b>SC1x (Optimization)</b> et <b>Six Sigma</b> pour la réduction de la variabilité.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 6. KPIS DYNAMIQUES (RÉCUPÉRATION DEPUIS NEON)
    # On récupère le nombre réel de camions et d'alertes stock
    try:
        df_flotte = get_data("SELECT COUNT(*) as total FROM flotte_vehicules")
        df_alertes = get_data("SELECT COUNT(*) as total FROM stocks_gdiz WHERE quantite_actuelle <= seuil_rop")
        n_camions = df_flotte['total'].iloc[0] if df_flotte is not None else 0
        n_alertes = df_alertes['total'].iloc[0] if df_alertes is not None else 0
    except:
        n_camions, n_alertes = 0, 0

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Flotte Live", f"{n_camions} Camions")
    with col2: st.metric("Axe Stratégique", "720 km")
    with col3: st.metric("Alertes Stock", n_alertes, delta_color="inverse")
    with col4: st.metric("Qualité Process", "3.4 σ")

    st.write("") 

    # 7. ACCÈS AUX MODULES
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🚛 Pilotage TMS")
        st.caption("ROI de flotte, analyse des coûts et tracking.")
        if st.button("Accéder au TMS", use_container_width=True, key="go_tms"):
            st.switch_page("pages/1_TMS_Logistics.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📦 Intelligence WMS")
        st.caption("Modèles MIT SC0x : EOQ, ROP et gestion ABC.")
        if st.button("Accéder au WMS", use_container_width=True, key="go_wms"):
            st.switch_page("pages/2_WMS_Logistics.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="card opti-card">', unsafe_allow_html=True)
        st.subheader("🎯 Smart Optimizer")
        st.markdown('<span class="six-sigma-badge">SIX SIGMA INTEGRATED</span>', unsafe_allow_html=True)
        st.caption("Minimisation du risque et des coûts via solveur CBC.")
        if st.button("Lancer l'Optimizer", use_container_width=True, key="go_opti"):
            st.switch_page("pages/3_Smart_Network_Optimizer.py")
        st.markdown('</div>', unsafe_allow_html=True)

    # 8. FOOTER
    st.markdown('<p style="text-align:center; color:#5a7090; font-size:11px; margin-top:40px;">Bénin Logistics Hub | Projet Portfolio MIT CTL MicroMasters | Powered by Neon PostgreSQL & PuLP</p>', unsafe_allow_html=True)
    

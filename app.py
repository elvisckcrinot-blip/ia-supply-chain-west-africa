import streamlit as st

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="West Africa Logistics Hub",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS PERSONNALISÉ
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  /* Fond principal */
  .stApp {
    background: linear-gradient(135deg, #0a1628 0%, #0d2240 50%, #0a1628 100%);
    color: #e8edf5;
  }

  /* Hero section */
  .hero-container {
    background: linear-gradient(120deg, rgba(255,140,0,0.08) 0%, rgba(255,200,50,0.04) 100%);
    border: 1px solid rgba(255,160,30,0.2);
    border-radius: 20px;
    padding: 48px 56px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
  }
  .hero-container::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(255,160,30,0.12) 0%, transparent 70%);
    border-radius: 50%;
  }
  .hero-tag {
    display: inline-block;
    background: rgba(255,160,30,0.15);
    color: #ffad1f;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    padding: 6px 16px;
    border-radius: 20px;
    border: 1px solid rgba(255,160,30,0.3);
    margin-bottom: 20px;
  }
  .hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 52px;
    font-weight: 800;
    line-height: 1.1;
    color: #ffffff;
    margin: 0 0 16px 0;
  }
  .hero-title span {
    color: #ffad1f;
  }
  .hero-subtitle {
    font-size: 17px;
    color: #8fa3c0;
    max-width: 560px;
    line-height: 1.7;
    font-weight: 300;
  }

  /* Cartes modules */
  .module-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    padding: 36px 32px;
    height: 100%;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }
  .module-card:hover {
    border-color: rgba(255,160,30,0.35);
    background: rgba(255,255,255,0.07);
  }
  .module-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 0 0 16px 16px;
  }
  .card-tms::after { background: linear-gradient(90deg, #ffad1f, #ff6b35); }
  .card-wms::after { background: linear-gradient(90deg, #00c4a7, #0072ff); }

  .card-icon {
    font-size: 36px;
    margin-bottom: 16px;
    display: block;
  }
  .card-badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 12px;
    margin-bottom: 14px;
  }
  .badge-tms { background: rgba(255,173,31,0.15); color: #ffad1f; border: 1px solid rgba(255,173,31,0.3); }
  .badge-wms { background: rgba(0,196,167,0.12); color: #00c4a7; border: 1px solid rgba(0,196,167,0.3); }

  .card-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 10px 0;
  }
  .card-desc {
    font-size: 14px;
    color: #7a92b0;
    line-height: 1.7;
    margin-bottom: 24px;
  }
  .feature-list {
    list-style: none;
    padding: 0; margin: 0;
  }
  .feature-list li {
    font-size: 13px;
    color: #9db3cc;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .feature-list li:last-child { border-bottom: none; }
  .feat-dot-tms { color: #ffad1f; font-size: 10px; }
  .feat-dot-wms { color: #00c4a7; font-size: 10px; }

  /* Métriques */
  .kpi-row {
    display: flex;
    gap: 16px;
    margin-top: 32px;
  }
  .kpi-item {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 18px 22px;
    flex: 1;
    text-align: center;
  }
  .kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    color: #ffad1f;
    margin-bottom: 4px;
  }
  .kpi-label {
    font-size: 12px;
    color: #5a7090;
    letter-spacing: 0.5px;
  }

  /* Footer */
  .footer-bar {
    margin-top: 48px;
    padding-top: 24px;
    border-top: 1px solid rgba(255,255,255,0.07);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
  }
  .footer-text { font-size: 12px; color: #3d5570; }
  .footer-accent { color: #ffad1f; font-weight: 500; }

  /* Masquer éléments Streamlit par défaut */
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
  header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 10px;">
        <div style="font-size:40px;">🌍</div>
        <div style="font-family:'Syne',sans-serif; font-size:15px; font-weight:700; color:#fff; margin-top:8px;">West Africa</div>
        <div style="font-size:11px; color:#5a7090; letter-spacing:2px; text-transform:uppercase;">Logistics Hub</div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.07); margin: 16px 0;">
    """, unsafe_allow_html=True)

    st.markdown("**Navigation**")
    st.page_link("home.py", label="🏠 Accueil", disabled=True)
    st.page_link("pages/1_TMS_Logistics.py", label="🚛 TMS Logistics")
    st.page_link("pages/2_WMS_Logistics.py", label="🏭 WMS Logistics")

    st.markdown("""
    <hr style="border-color:rgba(255,255,255,0.07); margin: 20px 0 12px;">
    <div style="font-size:11px; color:#3d5570; text-align:center;">
        Basé sur les modèles<br><span style="color:#ffad1f;">MIT Center for Transportation & Logistics</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-tag">🌍 Plateforme Opérationnelle · Afrique de l'Ouest</div>
    <h1 class="hero-title">West Africa<br><span>Logistics Hub</span></h1>
    <p class="hero-subtitle">
        Interface de pilotage stratégique centralisant vos solutions de transport et d'entrepôt,
        optimisées selon les standards du MIT CTL pour l'axe logistique Cotonou–Malanville.
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CARTES MODULES
# ─────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="module-card card-tms">
        <span class="card-icon">🚛</span>
        <span class="card-badge badge-tms">Transport Management</span>
        <h2 class="card-title">TMS Logistics</h2>
        <p class="card-desc">
            Orchestration complète des flux de transport sur l'axe Cotonou–Malanville.
            Optimisation des tournées, suivi GPS et gestion du docking à la GDIZ.
        </p>
        <ul class="feature-list">
            <li><span class="feat-dot-tms">●</span> Gestion du docking & quais GDIZ</li>
            <li><span class="feat-dot-tms">●</span> Optimisation des distances (MIT SC0x)</li>
            <li><span class="feat-dot-tms">●</span> Suivi GPS territorial en temps réel</li>
            <li><span class="feat-dot-tms">●</span> ROI social : économies reinjectées en emploi local</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_TMS_Logistics.py", label="Ouvrir TMS Logistics →")

with col2:
    st.markdown("""
    <div class="module-card card-wms">
        <span class="card-icon">🏭</span>
        <span class="card-badge badge-wms">Warehouse Management</span>
        <h2 class="card-title">WMS Logistics</h2>
        <p class="card-desc">
            Pilotage intelligent de l'entrepôt : gestion des stocks, traçabilité
            des entrées/sorties et optimisation des emplacements selon la demande.
        </p>
        <ul class="feature-list">
            <li><span class="feat-dot-wms">●</span> Gestion des stocks en temps réel</li>
            <li><span class="feat-dot-wms">●</span> Traçabilité entrées / sorties</li>
            <li><span class="feat-dot-wms">●</span> Optimisation des emplacements</li>
            <li><span class="feat-dot-wms">●</span> Tableaux de bord opérationnels</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_WMS_Logistics.py", label="Ouvrir WMS Logistics →")

# ─────────────────────────────────────────────
# KPI GLOBAUX
# ─────────────────────────────────────────────
st.markdown("""
<div class="kpi-row">
    <div class="kpi-item">
        <div class="kpi-value">3 780 000</div>
        <div class="kpi-label">FCFA économisés / an · 10 camions</div>
    </div>
    <div class="kpi-item">
        <div class="kpi-value">2</div>
        <div class="kpi-label">Modules actifs</div>
    </div>
    <div class="kpi-item">
        <div class="kpi-value">MIT CTL</div>
        <div class="kpi-label">Référentiel académique</div>
    </div>
    <div class="kpi-item">
        <div class="kpi-value">Cotonou</div>
        <div class="kpi-label">Axe logistique principal</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer-bar">
    <span class="footer-text">© 2025 <span class="footer-accent">West Africa Logistics Hub</span> · Tous droits réservés</span>
    <span class="footer-text">Propulsé par <span class="footer-accent">Streamlit</span> · Modèles <span class="footer-accent">MIT CTL</span></span>
</div>
""", unsafe_allow_html=True)

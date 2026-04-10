import streamlit as st

st.set_page_config(page_title="West Africa Logistics Hub · MIT CTL", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
.stApp{background:linear-gradient(135deg,#0a1628 0%,#0d2240 50%,#0a1628 100%);color:#e8edf5;}
[data-testid="stSidebar"]{background:rgba(10,18,38,.95)!important;border-right:1px solid rgba(255,255,255,.07)!important;}
.hero{background:linear-gradient(120deg,rgba(255,140,0,.08) 0%,rgba(13,34,64,.60) 60%,rgba(10,18,40,.80) 100%);border:1px solid rgba(255,160,30,.20);border-radius:20px;padding:56px 52px 48px;margin-bottom:40px;position:relative;overflow:hidden;}
.hero::before{content:'';position:absolute;top:-80px;right:-80px;width:380px;height:380px;background:radial-gradient(circle,rgba(255,160,30,.10) 0%,transparent 65%);border-radius:50%;}
.eyebrow{display:inline-block;background:rgba(255,173,31,.12);color:#ffad1f;font-size:10px;font-weight:700;letter-spacing:3px;text-transform:uppercase;padding:5px 16px;border-radius:20px;border:1px solid rgba(255,173,31,.28);margin-bottom:18px;}
.hero-title{font-family:'Syne',sans-serif;font-size:52px;font-weight:800;color:#fff;line-height:1.05;margin:0 0 6px 0;}
.hero-title span{color:#ffad1f;}.hero-sub{font-size:16px;color:#7a92b0;font-weight:300;margin:0 0 28px 0;max-width:540px;}
.pill{display:inline-block;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.10);color:#8fa3c0;font-size:11px;padding:5px 14px;border-radius:20px;margin-right:8px;}
.section-title{font-family:'Syne',sans-serif;font-size:20px;font-weight:700;color:#fff;margin:0 0 4px 0;}
.section-bar{width:36px;height:3px;background:linear-gradient(90deg,#ffad1f,#ff6b35);border-radius:2px;margin-bottom:24px;}
.section-sub{font-size:13px;color:#5a7090;margin-bottom:28px;margin-top:-16px;}
.stat-strip{background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:20px 28px;display:flex;align-items:center;justify-content:space-around;flex-wrap:wrap;gap:16px;margin-bottom:40px;}
.stat-val{font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:#ffad1f;text-align:center;}
.stat-lbl{font-size:11px;color:#5a7090;margin-top:2px;text-align:center;}
.card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:32px 28px 28px;}
.card-tag{font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#ffad1f;margin-bottom:10px;}
.card-name{font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#fff;margin-bottom:10px;}
.card-desc{font-size:13px;color:#7a92b0;line-height:1.6;margin-bottom:20px;}
.card-feat{list-style:none;padding:0;margin:0 0 24px 0;}
.card-feat li{font-size:12px;color:#8fa3c0;padding:5px 0;border-bottom:1px solid rgba(255,255,255,.05);}
.card-feat li:last-child{border-bottom:none;}
.mit-banner{background:rgba(255,173,31,.06);border:1px solid rgba(255,173,31,.18);border-radius:14px;padding:24px 32px;margin:40px 0;display:flex;align-items:center;gap:20px;}
.mit-logo{font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:#ffad1f;white-space:nowrap;}
.mit-text{font-size:13px;color:#7a92b0;line-height:1.6;}
.divider{height:1px;background:rgba(255,255,255,.07);margin:36px 0;}
.footer{text-align:center;padding:24px 0 8px;font-size:12px;color:#3d5570;}
.footer span{color:#ffad1f;font-weight:500;}
.stButton>button{background:linear-gradient(135deg,#ffad1f,#ff6b35)!important;color:#0a1628!important;font-weight:700!important;border:none!important;border-radius:10px!important;padding:12px 28px!important;width:100%!important;}
#MainMenu,footer,header{visibility:hidden;}
</style>""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown('<div style="text-align:center;padding:24px 0 12px;"><div style="font-size:42px;">🌍</div><div style="font-family:Syne,sans-serif;font-size:16px;font-weight:800;color:#fff;margin-top:10px;">WA Logistics Hub</div><div style="font-size:10px;color:#5a7090;letter-spacing:2.5px;text-transform:uppercase;margin-top:5px;">MIT CTL Platform</div></div><hr style="border-color:rgba(255,255,255,.07);margin:12px 0 20px;">', unsafe_allow_html=True)
    st.markdown("**Navigation**")
    st.page_link("app.py",                   label="🏠 Accueil Hub",    disabled=True)
    st.page_link("pages/1_TMS_Logistics.py", label="🚛 TMS Logistics")
    st.page_link("pages/2_WMS_Logistics.py", label="📦 WMS Logistics")
    st.markdown('<hr style="border-color:rgba(255,255,255,.07);margin:20px 0 16px;"><div style="font-size:11px;color:#3d5570;text-align:center;line-height:1.7;">Référentiel académique<br><span style="color:#ffad1f;">MIT Center for Transportation<br>& Logistics</span></div>', unsafe_allow_html=True)

# ── HERO ──
st.markdown('<div class="hero"><div class="eyebrow">🌍 West Africa Logistics Platform</div><h1 class="hero-title">Logistics <span>Hub</span></h1><p class="hero-sub">Plateforme intégrée de pilotage logistique — Transport & Entrepôt — développée selon les référentiels <strong style="color:#c8d8ec;">MIT CTL</strong>.</p><span class="pill">🚛 TMS Logistics</span><span class="pill">📦 WMS Logistics</span><span class="pill">📍 Axe Cotonou – Malanville</span><span class="pill">🎓 MIT SC0x · SC1x</span></div>', unsafe_allow_html=True)

# ── STATS ──
st.markdown('<div class="stat-strip"><div><div class="stat-val">720 km</div><div class="stat-lbl">Axe GDIZ → Malanville</div></div><div><div class="stat-val">2</div><div class="stat-lbl">Modules actifs</div></div><div><div class="stat-val">100+</div><div class="stat-lbl">SKU gérés (WMS)</div></div><div><div class="stat-val">MIT</div><div class="stat-lbl">Référentiel CTL</div></div><div><div class="stat-val">ROP · EOQ</div><div class="stat-lbl">Modèles intégrés</div></div></div>', unsafe_allow_html=True)

# ── MODULE CARDS ──
st.markdown('<p class="section-title">🧩 Modules de la Plateforme</p><div class="section-bar"></div><p class="section-sub">Sélectionnez un module pour accéder à son tableau de bord.</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2, gap="large")
with c1:
    st.markdown('<div class="card"><span style="font-size:36px;">🚛</span><div class="card-tag">Transport Management System</div><div class="card-name">TMS Logistics</div><div class="card-desc">Pilotage opérationnel du transport sur l\'axe <strong style="color:#c8d8ec;">GDIZ → Malanville</strong>. Optimisation des coûts, suivi en temps réel et gestion du docking.</div><ul class="card-feat"><li>⛽ MIT SC0x — Efficacité énergétique & ROI</li><li>🏢 Gestion du docking GDIZ</li><li>📍 Tracking expéditions temps réel</li><li>🌿 CO₂ évité & emplois finançables</li></ul></div>', unsafe_allow_html=True)
    if st.button("Ouvrir TMS Logistics →", key="btn_tms"):
        st.switch_page("pages/1_TMS_Logistics.py")
with c2:
    st.markdown('<div class="card"><span style="font-size:36px;">📦</span><div class="card-tag">Warehouse Management System</div><div class="card-name">WMS Logistics</div><div class="card-desc">Intelligence entrepôt pilotée par les modèles <strong style="color:#c8d8ec;">MIT CTL</strong> — ROP, EOQ Wilson, Analyse ABC et prévisions de rupture.</div><ul class="card-feat"><li>📊 Analyse ABC (Pareto) — Valeur financière</li><li>🔴 ROP · EOQ Wilson — Réappro optimal</li><li>⚠️ Alertes rupture & statuts stock</li><li>🛒 Plan d\'achat exportable (.csv)</li></ul></div>', unsafe_allow_html=True)
    if st.button("Ouvrir WMS Logistics →", key="btn_wms"):
        st.switch_page("pages/2_WMS_Logistics.py")

# ── MIT BANNER ──
st.markdown('<div class="divider"></div><div class="mit-banner"><div class="mit-logo">MIT<br>CTL</div><div class="mit-text"><strong style="color:#c8d8ec;">MIT Center for Transportation & Logistics</strong><br>Cette plateforme applique les référentiels <strong style="color:#c8d8ec;">SC0x</strong> et <strong style="color:#c8d8ec;">SC1x</strong> du MIT CTL. Modèles : Wilson EOQ, ROP, Pareto ABC, optimisation de flotte et analyse d\'impact carbone.</div></div>', unsafe_allow_html=True)

# ── FOOTER ──
st.markdown('<div class="footer">© 2025 <span>West Africa Logistics Hub</span> · Propulsé par <span>Streamlit</span> · Référentiel <span>MIT Center for Transportation & Logistics</span></div>', unsafe_allow_html=True)

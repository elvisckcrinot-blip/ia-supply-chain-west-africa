import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TMS Logistics · MIT CTL",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a1628 0%, #0d2240 50%, #0a1628 100%);
    color: #e8edf5;
}

/* ── Page Header ── */
.page-header {
    background: linear-gradient(120deg, rgba(255,140,0,0.10) 0%, rgba(255,200,50,0.04) 100%);
    border: 1px solid rgba(255,160,30,0.25);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute; top: -50px; right: -50px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(255,160,30,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.page-tag {
    display: inline-block;
    background: rgba(255,173,31,0.15);
    color: #ffad1f;
    font-size: 10px; font-weight: 700;
    letter-spacing: 2.5px; text-transform: uppercase;
    padding: 5px 14px; border-radius: 20px;
    border: 1px solid rgba(255,173,31,0.3);
    margin-bottom: 14px;
}
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 38px; font-weight: 800;
    color: #ffffff; margin: 0 0 8px 0; line-height: 1.1;
}
.page-title span { color: #ffad1f; }
.page-sub { font-size: 15px; color: #7a92b0; font-weight: 300; }

/* ── Section Headers ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px; font-weight: 700;
    color: #ffffff; margin: 0 0 4px 0;
}
.section-bar {
    width: 36px; height: 3px;
    background: linear-gradient(90deg, #ffad1f, #ff6b35);
    border-radius: 2px; margin-bottom: 20px;
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 20px;
}

/* ── KPI Metrics ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    padding: 18px 20px !important;
}
[data-testid="metric-container"] label {
    color: #5a7090 !important; font-size: 12px !important;
    letter-spacing: 0.5px !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffad1f !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 24px !important; font-weight: 800 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #00c4a7 !important;
}

/* ── Progress bar ── */
.stProgress > div > div { background-color: #ffad1f !important; }

/* ── Inputs ── */
.stTextInput input, .stSelectbox select, .stNumberInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #e8edf5 !important;
    border-radius: 8px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #ffad1f, #ff6b35) !important;
    color: #0a1628 !important;
    font-weight: 700 !important; font-size: 13px !important;
    border: none !important; border-radius: 8px !important;
    padding: 10px 24px !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Form submit ── */
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #ffad1f, #ff6b35) !important;
    color: #0a1628 !important;
    font-weight: 700 !important;
    border: none !important; border-radius: 8px !important;
    width: 100% !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── Alerts ── */
.stAlert { border-radius: 10px !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    font-weight: 600 !important;
    color: #c8d8ec !important;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: rgba(255,255,255,0.07);
    margin: 32px 0;
}

/* ── Quai table ── */
.quai-table { width: 100%; border-collapse: collapse; }
.quai-table th {
    text-align: left; font-size: 11px; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase;
    color: #5a7090; padding: 8px 12px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.quai-table td {
    padding: 10px 12px; font-size: 13px; color: #c8d8ec;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.quai-table tr:last-child td { border-bottom: none; }

/* Masquer éléments Streamlit */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DONNÉES DE RÉFÉRENCE
# ─────────────────────────────────────────────────────────────────────────────
VILLES_BENIN = {
    "GDIZ (Départ)":  0,
    "Abomey-Calavi":  15,
    "Cotonou":        25,
    "Ouidah":         35,
    "Allada":         12,
    "Porto-Novo":     65,
    "Bohicon":        105,
    "Dassa":          185,
    "Savalou":        205,
    "Glazoué":        200,
    "Parakou":        395,
    "Djougou":        450,
    "Natitingou":     520,
    "Kandi":          615,
    "Malanville":     720,
}
DISTANCE_MAX    = 720   # Malanville
PRIX_CARBURANT  = 700   # FCFA / L
CO2_PAR_LITRE   = 2.6   # kg CO2 / L
SALAIRE_ANNUEL  = 756_000  # FCFA

LISTE_VILLES = sorted(VILLES_BENIN.keys())
STATUTS      = ["Préparation", "En Transit", "Livré", "Incident"]

QUAIS_INITIAL = pd.DataFrame({
    "Quai":      ["A1",          "A2",  "B1",  "B2"],
    "Statut":    ["Occupé",      "Libre","Libre","Occupé"],
    "Camion":    ["RB 1234 BJ",  "—",   "—",   "RB 5678 BJ"],
    "Opération": ["Déchargement","—",   "—",   "Chargement"],
})


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def init_session():
    if "db_tms" not in st.session_state:
        st.session_state.db_tms = pd.DataFrame([
            {"ID": "EXP-GDIZ-101", "Article": "Groupe INGCO",  "Position": "Bohicon",    "Statut": "En Transit"},
            {"ID": "EXP-GDIZ-102", "Article": "Ciment Dangote","Position": "Parakou",    "Statut": "En Transit"},
            {"ID": "EXP-GDIZ-103", "Article": "Matériel BTP",  "Position": "Malanville", "Statut": "Livré"},
        ])
    if "quais" not in st.session_state:
        st.session_state.quais = QUAIS_INITIAL.copy()
    if "docking_log" not in st.session_state:
        st.session_state.docking_log = []

init_session()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:20px 0 10px;">
        <div style="font-size:36px;">🚛</div>
        <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:#fff;margin-top:8px;">TMS Logistics</div>
        <div style="font-size:10px;color:#5a7090;letter-spacing:2px;text-transform:uppercase;margin-top:4px;">Transport Management</div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.07);margin:12px 0;">
    """, unsafe_allow_html=True)

    st.markdown("**Navigation**")
    st.page_link("app.py",                      label="🏠 Accueil Hub")
    st.page_link("pages/1_TMS_Logistics.py",    label="🚛 TMS Logistics", disabled=True)
    st.page_link("pages/2_WMS_Logistics.py",    label="📦 WMS Logistics")

    st.markdown("""
    <hr style="border-color:rgba(255,255,255,0.07);margin:20px 0 12px;">
    <div style="font-size:11px;color:#3d5570;text-align:center;">
        Référentiel<br><span style="color:#ffad1f;">MIT Center for Transportation & Logistics</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# EN-TÊTE PAGE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-tag">🚛 Transport Management System</div>
    <h1 class="page-title">TMS <span>Logistics</span></h1>
    <p class="page-sub">Pilotage & Optimisation · Axe Cotonou – Malanville · Modèles MIT CTL</p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 1 — EFFICACITÉ ÉNERGÉTIQUE & ROI
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<p class="section-title">⛽ Efficacité Énergétique & ROI Social</p>'
    '<div class="section-bar"></div>',
    unsafe_allow_html=True
)

with st.expander("⚙️ Paramètres du modèle d'optimisation MIT SC0x", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        n_camions = st.number_input(
            "Flotte (nombre de camions)",
            min_value=1, max_value=500, value=10, step=1
        )
    with col2:
        d_actuelle = st.number_input(
            "Distance actuelle (km/jour)",
            min_value=1.0, max_value=2000.0, value=80.0, step=1.0
        )
        d_opti = st.number_input(
            "Distance optimisée (km/jour)",
            min_value=1.0, max_value=2000.0, value=65.0, step=1.0
        )
    with col3:
        jours = st.number_input(
            "Jours d'activité / an",
            min_value=1, max_value=365, value=300, step=1
        )
        conso = st.number_input(
            "Consommation (L / 100 km)",
            min_value=1.0, max_value=100.0, value=12.0, step=0.5
        )

# --- Calculs ---
if d_opti >= d_actuelle:
    st.warning("⚠️ La distance optimisée doit être inférieure à la distance actuelle pour générer un gain.")
    gain_km_annuel = 0.0
    economie_fcfa  = 0.0
    co2_evite      = 0.0
else:
    gain_km_annuel = (d_actuelle - d_opti) * n_camions * jours
    economie_fcfa  = gain_km_annuel * (conso / 100) * PRIX_CARBURANT
    co2_evite      = gain_km_annuel * (conso / 100) * CO2_PAR_LITRE

emplois = int(economie_fcfa // SALAIRE_ANNUEL) if economie_fcfa > 0 else 0

# --- KPIs ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("💰 Économie annuelle",   f"{economie_fcfa:,.0f} FCFA")
k2.metric("📏 Distance sauvée",     f"{gain_km_annuel:,.0f} km/an")
k3.metric("🌿 CO₂ évité",           f"{co2_evite:,.0f} kg")
k4.metric("👷 Emplois finançables", str(emplois),
          help=f"Basé sur un salaire annuel de {SALAIRE_ANNUEL:,.0f} FCFA")

if economie_fcfa > 0:
    st.success(
        f"✅ L'économie de **{economie_fcfa:,.0f} FCFA/an** peut financer "
        f"**{emplois} poste(s)** de travail local."
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 2 — GESTION DU DOCKING
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<p class="section-title">🏢 Gestion du Docking — GDIZ</p>'
    '<div class="section-bar"></div>',
    unsafe_allow_html=True
)

col_left, col_right = st.columns([1, 1.6], gap="large")

with col_left:
    # ── Formulaire accès quai ──
    with st.form("form_docking", clear_on_submit=True):
        st.markdown("**Contrôle d'accès quai**")
        camion_immat = st.text_input("Immatriculation du camion", placeholder="Ex : RB 0000 BJ")
        flux_op      = st.selectbox("Type d'opération", ["Chargement", "Déchargement"])
        quai_sel     = st.selectbox("Quai cible", st.session_state.quais["Quai"].tolist())
        submitted    = st.form_submit_button("✅ Valider l'accès")

    if submitted:
        if not camion_immat.strip():
            st.error("❌ Veuillez saisir une immatriculation.")
        else:
            immat_clean = camion_immat.strip().upper()
            mask = st.session_state.quais["Quai"] == quai_sel
            st.session_state.quais.loc[mask, "Statut"]    = "Occupé"
            st.session_state.quais.loc[mask, "Camion"]    = immat_clean
            st.session_state.quais.loc[mask, "Opération"] = flux_op
            st.session_state.docking_log.append(
                f"✔ {immat_clean} · {flux_op} · Quai {quai_sel}"
            )
            st.success(f"Accès autorisé : **{immat_clean}** → Quai **{quai_sel}**")

    # ── Libérer un quai ──
    st.markdown("**Libérer un quai**")
    quai_lib = st.selectbox(
        "Quai à libérer",
        st.session_state.quais["Quai"].tolist(),
        key="quai_lib_select"
    )
    if st.button("🔓 Libérer le quai"):
        mask = st.session_state.quais["Quai"] == quai_lib
        st.session_state.quais.loc[mask, "Statut"]    = "Libre"
        st.session_state.quais.loc[mask, "Camion"]    = "—"
        st.session_state.quais.loc[mask, "Opération"] = "—"
        st.success(f"Quai **{quai_lib}** libéré.")

with col_right:
    st.markdown("**État des quais en temps réel**")

    rows_html = ""
    for _, row in st.session_state.quais.iterrows():
        if row["Statut"] == "Occupé":
            badge = (
                '<span style="background:rgba(255,80,80,0.15);color:#ff5050;'
                'font-size:11px;font-weight:700;padding:3px 10px;border-radius:12px;">🔴 Occupé</span>'
            )
        else:
            badge = (
                '<span style="background:rgba(0,196,167,0.15);color:#00c4a7;'
                'font-size:11px;font-weight:700;padding:3px 10px;border-radius:12px;">🟢 Libre</span>'
            )
        rows_html += f"""
        <tr>
            <td><strong>{row['Quai']}</strong></td>
            <td>{badge}</td>
            <td style="color:#8fa3c0;">{row['Camion']}</td>
            <td style="color:#8fa3c0;">{row['Opération']}</td>
        </tr>"""

    st.markdown(f"""
    <div class="card" style="padding:20px;">
        <table class="quai-table">
            <thead><tr>
                <th>Quai</th><th>Statut</th><th>Camion</th><th>Opération</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # Journal des accès (5 derniers)
    if st.session_state.docking_log:
        st.markdown("**Journal des accès**")
        for log in reversed(st.session_state.docking_log[-5:]):
            st.markdown(
                f"<div style='font-size:12px;color:#7a92b0;padding:4px 0;"
                f"border-bottom:1px solid rgba(255,255,255,0.05);'>{log}</div>",
                unsafe_allow_html=True
            )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 3 — TRACKING DES EXPÉDITIONS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<p class="section-title">📦 Suivi des Expéditions</p>'
    '<div class="section-bar"></div>',
    unsafe_allow_html=True
)

col_form, col_info = st.columns([1, 1.6], gap="large")

with col_form:
    with st.form("form_tracking", clear_on_submit=True):
        st.markdown("**Mettre à jour une expédition**")
        id_exp   = st.text_input("ID Expédition", placeholder="Ex : EXP-GDIZ-104")
        article  = st.text_input("Article / Marchandise", placeholder="Ex : Ciment Dangote")
        position = st.selectbox("Dernière position constatée", LISTE_VILLES)
        statut   = st.selectbox("Statut", STATUTS)
        submit_t = st.form_submit_button("📍 Actualiser le tracking")

    if submit_t:
        if not id_exp.strip():
            st.error("❌ Veuillez saisir un ID d'expédition.")
        elif not article.strip():
            st.error("❌ Veuillez saisir le nom de l'article.")
        else:
            id_clean = id_exp.strip().upper()
            if id_clean in st.session_state.db_tms["ID"].values:
                mask = st.session_state.db_tms["ID"] == id_clean
                st.session_state.db_tms.loc[mask, "Article"]  = article.strip()
                st.session_state.db_tms.loc[mask, "Position"] = position
                st.session_state.db_tms.loc[mask, "Statut"]   = statut
                st.success(f"✅ Expédition **{id_clean}** mise à jour.")
            else:
                new_row = pd.DataFrame([{
                    "ID":       id_clean,
                    "Article":  article.strip(),
                    "Position": position,
                    "Statut":   statut,
                }])
                st.session_state.db_tms = pd.concat(
                    [st.session_state.db_tms, new_row], ignore_index=True
                )
                st.success(f"✅ Expédition **{id_clean}** ajoutée.")

with col_info:
    df_transit = st.session_state.db_tms[
        st.session_state.db_tms["Statut"] == "En Transit"
    ]
    if not df_transit.empty:
        derniere          = df_transit.iloc[-1]
        position_actuelle = derniere["Position"]
        km_faits          = VILLES_BENIN.get(position_actuelle, 0)
        progression       = min(km_faits / DISTANCE_MAX, 1.0)

        st.markdown(f"""
        <div class="card">
            <div style="font-size:11px;color:#5a7090;letter-spacing:1.5px;
                        text-transform:uppercase;margin-bottom:8px;">
                Dernière expédition en transit
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:20px;
                        font-weight:700;color:#fff;margin-bottom:4px;">
                {derniere['ID']}
            </div>
            <div style="font-size:13px;color:#8fa3c0;margin-bottom:16px;">
                {derniere['Article']}
            </div>
            <div style="font-size:13px;color:#c8d8ec;">
                📍 <strong>{position_actuelle}</strong>
                &nbsp;·&nbsp; {km_faits} km / {DISTANCE_MAX} km
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(progression)
        st.caption(f"Progression vers Malanville : {progression * 100:.1f}%")
    else:
        st.info("Aucune expédition en transit actuellement.")

# ── Dashboard tableau ──
st.markdown("**📋 Dashboard opérationnel**")

filtre = st.selectbox("Filtrer par statut", ["Tous"] + STATUTS, key="filtre_statut")
df_display = st.session_state.db_tms.copy()
if filtre != "Tous":
    df_display = df_display[df_display["Statut"] == filtre]

if df_display.empty:
    st.info("Aucune expédition pour ce filtre.")
else:
    st.dataframe(df_display.reset_index(drop=True), use_container_width=True)

# ── Statistiques rapides ──
total      = len(st.session_state.db_tms)
en_transit = len(st.session_state.db_tms[st.session_state.db_tms["Statut"] == "En Transit"])
livres     = len(st.session_state.db_tms[st.session_state.db_tms["Statut"] == "Livré"])
incidents  = len(st.session_state.db_tms[st.session_state.db_tms["Statut"] == "Incident"])

s1, s2, s3, s4 = st.columns(4)
s1.metric("Total expéditions", total)
s2.metric("En Transit",        en_transit)
s3.metric("Livrées",           livres)
s4.metric("Incidents",         incidents)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;
            f

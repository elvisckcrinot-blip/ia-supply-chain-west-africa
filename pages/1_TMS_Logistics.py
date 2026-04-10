import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="TMS Logistics · MIT CTL", page_icon="🚛", layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
.stApp{background:linear-gradient(135deg,#0a1628 0%,#0d2240 50%,#0a1628 100%);color:#e8edf5;}
.page-header{background:linear-gradient(120deg,rgba(255,140,0,.10) 0%,rgba(255,200,50,.04) 100%);border:1px solid rgba(255,160,30,.25);border-radius:16px;padding:32px 40px;margin-bottom:32px;position:relative;overflow:hidden;}
.page-header::before{content:'';position:absolute;top:-50px;right:-50px;width:220px;height:220px;background:radial-gradient(circle,rgba(255,160,30,.12) 0%,transparent 70%);border-radius:50%;}
.page-tag{display:inline-block;background:rgba(255,173,31,.15);color:#ffad1f;font-size:10px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;padding:5px 14px;border-radius:20px;border:1px solid rgba(255,173,31,.3);margin-bottom:14px;}
.page-title{font-family:'Syne',sans-serif;font-size:38px;font-weight:800;color:#fff;margin:0 0 8px 0;line-height:1.1;}
.page-title span{color:#ffad1f;}.page-sub{font-size:15px;color:#7a92b0;font-weight:300;}
.section-title{font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:#fff;margin:0 0 4px 0;}
.section-bar{width:36px;height:3px;background:linear-gradient(90deg,#ffad1f,#ff6b35);border-radius:2px;margin-bottom:20px;}
.card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:24px 28px;margin-bottom:20px;}
.divider{height:1px;background:rgba(255,255,255,.07);margin:32px 0;}
[data-testid="metric-container"]{background:rgba(255,255,255,.04)!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:12px!important;padding:18px 20px!important;}
[data-testid="metric-container"] label{color:#5a7090!important;font-size:12px!important;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:#ffad1f!important;font-family:'Syne',sans-serif!important;font-size:24px!important;font-weight:800!important;}
[data-testid="metric-container"] [data-testid="stMetricDelta"]{color:#00c4a7!important;}
.stProgress>div>div{background-color:#ffad1f!important;}
.stTextInput input,.stNumberInput input{background:rgba(255,255,255,.05)!important;border:1px solid rgba(255,255,255,.12)!important;color:#e8edf5!important;border-radius:8px!important;}
.stButton>button{background:linear-gradient(135deg,#ffad1f,#ff6b35)!important;color:#0a1628!important;font-weight:700!important;border:none!important;border-radius:8px!important;padding:10px 24px!important;}
[data-testid="stFormSubmitButton"]>button{background:linear-gradient(135deg,#ffad1f,#ff6b35)!important;color:#0a1628!important;font-weight:700!important;border:none!important;border-radius:8px!important;width:100%!important;}
[data-testid="stDataFrame"]{border:1px solid rgba(255,255,255,.08)!important;border-radius:12px!important;overflow:hidden!important;}
.stAlert,.streamlit-expanderHeader{border-radius:10px!important;}
.quai-table{width:100%;border-collapse:collapse;}
.quai-table th{text-align:left;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#5a7090;padding:8px 12px;border-bottom:1px solid rgba(255,255,255,.08);}
.quai-table td{padding:10px 12px;font-size:13px;color:#c8d8ec;border-bottom:1px solid rgba(255,255,255,.05);}
.quai-table tr:last-child td{border-bottom:none;}
#MainMenu,footer,header{visibility:hidden;}
</style>""", unsafe_allow_html=True)

# ── DONNÉES DE RÉFÉRENCE ──
VILLES_BENIN = {
    "Usine X · GDIZ (Départ)":0,"Glo-Djigbé":5,"Abomey-Calavi":15,"Cotonou":25,
    "Sèmè-Kpodji":40,"Ouidah":45,"Allada":45,"Porto-Novo":55,"Cana":95,
    "Bohicon":105,"Dassa":185,"Glazoué":205,"Savalou":215,"Savè":235,
    "Parakou":395,"Djougou":450,"Natitingou":520,"Kandi":615,"Malanville":720,
}
DISTANCE_MAX, PRIX_CARBURANT, CO2_PAR_LITRE, SALAIRE_ANNUEL = 720, 700, 2.6, 756_000
LISTE_VILLES = sorted(VILLES_BENIN.keys())
MARCHANDISES = sorted(["Cajou","Coton brut","Huile de palme","Maïs","Manioc transformé","Riz paddy","Soja","Tourteau de soja",
    "Agrégats / Gravier","Bois de construction","Carrelage","Ciment Dangote","Fer à béton","Tuyauterie PVC",
    "Équipements frigorifiques","Groupe électrogène INGCO","Matériel électrique","Outillage INGCO",
    "Carburant (fûts)","Engrais NPK","Gaz butane","Produits phytosanitaires",
    "Boissons (palette)","Produits alimentaires emballés"])
STATUTS = ["Préparation","En Transit","Livré","Incident"]
SYSTEMES = {"TMS — Transport Management System":"Orchestration des tournées, docking, suivi GPS corridor",
    "WMS — Warehouse Management System":"Gestion des stocks entrepôt, traçabilité SKU",
    "MIT SC0x — Supply Chain Analytics":"Optimisation distances, calcul ROI carburant & CO₂",
    "MIT CTL — Demand Forecasting":"Prévision des flux marchandises par corridor",
    "ERP Intégration (en cours)":"Synchronisation commandes / expéditions / facturation"}

# ── SESSION STATE ──
def init_session():
    if "db_tms" not in st.session_state:
        st.session_state.db_tms = pd.DataFrame([
            {"ID":"EXP-GDIZ-101","Marchandise":"Groupe électrogène INGCO","Tonnage (T)":8.5, "Position":"Bohicon",                 "Statut":"En Transit", "Heure MAJ":"08:30"},
            {"ID":"EXP-GDIZ-102","Marchandise":"Ciment Dangote",          "Tonnage (T)":30.0,"Position":"Parakou",                 "Statut":"En Transit", "Heure MAJ":"09:15"},
            {"ID":"EXP-GDIZ-103","Marchandise":"Soja",                    "Tonnage (T)":25.0,"Position":"Malanville",              "Statut":"Livré",      "Heure MAJ":"06:00"},
            {"ID":"EXP-GDIZ-104","Marchandise":"Engrais NPK",             "Tonnage (T)":20.0,"Position":"Usine X · GDIZ (Départ)","Statut":"Préparation","Heure MAJ":"10:00"},
        ])
    if "db_dock"      not in st.session_state: st.session_state.db_dock = pd.DataFrame(columns=["Heure","Camion","Marchandise","Tonnage (T)","Opération","Quai"])
    if "quais"        not in st.session_state: st.session_state.quais = pd.DataFrame({"Quai":["A1","A2","B1","B2"],"Statut":["Occupé","Libre","Libre","Occupé"],"Camion":["RB 1234 BJ","—","—","RB 5678 BJ"],"Marchand.":["Ciment Dangote","—","—","Maïs"],"Opération":["Déchargement","—","—","Chargement"]})
    if "docking_log"  not in st.session_state: st.session_state.docking_log = []
init_session()

# ── SIDEBAR ──
with st.sidebar:
    st.markdown('<div style="text-align:center;padding:20px 0 10px;"><div style="font-size:36px;">🚛</div><div style="font-family:Syne,sans-serif;font-size:15px;font-weight:700;color:#fff;margin-top:8px;">TMS Logistics</div><div style="font-size:10px;color:#5a7090;letter-spacing:2px;text-transform:uppercase;">Transport Management</div></div><hr style="border-color:rgba(255,255,255,.07);margin:12px 0;">', unsafe_allow_html=True)
    st.markdown("**Navigation**")
    st.page_link("home.py",                  label="🏠 Accueil Hub")
    st.page_link("pages/1_TMS_Logistics.py", label="🚛 TMS Logistics", disabled=True)
    st.page_link("pages/2_WMS_Logistics.py", label="🏭 WMS Logistics")
    with st.expander("🧠 Systèmes pilotes"):
        for nom, desc in SYSTEMES.items():
            st.markdown(f'<div style="margin-bottom:10px;"><div style="font-size:12px;color:#ffad1f;font-weight:600;">{nom}</div><div style="font-size:11px;color:#5a7090;">{desc}</div></div>', unsafe_allow_html=True)
    st.markdown('<hr style="border-color:rgba(255,255,255,.07);margin:14px 0;"><div style="font-size:11px;color:#3d5570;text-align:center;">Référentiel<br><span style="color:#ffad1f;">MIT Center for Transportation & Logistics</span></div>', unsafe_allow_html=True)

# ── EN-TÊTE ──
st.markdown('<div class="page-header"><div class="page-tag">🚛 Transport Management System · GDIZ</div><h1 class="page-title">TMS <span>Logistics</span></h1><p class="page-sub">Pilotage & Optimisation · Axe Usine X (GDIZ) → Malanville · Modèles MIT CTL</p></div>', unsafe_allow_html=True)

# ══ MODULE 1 — ROI ÉNERGÉTIQUE ══
st.markdown('<p class="section-title">⛽ Efficacité Énergétique & ROI Social</p><div class="section-bar"></div>', unsafe_allow_html=True)
with st.expander("⚙️ Paramètres du modèle MIT SC0x", expanded=True):
    c1,c2,c3 = st.columns(3)
    n_camions  = c1.number_input("Flotte (camions)",          min_value=1,   max_value=500,   value=10,   step=1)
    d_actuelle = c2.number_input("Distance actuelle (km/j)",  min_value=1.0, max_value=2000., value=80.0, step=1.0)
    d_opti     = c2.number_input("Distance optimisée (km/j)", min_value=1.0, max_value=2000., value=65.0, step=1.0)
    jours      = c3.number_input("Jours d'activité / an",     min_value=1,   max_value=365,   value=300,  step=1)
    conso      = c3.number_input("Consommation (L/100km)",    min_value=1.0, max_value=100.,  value=32.0, step=0.5, help="Typique camion lourd Bénin : 28–35 L/100km")

if d_opti >= d_actuelle:
    st.warning("⚠️ La distance optimisée doit être inférieure à la distance actuelle.")
    gain_km_annuel = economie_fcfa = co2_evite = 0.0
else:
    gain_km_annuel = (d_actuelle - d_opti) * n_camions * jours
    economie_fcfa  = gain_km_annuel * (conso / 100) * PRIX_CARBURANT
    co2_evite      = gain_km_annuel * (conso / 100) * CO2_PAR_LITRE

k1,k2,k3,k4 = st.columns(4)
k1.metric("💰 Économie annuelle",   f"{economie_fcfa:,.0f} FCFA")
k2.metric("📏 Distance sauvée",     f"{gain_km_annuel:,.0f} km/an")
k3.metric("🌿 CO₂ évité",           f"{co2_evite:,.0f} kg")
k4.metric("👷 Emplois finançables", f"{int(economie_fcfa//SALAIRE_ANNUEL)}" if economie_fcfa>0 else "0", help=f"Base : {SALAIRE_ANNUEL:,} FCFA/an/employé")
if economie_fcfa > 0:
    st.success(f"✅ Économie de **{economie_fcfa:,.0f} FCFA/an** → **{int(economie_fcfa//SALAIRE_ANNUEL)} poste(s)** de travail local.")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ══ MODULE 2 — DOCKING ══
st.markdown('<p class="section-title">🏢 Gestion du Docking — Usine X · GDIZ</p><div class="section-bar"></div>', unsafe_allow_html=True)
col_left, col_right = st.columns([1, 1.6], gap="large")

with col_left:
    with st.form("form_docking", clear_on_submit=True):
        st.markdown("**Enregistrer une opération**")
        camion_immat = st.text_input("Immatriculation",     placeholder="Ex : RB 1234 BJ")
        marchand_d   = st.selectbox("Marchandise",          MARCHANDISES, key="march_dock")
        tonnage_d    = st.number_input("Tonnage (T)",       min_value=0.1, max_value=70.0, value=25.0, step=0.5, key="ton_dock")
        flux_op      = st.radio("Opération",                ["Chargement","Déchargement"], horizontal=True)
        quai_sel     = st.selectbox("Quai assigné",         st.session_state.quais["Quai"].tolist())
        submitted_d  = st.form_submit_button("✅ Valider l'opération")
    if submitted_d:
        if not camion_immat.strip():
            st.error("❌ Veuillez saisir une immatriculation.")
        else:
            ic = camion_immat.strip().upper()
            mask = st.session_state.quais["Quai"] == quai_sel
            st.session_state.quais.loc[mask, ["Statut","Camion","Marchand.","Opération"]] = ["Occupé", ic, marchand_d, flux_op]
            st.session_state.db_dock = pd.concat([st.session_state.db_dock, pd.DataFrame([{"Heure":datetime.now().strftime("%H:%M"),"Camion":ic,"Marchandise":marchand_d,"Tonnage (T)":tonnage_d,"Opération":flux_op,"Quai":quai_sel}])], ignore_index=True)
            st.session_state.docking_log.append(f"✔ {ic} · {marchand_d} · {flux_op} · Quai {quai_sel}")
            st.success(f"Opération validée : **{ic}** → Quai **{quai_sel}**")
    st.markdown("**Libérer un quai**")
    quai_lib = st.selectbox("Quai à libérer", st.session_state.quais["Quai"].tolist(), key="lib_quai")
    if st.button("🔓 Libérer le quai"):
        st.session_state.quais.loc[st.session_state.quais["Quai"]==quai_lib, ["Statut","Camion","Marchand.","Opération"]] = ["Libre","—","—","—"]
        st.success(f"Quai **{quai_lib}** libéré.")

with col_right:
    st.markdown("**État des quais en temps réel**")
    rows_html = ""
    for _, row in st.session_state.quais.iterrows():
        b = '<span style="background:rgba(255,80,80,.15);color:#ff5050;font-size:11px;font-weight:700;padding:3px 10px;border-radius:12px;">🔴 Occupé</span>' if row["Statut"]=="Occupé" else '<span style="background:rgba(0,196,167,.15);color:#00c4a7;font-size:11px;font-weight:700;padding:3px 10px;border-radius:12px;">🟢 Libre</span>'
        rows_html += f'<tr><td><strong>{row["Quai"]}</strong></td><td>{b}</td><td style="color:#8fa3c0;">{row["Camion"]}</td><td style="color:#8fa3c0;">{row["Marchand."]}</td><td style="color:#8fa3c0;">{row["Opération"]}</td></tr>'
    st.markdown(f'<div class="card" style="padding:20px;"><table class="quai-table"><thead><tr><th>Quai</th><th>Statut</th><th>Camion</th><th>Marchandise</th><th>Opération</th></tr></thead><tbody>{rows_html}</tbody></table></div>', unsafe_allow_html=True)
    if not st.session_state.db_dock.empty:
        t1,t2 = st.columns(2)
        t1.metric("Tonnage journalier", f"{st.session_state.db_dock['Tonnage (T)'].sum():,.1f} T")
        t2.metric("Opérations du jour", len(st.session_state.db_dock))
        st.markdown("**5 dernières opérations**")
        st.dataframe(st.session_state.db_dock.tail(5)[["Heure","Camion","Marchandise","Tonnage (T)","Opération","Quai"]], use_container_width=True)
    if st.session_state.docking_log:
        st.markdown("**Journal des accès**")
        for log in reversed(st.session_state.docking_log[-5:]):
            st.markdown(f'<div style="font-size:12px;color:#7a92b0;padding:4px 0;border-bottom:1px solid rgba(255,255,255,.05);">{log}</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ══ MODULE 3 — TRACKING ══
st.markdown('<p class="section-title">📦 Suivi des Expéditions</p><div class="section-bar"></div>', unsafe_allow_html=True)
col_form, col_info = st.columns([1, 1.6], gap="large")

with col_form:
    with st.form("form_tracking", clear_on_submit=True):
        st.markdown("**Enregistrer / mettre à jour**")
        id_exp     = st.text_input("Référence expédition",        placeholder="Ex : EXP-GDIZ-105")
        marchand_t = st.selectbox("Marchandise",                  MARCHANDISES, key="march_track")
        tonnage_t  = st.number_input("Tonnage (T)",               min_value=0.1, max_value=70.0, value=20.0, step=0.5, key="ton_track")
        position   = st.selectbox("Dernière position constatée",  LISTE_VILLES)
        statut     = st.selectbox("Statut",                       STATUTS)
        submit_t   = st.form_submit_button("📍 Actualiser le tracking")
    if submit_t:
        if not id_exp.strip():
            st.error("❌ Veuillez saisir une référence d'expédition.")
        else:
            id_clean, heure = id_exp.strip().upper(), datetime.now().strftime("%H:%M")
            if id_clean in st.session_state.db_tms["ID"].values:
                mask = st.session_state.db_tms["ID"] == id_clean
                st.session_state.db_tms.loc[mask, ["Marchandise","Tonnage (T)","Position","Statut","Heure MAJ"]] = [marchand_t, tonnage_t, position, statut, heure]
                st.success(f"✅ Expédition **{id_clean}** mise à jour.")
            else:
                st.session_state.db_tms = pd.concat([st.session_state.db_tms, pd.DataFrame([{"ID":id_clean,"Marchandise":marchand_t,"Tonnage (T)":tonnage_t,"Position":position,"Statut":statut,"Heure MAJ":heure}])], ignore_index=True)
                st.success(f"✅ Expédition **{id_clean}** ajoutée.")

with col_info:
    df_t = st.session_state.db_tms[st.session_state.db_tms["Statut"]=="En Transit"]
    if not df_t.empty:
        d = df_t.iloc[-1]
        km = VILLES_BENIN.get(d["Position"], 0)
        st.markdown(f'<div class="card"><div style="font-size:11px;color:#5a7090;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;">Dernière expédition en transit</div><div style="font-family:Syne,sans-serif;font-size:20px;font-weight:700;color:#fff;margin-bottom:4px;">{d["ID"]}</div><div style="font-size:13px;color:#8fa3c0;margin-bottom:4px;">{d["Marchandise"]}</div><div style="font-size:12px;color:#5a7090;margin-bottom:14px;">{d["Tonnage (T)"]} T · MAJ {d["Heure MAJ"]}</div><div style="font-size:13px;color:#c8d8ec;">📍 <strong>{d["Position"]}</strong> · {km} km / {DISTANCE_MAX} km</div></div>', unsafe_allow_html=True)
        st.progress(min(km / DISTANCE_MAX, 1.0))
        st.caption(f"Progression vers Malanville : {min(km/DISTANCE_MAX,1.0)*100:.1f}%")
    else:
        st.info("Aucune expédition en transit actuellement.")

st.markdown("**📋 Dashboard opérationnel**")
filtre = st.selectbox("Filtrer par statut", ["Tous"] + STATUTS, key="filtre_statut")
df_display = st.session_state.db_tms if filtre == "Tous" else st.session_state.db_tms[st.session_state.db_tms["Statut"]==filtre]
st.info("Aucune expédition pour ce filtre.") if df_display.empty else st.dataframe(df_display.reset_index(drop=True), use_container_width=True)

db = st.session_state.db_tms
s1,s2,s3,s4,s5 = st.columns(5)
s1.metric("Total expéditions", len(db))
s2.metric("En Transit",        len(db[db["Statut"]=="En Transit"]))
s3.metric("Livrées",           len(db[db["Statut"]=="Livré"]))
s4.metric("Incidents",         len(db[db["Statut"]=="Incident"]))
s5.metric("Tonnage total",     f"{db['Tonnage (T)'].sum():,.1f} T")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;"><span style="font-size:12px;color:#3d5570;">© 2025 <span style="color:#ffad1f;font-weight:500;">West Africa Logistics Hub</span> · TMS Module</span><span style="font-size:12px;color:#3d5570;">Propulsé par <span style="color:#ffad1f;font-weight:500;">Streamlit</span> · Référentiel <span style="color:#ffad1f;font-weight:500;">MIT CTL</span></span></div>', unsafe_allow_html=True)

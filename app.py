import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="West Africa Logistics Hub", 
    layout="wide", 
    page_icon="🌍"
)

# 2. STYLE PROFESSIONNEL (HUB)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        font-weight: bold; 
        height: 6em; 
        font-size: 20px;
        border: 1px solid #dee2e6;
        transition: 0.3s;
    }
    .stButton>button:hover {
        border-color: #1E3A8A;
        color: #1E3A8A;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .title-text { text-align: center; color: #1E3A8A; font-weight: 800; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. CONTENU DE LA PAGE D'ACCUEIL
st.markdown("<h1 class='title-text'>🌍 West Africa Logistics Hub</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #6B7280;'>Plateforme Intégrée de Pilotage : Usine X - Bénin</h3>", unsafe_allow_html=True)
st.write("---")

st.info("### 🚀 Bienvenue dans votre Tour de Contrôle Logistique")
st.write("""
Cette solution centralise vos opérations pour une efficacité maximale. 
Utilisez le menu latéral à gauche pour naviguer ou les accès rapides ci-dessous :
""")

st.write("##")

# 4. ACCÈS RAPIDES (Colonnes)
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 🚛 Module TMS Logistics")
    st.write("""
    - **Docking :** Gestion des entrées/sorties Usine X.
    - **Tonnage :** Suivi par filière (Coton, Soja, Acajou, etc.).
    - **Tracking :** Suivi territorial en temps réel au Bénin.
    - **ROI :** Optimisation des coûts de carburant.
    """)
    st.caption("👈 Cliquez sur **1_🚛_TMS_Logistics** dans le menu")

with col2:
    st.markdown("### 📦 Module WMS Logistics")
    st.write("""
    - **Inventaire :** Analyse en temps réel de l'état du stock.
    - **Analyse ABC :** Classification stratégique par valeur.
    - **Satisfaction :** Ajustement automatique du taux de service.
    - **Achat :** Plan de réapprovisionnement automatique.
    """)
    st.caption("👈 Cliquez sur **2_📦_WMS_Logistics** dans le menu")

st.write("---")

# 5. SECTION EXPERTISE
st.markdown("#### 💡 Intelligence de Flux")
st.success("""
**Note Stratégique :** Ce Hub intègre une logique d'optimisation du cash-flow. 
Le WMS protège vos articles de Classe A (Satisfaction 98%) tandis que le TMS optimise le coût à la tonne-kilomètre.
""")

st.write("##")
st.markdown("<p style='text-align: center; color: gray;'>Développé par Elvis – Expertise Supply Chain & Pilotage de Flux</p>", unsafe_allow_html=True)

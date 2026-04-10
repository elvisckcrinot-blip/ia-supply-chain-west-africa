import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="West Africa Logistics Hub",
    page_icon="🌍",
    layout="wide"
)

# 2. ACCUEIL ET TITRE
st.title("🌍 West Africa Logistics Hub")
st.markdown("---")

st.header("Bienvenue dans votre interface de pilotage")
st.write("Cette plateforme centralise vos solutions technologiques pour la Supply Chain au Bénin.")

# 3. PANNEAU DE NAVIGATION (TMS & WMS)
col1, col2 = st.columns(2)

with col1:
    st.info("### 🚛 TMS Logistics")
    st.write("**Transport Management System**")
    st.write("- Gestion du Docking (GDIZ)\n- Optimisation du carburant\n- Suivi des marchandises (Tracking)")
    st.write("👈 *Accédez au module dans le menu à gauche*")

with col2:
    st.success("### 📦 WMS Logistics")
    st.write("**Warehouse Management System**")
    st.write("- Gestion d'entrepôt\n- Simulation de scénarios stratégiques\n- Plan de réapprovisionnement")
    st.write("👈 *Accédez au module dans le menu à gauche*")

# 4. BARRE LATÉRALE (SIDEBAR)
st.sidebar.title("Navigation")
st.sidebar.success("Ouvrez le menu '>>' pour changer de module.")
st.sidebar.markdown("---")
st.sidebar.write("👤 **Utilisateur :** Elvis")
st.sidebar.write("🎓 **Expertise :** MIT CTL Models")

# 5. NOTE STRATÉGIQUE (L'UPPERCUT)
st.markdown("---")
with st.expander("🔍 Pourquoi cette solution est-elle unique ?"):
    st.write("""
    Contrairement aux logiciels classiques (ERP/WMS standards), cette plateforme intègre :
    1. **L'Optimisation Mathématique :** Modèles du MIT pour réduire les distances de 15% à 20%.
    2. **Le ROI Social :** Chaque gain de carburant est converti en capacité d'embauche.
    3. **La Résilience :** Simulateur de crises (retards ports, hausses demande) pour protéger votre CA.
    """)
    

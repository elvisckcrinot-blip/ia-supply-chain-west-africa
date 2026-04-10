import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="West Africa Logistics Hub",
    page_icon="🌍",
    layout="wide"
)

# 2. DESIGN DE L'ACCUEIL
st.title("🌍 West Africa Logistics Hub")
st.markdown("---")

st.header("Interface de Pilotage Stratégique")
st.write("Bienvenue Elvis. Cette plateforme centralise vos solutions technologiques basées sur les modèles d'excellence du MIT CTL.")

# 3. MISE EN AVANT DU TMS (TON CHEF-D'ŒUVRE)
st.info("### 🚛 TMS Logistics : Transport Management System")
col1, col2 = st.columns([2, 1])

with col1:
    st.write("""
    **Capacités opérationnelles :**
    *   **Gestion du Docking :** Contrôle des flux d'entrée et occupation des quais à la GDIZ.
    *   **Optimisation MIT SC0x :** Réduction des distances et transformation des gains de carburant en capital humain.
    *   **Suivi GPS Territorial :** Localisation précise des marchandises sur l'axe Cotonou-Malanville.
    """)
    st.markdown("👈 **Accédez au module complet via le menu latéral [ >> ]**")

with col2:
    st.metric("ROI Social Estimé", "3 780 000 FCFA", delta="Gain/an/10 camions")
    st.caption("Économie réinjectable dans la création d'emplois locaux.")

st.markdown("---")

# 4. RAPPEL DU WMS
st.success("### 📦 WMS Logistics : Warehouse Management System")
st.write("Gestion avancée de l'inventaire, simulation de scénarios de crise et planification automatique des commandes.")

# 5. PIED DE PAGE PROFESSIONNEL
st.sidebar.title("Navigation")
st.sidebar.info("Utilisez le menu ci-dessus pour naviguer entre le TMS et le WMS.")
st.sidebar.markdown("---")
st.sidebar.write("🎓 **Méthodologie :** MIT MicroMaster SCM")
st.sidebar.write("📍 **Localisation :** Bénin (GDIZ)")
    

import streamlit as st

# 1. CONFIGURATION DE LA PAGE (Doit être la toute première ligne)
st.set_page_config(
    page_title="Hub Logistique Afrique de l'Ouest",
    page_icon="🌍",
    layout="wide"
)

# 2. DESIGN DE LA PAGE D'ACCUEIL
st.title("🌍 Plateforme Logistique Intégrée")
st.markdown("---")

st.header("Bienvenue dans votre interface de pilotage")
st.write("Cette application centralise vos solutions logistiques pour le Bénin.")

# 3. PANNEAU D'ORIENTATION
col1, col2 = st.columns(2)

with col1:
    st.info("### 🚛 GDIZ Smart Docking")
    st.write("Gestion des flux de camions et optimisation des accès usines en temps réel.")
    if st.button("Accéder au Docking"):
        st.switch_page("app.py")

with col2:
    st.success("### 📦 INGCO BÉNIN")
    st.write("Optimisation des stocks (500 articles), gestion des conteneurs et calculs MIT.")
    st.write("👈 *Cliquez sur 'INGCO' dans le menu à gauche*")

# 4. MESSAGE D'AIDE
st.sidebar.success("Sélectionnez un module ci-dessus")
st.sidebar.markdown("---")
st.sidebar.write("👤 Utilisateur : Elvis")
      

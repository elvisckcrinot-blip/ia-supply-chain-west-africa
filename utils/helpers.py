import pandas as pd
import streamlit as st

# =================================================================
# SECTION 1 : CHARGEMENT ET RÉCUPÉRATION (DATA PIPELINE)
# =================================================================

def load_logistics_data(file_path):
    """
    Charge les données logistiques avec gestion d'erreurs avancée.
    Supporte les formats standards : CSV, XLSX, XLS.
    """
    try:
        if file_path.name.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"❌ Échec de lecture : Vérifiez le format du fichier. Détails : {e}")
        return None

# =================================================================
# SECTION 2 : PRÉ-TRAITEMENT ACADÉMIQUE (MIT SC0x READY)
# =================================================================

def preprocess_for_mit(df):
    """
    Nettoyage rigoureux des données pour les moteurs de calcul.
    Vérifie la présence et la validité des colonnes critiques.
    """
    if df is None: return None
    
    # Standardisation des noms de colonnes (retrait des espaces et majuscules)
    df.columns = [c.strip() for c in df.columns]
    
    # Identification des colonnes numériques critiques
    cols_numeriques = ['Valeur', 'Prix', 'Quantité', 'ROP_Seuil']
    for col in cols_numeriques:
        if col in df.columns:
            # Conversion forcée en numérique (remplace les erreurs par NaN)
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Suppression des lignes corrompues sur les piliers du calcul
    # On garde les lignes où le calcul du profit ou du stock est possible
    df = df.dropna(subset=[c for c in ['Prix', 'Quantité'] if c in df.columns])
    
    return df

# =================================================================
# SECTION 3 : COMPOSANTS VISUELS (UI HELPERS)
# =================================================================

def apply_ui_theme():
    """Injecte les variables de style pour les cartes et boutons."""
    st.markdown("""
        <style>
        .stMetric { border: 1px solid rgba(255,173,31,0.2); padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.1); }
        .stDataFrame { border: 1px solid rgba(255,255,255,0.1); border-radius: 5px; }
        </style>
    """, unsafe_allow_html=True)
    

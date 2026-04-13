import pandas as pd
import streamlit as st
import psycopg2

# =================================================================
# SECTION 1 : CONNEXION BASE DE DONNÉES (POSTGRESQL / NEON)
# =================================================================

def init_connection():
    """Initialise la connexion en utilisant les Secrets de Streamlit."""
    try:
        return psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            port=st.secrets["postgres"]["port"],
            database=st.secrets["postgres"]["database"],
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"]
        )
    except Exception as e:
        st.error(f"❌ Erreur de connexion à la base de données : {e}")
        return None

def get_data(query):
    """Exécute une requête SQL et retourne un DataFrame Pandas."""
    conn = init_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"❌ Erreur lors de la récupération des données : {e}")
            return None
    return None

# =================================================================
# SECTION 2 : CHARGEMENT DE FICHIERS (BACKUP / IMPORT)
# =================================================================

def load_logistics_data(file_path):
    """Charge les données depuis un fichier CSV ou Excel."""
    try:
        if file_path.name.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"❌ Échec de lecture du fichier : {e}")
        return None

# =================================================================
# SECTION 3 : PRÉ-TRAITEMENT ACADÉMIQUE (MIT SC0x READY)
# =================================================================

def preprocess_for_mit(df):
    """Nettoyage rigoureux des données pour les moteurs de calcul."""
    if df is None: return None
    
    # Standardisation des colonnes
    df.columns = [c.strip() for c in df.columns]
    
    # Conversion numérique forcée
    cols_numeriques = ['Valeur', 'Prix', 'Quantité', 'ROP_Seuil', 'prix_unitaire', 'quantite_actuelle']
    for col in cols_numeriques:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Nettoyage des lignes vides sur les colonnes critiques
    cols_critiques = [c for c in ['Prix', 'Quantité', 'prix_unitaire', 'quantite_actuelle'] if c in df.columns]
    if cols_critiques:
        df = df.dropna(subset=cols_critiques)
    
    return df

# =================================================================
# SECTION 4 : COMPOSANTS VISUELS (UI HELPERS)
# =================================================================

def apply_ui_theme():
    """Injecte le style visuel pour les cartes et les tableaux."""
    st.markdown("""
        <style>
        .stMetric { border: 1px solid rgba(255,173,31,0.2); padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.1); }
        .stDataFrame { border: 1px solid rgba(255,255,255,0.1); border-radius: 5px; }
        div.stButton > button { font-weight: bold; border-radius: 8px; }
        </style>
    """, unsafe_allow_html=True)
            

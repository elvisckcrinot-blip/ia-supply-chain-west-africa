import pandas as pd
import streamlit as st
import psycopg2

# =================================================================
# SECTION 1 : CONNEXION & ECRITURE BASE DE DONNÉES (POSTGRESQL)
# =================================================================

def init_connection():
    """ 
    Connexion Ultime Neon : Intégration de l'Endpoint ID dans le User.
    Résout les erreurs SNI et Endpoint ID non spécifié sans SQLAlchemy.
    """
    try:
        host = st.secrets["postgres"]["host"]
        user = st.secrets["postgres"]["user"]
        password = st.secrets["postgres"]["password"]
        database = st.secrets["postgres"]["database"]
        port = st.secrets["postgres"]["port"]
        
        # Extraction précise de l'endpoint_id (ex: ep-steep-glitter-...)
        endpoint_id = host.split('.')[0]
        
        # TECHNIQUE NEON : Combiner l'identifiant et l'utilisateur avec '$'
        user_with_endpoint = f"{endpoint_id}${user}"
        
        return psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user_with_endpoint,
            password=password,
            sslmode="require"
        )
    except Exception as e:
        st.error(f"❌ Échec de la connexion sécurisée : {e}")
        return None

def get_data(query):
    """Exécute une requête SQL de lecture et retourne un DataFrame."""
    conn = init_connection()
    if conn:
        try:
            # On utilise pandas avec la connexion psycopg2 brute
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"❌ Erreur lors de la récupération : {e}")
            if conn: conn.close()
            return None
    return None

def save_optimization_result(camion_id, destination, cout_estime, statut="Planifié"):
    """Enregistre un résultat d'optimisation dans historique_trajets."""
    conn = init_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = """
                INSERT INTO historique_trajets (camion_id, destination, cout_estime, statut_livraison)
                VALUES (%s, %s, %s, %s)
            """
            cur.execute(query, (camion_id, destination, cout_estime, statut))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            st.error(f"❌ Erreur lors de l'enregistrement : {e}")
            if conn: conn.close()
            return False
    return False

# =================================================================
# SECTION 2 : CHARGEMENT DE FICHIERS (IMPORT EXCEL/CSV)
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
    
    # Nettoyage des lignes vides
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
    

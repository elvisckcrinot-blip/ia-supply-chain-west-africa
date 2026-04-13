import pandas as pd
import streamlit as st
import psycopg2

# =================================================================
# SECTION 1 : CONNEXION & ECRITURE BASE DE DONNÉES (POSTGRESQL)
# =================================================================

def init_connection():
    """ Initialise la connexion vers Neon avec SSL et Endpoint ID. """
    try:
        # On récupère l'identifiant du projet (endpoint) depuis l'hôte
        host = st.secrets["postgres"]["host"]
        # On extrait la première partie de l'URL (ex: ep-steep-glitter-...)
        endpoint_id = host.split('.')[0]
        
        return psycopg2.connect(
            host=host,
            port=st.secrets["postgres"]["port"],
            database=st.secrets["postgres"]["database"],
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"],
            # AJOUT DU MODE SSL (Exigence Neon pour la sécurité)
            sslmode="require",
            # Correction SNI Support (Réveil du serveur Neon)
            options=f"-c endpointn={endpoint_id}"
        )
    except Exception as e:
        st.error(f"❌ Erreur de connexion à la base de données : {e}")
        return None

def get_data(query):
    """Exécute une requête SQL de lecture et retourne un DataFrame."""
    conn = init_connection()
    if conn:
        try:
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
            st.error(f"❌ Erreur lors de l'enregistrement du trajet : {e}")
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
            

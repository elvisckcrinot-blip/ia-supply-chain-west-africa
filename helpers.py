import pandas as pd
import streamlit as st
import pg8000.native

def init_connection():
    """Initialise la connexion à la base de données Neon PostgreSQL."""
    try:
        host = st.secrets["postgres"]["host"]
        user = st.secrets["postgres"]["user"]
        password = st.secrets["postgres"]["password"]
        database = st.secrets["postgres"]["database"]
        port = st.secrets["postgres"]["port"]
        
        # Formatage spécifique pour Neon (endpoint ID dans le user)
        endpoint_id = host.split('.')[0].replace('-pooler', '')
        user_neon = f"{user}@{endpoint_id}"

        conn = pg8000.native.Connection(
            host=host,
            port=int(port),
            database=database,
            user=user_neon,
            password=password,
            ssl_context=True
        )
        return conn
    except Exception as e:
        st.error(f"❌ Échec de la connexion sécurisée : {e}")
        return None

def get_data(query):
    """Exécute une requête de lecture et retourne un DataFrame."""
    conn = init_connection()
    if conn:
        try:
            rows = conn.run(query)
            cols = [col["name"] for col in conn.columns]
            conn.close()
            return pd.DataFrame(rows, columns=cols)
        except Exception as e:
            st.error(f"❌ Erreur lors de la récupération : {e}")
            return None
    return None

def save_optimization_result(camion_id, destination, cout_estime, statut="Planifié"):
    """Enregistre un résultat d'optimisation dans l'historique."""
    conn = init_connection()
    if conn:
        try:
            conn.run(
                "INSERT INTO historique_trajets (camion_id, destination, cout_estime, statut_livraison) VALUES (:1, :2, :3, :4)",
                camion_id, destination, cout_estime, statut
            )
            conn.close()
            return True
        except Exception as e:
            st.error(f"❌ Erreur lors de l'enregistrement : {e}")
            return False
    return False

def load_logistics_data(file_path):
    """Charge un fichier CSV ou Excel."""
    try:
        if file_path.name.endswith('.csv'):
            return pd.read_csv(file_path)
        else:
            return pd.read_excel(file_path)
    except Exception as e:
        st.error(f"❌ Échec de lecture du fichier : {e}")
        return None

def preprocess_for_mit(df):
    """Nettoie et convertit les types de données pour l'analyse."""
    if df is None: return None
    df.columns = [c.strip() for c in df.columns]
    
    cols_numeriques = ['Valeur', 'Prix', 'Quantité', 'ROP_Seuil', 'prix_unitaire', 'quantite_actuelle']
    for col in cols_numeriques:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    cols_critiques = [c for c in ['Prix', 'Quantité', 'prix_unitaire', 'quantite_actuelle'] if c in df.columns]
    if cols_critiques:
        df = df.dropna(subset=cols_critiques)
    return df

def apply_ui_theme():
    """Applique le style CSS personnalisé à l'interface Streamlit."""
    st.markdown("""
        <style>
        .stMetric { 
            border: 1px solid rgba(255,173,31,0.2); 
            padding: 15px; 
            border-radius: 10px; 
            background: rgba(0,0,0,0.1); 
        }
        .stDataFrame { 
            border: 1px solid rgba(255,255,255,0.1); 
            border-radius: 5px; 
        }
        div.stButton > button { 
            font-weight: bold; 
            border-radius: 8px; 
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
            

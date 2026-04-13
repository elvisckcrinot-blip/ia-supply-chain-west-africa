import pandas as pd
import streamlit as st
import psycopg2

def init_connection():
    try:
        host = st.secrets["postgres"]["host"]
        user = st.secrets["postgres"]["user"]
        password = st.secrets["postgres"]["password"]
        database = st.secrets["postgres"]["database"]
        port = st.secrets["postgres"]["port"]
        endpoint_id = host.split('.')[0]
        conn_string = (
            f"postgresql://{user}:{password}@{host}:{port}/{database}"
            f"?options=endpoint%3D{endpoint_id}&sslmode=require"
        )
        return psycopg2.connect(conn_string)
    except Exception as e:
        try:
            host = st.secrets["postgres"]["host"]
            user = st.secrets["postgres"]["user"]
            password = st.secrets["postgres"]["password"]
            database = st.secrets["postgres"]["database"]
            port = st.secrets["postgres"]["port"]
            endpoint_id = host.split('.')[0]
            user_with_endpoint = f"{endpoint_id}${user}"
            return psycopg2.connect(
                host=host,
                port=int(port),
                database=database,
                user=user_with_endpoint,
                password=password,
                sslmode="require"
            )
        except Exception as e2:
            st.error(f"❌ Échec de la connexion sécurisée : {e2}")
            return None

def get_data(query):
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

def load_logistics_data(file_path):
    try:
        if file_path.name.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"❌ Échec de lecture du fichier : {e}")
        return None

def preprocess_for_mit(df):
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
    st.markdown("""
        <style>
        .stMetric { border: 1px solid rgba(255,173,31,0.2); padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.1); }
        .stDataFrame { border: 1px solid rgba(255,255,255,0.1); border-radius: 5px; }
        div.stButton > button { font-weight: bold; border-radius: 8px; }
        </style>
    """, unsafe_allow_html=True)
        

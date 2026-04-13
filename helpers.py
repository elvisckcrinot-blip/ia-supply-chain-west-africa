import pandas as pd
import streamlit as st

# --- CONFIGURATION DE LA BASE DE DONNÉES (DÉSACTIVÉE) ---

def get_data(query):
    """
    Simule la récupération de données. 
    Retourne None pour éviter les erreurs de connexion Neon.
    """
    return None

def save_optimization_result(camion_id, destination, cout_estime, statut="Planifié"):
    """
    Simule l'enregistrement.
    Désactivé pour passer l'erreur d'authentification.
    """
    return False

# --- LOGISTIQUE & TRAITEMENT DE DONNÉES ---

def load_logistics_data(file_path):
    """Charge un fichier CSV ou Excel de manière sécurisée."""
    try:
        if file_path.name.endswith('.csv'):
            return pd.read_csv(file_path)
        else:
            return pd.read_excel(file_path)
    except Exception as e:
        st.error(f"❌ Échec de lecture du fichier : {e}")
        return None

def preprocess_for_mit(df):
    """Nettoie et convertit les colonnes logistiques en nombres exploitables."""
    if df is None: 
        return None
    
    # Nettoyage des noms de colonnes (supprime les espaces invisibles)
    df.columns = [c.strip() for c in df.columns]
    
    # Conversion forcée en numérique pour les colonnes clés
    cols_numeriques = [
        'Valeur', 'Prix', 'Quantité', 'ROP_Seuil', 
        'prix_unitaire', 'quantite_actuelle'
    ]
    for col in cols_numeriques:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Suppression des lignes où les données vitales sont manquantes
    cols_critiques = [c for c in ['Prix', 'Quantité', 'prix_unitaire', 'quantite_actuelle'] if c in df.columns]
    if cols_critiques:
        df = df.dropna(subset=cols_critiques)
    
    return df

# --- INTERFACE UTILISATEUR (UI) ---

def apply_ui_theme():
    """Applique le style visuel sombre et moderne (TMS Logistics)."""
    st.markdown("""
        <style>
        /* Style des cartes de métriques */
        .stMetric { 
            border: 1px solid rgba(255,173,31,0.2); 
            padding: 15px; 
            border-radius: 10px; 
            background: rgba(0,0,0,0.1); 
        }
        /* Style des tableaux de données */
        .stDataFrame { 
            border: 1px solid rgba(255,255,255,0.1); 
            border-radius: 5px; 
        }
        /* Style des boutons */
        div.stButton > button { 
            font-weight: bold; 
            border-radius: 8px; 
            background-color: #ffad1f; 
            color: black;
            border: none;
            width: 100%;
        }
        div.stButton > button:hover {
            background-color: #e6991a;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    

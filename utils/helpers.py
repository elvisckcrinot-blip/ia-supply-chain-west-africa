import pandas as pd
import streamlit as st

def load_logistics_data(file_path):
    """
    Charge les données depuis le dossier data/raw/
    Supporte CSV et Excel.
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        return None

def preprocess_for_mit(df):
    """
    Nettoie les données pour les calculs MIT (Wilson/Pareto).
    Assure que les colonnes numériques sont propres.
    """
    # Exemple : suppression des lignes sans prix ou sans quantité
    df = df.dropna(subset=['Prix', 'Quantité'])
    return df
  

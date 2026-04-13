import numpy as np
import pandas as pd

# =================================================================
# SECTION WMS : GESTION DES STOCKS (Référentiel MIT SC0x)
# =================================================================

def calcul_wilson_eoq(demande_annuelle, cout_commande, cout_stockage):
    """
    Modèle de Wilson (Economic Order Quantity).
    Objectif : Minimiser la somme des coûts de commande et de possession.
    """
    try:
        if demande_annuelle <= 0 or cout_stockage <= 0: 
            return 0
        # Formule racine(2DS/H)
        eoq = np.sqrt((2 * demande_annuelle * cout_commande) / cout_stockage)
        return int(np.round(eoq))
    except Exception:
        return 0

def calcul_point_de_commande(demande_moyenne, delai_fournisseur, stock_securite):
    """
    Calcul du Reorder Point (ROP).
    Déclenche le réapprovisionnement pour éviter la rupture pendant le Lead Time.
    """
    return int((demande_moyenne * delai_fournisseur) + stock_securite)

def analyse_pareto_abc(df, colonne_valeur):
    """
    Analyse de Pareto (Loi des 80/20).
    Segmentation stratégique : 
    A (80% valeur), B (15% valeur), C (5% valeur).
    """
    if df.empty: 
        return df
    
    # Tri par valeur décroissante
    df = df.sort_values(by=colonne_valeur, ascending=False).copy()
    
    # Calcul des cumuls
    total_valeur = df[colonne_valeur].sum()
    if total_valeur == 0:
        df['Classe_ABC'] = 'C'
        return df
        
    df['cum_sum'] = df[colonne_valeur].cumsum()
    df['cum_perc'] = 100 * df['cum_sum'] / total_valeur
    
    def assign_abc(perc):
        if perc <= 80: return 'A'
        elif perc <= 95: return 'B'
        else: return 'C'
        
    df['Classe_ABC'] = df['cum_perc'].apply(assign_abc)
    return df

# =================================================================
# SECTION TMS : TRANSPORT & KPI (Référentiel MIT SC1x)
# =================================================================

def calcul_cout_transport(distance, consommation_moyenne, prix_carburant, cout_fixe):
    """
    Modélisation du coût de revient d'un trajet (Linehaul Cost).
    Inclut l'analyse de l'empreinte carbone (Sustainability KPI).
    """
    try:
        carburant_total = (distance / 100) * consommation_moyenne
        cout_carburant = carburant_total * prix_carburant
        cout_total = cout_carburant + cout_fixe
        
        # Facteur d'émission standard (MIT SC0x) : ~2.68 kg CO2 par litre de diesel
        emissions_co2 = carburant_total * 2.68
        
        return int(cout_total), round(emissions_co2, 2)
    except ZeroDivisionError:
        return 0, 0.0

def calcul_rentabilite_flotte(cout_trajet, tarif_client, camions_jour):
    """
    Analyse du ROI (Return on Investment) annuel.
    Simulation basée sur une exploitation continue (360 jours).
    """
    profit_par_trajet = tarif_client - cout_trajet
    # Calcul de la marge nette annuelle
    profit_annuel = profit_par_trajet * camions_jour * 360
    return int(profit_annuel)
    

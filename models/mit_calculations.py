import numpy as np

# --- FONCTIONS WMS (Warehouse) ---

def calcul_wilson_eoq(demande_annuelle, cout_commande, cout_stockage):
    if demande_annuelle <= 0 or cout_stockage <= 0: return 0
    eoq = np.sqrt((2 * demande_annuelle * cout_commande) / cout_stockage)
    return int(eoq)

def calcul_point_de_commande(demande_moyenne, delai_fournisseur, stock_securite):
    return int((demande_moyenne * delai_fournisseur) + stock_securite)

def analyse_pareto_abc(df, colonne_valeur):
    """
    Segmentation ABC selon Pareto : indispensable pour le WMS.
    """
    df = df.sort_values(by=colonne_valeur, ascending=False)
    df['cum_sum'] = df[colonne_valeur].cumsum()
    df['cum_perc'] = 100 * df['cum_sum'] / df[colonne_valeur].sum()
    
    def assign_abc(perc):
        if perc <= 80: return 'A'
        elif perc <= 95: return 'B'
        else: return 'C'
        
    df['Classe_ABC'] = df['cum_perc'].apply(assign_abc)
    return df

# --- FONCTIONS TMS (Transport) ---

def calcul_cout_transport(distance, consommation_moyenne, prix_carburant, cout_fixe):
    carburant_total = (distance / 100) * consommation_moyenne
    cout_carburant = carburant_total * prix_carburant
    cout_total = cout_carburant + cout_fixe
    emissions_co2 = carburant_total * 2.68
    return int(cout_total), round(emissions_co2, 2)

def calcul_rentabilite_flotte(cout_trajet, tarif_client, camions_jour):
    profit_par_trajet = tarif_client - cout_trajet
    profit_journalier = profit_par_trajet * camions_jour
    profit_annuel = profit_journalier * 360
    return int(profit_annuel)
    

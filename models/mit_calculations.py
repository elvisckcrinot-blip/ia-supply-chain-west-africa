import numpy as np

def calcul_wilson_eoq(demande_annuelle, cout_commande, cout_stockage):
    if demande_annuelle <= 0 or cout_stockage <= 0:
        return 0
    eoq = np.sqrt((2 * demande_annuelle * cout_commande) / cout_stockage)
    return int(eoq)

def calcul_point_de_commande(demande_moyenne, delai_fournisseur, stock_securite):
    rop = (demande_moyenne * delai_fournisseur) + stock_securite
    return int(rop)

def analyse_pareto_abc(df, colonne_valeur):
    df = df.sort_values(by=colonne_valeur, ascending=False)
    df['cum_sum'] = df[colonne_valeur].cumsum()
    df['cum_perc'] = 100 * df['cum_sum'] / df[colonne_valeur].sum()
    
    def assign_abc(perc):
        if perc <= 80: return 'A'
        elif perc <= 95: return 'B'
        else: return 'C'
        
    df['Classe_ABC'] = df['cum_perc'].apply(assign_abc)
    return df

def calcul_cout_transport(distance, consommation_moyenne, prix_carburant, cout_fixe):
    """
    Calcule le coût total en FCFA et l'empreinte CO2.
    """
    carburant_total = (distance / 100) * consommation_moyenne
    cout_carburant = carburant_total * prix_carburant
    cout_total = cout_carburant + cout_fixe
    emissions_co2 = carburant_total * 2.68
    
    # Retourne le coût en entier (FCFA) et le CO2 avec 2 décimales
    return int(cout_total), round(emissions_co2, 2)
    

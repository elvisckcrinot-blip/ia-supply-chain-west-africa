import numpy as np

def calcul_wilson_eoq(demande_annuelle, cout_commande, cout_stockage):
    """
    Modèle Wilson (EOQ) : Calcule la quantité économique de commande.
    Optimise le compromis entre coût de stockage et coût de passation de commande.
    """
    if demande_annuelle <= 0 or cout_stockage <= 0:
        return 0
    eoq = np.sqrt((2 * demande_annuelle * cout_commande) / cout_stockage)
    return int(eoq)

def calcul_point_de_commande(demande_moyenne, delai_fournisseur, stock_securite):
    """
    Modèle ROP (Reorder Point) : Définit quand commander.
    Formule : (Demande journalière * Délai en jours) + Stock de sécurité.
    """
    rop = (demande_moyenne * delai_fournisseur) + stock_securite
    return int(rop)

def analyse_pareto_abc(df, colonne_valeur):
    """
    Segmentation ABC : Classe les produits par importance financière.
    A : 80% de la valeur (20% des produits)
    B : 15% de la valeur (30% des produits)
    C : 5% de la valeur (50% des produits)
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
  

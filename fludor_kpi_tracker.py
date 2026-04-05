# Script de surveillance des pertes pour Fludor SA
# Objectif : Maintenir les pertes d'approvisionnement < 0.20%

def check_stock_loss(matiere_recue, matiere_perdue):
    # Calcul du taux de perte
    taux_perte = (matiere_perdue / matiere_recue) * 100
    
    print(f"📊 Analyse du lot : Taux de perte actuel = {taux_perte:.4f}%")
    
    if taux_perte > 0.20:
        print("⚠️ ALERTE : Seuil de 0.20% dépassé ! Action corrective requise.")
    else:
        print("✅ Objectif Qualité atteint : Le stock est sécurisé.")

# Test avec les données réelles (ex: 1000kg reçus, 5kg perdus)
check_stock_loss(1000, 5) 
  

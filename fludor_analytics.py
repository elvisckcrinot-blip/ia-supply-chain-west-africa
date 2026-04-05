import matplotlib.pyplot as plt

# Données d'échantillon (Simulation de 7 jours à Cana)
jours = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
pertes_reelles = [0.15, 0.25, 0.18, 0.30, 0.12, 0.19, 0.22] # Taux en %

plt.figure(figsize=(10, 5))
plt.plot(jours, pertes_reelles, marker='o', label='Pertes Réelles (%)', color='blue', linewidth=2)
plt.axhline(y=0.20, color='red', linestyle='--', label='Objectif Fludor (0.20%)')

plt.title('Analyse des Pertes Matières Premières - Fludor SA')
plt.xlabel('Jours de la semaine')
plt.ylabel('Taux de perte (%)')
plt.legend()
plt.grid(True, linestyle=':')

# Sauvegarde du graphique de démonstration
plt.savefig('visualisation_pertes.png')
print("Graphique de preuve généré.")

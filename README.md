# Autocompletion-NGram
Implémentation d'un modèle d'autocomplétion basé sur les N-grammes avec lissage de Kneser-Ney, permettant de prédire les mots suivants les plus probables à partir d'un corpus en Python.

# Fonctionnalités
- Prédiction de mots basée sur un modèle n-grammes.
- Utilisation des unigrammes, bigrammes et trigrammes pour améliorer la précision des suggestions.
- Utilisation de la fonction de lissage de Kneser-Ney pour gérer les mots inconnus.

# Structure du projet
- data/ : Contient le corpus d'entraînement ainsi que le fichier test.
- autocompletion.py : Point d'entrée du programme, gère l'exécution et l'affichage des résultats.
- dictionnaire.json : Contient les fréquences des n-grammes calculées à partir du corpus.

# Prérequis
- Python version 3.x

# Note
- Pour exécuter le projet, saisissez la commande `python autocompletion.py` dans votre terminal.

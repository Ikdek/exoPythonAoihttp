# RSS Keyword Scanner

Ce script Python permet d'extraire les articles de flux RSS à partir d'une liste de liens en fonction d'une liste de mots-clés.

## SOMMAIRE

- Principes du script
- Structure du code
- Configuration et utilisation
- Format du résultat
- Pistes d'amélioration

## STRUCTURE DU CODE

1. Importation des modules

   - asyncio, aiohttp : pour la gestion asynchrone des requêtes HTTP.
   - feedparser : pour lire et analyser le contenu XML des flux RSS.
   - logging : gestion des messages d’info/erreur dans la console.
   - time : pour calculer le temps d’exécution.

2. Définition des mots-clés

   keywords = ["nutella"]

   Liste des mots-clés que le script cherchera dans chaque article.

3. Fonctions principales

   a. fetch_feed(session, url)
   - Récupère le contenu brut du flux RSS à l’URL donnée.
   - Fonctionne en asynchrone.
   - Retourne le texte du flux, ou None en cas d’erreur.

   b. find_matching_articles(parsed_feed, keywords)
   - Analyse le flux RSS pour trouver les articles correspondant aux mots-clés.
   - Pour chaque entrée (article), extrait le titre, le lien, le résumé, la date de publication.
   - Retourne une liste des articles correspondants.

   c. process_rss_url(session, url)
   - Appelle fetch_feed pour télécharger un flux RSS puis l’analyse.
   - Filtre les articles : retient ceux dont le titre ou le résumé contient au moins un des mots-clés.
   - Ajoute à la liste des résultats toutes les informations utiles + le mot-clé qui a permis la correspondance.

   d. main()
   - Lit le fichier rss_list.txt pour obtenir toutes les URLs à consulter.
   - Lance autant de tâches asynchrones qu’il y a d’URLs (pour aller plus vite).
   - Écrit les résultats récoltés dans le fichier resultat.txt, dans un format clair.

4. Lancement du programme
   - Chronomètre le temps d’exécution.
   - Affiche étape par étape la progression dans les logs.

## CONFIGURATION ET UTILISATION

1. Dépendances à installer :

   pip install aiohttp feedparser

2. Préparer le fichier rss_list.txt

   Placez chaque URL de flux RSS sur une ligne distincte, par exemple :

   https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml
   https://france24.com/fr/rss

3. Modifier les mots-clés

   Ouvrez le script, ajustez la liste keywords si nécessaire.

4. Lancer le script

   python ton_script.py

## FORMAT DU RESULTAT

Le fichier resultat.txt créé aura cette structure pour chaque article trouvé :

📖 Titre : <titre de l'article>
📅 Date de publication : <date>
🔗 URL : <lien>
🔑 Mot-clé : <mot-clé ayant correspondu>

## EXEMPLE DE RESULTAT

📖 Titre : 60 % des administrateurs du CAC40 ont des compétences en RSE. Vraiment ?
📅 Date de publication : Thu, 30 Jan 2025 06:00:00 +0000
🔗 URL : https://youmatter.world/fr/categorie-economie-business/60-administrateurs-cac40-competences-rse-vraiment/
🔑 Mot-clé : actualité

# RESSOURCES

- logging : https://realpython.com/python-logging/
- aiohttp : https://pypi.org/project/aiohttp/
- feedparser : https://pypi.org/project/feedparser/
- asyncio : https://docs.python.org/3/library/asyncio.html
- Python : https://www.python.org/


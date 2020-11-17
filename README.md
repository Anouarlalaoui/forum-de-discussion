# Debate-Forum
Un forum afin de débattre sur plusieur sujets.

##Technologies utilisées:
Backend: Python / Flask avec modèle Jinga2
Base de données: MySQL
Frontend: HTML, CSS, Bootstrap, Jquery

##Vous souhaitez exécuter ce projet, voici les étapes:
Étape 1: Cloner le projet
Étape 2: Installez les dépendances avec la commande suivante:
pip install -r requirements.txt

Étape 3: Créez le fichier .env dans le projet où les informations d'identification seront stockées
MYSQL_HOST = votre_nom_hôte MYSQL_USER = votre_utilisateur MYSQL_PASSWORD = votre_mot de passe MYSQL_DB = votre_db

Étape 4: exécutez la commande suivante pour exécuter le projet maintenant
python app.py

Étape 5: Terminé
Les contributions et suggestions sont les bienvenues

#####POURQUOI FLASK ?

Flask est un framework pour les développeurs Python basé sur Werkzeug (boîte à outils WSGI) et Jinja 2 (moteur de modèle). Il relève de la licence BSD. Flask est très simple à installer et à utiliser. Comme d'autres frameworks, il est livré avec plusieurs fonctionnalités prêtes à l'emploi, telles qu'un serveur de développement intégré, un déboguer, une prise en charge des tests unitaires, la création de modèles, des cookies sécurisés et la distribution de requêtes RESTful. 

Principales fonctionnalités de Flask 
Routage ingénieux 

L'objectif de conception de Flask-RESTful est de fournir des ressources basées sur des vues enfichables Flask. Les vues enfichables fournissent un moyen simple d'accéder aux méthodes HTTP. 

Analyse des demandes reposantes 

L'analyse des requêtes fait référence à une interface, modelée sur l'interface de l'analyseur Python pour les arguments de ligne de commande, appelée « argparser ». L'analyseur de requête RESTful est conçu pour fournir un accès uniforme et simple à toute variable qui se trouve dans l'objet de requête (flask.request). 

Champs de sortie 

Dans la plupart des cas, les développeurs d'applications préfèrent contrôler les données de réponse , et Flask-RESTful fournit un mécanisme dans lequel vous pouvez utiliser des modèles ORM ou même des classes personnalisées en tant qu'objet à rendre. Un autre fait intéressant à propos de ce framework est que les développeurs d'applications n'ont pas à se soucier d'exposer des structures de données internes car il permet de formater et de filtrer les objets de réponse. Ainsi, lorsque nous examinons le code, il sera évident quelles données seront utilisées pour le rendu et comment elles seront mises en forme. Avantages du framework Flask 

Voici quelques-uns des avantages du framework Flask: 
Serveur de développement et déboguer intégrés 
Répartition des demandes RESTful prête à l'emploi 
Prise en charge des cookies sécurisés 
Prise en charge intégrée des tests unitaires 
Configuration très minimale 
Plus rapide (performances) 
Intégration NoSQL facile 
Documentation complète

#####Explication Code :


Le forum de discussion du projet contient les modules python suivants: 
=> app.py 
=> connecteur.py 
=> encryption.py 
=> get_data.py

Le forum de discussion du projet contient les modules python suivants:

=> app.py
=> connecteur.py
=> encryption.py
=> get_data.py

1. app.py:

    Il s'agit du fichier principal sur lequel l'application flask et tous les routages de l'application ont été configurés. Ce fichier contient l'initialisation de l'application flask et la variable d'environnement de lecture.

Le fichier app.py contient les itinéraires suivants:

A. / index:
     La page d'accueil est rendue par ce qui contient tous les sujets de discussion. Les utilisateurs peuvent également créer un sujet s'ils sont connectés. Cette page contient également une option d'inscription et de connexion.
B. / connexion:
     Route de connexion pour l'utilisateur avec nom d'utilisateur et mot de passe
C. / registre:
     Route pour enregistrer un nouvel utilisateur avec un nouveau nom d'utilisateur et mot de passe et fait également la validation de l'utilisateur existant
D. / sujet de recherche:
     Itinéraire de recherche des sujets de la page d'accueil avec les mots-clés donnés
E. validate_user_name:
     Utilisé pour valider si l'utilisateur existe déjà ou non lors de l'inscription
F. / déconnexion:
     Déconnexion de l'utilisateur
G. / create-topic:
     Route pour créer un nouveau sujet, enregistre le sujet et également l'utilisateur qui a créé le sujet avec la date et l'heure de création du sujet
H. / create-claim:
     Route pour créer une revendication du sujet donné et enregistre également l'utilisateur qui l'a créé avec la date et l'heure de la création
I. / topic / <topic_id>:
   Route de vérification du détail du sujet spécifique avec les revendications faites sur ce sujet, avec les autres informations comme l'utilisateur qui l'a créé au moment de la création.
J. / search-claim / <topic_id>:
   Rechercher les revendications d'un sujet donné avec les mots-clés spécifiques
K. / créer-réponse:
    Route pour créer la réponse de la revendication donnée et également enregistrer le type de réponse avec l'utilisateur qui l'a créée ainsi que la date / heure de création
L. / claim / <claim_id>:
    Route pour vérifier les détails des revendications avec toutes les réponses sur cette revendication donnée avec d'autres informations comme l'utilisateur qui l'a créée et datetime
M. @ app.errorhandler (404):
   Gestionnaire d'erreurs pour l'erreur 404


2. Connector.py:

Module qui se connecte à la base de données mysql en utilisant pymyql et renvoie également l'objet de connexion, qui peut être utilisé dans d'autres modules.
Obtient en gros tous les paramètres requis pour se connecter à la base de données, puis se connecte à la base de données mysql spécifiée

3. Encryption.py:

Module qui hache le mot de passe de l'utilisateur pour le sécuriser
Utilise la bibliothèque bcrypt pour cela.

4. Get_data.py:

Module qui contient des fonctions pour extraire les données de la base de données pour les sujets, les revendications et les réponses. Contient les requêtes SQL et une meilleure mise en forme du résultat qui peuvent être utilisées dans les routes app.py.

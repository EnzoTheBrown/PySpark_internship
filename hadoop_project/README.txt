0: MISE EN PLACE DU MODEL 'CLOUD':
    1: Avoir cloudera sur un docker
    2: Avoir un serveur http qui a un accès au fichier source et object à sa racine
    3: Le reste du code est à executer sur sa machine

1: LANCER UNE SERIE DE REQUETES:
    1: D'abord il faut creer les tables dans impala, mettez tous vos create table dans un fichier. voir: le fichier create_table
    2: Les requètes que vous voulez lancer sont a mettre à la suite dans un fichier par comme par exemple dans le fichier queries
    3: Dans benchmark.py il surffit d'utiliser la fonction launch(vos_requetes, vos_create_tables, container_ID)

2: DESCRIPTION DES FICHIERS:
    1: client_cloudera/benchmark.py n'as d'utilité que d'appeler les fonctions Queries.py en boucle pour envoyer des requètes à impala
        et de recevoir un temps en fonction de la quantité de données dans le hdfs
    2: client_cloudera/Queries.py permet donc d'envoyer des requètes à impala, de charger des données dans le hdfs
    3: client_cloudera/Parse.py va traiter le resultat des requètes pour en sortir des statistiques comme le temps d'execution, la place occupée
        en memoire par la requète.
    4: cloudera_config/client.py est a ajouter dans cloudera il permet ainse de recuperer les données du serveur http
        il faut changer dans le code, l'adresse de votre serveur ainsi que son numero de port.
        et lancer une commande comme python3 client.py 'Source'
        il va ainsi recuperer tous les fichier Source.
    5: cloudera_config/MakeClouderaGreatAgain.py nous pose des problèmes, à la base c'est un moyen de lancer un nouveau docker contenant cloudera
        et de le configurer automatiquement mais le problème c'est qu'on n'arrive pas a creer un nouveau conteneur via les appels system python.
    6: user_side/graphic.py n'est pas encore abouti, il nous permettra d'afficher un graph representant l'evolution du comportement des
         requètes en fonction de la quantité de donnée dans le hdfs

3: PROBLEMES RENCONTRES:
    Tout d'abord, la quantitée de connaissance a assimiler en quelques semaines n'etait pas evident, docker, les map/reduce, le framework hadoop,
    impala, hive, des notions de reseau à deterrer, le python, le java, les fichiers de logs et j'en passe. Etaient autant d'entrave qui ne pouvaient
    être facilement resolu du fait du peu d'information que l'on peur denicher pour ces sujet de pointe sur internet.

4: POUR CONTINUER:
    Continuer ce projet ne se reduit pas à simplement ajouter des nouvelles fonctionalités, il faut repenser l'essentiel
    par exemple recuperer les statistiques des requètes via un vrai systeme de logs, il faut aussi pouvoir envoyer des requètes
    via ssh et non docker exec, c'est un problème fondamentale pour pouvoir exporter notre travail sur un vrai environement de cloud.


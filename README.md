#### **Get books**

#### Présentation
À la demmande de Sam j'ai développé une solution pour récupérer les données
de tous les livres presents sur le site [booktoscrap](http://booktoscrap.com).

Le programe créera un dossier "data" qui répertorie toutes les catégories des livres.
Dans des sous dossiers nominatifs contenant un dossier "images"(ceux sont les images des livres)
et un tableau au nom de la catégorie qui contient les donnée demandées. 

#### Instalation

[Python >=3.3](https://www.python.org/downloads/) est requis !
###### Environnement virtuel
À la racine du projet, exécutez:
`python -m venv env`
Pour initialiser votre environnement virtuel
Reportez vous à la documentation [Commande pour activer l'environnement virtuel](https://docs.python.org/fr/3/library/venv.html)
Pour savoir comment activer l'environnement selon votre invite de commande.

###### Une fois votre environnement lancé.

Installez les librairies dont depends l'application.
Pour cela éxecutez:
`python -m pip install -r requirements.txt`

###### Le programme est prêt !

Vous pouvez éxecuter la collecte des données grace à la commande:
`python get_books.py`

##### Prennez un café ☕
Le scraping dure environs 25mins sur ma machine de développement.
Cette machine à des performances trés modestes.
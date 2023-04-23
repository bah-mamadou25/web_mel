
# web_mel

## Description
Ce projet est une application web développée avec Django. Elle consiste à transformer un logiciel bureautique de classification de documents électroniques en application web

## Prérequis
- Python 3.x
- pip

## Installation
 - Clonez ce dépôt sur votre machine locale :
    ```
    git clone https://github.com/bah-mamadou25/web_mel.git
    ``` 
    

 - Déplacez-vous dans le répertoire du projet :
    ```
    cd nom-du-projet
    ```
 - Isolez votre projet à l'aide d'un environement virtuel : nous utiliserons *virtualenv* 

	 - `pip install virtualenv` 
	 - `virtualenv env` où "env" est le nom de votre environnement virtuel
	 - Activez votre environnement virtuel : `source env/bin/activate` 

 - Installez les dépendances requises :
    ```
    pip install -r requirements.txt
    ```
    

 - Exécutez les migrations de la base de données :
    ```
     ~~python manage.py migrate~~
    ```
 - Lancez le serveur de développement :
    ```
    python manage.py runserver
    ```

 - Ouvrez votre navigateur web à l'adresse suivante : <br>
    http://127.0.0.1:8000/
    

 - Vous pouvez maintenant utiliser l'application.

## Contribution
Si vous souhaitez contribuer à ce projet, veuillez suivre les étapes suivantes :

1. ...

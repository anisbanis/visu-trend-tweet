---
title: Rapport VTT
author: Anis Bouaziz
        Jean-Marc Fares
date: 24 mai 2020
---
# VTT 🚴‍♂️
## Une webapp de visualisation de tweets en `python` et `javascript`

## 0 - Introduction

VTT est une webapp se donnant pour but de rechercher, filtrer et visualiser rapidement une série de tweets. En pratique, VTT consiste en un serveur écrit en `python` servant un site écrit en HTML/CSS/JS.  
Ce projet se veut être une application directe des enseignements de l'UE Langages dynamiques ([Python](https://www.lri.fr/~conchon/LangDyn/ "Sylvain Conchon: Cours sur Python (2017-2020)") & [JS](https://www.lri.fr/~kn/ld_en.html "Kim NGuyen: Programmation Web Avancée (2017-2020)")) du master ISD de l'Université Paris-Saclay.  
Ce projet requiert python 3.6+.  
La structure du projet aura l'allure suivante :  
```bash
visu-trend-tweet
├── README.md
├── backend
├── frontend
├── rapport.md (ce fichier)
├── tweets.csv
└── vtt.py
```
**Fig. 0 :** _Structure du projet_  

## 1 - Les données

Un jeu de données de test nous est fourni dans le cadre de l'UE. Il s'agit d'un jeu de tweets sous forme d'un fichier CSV, nomé `tweets.csv`.  

```bash
$ wc -l tweets.csv 
   33675 tweets.csv
$ du -h tweets.csv 
6.0M	tweets.csv
```
**Fig. 1 :** _Le fichier comporte 33674 tweets (1 tweet par ligne, sans compter le header) et fait 6Mo_  

```csv
"id","user_id","user_name","user_screen_name","user_followers_count","text","place_name","place_country","place_country_code","longitude","latitude","lang","date","timestamp","hashtag_0","hashtag_1","hashtag_2"
"1080003336894595073","118714827","ずらやん@ばなび🍒月西か39b","zurayan",1340,"I'm at 神田明神 文化交流館 in 千代田区, 東京都 https://t.co/I3bjEHSvbd","東京 千代田区","日本","JP",139.7676,35.701847,"ja","2019-01-01T07:30:35+00:00","1546327835664","","",""
"1080003416573857792","866788685357998085","Ivory Shews","IvoryShews",62,"Denim air force ones high. 60 shipped gifted on PayPal or 65 invoiced. #airforces #airforce1 #nike #ivoryshews #forsale #kickstagram #instakicks #sneakerheadsofinstagram #sneakerheads… https://t.co/ALCkhG6uPL","Memphis, TN","United States","US",-90.0524,35.1426,"en","2019-01-01T07:30:54+00:00","1546327854661","airforces","airforce1","nike"
...
...
```
**Fig. 2 :** _Extrait du fichier `tweets.csv` fourni dans le sujet_  

Les champs se divisent en deux catégories :  
  - Informations relatives à l'utilisateur  
`user_id, user_name, user_screen_name, user_followers_count`
  - Informations relatives au tweet  
`id, text, place_name, place_country, place_country_code, longitude, latitude, lang, date, timestamp, hashtag_0, hashtag_1, hashtag_2`

Pour simplifier, on peut dire qu'un utilisateur est un couple `(user_id, user_name)` et qu'un tweet est un quintuplet `(tweet_id, utilisateur, corps, lieu, hashtags)`.
On remarque en particulier que les trois premiers hashtags sont déja extraits du corps du texte.

## 2 - Serveur WSIG-like

L'un des composants principaux de cette webapp est un serveur capable de servir de pages statiques au client, ainsi que de satisfaire des requêtes paramétrées.  
Nous décidons de découpler l'aspect applicatif et l'aspect service dans deux modules distincts, pour rendre l'implémentation de la logique métier indépendante de la solution de serveur.  
```bash
visu-trend-tweet
├── ...
├── backend
│   ├── __init__.py
│   ├── __main__.py
│   ├── __pycache__
│   ├── app.py
│   ├── server.py
│   └── tools.py
└── vtt.py
```
**Fig. 3 :** _Organisation du paquet backend_

Nous nous proposons d'implémenter la logique de serveur dans `server.py` et la logique applicative dans `app.py`, le module principal s'occupera simplement d'implémenter la logique "métier".  
### a. `vtt.py`
Le module vtt nous servira à déclarer les différents traitements sur les données, puis démarer le serveur.  

```python=
from backend import Application

vtt = Application(__name__)

@vtt.rule('/fabulous')
def fab(user):
    return f"Hey {user}, you are fabulous !"
    
vtt.run()
```
__Fig. 4 :__ _Code type d'instantiation d'une application avec le paquet backend, correspondant schématiquement à `vtt.py`_  

Pour créer une application et la servir, il nous suffit simplement d'instantier la classe Application, d'éventuellement y ajouter differentes règles - qui correspondront à un endpoint et a une URL - puis de lancer le serveur avec la fonction `run()`.

**Exemple** curl simple sur un endpoint
Dans un premier terminal on lance le serveur :
```bash
$ python vtt.py
Serving HTTP on 127.0.0.1 port 8080 (http://127.0.0.1:8080/) ...
```
Depuis un second terminal, on execute une requête sur ce endpoint : 

```bash
$ curl "localhost:8080/fabulous?user=Alice"
Hey Alice, you are fabulous !
```
On observe bien que l'endpoint existe et que le query parameter à bien été passé.

### b. `server.py`
Pour satisfaire des requêtes HTTP, python 3 nous fournit un module : [`http.server`](https://docs.python.org/3/library/http.server.html "http.server: HTTP Server et Request Handlers").  
Deux classes sont principalement à utiliser : [`HTTPServer`](https://docs.python.org/3/library/http.server.html#http.server.HTTPServer) et [`SimpleHTTPRequestHandler`](https://docs.python.org/3/library/http.server.html#http.server.SimpleHTTPRequestHandler). La première sert à intercepter les requêtes et instancie la seconde à chaque fois qu'il y a une requête pour la traiter.  

La méthode utilitaire `serve` est utilisée pour lancer le serveur, il s'agit du point d'entrée à préférer pour le module `backend.server`. Elle s'occupe essentiellement de configurer la classe serveur avec l'adresse de la socket ouverte pour écouter les requêtes, de configurer le RequestHandler et de lancer le service.  
Afin de supporter plusieurs requêtes de façon concurrente, nous pouvons demander au serveur d'ouvrir une thread pour chacune. Pour ce faire, nous suivons toutes les threads en les ajoutant à une liste de threads pour eventuellement attendre leur terminaison dans le futur. On remarque que le join se fait dans un générateur qui est passé à une fonction utilitaire `progress_bar`qui va automatiquement consommer (joindre le thread ici) chaque element du générateur et mettre à jour la barre de chargement au fur et à mesure.  

```python=
 def server_close(self):
     super().server_close()
     if self.wait_for_threads:
         threads, self._threads = self._threads, None
         if threads:
             l = len(threads)
             progress_bar((t.join() for t in threads),
                          l,
                          prefix='Waiting for threads :',
                          suffix='Completed :',
                          bar_length=50)
     else:
         print('Not waiting for threads, terminating.')
```
**Fig. 5 :** _Traitement des threads à la terminaison du serveur_

Un bug que l'on a rencotré est que quand on demande l'arret du serveur en mode multi-threadé, il attendrait indéfiniment des threads (ou s'executent les RequestHandlers). A priori, nous pensions qu'il s'agissait d'une erreur de déréférencement, puis que le problème à été réglé en changeant le code de la Fig. 6 à celui de la Fig. 7 :  
```python=
HandlerClass.protocol_version = protocol

with ServerClass(server_address=addr,
                 RequestHandlerClass=partial(HandlerClass,  
                                             directory=directory,  
                                             app=app)) as httpd:
```
**Fig. 6 :** _Passage de `protocol_version` avant passage de `directory`_

```python=
HandlerClass = partial(HandlerClass, directory=directory, app=app)
HandlerClass.protocol_version = protocol

with ServerClass(server_address=addr,
                 RequestHandlerClass=HandlerClass) as httpd:
```
**Fig. 7 :** _Passage de `protocol_version` **après** passage de `directory`_

Enfin, c'est dans la classe `CompleteHTTPRequestHandler`  que l'on vérifie si l'url demandée correspond à un endpoint enregistré par l'applicatif (dans les methodes `do_GET` et `do_POST`). On remarquera que c'est ici que se fait la sérialization, elle pourrait être plus fine, ici c'est simplement un passage en `str`.  

```python=
from urllib.parse import parse_qsl

url = urlparse(self.path)
path = url.path
query = dict(parse_qsl(url.query))

if self.app.is_rule(path):
    output = bytes(str(self.app._exec_rule(path, 'GET', query)), 'utf-8')
    self.wfile.write(output)
else:
    super().do_GET()
```
**Fig. 8 :** _Requête GET_

### c. `app.py`

La classe `Application` à pour but de retenir les correspondances entre des URL spécifiques (que l'on appellera des _règles_ ou _rules_) et des fonctions. Il y a deux structures de données principales :  
  - `rules` : dictionnaire associant un chemin d'URL à un _endpoint_, ses méthodes HTTP et les arguments qu'il accepte.  
  - `endpoints` : dictionnaire associant un _endpoint_ avec une fonction.  

On fait ici la distinction entre endpoint et fonction, car on pourrait vouloir retrouver une URL sachant une certaine fonctcion. Dans ce cas, on pourrait avoir deux fonctions portant le même nom, mais ne designant pas le même endpoint, typiquement :  

```python=
class User:
    def __init__(self, app):
        self.app = app
    
    @self.app.rule('/user/auth')
    def auth():
        pass

class Admin:
    def __init__(self, app):
        self.app = app
    
    @self.app.rule('/admin/auth')
    def auth():
        pass

from backend import Application

app = Application('test')
user = User(app)
admin = Admin(app)
```
**Fig. 8 :** Exemple de collision de nom dans endpoint_

Ici, si l'on utilisait simplement le nom de la methode pour désigner le endpoint, on ne pourrait pas faire la distinction entre  `User.auth` et `Admin.auth` pour en retrouver l'URL (dans l'application VTT il n'y a pas encore besoin de faire de reverse lookup).  

Ensuite, on peut executer une règle étant donné son URL, des paramètres (on vérifie bien que les bons paramètres sont passés) ainsi qu'une méthode.  

Enfin, nous avons une méthode utilitaire `run()` qui nous permet de lancer le serveur associé à cette application.  

## 3 - Interrogation des données

On utilise bibliotheque pandas afin de faciliter la manipulation et l'analyse des données.l'implementation d'un Dataframe contenant les données permet de faire les traitement nécessaire afin de renvoyer le résultat attendu au client.

## 4 - Client asynchrone

Le client asynchrone joue le role de passerelle entre le serveur traitant les requetes que le client envoie et le client recevant les reponses du serveur.le transfert d'informations se fera sous form de requetes `Http`.  
La fonction `Client.ajax` envoie une requete `Http` et encapsule le retour sous forme d'un objet `Promise` qui lui se résout et renvoie le résultat dés qu'il reçoit la réponse.  
```javascript=
Promise ((resolve, reject) => {
		let xhr = new XMLHttpRequest();
		xhr.addEventListener("readystatechange", function() {
			/* requete teminée */
			if (this.readyState == 4 ) {
				if (this.status == 200)
					resolve(this. responseText);
                else
                    reject(this.status + " : " + this.responseText);
            }
        });
        xhr.open(method, url);

        xhr.send();
    })
```
`Serve.py` reçoit la requete `http(methode,url)` qui traduirat en `regle,parametre` c'est ce qui va permetre de lancer le traitement spécifique.Par exemple le client veut recevoir(GET) `Traitement1(p1,p2)`=>
la requete `Http` correspondante:
```javascript=
let url = "http://127.0.0.1:8080/Traitement1?p1=value1&p2=value2
//on peut faire plusieurs appel ajax dans une fonctins asynch comme
//Client.query
try {
	res = await Client.ajax(" GET", url);
	return res;
	}
catch (str) {
	alert ("ERROR")
	res= str;
	}
```
Maintenant le traitement dans `vtt.py` qui va lancer le serveur est : 
```python=
@app.rule('/search', methods=('GET,'))
def search(p1,p2): //p1==value1 & p2==value2s
    tmp=df.loc[df['text'].str.contains(p)]
    print(p)
```
On sait baser sur deux principe dans cette partie,l'asynchonisation des requetes ajax pour faire des traitements parallèles,et la synchonisation du retour serveur à l'aide des promesses.




## 5 - Présentation
`html,css,javascript` ont été utilisés pour l'affichage des graphes et des pages.
Pour pouvoir déssiner les graphes qu'on veut afficher on a utilisé l'element `html` padas afin de faire des déssins dynamiques manipulier les dimentions des histogramme par exemlple.
Voici un exemple d'un histogramme pour la recherches des tweets contenant un "yes".


![](https://i.imgur.com/9FQko0i.png)


## 6 - Conclusion

VTT est encore dans sa phase de développement la plus précoce (~60h $travail \times homme$), plusieurs améliorations sont possibles :  

  - Le frontend est légèrement austère
  - Plus de filtres de recherche
  - Un affichage des tweets sur une carte du monde
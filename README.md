# Jeux de Merelle Et Morpion

C'est un projet réalisé lors de la première année de Bachelor à l'ESEO.
Il s'agit de deux jeux : le jeu de Merelle et le jeu de Morpion.
Il y a deux modes de jeu :
- Joueur contre Joueur (Avec un serveur hébergé et deux clients)
- Joueur contre IA

## Installation

Il vous suffit d’extraire tout le dossier de l’archive. Et voilà le programme est installé.

Pour se connecter à un serveur, il vous suffit de modifier l'adresse IP dans le répertoir `programme/multi` dans le fichier `client.py`.
Si votre serveur est hébergé sur la même machine que le client, vous pouvez mettre `localhost`.

```py
def connexion():
    hote = "ip-du-serveur"
    port = 12800
```

## Lancé le programme

Si vous utilisez un terminal de commande et que vous n’utilisez pas le fichier "run.bat", 
n’oublier pas de mettre le terminal en plein écran. Sinon vous risquez d’avoir des problèmes 
d’affichages pour les plateaux.

### Pour Windows :
Il vous suffit de lancer le fichier "run.bat" situer dans le dossier programme

### Pour Linux :
Ouvrer un terminal, rendez-vous dans le dossier programme, entrer la commande 
"python3 main.py" et entrer.

## Utilisation

### Les menus :
Quand le programme est lancer, il affiche un menu. Pour naviguer dans le menu vous devez 
utiliser des nombres entiers.
Pour la partie en ligne, le programme va tenter de se connecter au server. Si le serveur 
sélectionner n’est pas accessible, le programme affichera un message d’erreur et retournera 
au menu principal. Pour cela, regardez la partie installation pour configurer votre propre 
serveur.


### Version terminale :

- Le Morpion : </br>
Pour jouer au morpion, il vous suffit de rentrer les coordonnées de la case que vous voulez

- Le Merelle : </br>
Pour jouer au merelle, le programme vous demandera des lettres ou des chiffres, afficher sur la 
droite du plateau. Pour les déplacements, si vous posséder plus de 3 pions, il vous sera 
demander un nombre entier indiquant la direction désirée. Au contraire si vous ne possédé 
que 3 pions, le programme vous demandera un des caractères affichés à la droite du plateau.

### Version graphique :

- Le Morpion : </br>
Pour l’interface graphique, par manque de temps est dans un fichier a part. le jeu du morpion est 
fonctionnelle. Vous pouvez la lancé en executant le fichier `run.bat` dans le dossier `interface Tkinter`

- Le Merelle : </br>
La partie merelle est seulement pour montrer l’interface mais n’est pas fonctionnel.

## Partie en ligne

Pour la partie en ligne, nous avons un problème et par manque de temps nous ne pouvons pas le 
résoudre. Ceci n’est que pour le merelle. Le morpion en ligne fonctionne correctement.


# Information complémentaire

Si nous avions eu plus de temps, nous aurions fini le jeu de merelle avec Tkinter. Nous aurions aussi 
réglé les derrière bug sur la partie en ligne. Et nous aurions aussi plus optimiser le code en 
regroupant certaine fonction dans un fichier commun

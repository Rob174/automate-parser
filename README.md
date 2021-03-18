

# automate-parser v1.0

Ce programme réalisé en python dans le cadre de la formation d'automates et langages de l'[INSA Toulouse](http://www.insa-toulouse.fr/) a pour but de générer un programme C, reconnaissant une grammaire de type 2 (context free) précédement donnée.
Ce programme C une fois compilé pourra être executé avec en paramètre une chaîne de caractères, le programme vérifiera ensuite si cette chapine appartient ou non à la grammaire initiale. 

## Mode d'emploi:

 1. Créer et placer un fichier `grammaire` dans le dossier racine du projet, comportant une grammaire type *(cf Définitions)*
 2. Compiler le projet python avec en paramètres: `grammaire -o parser`, un fichier `parser`.c sera ensuite généré
 3. Executer la commande `./Makefile.sh` générant un exécutable `parser`
 4. Si l'erreur `line 2: $'\r': command not found` apparaît, faire la commande `dos2unix ./Makefile.sh` et refaire l'étape **3.** 
 5. Executer le programme avec la commande `./parser "A"`, `A` étant le mot à tester

Le résultat sera *"**OK**"* si le mot appartient à la grammaire initiale, *"**KO**"* sinon.


## Echantillons de données:

|Grammaire   			|Mot en entrée          |	Sortie  |
|----------------------|-------------------------|---------------------|
|S : a S b <br> S : a b|`a a b b`                |![#78e08f](https://via.placeholder.com/15/78e08f/000000?text=+) **`OK`**               |
|S : a S b <br> S : a b|`a a b b b`              |![#e55039](https://via.placeholder.com/15/e55039/000000?text=+) **`KO`**               |
| S : a S b <br> S : a b <br> S : A B <br> A : A A a <br> A : a <br> B : b |`a a a a b b` |![#78e08f](https://via.placeholder.com/15/78e08f/000000?text=+) **`OK`** théoriquement mais  segfault en pratique car left-recursion				|
| S : a S b <br> S : a b <br> S : A B <br> A : A A a <br> A : a <br> B : b |`a a a a b b b` |![#e55039](https://via.placeholder.com/15/e55039/000000?text=+) **`KO`** théoriquement mais  segfault en pratique car left-recursion				|
| S : int <br> S : string <br> S : { Assoc } <br> Assoc : KeyVal AssocBis <br> Assoc : <br> AssocBis : , KeyVal AssocBis <br> AssocBis : <br> KeyVal : id = S |`{ id = int , id = string }` |![#78e08f](https://via.placeholder.com/15/78e08f/000000?text=+) **`OK`**				|


## Détails de la réalisation:

- Générer le dictionnaire
	- Importer le fichier de grammaire
	- Pour chaque ligne (i.e. règle) lue:
		- Séparer la partie gauche de la partie droite
		- Ajouter une entrée dans le dictionnaire correspondant au nom de la fonction à appeller
- Générer les fonctions pour chaque règle du dictionnaire, qui feront appel à:
	- la fonction `strequ()` permet de comparer le paramètre au terminal attendu
	- la fonction `next_val()` permet de se déplacer au non-terminale suivant
- Générer les fonctions "mères" *(cf. Définitions)*
- Générer la fonction `main()` acceptant un argument (le mot qui sera parsé par le code C) et appelle la première fonction mère

## Définitions
#### grammaire type:
La syntaxe des grammaires reconnues est la suivante :  
- Une regle par ligne
- Partie gauche separee de la partie droite par ":"
- Les non-terminaux sont des mots avec un premier symbole correspondant a une majuscule
- Les terminaux sont en minuscule
- Les terminaux et non-terminaux sont separes par un espace dans la partie droite
- L'axiome est le non-terminal de gauche de la premiere regle de la grammaire.
#### fonction "mère":
Pour une règle B, la fonction mère `parserB()` appellera grâce à une boucle `while` toutes les fonctions `parserBX()`, `X` permettant de désigner la `X` règle correspondant au non-terminal `B`.

## Acteurs du projet: (4IR A2)
[BAUDOINT Emma](https://github.com/Emma-bau) | [BAURES Vincent](https://github.com/VBaures) | [CALMET Alicia](https://github.com/AliciaC8) | [JACQUES Matthieu](https://github.com/Matthieu-Jck) | [MOINE Robin](https://github.com/Rob174) | [SMANIOTTO Nathan](https://github.com/nsmaniotto)

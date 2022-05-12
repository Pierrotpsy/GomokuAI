# Principe de l'agorithme Minimax et approche du problème

L’algorithme Minimax est un algorithme qui s'applique à la théorie des jeux pour les jeux à deux joueurs. Ils sont adversaires et le but de l’un est de maximiser son gain, tandis que l’autre minimise sa perte. 

 Le principe de l’algorithme est de jouer le coût le plus fort : pré-jouer tous les coups possibles et choisir celui qui nous rapproche le plus de la victoire. Pour ce faire, on va devoir d’abord jouer tous les coups possibles puis tous ceux de l’adversaire et ainsi de suite jusqu’à la victoire ou la défaite. Dans la plupart des jeux comme par exemple le jeu des échecs, nous devons nous arrêter à une certaine profondeur de prédiction car il y a trop de coups possibles. 

Ici, l’objectif du projet est de jouer à un jeu de plateau qui s’appelle le Gomoku. La taille du plateau est de 15 cases sur 15 cases et le premier qui réussit à aligner 5 pions verticalement, horizontalement ou sur une diagonale gagne. L’espace de recherche est donc de (225)! 

Nous sommes soumis à certaines contraintes, comme par exemple le fait que notre IA doive jouer son coup en moins de 5 secondes et la condition de jouer avec la variante LongPro. 

## Structure du projet

Nous avons travaillé sur plusieurs classes.  

Nous avons une première classe Game, composée de fonctions qui créent la board, qui se chargent de l’afficher et de la modifier en remplaçant les espaces libres par le nouveau coup joué. Cette classe comporte aussi une fonction evaluate qui prend en paramètre le joueur et qui compte combien le joueur en question a de pions alignés. La fonction getNeighbours, elle, prend chaque case remplie pour les 2 joueurs et regarde ses voisins (à une distance de 2 près). Avec la fonction boardFitness, on examine par joueur si le voisin est un pion adverse ou non. Si un pion est à côté d’un pion de sa couleur, il continue d’étudier les cases suivantes dans chaque direction jusqu’à ce qu’il soit bloqué ou non. Sinon, il est bloqué directement, soit du côté de la queue (tail), soit du côté de la tête (head). On continue cet examen pour tous les pions d’un joueur et ensuite on classifie les potentielles chaines de pions en attribuant des scores. Si le pion n’est pas bloqué par des pions adverses, on lui attribue un type ‘open’ qui vaut beaucoup de points. S’il est bloqué par la queue ou par la tête, on lui attribue un type ‘counter’ qui vaut moins de points. Et si lui, ou la chaine de pions qu’il constitue en partie est bloqué des 2 côtés par des pions advers, on lui attribue un type ‘block’ ce qui donne une valeur nulle. Les scores attribués pour des ‘open’ et ‘counter’ sont pondérés en fonction de la taille de la chaine de pions. Si la taille est de 5, on attribue au joueur que l’on étudie une victoire. On finit par retourner les scores de chaque joueur.  

Nous avons également implémenté un module nommé Players qui est composé de plusieurs classes (Manual et AI) qui utilisent les fonctions de la classe Game pour pouvoir placer les pions. La classe Manual est faite pour que l’humain puisse faire son coup à l’endroit qu’il choisit manuellement. La classe AI sert à placer le pion lorsque c’est à son tour de jouer, en fonction du meilleur coup possible. Elle est contrainte en temps car elle doit donner une réponse en moins de 5 secondes. C’est la fonction minimax qui s’occupe de choisir le meilleur coup à jouer grâce notamment à l’élagage alpha-beta. 

## Heuristiques et fonctions clés
- fonction minimax : Dans la fonction minimax, nous choisissons le meilleur coup à jouer grâce à un procédé récursif (on remonte peu à peu dans l’arbre des possibilités et on choisit alternativement les valeurs qui maximisent le gain ou qui minimisent la perte). L’élagage alpha-beta permet d’accélérer la recherche en identifiant les chemins dans l’arbre qui sont explorés inutilement. isMax est le premier joueur à qui nous attribuons alpha et nous attribuons beta au 2ème joueur qui doit minimiser sa perte. Nous parcourons l’arbre en profondeur  (depth=2) et nous procédons à une coupure de l’arbre (prunning) quand la condition est satisfaite (alpha >=beta). 

- fonction autoBlock : La fonction autoBlock de la classe Game, permet de gagner en temps et en certitude car elle force notre IA a bloqué le deuxième côté d’une chaine de 4 pions adverses alignés déjà bloqué par un de nos pions. Nous avions remarqué que l’IA avait parfois des difficultés à faire cette action. 

- fonction boardFitness : Enfin, nous avons évolués sur notre façon d’attribuer des scores à des alignements de pions ‘open’ et ‘counter’ car nous avons réalisé que parfois, l’IA ne calculait pas forcément le meilleur coup. Nous avons donc mis par exemple une très grande différence de score entre counter_4 et open_4 car counter_4 peut être facilement bloqué par l’adversaire alors qu’un open_4 équivaut à une “quasi”-victoire car même si l’adversaire peut bloquer un côté, l’IA pourra jouer sur l’autre côté et gagner. 

## 

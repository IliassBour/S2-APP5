###  Gabarit pour l'application de traitement des frequences de mots dans les oeuvres d'auteurs divers
###  Le traitement des arguments a ete inclus:
###     Tous les arguments requis sont presents et accessibles dans args
###     Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments
###
###  Frederic Mailhot, 26 fevrier 2018
###    Revise 16 avril 2018
###    Revise 7 janvier 2020
###   Modifié par IliassBour et PedroScocci

###  Parametres utilises, leur fonction et code a generer
###
###  -d   Deja traite dans le gabarit:  la variable rep_auth contiendra le chemin complet vers le repertoire d'auteurs
###       La liste d'auteurs est extraite de ce repertoire, et est comprise dans la variable authors
###
###  -P   Si utilise, indique au systeme d'utiliser la ponctuation.  Ce qui est considÃ©re comme un signe de ponctuation
###       est defini dans la liste PONC
###       Si -P EST utilise, cela indique qu'on dÃ©sire conserver la ponctuation (chaque signe est alors considere
###       comme un mot.  Par defaut, la ponctuation devrait etre retiree
###
###  -m   mode d'analyse:  -m 1 indique de faire les calculs avec des unigrammes, -m 2 avec des bigrammes.
###
###  -a   Auteur (unique a traiter).  Utile en combinaison avec -g, -G, pour la generation d'un texte aleatoire
###       avec les caracteristiques de l'auteur indique
###
###  -G   Indique qu'on veut generer un texte (voir -a ci-haut), le nombre de mots Ã  generer doit Ãªtre indique
###
###  -g   Indique qu'on veut generer un texte (voir -a ci-haut), le nom du fichier en sortie est indique
###
###  -F   Indique qu'on desire connaitre le rang d'un certain mot pour un certain auteur.  L'auteur doit etre
###       donnÃ© avec le parametre -a, et un mot doit suivre -F:   par exemple:   -a Verne -F Cyrus
###
###  -v   Deja traite dans le gabarit:  mode "verbose",  va imprimer les valeurs donnÃ©es en parametre
###
###
###  Le systeme doit toujours traiter l'ensemble des oeuvres de l'ensemble des auteurs.  Selon la presence et la valeur
###  des autres parametres, le systeme produira differentes sorties:
###
###  avec -a, -g, -G:  generation d'un texte aleatoire avec les caracteristiques de l'auteur identifie
###  avec -a, -F:  imprimer la frequence d'un mot d'un certain auteur.  Format de sortie:  "auteur:  mot  frequence"
###                la frequence doit Ãªtre un nombre reel entre 0 et 1, qui represente la probabilite de ce mot
###                pour cet auteur
###  avec -f:  indiquer l'auteur le plus probable du texte identifie par le nom de fichier qui suit -f
###            Format de sortie:  "nom du fichier: auteur"
###  avec ou sans -P:  indique que les calculs doivent etre faits avec ou sans ponctuation
###  avec -v:  mode verbose, imprimera l'ensemble des valeurs des paramÃ¨tres (fait deja partie du gabarit)


import math
import argparse
import glob
import sys
import os
import re
from pathlib import Path
from random import randint
from random import choice
from pythonds3.graphs import Graph

### Ajouter ici les signes de ponctuation Ã  retirer
PONC = ["!", '"', "'", ")", "(", ",", ".", ";", ":", "?", "-", "_"]

###  Vous devriez inclure vos classes et mÃ©thodes ici, qui seront appellÃ©es Ã  partir du main
def buildGraph(wordFile, mode):
    g = Graph()
    wfile = open(wordFile, 'r', encoding="utf-8")
    last = ""
    firstWord = 0
    lastWord = ""
    lastBigram = ""

    for line in wfile:
        ligne = line[:-1]
        words = re.split(r'[_;,.:;\[\]?!\"\'\s\t()\-]\s*', ligne.lower())

        for word in words:
            if mode is 1:
                if len(word) > 2:
                    if g.get_vertex(word) is None:
                        g.set_vertex(word)
                        g.get_vertex(word).set_discovery_time(1)
                    else:
                        frequence = g.get_vertex(word).get_discovery_time()
                        g.get_vertex(word).set_discovery_time(frequence + 1)

                    if firstWord == 0:
                        firstWord = 1
                    elif last != word:
                        g.add_edge(last, word)

                    last = word
            elif mode is 2:
                if len(word) > 2:
                    if firstWord == 0:
                        lastWord = word + " "
                        firstWord = 1
                    else:
                        bigram = lastWord + word

                        if g.get_vertex(bigram) is None:
                            g.set_vertex(bigram)
                            g.get_vertex(bigram).set_discovery_time(1)
                        else:
                            frequence = g.get_vertex(bigram).get_discovery_time()
                            g.get_vertex(bigram).set_discovery_time(frequence + 1)

                        g.add_edge(lastBigram, bigram)

                        lastBigram = bigram
                        lastWord = word + " "

    return g

def additionnerGraph(g, wordFile, mode):
    wfile = open(wordFile, 'r')
    last = ""
    firstWord = 0
    lastWord = ""
    lastBigram = ""

    for line in wfile:
        ligne = line[:-1]
        words = re.split(r'[_;,.:;?!\"\'\s\t()\-]\s*', ligne.lower())

        for word in words:
            if mode is 1:
                if len(word) > 2:
                    if g.get_vertex(word) is None:
                        g.set_vertex(word)
                        g.get_vertex(word).set_discovery_time(1)
                    else:
                        frequence = g.get_vertex(word).get_discovery_time()
                        g.get_vertex(word).set_discovery_time(frequence + 1)

                    if firstWord == 0:
                        firstWord = 1
                    elif word != last:
                        g.add_edge(last, word)

                    last = word
            elif mode is 2:
                if len(word) > 2:
                    if firstWord == 0:
                        lastWord = word + " "
                        firstWord = 1
                    else:
                        bigram = lastWord + word

                        if g.get_vertex(bigram) is None:
                            g.set_vertex(bigram)
                            g.get_vertex(bigram).set_discovery_time(1)
                        else:
                            frequence = g.get_vertex(bigram).get_discovery_time()
                            g.get_vertex(bigram).set_discovery_time(frequence + 1)

                        g.add_edge(lastBigram, bigram)

                        lastBigram = bigram
                        lastWord = word + " "

    return g

def buildGraphAuteur(rep_texts, mode):
    if os.path.isabs(rep_texts):
        rep = rep_texts
    else:
        rep = os.path.join(cwd, rep_texts)

    rep = os.path.normpath(rep)
    # print("path : ", rep)
    textes = os.listdir(rep)

    first = 0
    graphe = Graph()

    for text in textes:
        if first is 0:
            graphe = buildGraph(rep + "\\" + text, mode)
        else:
            graphe = additionnerGraph(graphe, rep + "\\" + text, mode)

    return graphe

def triFusion(tab, graphe):
    if len(tab) == 1:
        return tab
    else:
        tab1 = []
        tab2 = []
        taille1 = math.ceil(len(tab) / 2)
        taille2 = len(tab) - taille1

        for i in range(taille1):
            tab1.append(tab[i])

        for i in range(taille2):
            tab2.append(tab[i + taille1])

        tab1 = triFusion(tab1, graphe)
        tab2 = triFusion(tab2, graphe)

        i = 0
        j = 0
        for k in range(len(tab)):
            if i >= len(tab1):
                tab[k] = tab2[j]
                j = j + 1
            elif j >= len(tab2):
                tab[k] = tab1[i]
                i = i + 1
            else:
                if graphe.get_vertex(tab1[i]).get_discovery_time() > graphe.get_vertex(tab2[j]).get_discovery_time():
                    tab[k] = tab1[i]
                    i = i + 1
                else:
                    tab[k] = tab2[j]
                    j = j + 1
        return tab

def calculFrequence(graphe):
    tab = []
    size = graphe.get_vertices()

    for vertex in size:
        tab.append(vertex)

    tab = triFusion(tab, graphe)

    return tab

def calculProximiteAuteur(gInconnu, rep_aut, auteur, mode):
    graphesA = buildGraphAuteur(rep_aut + "\\" + auteur, mode)
    prox = 0
    commun = []

    for motIn in gInconnu.get_vertices():
        if graphesA.get_vertex(motIn) is not None:
            commun.append(motIn)

    for mot in commun:
        ai = graphesA.get_vertex(mot).get_discovery_time() / len(commun)
        ti = gInconnu.get_vertex(mot).get_discovery_time() / len(commun)
        prox += pow(ai - ti, 2)

    prox = math.sqrt(prox)

    prox = round(prox, 2)
    print(auteur + ": " + str(prox))

def calculProximiteToutAuteur(gInconnu, rep_aut, authors, mode):
    graphesA = []
    prox = []
    for a in authors:
        graphesA.append(buildGraphAuteur(rep_aut + "\\" + a, mode))
        prox.append(0)

    i = 0
    for auteur in graphesA:
        commun = []
        for motIn in gInconnu.get_vertices():
            if auteur.get_vertex(motIn) is not None:
                commun.append(motIn)

        for mot in commun:
            ai = graphesA[i].get_vertex(mot).get_discovery_time() / len(commun)
            ti = gInconnu.get_vertex(mot).get_discovery_time() / len(commun)
            prox[i] += math.pow(ai - ti, 2)
        prox[i] = math.sqrt(prox[i])
        i += 1

    for index in range(len(prox)):
        prox[index] = round(prox[index], 2)
        print(authors[index] + ": " + str(prox[index]))

def getWeight(tabWord, graphe):
    weight = 0
    for word in tabWord:
        weight += word.get_discovery_time()
    return weight

def buildRandomText(mode, nbWord, graphe):
    tab = []
    L = 1
    vertices = graphe.get_vertices()

    for vertex in vertices:
        tab.append(vertex)

    debut = choice(tab)

    if mode == 1:
        text = debut
        word = debut
        for suffix in range(nbWord - 1):
            tabSuffix = graphe.get_vertex(word).get_neighbors()
            poid = getWeight(tabSuffix, graphe)
            rand = randint(1, poid)

            for suffix in tabSuffix:
                rand -= suffix.get_discovery_time()
                if rand <= 0 and word != suffix.get_key():
                    word = suffix.get_key()
                    if len(text) > 50 * L:
                        text += "\n"
                        L += 1
                    break

            text += " " + word

    elif mode == 2:
        text = graphe.get_vertex(debut).get_key()
        bigramme = graphe.get_vertex(debut).get_key()

        for i in range (1, nbWord):
            neighbors = graphe.get_vertex(bigramme).get_neighbors()
            weightTot = 0
            for item in neighbors:
                weightTot += item.get_discovery_time()
            randNext = randint(1, weightTot)

            for item in neighbors:
                randNext -= item.get_discovery_time()
                if randNext <= 0:
                    bigramme = item.get_key()
                    words = bigramme.split()
                    if len(text) > 50*L:
                        text += "\n"
                        L += 1
                    text += " " + words[1]
                    break

    return text

### Main: lecture des paramÃ¨tres et appel des mÃ©thodes appropriÃ©es
###
###       argparse permet de lire les paramÃ¨tres sur la ligne de commande
###             Certains paramÃ¨tres sont obligatoires ("required=True")
###             Ces paramÃ¨tres doivent Ãªtres fournis Ã  python lorsque l'application est exÃ©cutÃ©e
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='markov_cip1_cip2.py')
    parser.add_argument('-d', required=True, help='Repertoire contenant les sous-repertoires des auteurs')
    parser.add_argument('-a', help='Auteur a traiter')
    parser.add_argument('-f', help='Fichier inconnu a comparer')
    parser.add_argument('-m', required=True, type=int, choices=range(1, 3),
                        help='Mode (1 ou 2) - unigrammes ou digrammes')
    parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer')
    parser.add_argument('-G', type=int, help='Taille du texte a generer')
    parser.add_argument('-g', help='Nom de base du fichier de texte a generer')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    parser.add_argument('-P', action='store_true', help='Retirer la ponctuation')
    parser.add_argument('-A', action='store_true', help='Retirer la ponctuation')
    args = parser.parse_args()

    ### Lecture du rÃ©pertoire des auteurs, obtenir la liste des auteurs
    ### Note:  args.d est obligatoire
    ### auteurs devrait comprendre la liste des rÃ©pertoires d'auteurs, peu importe le systÃ¨me d'exploitation
    cwd = os.getcwd()
    if os.path.isabs(args.d):
        rep_aut = args.d
    else:
        rep_aut = os.path.join(cwd, args.d)

    rep_aut = os.path.normpath(rep_aut)
    authors = os.listdir(rep_aut)
    ### Enlever les signes de ponctuation (ou non) - DÃ©finis dans la liste PONC
    if args.P:
        remove_ponc = True
    else:
        remove_ponc = False

    ### Si mode verbose, reflÃ©ter les valeurs des paramÃ¨tres passÃ©s sur la ligne de commande
    if args.v:
        print("Mode verbose:")
        print("Calcul avec les auteurs du repertoire: " + args.d)
        if args.f:
            print("Fichier inconnu a,"
                  " etudier: " + args.f)

        print("Calcul avec des " + str(args.m) + "-grammes")
        if args.F:
            print(str(args.F) + "e mot (ou digramme) le plus frequent sera calcule")

        if args.a:
            print("Auteur etudie: " + args.a)

        if args.P:
            print("Retirer les signes de ponctuation suivants: {0}".format(" ".join(str(i) for i in PONC)))

        if args.G:
            print("Generation d'un texte de " + str(args.G) + " mots")

        if args.g:
            print("Nom de base du fichier de texte genere: " + args.g)

        print("Repertoire des auteurs: " + rep_aut)
        print("Liste des auteurs: ")
        for a in authors:
            aut = a.split("/")
            print("    " + aut[-1])

### Ã€ partir d'ici, vous devriez inclure les appels Ã  votre code
    if args.A or args.a:
        cwd = os.getcwd()
        if os.path.isabs(args.d):
            rep_aut = args.d
        else:
            rep_aut = os.path.join(cwd, args.d)

        rep_aut = os.path.normpath(rep_aut)

        if args.a:
            pathTexts = rep_aut + "\\" + args.a

    if args.F: # calcul de la fréquence du mot
        if args.a: #pour un auteur
            graphAuteur = buildGraphAuteur(pathTexts, args.m)
            tabFreq = calculFrequence(graphAuteur)

            print("Le " + str(args.F) + "e element le plus frequent est de l'auteur " + args.a + " : " + str(tabFreq[args.F - 1]))
        elif args.A: #pour chaque auteur
            for author in authors:
                pathTexts = rep_aut + "\\" + author
                graphAuteur = buildGraphAuteur(pathTexts, args.m)
                tabFreq = calculFrequence(graphAuteur)

                for element in range(1, args.F+1    ):
                    print("Le " + str(element) + "e element le plus frequent est de l'auteur " + author + " : " + str(tabFreq[element-1]))

    if args.f: #calcul de la proximité du texte inconnu
        if os.path.isabs(args.f):
            relativepath = args.f
        else:
            relativepath = os.path.join(cwd, args.f)
        #il faut que le fichier inconnu soit dans le même dossier que markov.py
        relativepath = os.path.normpath(relativepath)

        #print("path du texte inconnnue " + relativepath)

        gInconnu = buildGraph(relativepath, args.m)

        if args.a: #pour un auteur
            calculProximiteAuteur(gInconnu, rep_aut, args.a, args.m)
        elif args.A: #pour tous les auteurs
            calculProximiteToutAuteur(gInconnu, rep_aut, authors, args.m)
    if args.G and args.g: # génére un texte random
        if args.A: #pour un auteur
            file = open(args.g, "w", encoding="utf-8")
            for author in authors:
                file.write("Auteur : " + author + "\n:: Debut:\n")

                pathTexts = rep_aut + "\\" + author
                graphAuteur = buildGraphAuteur(pathTexts, args.m)
                text = buildRandomText(args.m, args.G, graphAuteur)

                file.write(text + "\n:: Fin\n")
        elif args.a: #pour tous les auteurs
            file = open(args.g, "w")
            graphAuteur = buildGraphAuteur(pathTexts, args.m)
            text = buildRandomText(args.m, args.G, graphAuteur)

            file.write(text)

        file.close()
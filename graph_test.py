#  l'import randint servira pour générer "aléatoirement" le graph
from random import randint
#  l'import json servira pour écrire dans un fichier les dictionnaires
import json
# l'import argparse va permettre de récupérer des arguments lors de l'éxécution du script dans un terminal si il y en a
import argparse


class Graph:
    # variable du constructeur de l'objet graph nombre_s -> le nombre de sommets, nombre_a -> le nombre d'arêtes, p -> graph pondéré ou non
    # maxp -> valeur maximum de pondération (par arête), minp -> valeur minimum de pondération (par arête), o -> graph orienté ou non
    # v -> impression ou non d'information dans le terminal
    def __init__(self, nombre_s, nombre_a, p, maxp, minp, o, v):
        self.v = v
        if self.v == 0 or self.v == 2:
            print("###################\n#CREATION DU GRAPH#\n###################\n\n")
        self.ns = nombre_s
        self.na = nombre_a
        self.p = p
        self.p = p
        self.o = o
        # initialisation (self.td) qui va contenir en clé le numéro du sommet et en valeur un liste contenant les sommets auquel il est relié
        self.td = {}
        # initialisation (self.tp) qui contiendra les valeurs des arrêtes (si la clé est 36 alors l'arêtes est celle qui relie trois et six))
        self.tp = {}
        # conteur qui est la condition du while qui créer les arêtes
        self.count_a = 0
        # initialisation du dictionnaire (avec les sommets/arêtes) vide
        for i in range(nombre_s):
            self.td[str(i)] = []
        # si le graph a générer n'est pas orienté
        if o == 0:
            # tant que le nombre d'arêtes n'est pas généré on ré-essaye d'en créer
            while self.count_a < nombre_a:
                # sommet aléatoire de départ générer aléatoirement entre 0 et le nombre de sommet (pour qu'i soit dans la taille de  graph demandé)
                s = randint(0, nombre_s-1)
                # sommet aléatoire "d'arriver" générer aléatoirement entre 0 et le nombre de sommet (pour qu'i soit dans la taille de  graph demandé)
                a = randint(0, nombre_s-1)
                # condition si s et a différent (on ne souhaite pas qu'un sommet pointe vers lui même), si s n'est pas dans a ou l'inverse ( on ne les re-rajoutes pas)
                if s != a and s not in self.td[str(a)] and a not in self.td[str(s)]:
                    # on met à jour le graph en ajoutant l'arête dans a et s
                    self.td[str(s)].append(a)
                    self.td[str(a)].append(s)
                    # on ajoute 1 au conteur d'arête (pour la condition d'arrêt du while)
                    self.count_a += 1
                    # si on a demandé beaucoup d'information en temps réel on pourra voir chaque arrête ajouté
                    if self.v == 2:
                        print("arêtes créé entre "+str(s)+" et "+str(a)+"ajouté au graph")
        # si on veut un graph orienté on attribut une fois l'arête à un sommet ducoup elle part de s pour aller vers a
        if o == 1:
            while self.count_a < nombre_a:
                s = randint(0, nombre_s-1)
                a = randint(0, nombre_s-1)
                if s != a and s not in self.td[str(a)] and a not in self.td[str(s)]:
                    self.td[str(s)].append(a)
                    self.count_a += 1
                if self.v == 2:
                    print("arêtes en direction de " + str(s) + " vers " + str(a) + "ajouté au graph")
        # si on veut un graph pondéré on attribut une valeur entre le min et le max demandé à chaque arêtes
        if p == 1:
            print("\n###################################\n#Attribution des valeur aux arêtes#\n###################################\n")
            for i in range(nombre_a):
                v_p = randint(minp, maxp)
                self.tp[i](v_p)
                # et si v == 3 on écrit dans le terminal chaque valeur ajouté
                if self.v == 2:
                    print("valeur ", v_p, " attribué à l'arête", i)
        if self.v == 0 or self.v == 2:
            print("###############\n#Graphe généré#\n###############\n", self.td, "\n\n")


def Dominating_set_m(graph_d, df):
    if graph_d.v == 0 or graph_d.v == 2:
        print("\n#############################\n#Recherche du dominating set#\n#############################\n\n")
    # création d'une copy du graph que l'on pourra modifié
    ct = graph_d.td.copy()
    # dictionnaire avec les sommets en key et leur nombre d'arêtes associées en valeur
    tal = {}
    # total de point comptabilisé dans le dominating set
    tt = 0
    # liste avec les points du dominating set
    td = []
    # pour le nombre de sommet du graphe  attribution d'une valeur (nombre de connexion) à tal en accédant au dictionnaire ct avec la clé casté en string (str(i))
    for i in range(len(graph_d.td)):
        tal[str(i)] = len(ct.get(str(i)))
    # tant que le total de point comptabilisé n'est pas égale au nombre de sommet du graph on continue
    while tt < graph_d.ns:
        # recherche de la key avec le plus d'arête
        key_max_v = max(ct, key=tal.get)
        if graph_d.v == 2:
            print("clé en cour de traitement ", key_max_v)
        # ajout du sommet au tablau dominating set
        td.append(key_max_v)
        # création d'un tableau temporaire dans lequel on copie tout les points testé grâce à cette key (key_max_v)
        vt = ct[str(key_max_v)].copy()
        vt.append(int(key_max_v))
        # mis à jour de tt avec le nombre de point comptabilisé
        tt += len(vt)
        # suppression des points comptabilisé du tableau ct et tal car ils sont plus intéressant
        for cle in vt:
            del ct[str(cle)]
            del tal[str(cle)]
        # suppression des points comptabilisé dans les valeurs (liste de connexion) de ct car il ne sont plus intéressant
        for cle, value in ct.items():
            n = []
            for f in value:
                if f not in vt:
                    n.append(f)
            ct[cle] = n
    # affichage des résultats en fonction de la verbose choisis
    if graph_d.v == 0 or graph_d.v == 2:
        print("\ndominating set : ", td, "\nnb de points dans le dominating set -> ", len(td), "| nombre de points connectés -> ", tt)
    # écriture des résultats dans un fichier
    with open(df, 'w') as f:
        f.write("graphe original : " + json.dumps(graph_d.td) + "\n\n" + "dominating set " + json.dumps(td) + " nb de points dans le dominating set -> " + str(len(td)) + " | nombre de points connectés -> " + str(tt)+"\n\n")


# création de l'objet parser
parser = argparse.ArgumentParser()
# ajout d'argument à l'objet parser
parser.add_argument('-nb_s', type=int, help="nombre de sommets de votre graph", default=1000)
parser.add_argument('-nb_a', type=int, help="nombre d'arêtes de votre graph", default=15000)
parser.add_argument('-p', type=int, help="arêtes pondéré -> 1 sinon -> 0", default=0)
parser.add_argument('-max_p', type=int, help="valeur maximal pour la pondération ", default=10)
parser.add_argument('-min_p', type=int, help="valeur minimal pour la pondération", default=0)
parser.add_argument('-o', type=int, help="graph orienté 1 -> sinon 0", default=0)
parser.add_argument('-v', type=int, help="voulez vous avoir des informations en temps réel sur votre terminal -> 0 sinon 1, 2 -> toutes les informations", default=1)
parser.add_argument('-pf', type=str, help="path avec avec nom du fichier à la fin ou nom du fichier dans lequel vous voulez la réponse (si il existe le contenu actuel sera écrasé sinon le fichier sera créé)", default="res_graph.txt")
args = parser.parse_args()
# création de l'objet graph avec en argument les arguments du script ou les défauts
graph = Graph(args.nb_s, args.nb_a, args.p, args.max_p, args.min_p, args.o, args.v)
Dominating_set_m(graph, args.pf)
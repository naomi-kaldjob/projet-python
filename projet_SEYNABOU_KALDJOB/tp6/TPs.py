# Correction de G. Poux-Médard, 2021-2022

# =============== PARTIE 1 =============
# =============== 1.1 : REDDIT ===============
# Library
import praw
import math
import numpy as np
from collections import Counter
from scipy.sparse import csr_matrix
import re
# Fonction affichage hiérarchie dict
def showDictStruct(d):
    def recursivePrint(d, i):
        for k in d:
            if isinstance(d[k], dict):
                print("-"*i, k)
                recursivePrint(d[k], i+2)
            else:
                print("-"*i, k, ":", d[k])
    recursivePrint(d, 1)

# Identification
reddit = praw.Reddit(client_id='5OReEScx5mXTlYzfnIaTJA', client_secret='vtrYQ706ln118NJ8ySidoSUu7YtYnw', user_agent='last_chance')

# Requête
limit = 100
#all
hot_posts = reddit.subreddit('clustering').hot(limit=limit)#.top("all", limit=limit)#

# Récupération du texte
docs = []
docs_bruts = []
afficher_cles = False
for i, post in enumerate(hot_posts):
    if i%10==0: print("Reddit:", i, "/", limit)
    if afficher_cles:  # Pour connaître les différentes variables et leur contenu
        for k, v in post.__dict__.items():
            pass
            print(k, ":", v)

    if post.selftext != "":  # Osef des posts sans texte
        pass
        #print(post.selftext)
    docs.append(post.selftext.replace("\n", " "))
    docs_bruts.append(("Reddit", post))

#print(docs)

# =============== 1.2 : ArXiv ===============
# Libraries
import urllib, urllib.request, _collections
import xmltodict

import matplotlib.pyplot as plt
# Paramètres
query_terms = ["clustering"]
max_results = 50

# Requête
url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
data = urllib.request.urlopen(url)

# Format dict (OrderedDict)
data = xmltodict.parse(data.read().decode('utf-8'))

#showDictStruct(data)

# Ajout résumés à la liste
for i, entry in enumerate(data["feed"]["entry"]):
    if i%10==0: print("ArXiv:", i, "/", limit)
    docs.append(entry["summary"].replace("\n", ""))
    docs_bruts.append(("ArXiv", entry))
    #showDictStruct(entry)

# =============== 1.3 : Exploitation ===============
print(f"# docs avec doublons : {len(docs)}")
docs = list(set(docs))
print(f"# docs sans doublons : {len(docs)}")

for i, doc in enumerate(docs):
    print(f"Document {i}\t# caractères : {len(doc)}\t# mots : {len(doc.split(' '))}\t# phrases : {len(doc.split('.'))}")
    if len(doc)<100:
        docs.remove(doc)

longueChaineDeCaracteres = " ".join(docs)

# =============== PARTIE 2 =============
# =============== 2.1, 2.2 : CLASSE DOCUMENT ===============
from Classes import Document

# =============== 2.3 : MANIPS ===============
import datetime
collection = []
collection_arvix=[]
collection_reddit=[]
for nature, doc in docs_bruts:
    if nature == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formatés de la même manière à ce stade.
        #showDictStruct(doc)

        titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
        try:
            authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, séparés par une virgule
        except:
            authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
        summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
        date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime

        doc_classe = Document(titre, authors, date, doc["id"], summary)  # Création du Document
        collection.append(doc_classe)  # Ajout du Document à la liste.
        collection_arvix.append(doc_classe)
    elif nature == "Reddit":
        #print("".join([f"{k}: {v}\n" for k, v in doc.__dict__.items()]))
        titre = doc.title.replace("\n", '')
        auteur = str(doc.author)
        date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com/"+doc.permalink
        texte = doc.selftext.replace("\n", "")

        doc_classe = Document(titre, auteur, date, url, texte)

        collection.append(doc_classe)
        collection_reddit.append(doc_classe)

# Création de l'index de documents
id2doc = {}
for i, doc in enumerate(collection):
    id2doc[i] = doc.titre
    print(doc.auteur)
    #print(doc.authors)

# =============== 2.4, 2.5 : CLASSE AUTEURS ===============
from Classes import Author

# =============== 2.6 : DICT AUTEURS ===============
authors = {}
aut2id = {}
num_auteurs_vus = 0

# Création de la liste+index des Auteurs
for doc in collection:
    if doc.auteur not in aut2id:
        num_auteurs_vus += 1
        authors[num_auteurs_vus] = Author(doc.auteur)
        aut2id[doc.auteur] = num_auteurs_vus

    authors[aut2id[doc.auteur]].add(doc.texte)


# =============== 2.7, 2.8 : CORPUS ===============
from Corpus import Corpus
corpus = Corpus("Mon corpus")

# Construction du corpus à partir des documents
for doc in collection:
    corpus.add(doc)
corpus.show(tri="abc")
# affichage  les passages des documents contenant le mot-clef entrée en paramètre
corpus.search("Globular")
# tableau qui contient le mot clé et les contextes à gauche et à droite de ce mot clé
corpus.concorde(10,"Globular")
#les statistiques visuelles du corpus
z=corpus.stats()
# dictionnaire qui contient plusieurs informations sur le mot (son identifiant unique, son nombre total d’occurrence. . . )
vocab={}
for index in range(z.shape[0]):
    
    vocab[z.iloc[index,0]]=[index,z.iloc[index,1]]
#construction cette matrice mat TF  
s=0
listerow=list()#création d'une liste
while len(listerow)< (len(vocab)*len(collection)):
    for i in range(len(collection)):

        listerow.append(i) 
row = np.array(listerow)
listecol=list()

for i in range(len(collection)*len(vocab)):

    if i%len(collection)==0:
        s=i/len(collection)
    listecol.append(s)
col = np.array(listecol)

liste=list()
for d in vocab.keys() :
    for doc in collection :
        z=re.sub(r'[0-9]','',doc.titre)
        regex=re.compile('[^\w]|[\s]')
        a=regex.split(z)
        liste.append(a.count(d))

data=np.array(liste)

mat_TF=csr_matrix((data, (row, col)), shape=(len(collection), len(vocab))).toarray()
#stockage des informations sur le  nombre total de documents contenant des mots dans vocab

listeoccdoc=list()
for i in range(len(mat_TF[0])):
    s=0
    for j in range(len(mat_TF)):
        if mat_TF[j][i]>0:
           s=s+1
    
    listeoccdoc.append(s)
i=0
for cle,valeur in vocab.items():
   
    vocab[cle]=valeur+[listeoccdoc[i]]
    i=i+1
#construction cette matrice mat TF-IDF
tf=[]
idf=[]
for d,i in vocab.items() :
    for doc in collection :
        z=re.sub(r'[0-9]','',doc.titre)
        regex=re.compile('[^\w]|[\s]')
        a=regex.split(z)
        tf.append(a.count(d)/len(a))
        idf.append(math.log(len(collection)/i[2]))

data_idf=[tf[i] * idf[i] for i in range(len(tf))]
mat_TF_IDF=csr_matrix((data_idf, (row, col)), shape=(len(collection), len(vocab))).toarray()

print(mat_TF_IDF)

#===== td 7 partie 2 TF-IDF
#demander `a l’utilisateur d’entrer quelques mots-clefs
vecteur_motcle=[]

score={}
mot_cle = str(input("taper des mots clés: "))
#transformer ces mots-clefs sous la forme d’un vecteur sur le vocabulaire précédemment construit
z=re.sub(r'[0-9]','',mot_cle.lower())
regex=re.compile('[^\w]|[\s]')
a=regex.split(z)
#calculer une similarité entre votre vecteur requête et tous les documents
for d,i in vocab.items() :
        
        vecteur_motcle.append(a.count(d))
print(len(vecteur_motcle))
print(mat_TF_IDF[1])
avgdl=[]
for  i,doc in enumerate(collection) :
        score[doc.titre]=np.dot(mat_TF_IDF[i],vecteur_motcle)/(np.linalg.norm(mat_TF_IDF[i])*np.linalg.norm(vecteur_motcle))
        avgdl.append(len(doc.titre.split(' '))) 
 
#trier les scores résultats et afficher les meilleurs résultats.         
score=dict(sorted(score.items(),key=lambda item:item[1],
reverse=True))
print(score)
#=========== OKAPI-BM25=========
score_okapi={}
for  i,doc in enumerate(collection) :
    score=0
    for j in range(len(a)):
        n=vocab[str(a[0])]
        f=mat_TF[i][n[0]]
        moy=sum(avgdl) / len(avgdl)
        score=math.log((len(collection)-n[2]+0.5)/(n[2]+0.5))*((f*(1.2+1))/(f+1.2*(1-0.75+0.75*len(doc.titre.split(' ')))))+score
    score_okapi[doc.titre]=score
score_okapi=dict(sorted(score_okapi.items(),key=lambda item:item[1],
reverse=True))
print(score_okapi)
   
#graphe temporelle
trimestre={1:['01','02','03'],2:['04','05','06'],3:['07','08','09'],4:['10','11','12']}
for annee in range(1900,2022,1):
    frise=[]
    for i,documt in trimestre.items():
        somme=0
        for j, doc in enumerate(collection_arvix):
           
            if  str(doc.date[5:7]) in documt and str(doc.date[0:4])==str(annee):
                #print('c bon')
                z=re.sub(r'[0-9]','',doc.titre.lower())
                regex=re.compile('[^\w]|[\s]')
                a=regex.split(z)
                somme=somme+a.count(mot_cle.lower())
        frise.append(somme)
    print(str(annee)+"->"+str(frise))
f = plt.figure(figsize=(3,3), dpi=100)
a = f.add_subplot(121)
a.plot([1,2,3,4],frise)
f.savefig('evol.png')
# =============== 2.9 : SAUVEGARDE ===============
import pickle

# Ouverture d'un fichier, puis écriture avec pickle
with open("corpus.pkl", "wb") as f:
    pickle.dump(corpus, f)

# Supression de la variable "corpus"
del corpus

# Ouverture du fichier, puis lecture avec pickle
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

# La variable est réapparue


#print(len(id2doc))
#print(corpus.search(motcle))






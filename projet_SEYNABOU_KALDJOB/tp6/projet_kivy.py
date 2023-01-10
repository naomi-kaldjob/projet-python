import praw
import urllib, urllib.request, _collections
import xmltodict
from Classes import Document
import datetime

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from Corpus import Corpus
import re
import numpy as np 
import math
from scipy.sparse import csr_matrix
class projet2:
    #====initialisation
    def __init__(self):
       self.collection_arvix=[]
       self.collection_reddit=[]
       self.corpusa = Corpus("Mon corpus")
       self.collection=[]
    def arvix_redd(self,entreemotss):
        reddit = praw.Reddit(client_id='5OReEScx5mXTlYzfnIaTJA', client_secret='vtrYQ706ln118NJ8ySidoSUu7YtYnw', user_agent='last_chance')

    # Requête
        limit = 100
        hot_posts = reddit.subreddit(entreemotss).hot(limit=limit)#.top("all", limit=limit)#
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
        query_terms = [entreemotss]
        max_results = 50
        docs = list(set(docs))
        url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
        data = urllib.request.urlopen(url)
        data = xmltodict.parse(data.read().decode('utf-8'))

    #showDictStruct(data)

    # Ajout résumés à la liste
        for i, entry in enumerate(data["feed"]["entry"]):
            if i%10==0: print("ArXiv:", i, "/", limit)
            docs.append(entry["summary"].replace("\n", ""))
            docs_bruts.append(("ArXiv", entry))
            #showDictStruct(entry)

        # =============== 1.3 : Exploitation ===============
        #print(f"# docs avec doublons : {len(docs)}")
        docs = list(set(docs))
        #print(f"# docs sans doublons : {len(docs)}")

        for i, doc in enumerate(docs):
        # print(f"Document {i}\t# caractères : {len(doc)}\t# mots : {len(doc.split(' '))}\t# phrases : {len(doc.split('.'))}")
            if len(doc)<100:
                docs.remove(doc)

        longueChaineDeCaracteres = " ".join(docs)

        # =============== PARTIE 2 =============
        # =============== 2.1, 2.2 : CLASSE DOCUMENT ===============
    

        # =============== 2.3 : MANIPS ===============
        
        collection = []
        
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
                # Ajout du Document à la liste.
                self.collection.append(doc_classe)
                self.collection_arvix.append(doc_classe)
            elif nature == "Reddit":
                #print("".join([f"{k}: {v}\n" for k, v in doc.__dict__.items()]))
                titre = doc.title.replace("\n", '')
                auteur = str(doc.author)
                date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
                url = "https://www.reddit.com/"+doc.permalink
                texte = doc.selftext.replace("\n", "")

                doc_classe = Document(titre, auteur, date, url, texte)

                self.collection.append(doc_classe)
                self.collection_reddit.append(doc_classe)
        resultat=[self.corpuss(self.collection_reddit),self.corpuss(self.collection_arvix)]
        return resultat
      
       #==========fonction qui retoune le wordcloud
    def corpuss(self,collection):
       
        self.id2doc = {}
        for i, doc in enumerate(collection):
            self.corpusglobal=self.corpusa.add(doc)
            self.id2doc[i] = doc.titre
        self.chaine="".join([d for d in self.id2doc.values() ])
        
        word_cloud = WordCloud(collocations = False, background_color = 'white', max_words = 20).generate(self.chaine)
       
        return word_cloud

    def graph_evolution_temporelle(self,motcles,annees,entremotss,auteur,source):
        #vérification si la source est arvix 
        if source.lower()=="arvix":
            #affichage de l'évoloytion temporelle d'un mot par un graphique
           arv=self.frise_temporelle(motcles,annees,self.collection_arvix,auteur,entremotss)
           f = plt.figure(figsize=(3,3), dpi=100)
           a = f.add_subplot(121)
           a.plot([1,2,3,4],arv)
        #vérification si l'utilisateur saisie reddit comme source
        if source.lower()=="reddit":
               #affichage de l'évoloytion temporelle d'un mot par un graphique
            red=self.frise_temporelle(motcles,annees,self.collection_reddit,auteur,entremotss)
            f = plt.figure(figsize=(3,3), dpi=100)
            a = f.add_subplot(122)
            a.plot([1,2,3,4],red)
        #vérification si l'utilisateur saisie reddit et arvix comme source
        if source.lower()=="all":
               #affichage de l'évoloytion temporelle d'un mot par un graphique
            arv=self.frise_temporelle(motcles,annees,self.collection_arvix,auteur,entremotss)
            red=self.frise_temporelle(motcles,annees,self.collection_reddit,auteur,entremotss)
            f = plt.figure(figsize=(4,3), dpi=100)
            a = f.add_subplot(121)
            a.set_title(label="fréquence du mot/trimestre-arvix",fontsize=7,color='black')
            a.plot([1,2,3,4],arv)
            a = f.add_subplot(122)
            a.set_title(label="fréquence du mot/trimestre-reddit",fontsize=7,color='black')
            a.plot([1,2,3,4],red)
        return f 
    #=====prends en entrée une chaine de caractère d'auteurs et fractionne la chaîne pour retourner une liste 
    def liste_auteur(self,auteurss):
        z=re.sub(r'[0-9]','',auteurss)
        regex=re.compile('[^\w]|[\s]')
        self.auteur=regex.split(z)
        return self.auteur
    #fonction pour déterminer l'évolution temporelle d'un mot
    def frise_temporelle(self,motcle,annee,collection,auteurss,entremots):
        self.arvix_redd(entremots)
        self.frise=[]
        #une année a 12 mois et donc 4 trimestres. Les clés de la liste self.trimestre sont les numeros des trimestres et les valeurs:les mois correspondants
        self.trimestre={1:['01','02','03'],2:['04','05','06'],3:['07','08','09'],4:['10','11','12']}
         #calcule la fréquence d'un mot pour chaque semestre dans l'ensemble des documents pour un auteur donné
        for i,documt in self.trimestre.items():
            self.somme=0
            for j, doc in enumerate(collection):
                q=self.liste_auteur(doc.auteur.lower())
                
                if str(auteurss.lower())=="all":
                    if  str(doc.date[5:7]) in documt and str(doc.date[0:4])==str(annee):
                    
                        z=re.sub(r'[0-9]','',doc.titre.lower())
                        regex=re.compile('[^\w]|[\s]')
                        a=regex.split(z)
                        self.somme=self.somme+a.count(motcle.lower())
                else:
                    if  str(doc.date[5:7]) in documt and str(doc.date[0:4])==str(annee) and str(auteurss.lower()) in q:
                    
                        z=re.sub(r'[0-9]','',doc.titre.lower())
                        regex=re.compile('[^\w]|[\s]')
                        a=regex.split(z)
                        self.somme=self.somme+a.count(motcle.lower())
            self.frise.append(self.somme)
        return self.frise
    #Creation de la matrice tf-idf
    def mat_tf_idf(self,entremots):
    
        self.arvix_redd(entremots)
        #Récupération des statistiques 
        z=self.corpusa.stats()
        #création d'un vocabulaire
        self.vocab={}
        for index in range(z.shape[0]):
    
            self.vocab[z.iloc[index,0]]=[index,z.iloc[index,1]]
           
        s=0
        #création de la matrice tf
        listerow=list()
        while len(listerow)< (len(self.vocab)*len(self.collection)):
            for i in range(len(self.collection)):

                    listerow.append(i)
        row = np.array(listerow)
        listecol=list()

        for i in range(len(self.collection)*len(self.vocab)):

                if i%len(self.collection)==0:
                    s=i/len(self.collection)
                listecol.append(s)
        col = np.array(listecol)
        listeoccdoc=list()
        liste=list()
        for d in self.vocab.keys() :
            for doc in self.collection :
                z=re.sub(r'[0-9]','',doc.titre.lower())
                regex=re.compile('[^\w]|[\s]')
                a=regex.split(z)
                liste.append(a.count(d.lower()))

            data=np.array(liste)

        mat_TF=csr_matrix((data, (row, col)), shape=(len(self.collection), len(self.vocab))).toarray()
        #création de la matrice tf-idf
        for i in range(len(mat_TF[0])):
                s=0
                for j in range(len(mat_TF)):
                     if mat_TF[j][i]>0:
                        s=s+1
          
                listeoccdoc.append(s)
        i=0
        for cle,valeur in self.vocab.items():
   
            self.vocab[cle]=valeur+[listeoccdoc[i]]
            i=i+1
        tf=[]
        idf=[]
        for d,i in self.vocab.items() :
            for doc in self.collection :
                z=re.sub(r'[0-9]','',doc.titre.lower())
                regex=re.compile('[^\w]|[\s]')
                a=regex.split(z)
        
        
                tf.append(a.count(d.lower())/len(a))
                
                idf.append(math.log(len(self.collection)/i[1]))

        data_idf=[tf[i] * idf[i] for i in range(len(tf))]
        self.mat_TF_IDF=csr_matrix((data_idf, (row, col)), shape=(len(self.collection), len(self.vocab))).toarray()
        return self.mat_TF_IDF

    def score_tf(self,motcles,annees,entremots,auteur):
      #calacul du score_tf-idf
       mat=self.mat_tf_idf(entremots)
       z=re.sub(r'[0-9]','',motcles.lower())
       regex=re.compile('[^\w]|[\s]')
       a=regex.split(z)
       vecteur_motcle=[]
       for d,i in self.vocab.items() :
                    
            vecteur_motcle.append(a.count(d.lower()))
           
       avgdl=[]
       score={}
       for  i,doc in enumerate(self.collection) :
            q=self.liste_auteur(doc.auteur)
            if str(doc.date[0:4])==str(annees) and doc.date[0:4] and str(auteur.lower())=='all':
                if np.dot(mat[i],vecteur_motcle)/(np.linalg.norm(mat[i])*np.linalg.norm(vecteur_motcle))>0:
                    score[doc.titre]=np.dot(mat[i],vecteur_motcle)/(np.linalg.norm(mat[i])*np.linalg.norm(vecteur_motcle))
            if str(doc.date[0:4])==str(annees) and doc.date[0:4] and str(auteur) in q:
                if np.dot(mat[i],vecteur_motcle)/(np.linalg.norm(mat[i])*np.linalg.norm(vecteur_motcle))>0:
                    score[doc.titre]=np.dot(mat[i],vecteur_motcle)/(np.linalg.norm(mat[i])*np.linalg.norm(vecteur_motcle))
            
            avgdl.append(len(doc.titre.split(' '))) 
            
                    
       score=dict(sorted(score.items(),key=lambda item:item[1],reverse=True))
       return score

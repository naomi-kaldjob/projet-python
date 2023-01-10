# Correction de G. Poux-Médard, 2021-2022

from Classes import Author
from itertools import chain
import re
import pandas
# =============== 2.7 : CLASSE CORPUS ===============
class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
        

# =============== 2.8 : REPRESENTATION ===============
    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))



    def search(self,motcle):
        self.listdemot=list()
        docu = list(self.id2doc.values())
     
        print("documenttitre+++-------"+str(docu[0].titre))
        
   
        self.chaine="".join([d.titre for d in docu])
   
        
        print("------")
        print(self.chaine)
        print("-----------------")
       
        for m in re.finditer(motcle, self.chaine):
      
            z=m.end() 
            print(self.chaine[(m.start()-20):z])
            print(z)
          
            
  #"interface textuel et visuel comme dash , comparer les corpus"

      
            
    def concorde(self,taille,motcle):
        table = pandas.DataFrame(columns=['contexte gauche','motif trouve','contexte droit'])
        self.listdemot=list()
        self.motiftrouve=list()
        self.contexteg=list()
        self.contexted=list()
        docu = list(self.id2doc.values())
        #print("docum")
        print("documenttitre+++-------"+str(docu[0].titre))
        
       # map(search, self.id2doc.values())
        #for v in range(len(docu)):
         #   print(docu[v].titre)
        self.chaine=" ".join([d.titre for d in docu])
        #position=0
        #longueur=0
        for m in re.finditer(motcle, self.chaine):
       # resultat=stra[:m.start()] + stra[m.end():]
        #resultat = regex.find(stra)
       # resultat = re.findall('(cluster).+',self.chaine)
            z=m.start()
            k=m.end() 
            #print(self.chaine[(position+longueur):z-1])
            print(self.chaine[(z-taille):z-1])
            print(z)
            print(self.chaine[k+1: k+taille])
            self.contexteg.append(self.chaine[(z-taille):z-1])
            self.contexted.append(self.chaine[k+1: k+taille])
            self.motiftrouve.append(motcle)
           # new_row = {'contexte gauche':self.chaine[(z-taille):z-1],'motif trouve':motcle,'contexte droit':self.chaine[k+1: k+taille]}
           # new_df = pandas.DataFrame([new_row])
           # dfo = pandas.concat([table, new_df], axis=0, ignore_index=True)
            # position=position+z
           # longueur=len(motcle)+longueur
        new_row={}
        new_row['contexte gauche']=self.contexteg
        new_row['motif trouve']=self.motiftrouve
        new_row['contexte droite']=self.contexted
        table = pandas.DataFrame(new_row)
        #print( self.listdemot)
        print( table)
        
    def nettoyer_texte(self,chaine): 
        
       token= chaine.lower()
       token = token.strip()
       token = re.sub(r'[^\w\s]','',token)
       token = re.sub(r'[0-9]','',token) 
    def stats(self):
        freq = pandas.DataFrame(columns=['mots','term frequency','document frequency'])
        mots1=list()
        motssansdoublons=list()
        frequence=list()
        documentfrequency=list()
        docu=list(self.id2doc.values())
        for w in docu:
            
            z=re.sub(r'[0-9]','',w.titre) 
            regex=re.compile('[^\w]|[\s]')
            for z in regex.split(z): 
                if z!='':
                    mots1.append(z)
        motssansdoublons=list(set(mots1))
        motssansdoublons.sort()
        
        #print(mots1)
        #print(motssansdoublons)
        for w in motssansdoublons:
           somme=0
           frequence.append( mots1.count(w))
           for j in docu:
                #regex=re.compile(w)
                #if regex.match(j.titre)!=None:
                regex=re.compile('[^\w]|[\s]')
                 
                if w in regex.split(j.titre):
                        somme=somme+1
           documentfrequency.append(somme)
        new_row={}
        new_row['mots']=motssansdoublons
        new_row['term_frequency']=frequence
        new_row['document_frequency']=documentfrequency
        freq = pandas.DataFrame(new_row)
        
        return freq
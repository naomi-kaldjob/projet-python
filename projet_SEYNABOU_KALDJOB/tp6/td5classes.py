# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 16:16:32 2022

@author: pnkal
"""
from Classes import Document
class RedditDocument(Document):
    def _init_(self,titre,auteur,date,url,texte,nbcomment):
        self.nbcommentaires=nbcomment
        super()._init_(titre,auteur,date,url,texte)
    def getTitre(self):
        return self.titre
    def getAuteur(self):
        return self.auteur
    def getDate(self):
        return self.date
    def getUrl(self):
        return self.texte   
    def __str__(self):
        return self.auteur,self.date,self.titre,self.texte,self.nbcommentaires
   
class ArvixDocument(Document):
    def _init_(self,titre,auteur,date,url,texte,coauteurs):
        self.coauteurs=[]
        super()._init_(titre,auteur,date,url,texte)
    def getTitre(self):
        return self.titre
    def getAuteur(self):
        return self.auteur
    def getDate(self):
        return self.date
    def getUrl(self):
        return self.texte  
    def ajoutcoauteurs(self,coauteurs):
        self.coauteurs.append(coauteurs)
    def __str__(self):
        return self.auteur,self.date,self.titre,self.texte,self.coauteurs
    
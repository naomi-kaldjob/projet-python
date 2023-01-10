# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:26:38 2022

@author: ndieng1
"""

class Author :
    def __init__(self,name,ndoc,production):
        
        self.name=name #argument positionnel
        self.ndoc=ndoc
        self.production=production
       
    def add(self,documents):
        nbredocu=len(self.production)
        self.production[nbredocu]= documents
        
    def __str__(self):
         return("Le nom:"+self.name,"Le document:"+self.ndoc,"La production:"+self.production,"\n Le nombre de documents publiés:"+self.production)

        
        
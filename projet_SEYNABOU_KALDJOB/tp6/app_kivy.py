from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image

#from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from projet_kivy import projet2
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
import matplotlib.pyplot as plt
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.lang import Builder

class app_kivy(FloatLayout):
    def build(self):
        #affichage du logo
        self.add_widget(Image(source='logo.png',size_hint=(0.4,0.4),pos_hint={'x':.25, 'y':.70}))
        #Remplissage de champs de saisie de thématique par les utilisateurs 
        self.theme=MDTextField(
        hint_text="entrez une thématique",
        icon_left="magnify",icon_right_color_focus=( 0, 1, 0, 1),size_hint=(0.3,0.05),pos_hint={'x':.25, 'y':.60})
        self.add_widget(self.theme)
        # button qui lance l'affichage de wordcloud pour chaque corpus
        self.rechercher=MDRoundFlatIconButton(text="rechercher",
    text_color= "black",size_hint=(0.02,0.05), pos_hint={'x':.55, 'y':.62})
        self.rechercher.bind(on_press=self._graphique)
        self.add_widget(self.rechercher)
        # button qui permet d'ouvrir une nouvelle page
        self.suivant=MDRoundFlatIconButton(text="suivant",icon="arrow-right.png",
    text_color= "black",size_hint=(0.2,0.05),pos_hint={'x':.33, 'y':.10})
        self.suivant.bind(on_press=self._suivant)
        self.add_widget(self.suivant)
    
    def _graphique(self,instance):
        p=projet2()
        #Affichage des wordclouds reddit et Arvix
        a=p.arvix_redd(self.theme.text)
        nomsite=['wordcloud à partir des documents sous reddit','wordcloud à partir des documents sous Arvix']
        fig = plt.figure(figsize=(13,2),dpi=100)
        for i in range(len(a)):
            ax = fig.add_subplot(121+i)
            wordcloud = a[i]
            ax.set_title(label=nomsite[i],fontsize=10,color='black')
            ax.imshow(wordcloud)
            ax.axis('off')
        fig.savefig('nuage.png',facecolor='white')##F5F7FA
        self.add_widget(Image(source='nuage.png',pos_hint={'x':.001}))
       
    def _suivant(self,instance):
        
        self.theme2=self.theme.text
        theme="le thème choisi est"+self.theme.text
        #effacer les boutons et zones de saisie
        self.clear_widgets()
        self.thematique=Label(text=theme,
        size_hint=(0.1,0.15),pos_hint={'x':.10, 'y':.80},color='white')
        self.add_widget(self.thematique)
        #zone de saisie du mot clé
        self.motcle=MDTextField(
        hint_text="entrez une mot clé",
       size_hint=(0.2,0.05),pos_hint={'x':.25, 'y':.70})
        self.add_widget(self.motcle)
         #zone de saisie de la source
        self.source=MDTextField(
        hint_text="entrez une source(reddit ou Arvix ou all)",
       size_hint=(0.2,0.05),pos_hint={'x':.65, 'y':.70})
        self.add_widget(self.source)
         #zone de saisie du nom de l'auteur
        self.entréeauteur=MDTextField(
        hint_text="entrez un auteur ou ecrivez 'all' pour tous ",
       size_hint=(0.2,0.05),pos_hint={'x':.25, 'y':.80})
        self.add_widget(self.entréeauteur)
         #zone de saisie de l'année
        self.entréeannee=MDTextField(
        hint_text="entrez une année",
       size_hint=(0.2,0.05),pos_hint={'x':.65, 'y':.80})
        self.add_widget(self.entréeannee)
        #bouton rechercher
        self.motbutton=MDRoundFlatIconButton(text="rechercher",
    text_color= "black",size_hint=(0.1,0.05), pos_hint={'x':.25, 'y':.60})
        self.motbutton.bind(on_press=self.graph_temporel)
        self.add_widget(self.motbutton)
        #bouton qui retourne à la page d'avant
        self.retour=MDRoundFlatIconButton(text="retour",icon="arrow-left",
    text_color= "black",size_hint=(0.1,0.05), pos_hint={'x':.25, 'y':.10})
        self.retour.bind(on_press=self.buildretour)
        self.add_widget(self.retour)

    def graph_temporel(self,instance):
        p=projet2()
        #appel 
        a=p.graph_evolution_temporelle(self.motcle.text,self.entréeannee.text,self.theme2,self.entréeauteur.text,self.source.text)
        print(a)
        #sauvegarde des graphiques par une image
        a.savefig('evol.png')
        #Affichage de l'image
        self.add_widget(Image(source='evol.png', opacity= 0.9,size_hint_x= 0.35,size_hint_y= 0.35,pos_hint={'x': 0.15, 'y': 0.20},allow_stretch= True,keep_ratio=False))
        #calcul du score tf
        score=p.score_tf(self.motcle.text,self.entréeannee.text,self.theme2,self.entréeauteur.text)
        #integration du score et du titre des documents dans un tableau plot
        fig, ax = plt.subplots(figsize=(10,3), dpi=100)
        clust_data =[]
        compter=1
        for i,doc in score.items():
            #Récuperer les 3 meilleurs scores avec leur titre de document
            if compter<=3:
                clust_data.append([i,doc])
            compter=compter+3
        collabel=['titre de document','score']
        #eviter de stocker dans une table une liste vide
        if len(clust_data)>0:
            table=ax.table(cellText=clust_data,colLabels=collabel,loc='center')
            table.set_fontsize(15)
        ax.axis('tight')
        ax.axis('off')
        #sauvegarder une table plot dans un graphique
        fig.savefig('table.png')
        self.add_widget(Image(source='table.png', opacity= 0.9,size_hint_x= 0.4,size_hint_y= 0.4,pos_hint={'x':.50, 'y':.20},allow_stretch= True,keep_ratio=False))
    #===== fonction qui permet de retourner à la page principale
    def buildretour(self,instance):
        #affichage du logo
   
        self.add_widget(Image(source='logo.png',size_hint=(0.4,0.4),pos_hint={'x':.25, 'y':.70}))
        #zone de saisie de la thématique
        self.theme=MDTextField(
        hint_text="entrez une thématique",
        icon_left="magnify",icon_right_color_focus=( 0, 1, 0, 1),size_hint=(0.3,0.05),pos_hint={'x':.25, 'y':.60})
        self.add_widget(self.theme)
        #Affichage du bouton rechercher
        self.rechercher=MDRoundFlatIconButton(text="rechercher",
    text_color= "black",size_hint=(0.02,0.05), pos_hint={'x':.55, 'y':.62})
        self.rechercher.bind(on_press=self._graphique)
        self.add_widget(self.rechercher)
         #Affichage du bouton suivant
        self.suivant=MDRoundFlatIconButton(text="suivant",icon="arrow-right.png",
    text_color= "black",size_hint=(0.2,0.05),pos_hint={'x':.33, 'y':.10})
        self.suivant.bind(on_press=self._suivant)
        self.add_widget(self.suivant)
     
    
class Exemple_De_FloatLayoutApp(MDApp):
 
    def build(self):
        root=app_kivy()
        root.build()
        return root
if __name__=="__main__":
    Exemple_De_FloatLayoutApp().run()
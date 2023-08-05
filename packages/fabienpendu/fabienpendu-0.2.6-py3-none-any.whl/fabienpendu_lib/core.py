import importlib.resources  
from pathlib import Path
import pygame.mixer #à installer
import random      
import time
import tkinter as tk
import unidecode #à installer

class Pendu:
    """ Affiche le mot  du pendu sous la forme _ _  _  a _ e"""
    def  __init__(self, anglais=None):
        pygame.mixer.init()
        self.anglais = anglais
        self.root = tk.Tk()
        self.initialisetkinter()
        self.root.bind("<Key>", self.clavier)
        self.root.mainloop()

    def initialisetkinter(self):
        self.label = tk.Label(self.root, text= "Jeu du pendu", font=('Courier', 50, 'bold'))
        self.label.grid(row=0, column=0)
        self.label_perdu = tk.Label(self.root, text= "Perdu", font=('Courier', 50, 'bold'))
        self.label_gagne =  tk.Label(self.root, text= "Gagné", font=('Courier', 50, 'bold'), foreground= 'red')

        self.label_touches_utilisées = tk.Label(self.root,  text= 'Lettres utilisées:\n', font=('Courier', 20, 'bold'))
        self.label_touches_utilisées.grid(row=1, column=0)

        self.can = tk.Canvas(self.root, width=264, height=183, bg='black')
        self.can.grid(row=2, column = 0)
        with importlib.resources.path("fabienpendu_lib", "pendu_cool.gif") as path:
            self.mon_image  = tk.PhotoImage(file=path)
        self.can.create_image(0,0, anchor='nw', image=self.mon_image)

        #Initialisation variable et  affichage masque
        if self.anglais == None:
            dictionnaire = importlib.resources.read_text("fabienpendu_lib", "dico_mots_simple.txt")
        else:
            dictionnaire = importlib.resources.read_text("fabienpendu_lib", "dico_anglais.txt")
        mots = [mot for mot in dictionnaire.split()]
        mot_choisi = mots[random.randint(0, len(mots))]
        mot_choisi = "".join(mot_choisi.split())


        self.mot = mot_choisi
        self.liste_lettre = [i for i in self.mot]

        self.mot_masque=str( "_ "*(len(self.mot))).split()
        self .label_masque =  tk.Label(self.root, text= self.mot_masque, font=('Courier', 50, 'bold'))
        self.label_masque.grid()
        self.vie = 7
        self.nbr_pendu = 0
        self.touches_utilisées = "Lettres utilisées:\n"


    def clavier(self,event):
        """ gère les événements touches appuyées : joue son clavier , teste si échap appuyée """
        touche = event.keysym
        if touche:
            self.play("touche_clavier.wav") 
            self.touches_utilisées = self.touches_utilisées + touche
            self.label_touches_utilisées.config (text = self.touches_utilisées)
            self.rech_lettre(touche)

    def rech_lettre(self, lettre):
        """  Recherche lettre dans  la liste_lettre et modifie (ou pas )le mot masque en conséquence
                ; retourne 'Perdu' si plus de vie ; retourne Gagné si gagné """
        self.lettre_trouvée = False
        compt = 0
        for i in self.liste_lettre:
            if unidecode.unidecode(i) == lettre or lettre == 'apostrophe' and  i== "'":
                self.mot_masque[compt] = i
                self.lettre_trouvée = True
            compt += 1

        if self.lettre_trouvée:
            self.play("souffle_air.wav")
        else:
            self.play("buzzer_perdu.wav")
            
        if self.vie and "_" in self.mot_masque and not self.lettre_trouvée :
            self.vie -= 1
            self.aff(self.nbr_pendu)
            self.nbr_pendu += 1
            #return '-1 vie'
        
        elif self.vie and "_" in self.mot_masque and self.lettre_trouvée:
            self .label_masque.config(text= self.mot_masque)
            self.root.update()
            #return 'continue'
                    
        elif self.vie and not "_" in  self.mot_masque:#gagné
            self.label_masque.config(text= self.mot_masque)
            self.root.update()   # -----> pas necessaire affichage réactulisé avec grid 
            self.label_gagne.grid()
            self.play("applaudissement.wav")
            time.sleep(3)
            self.reset(self.root)
            self.initialisetkinter()

        
       
        
        

    def aff(self, nbr_pendu):
        """ affiche image pendu selectionnée . Teste si dernière image == partie finie"""
        im = "pendu_"+str(nbr_pendu)+'.gif'
        with importlib.resources.path("fabienpendu_lib",im) as image:
            self.mon_image = tk.PhotoImage(file = image )
        self.can.create_image(0,0, anchor='nw', image=self.mon_image)
        self.root.update()
        """test """
        if nbr_pendu == 6:
            self.label_perdu.grid()
            self.label_masque.config(text= self.mot)
            self.root.update()  
            self.play("sf-os-nuque-briser-05.wav")
            self.play("sf_cri_surprise_femme.wav")
            
            for a in range(2):
                for i in ['_1',  '',  '_2', '']:
                    im = "pendu_6"+str(i)+'.gif'
                    with importlib.resources.path("fabienpendu_lib",
                                                  im) as image:
                        self.mon_image = tk.PhotoImage(file = image )
                    self.can.create_image(0,0, anchor='nw', image=self.mon_image)
                    self.root.update()
                    time.sleep(0.5)

            self.reset(self.root)
            self.initialisetkinter()
            #return 'fini'
            
        
    def play(self, extrait):
        with importlib.resources.path("fabienpendu_lib", extrait) as son:
                    bruitage = pygame.mixer.Sound(son)
                    bruitage.play()#os.popen('aplay -q '+str(son))

        
    def reset(self,fen):
        for widget in fen.winfo_children():
            widget.destroy() 
      
            
def pendu():
    i = Pendu()
def hanged():
    i = Pendu('anglais')

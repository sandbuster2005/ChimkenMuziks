#made by sand
from os import listdir
from os.path import isdir,isfile
from random import randint
from .utils import *
import importlib

def init_image( self ):
    self.img_mode = "img"
    self.img_script = "appdata.scripts.test"
    self.thumbnail = None
    self.screen = None
    self.path_to_img = "appdata/image/"# chemin du dosier image
    self.imgs = []# liste des images contenu dans le chemin indiqué ,vide = random
    self.img = ""# image actuel
    self.show = 1# affiche ou non l'image selectionné
    
    if "64" in self.sys_architecture:
        self.img_command = "./libs/x86/jp2a_x86 --chars=\ \  --fill --color-depth=8"
        
    elif "arm" in self.sys_architecture:
        self.img_command = "./libs/arm/jp2a_arm --chars=\ \  --fill --color-depth=8"
        
    
    
    
def get_img( self, path, files = [], start = 0 ):
    """
    cette fonction permet de lister tout les png et jpg contenu dans le dossier image du programme 
    
    limite:
    cette fonction d'accéde pas au sous dossier
    """
    if start:
        self.imgs = []
        
    for f in listdir( path ):
        if isdir( path + f ):# un sous dossier existe
            self.get_img( path + f + "/" , [] )
            
        elif f[ -4: ] == ".png"  or f[ -4: ] == ".jpg":# c'est une image supporté par la librairie
            self.imgs.append( path + f )
    
    
def display_img( self ):
    """
    cette fonction affiche dans le terminal ;
    l'image choisis : image précisé
    une image aléatoire de la liste imgs :image non précisé
    
    limite:
    les images doit étre dans le dossiers image du programme
    """
    if self.img_mode == "img":
        if not ".mid" in self.song:
            self.get_metadata()
        
        if self.thumbnail != None:
            image = self.thumbnail
            
        else:
            image = self.img
            
        if self.img != "" or self.thumbnail != None:# une image est selectionné
            self.external_call( [ f"{ self.img_command } { image }" ], True )# image selectionné
            print("")
            
        elif self.img == "" and self.imgs != []:# il y a au moins une image et aucune selcetionné
            self.external_call( [ f"{ self.img_command } { self.imgs[ randint( 0, len( self.imgs ) - 1) ] }" ], True )# image aléatoire
            print("")
            
    if self.img_mode == "script":
        self.Screen.display()
        
def select_img( self ):
    """
    cette fonction permet de choisir une image parmit la galerie ou de choisir aléatoire
    
    limite:
    cette fonction demande une valeur numérique de l utilisateur pour selectionner l'image
    et affiche le nom de toute les image de la liste
    
    """
    
    word = "0"
    while all_numbers( word , len( self.imgs ) ):
        for x in range( len( self.imgs ) ):
            print( x, self.imgs[ x ] )
            
        print( len( self.imgs ), "random" )# index max +1
        word = input( "select img:" )
        
        if all_numbers( word, len( self.imgs ) ):
            if int( word ) == len( self.imgs ):
                self.img = ""# aleatoire
                word = ""
            
            else:
                self.external_call( [ f"{ self.img_command }  { self.imgs[ int( word ) ] }" ], True )
                confirm = input( "y/n ?" )
                
                if confirm.lower() == "y":
                    self.img = self.imgs[ int( word ) ] # selection
                    word = ""
            
        self.display()

def load_script(self):
    
    if self.img_script != "":
        self.Screen = importlib.import_module(self.img_script).Screen()
        print(self.Screen)
        
def screen_mode(self):
    choice = [ "image mode " , "script mode" ]
    word = self.ask_list(choice)
    
    if word == "0":
        self.img_mode = "img"
        
    if word == "1":
        self.img_mode = "script"
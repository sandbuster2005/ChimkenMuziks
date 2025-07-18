#made by sand
from os import listdir
from os.path import isdir,isfile
from random import randint
from .utils import *
from .terminal import *
from ..readchar import readchar
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
    
    #if self.sysname == 'nt':
    #    self.img_command = "libs\\win\\win32-dist\\jp2a.exe --chars=\"  \" --fill --colors"

    #elif "64" in self.sys_architecture:
    #    self.img_command = "./libs/x86/jp2a_x86 --chars=\ \  --fill --color-depth=8"
        
    #elif "arm" in self.sys_architecture:
    #    self.img_command = "./libs/arm/jp2a_arm --chars=\ \  --fill --color-depth=8"
   
    #else:
    #    print("WARNING: Image module not initialized, could not recognize used system")
        
    
    
    
def get_img( self, path, files = [], start = 0 ):
    """
    cette fonction permet de lister tout les png et jpg contenu dans le dossier image du programme 
    
    limite:
    cette fonction d'accéde pas au sous dossier
    """
    
    if self.sysname == 'nt':
        path = path.replace("/", "\\")
    
    if start:
        self.imgs = []
        
    for f in listdir( path ):
        
        if isdir( path + f ):# un sous dossier existe
            self.get_img( path + f + self.separator , [] )
            
        #elif self.sysname == 'nt':
        #    
        #    if f[ -4: ] == ".jpg" or f[ -4: ] == ".jpeg":# c'est une image supporté par la librairie
        #        self.imgs.append( path + f )
        #        
        #    if f[ -4: ] == ".png":# c'est une image précédemment non supporté par la librairie Windows
        #        self.imgs.append( path + f )
       
        else:
            
            if f[ -4: ] == ".png"  or f[ -4: ] == ".jpg" or f[ -4: ] == ".jpeg":# c'est une image supporté par la librairie
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
            
            #self.external_call( f"{ self.img_command } { image }", True )# image selectionné
            self.print_image_to_screen(image, 5)
            print("")
            
       elif self.img == "" and self.imgs != []:# il y a au moins une image et aucune selcetionné
            
            #self.external_call( f"{ self.img_command } { self.imgs[ randint( 0, len( self.imgs ) - 1) ] }", True )# image aléatoire
            self.print_image_to_screen( self.imgs[ randint( 0, len( self.imgs ) - 1) ] , 5)
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
        
        wipe()
        word = self.ask_list(self.imgs+["random"],"select img:" )
        
        if all_numbers( word, len( self.imgs ) ):
            if int( word ) == len( self.imgs ):
                self.img = ""# aleatoire
                word = ""
            
            else:
                #self.external_call( f"{ self.img_command }  { self.imgs[ int( word ) ] }" , True )
                self.print_image_to_screen(self.imgs[ int( word ) ], 5)

                out("y/n ?")
                confirm = readchar(  )
                
                if confirm.lower() == "y":
                    self.img = self.imgs[ int( word ) ] # selection
                    word = ""
            
        self.display()

def load_script(self):
    """
    WIP
    """
    if self.img_script != "":
        self.Screen = importlib.import_module(self.img_script).Screen()
        
def screen_mode(self):
    """
    WIP
    """
    choice = [ "image mode " , "script mode" ]
    word = self.ask_list(choice)
    
    if word == "0":
        self.img_mode = "img"
        
    if word == "1":
        self.img_mode = "script"
#made by sand
from os import listdir
from os.path import isdir,isfile
from .ffiles import *
from .ffiles import get_file as getfile
from .utils import *


def init_file( self ):
    self.path_to_file = r"/home/sand/Musique/musiqe/"# chemin du dossier musique
    self.dirs = []# liste des dossier dans le chemin indiqué
    self.files = []# chanson chargé
    self.favorite = ""
        
def get_file( self, path, files = [] ):
    """
    cette fonction permet de récuperer tout les fichier waw,mp3 et m4a dans un dossier et sous dossiers,
    elle remet aussi a 0 l'historique ,stop toute chanson en cours de lecture et ajoute a la liste des dossiers
    le dossiers et les sous dossiers si il n'y sont pas
    
    limite:
    path est un chemin d'accés auquel l'utilisateur peut accéder
    files est une liste qui peut contenir des chemin d'accés auquel l'utilisateur peut accéder au préalable
    renvoie les ficher déja inclus et ceux du dossier scanné
    """
    self.song = None
    self.played = []
    self.player.stop()
    for f in listdir( path ):
        if isdir( path + f ):
            
            if [ path + f , '1' ] in self.dirs:# le dossier est activé
                files += self.get_file( path + f + "/", [] )
            
            elif [ path + f, '0' ] in self.dirs:# le dossier est desactivé 
                continue
            
            else:# le dossier n'est pas repertorié
                files += self.get_file( path + f + "/", [] )
                self.dirs.append( [ path + f, '1' ] )
                
        if f[ -4: ] == ".mp3"  or f[ -4: ] == ".m4a" or f[ -4: ] == ".wav" or f[ -5: ] == ".flac" or f[ -4: ] == ".mid":#le fichier est un audio
            files.append( path + "/" + f )
            
    return files


def select_dir( self ):
    """
    cette fonction permet d'activer/desactiver des dossiers de la liste de dossier sous dossier
    pour oculter les chanson qu'il contient
    
    limite:
    demande une valeur numérique a l'utilisateur pour selectionner un dossier/sous dossiers
    """
    word = "0"
    while all_numbers( word ):
        white()
        
        for x in range( len( self.dirs ) ):
            print( x, self.dirs[ x ] )
            
        word = input( "switch folder on/off:" )
        
        if all_numbers( word, len( self.dirs ), 1 ):
            self.switch_dir( int( word ) )


def switch_dir( self, word ):
    """
    cette fonction permet d'activer ou desactiver un dossier de la liste
    """
    self.dirs[ word ][ 1 ] = str( 1 - int( self.dirs[ word ][ 1 ] ) )
  
  
def find_file( self, word ):
    """
    cette fonction renvoie une liste contentant toute les chaine de charactères de la liste de chanson chargés
    contenant une chaine de charactère word
    
    limite:
    toute les charactère sont considérée comme minuscule
    """
    return [ [ self.files[ x ].rsplit( "/" )[ -1 ], x ] for x in range(len(self.files)) if word.lower() in self.files[ x ].lower().rsplit( "/", 1 )[ -1 ] ]#cherche dans la liste de son en ignorant les majuscules    


def check_adress( self ):
    """
    cette fonction permet de verifier si l'adresse existe et est un dossier
    """
    if not isdir( self.path_to_file ):
        while not isdir( self.path_to_file ):
            try:
                self.path_to_file = str(self.external_return(["xplr"],))[2:-3]+"/"
            except:
                self.path_to_file = input("chemin du dossier musique: ")
    self.write_param()
    
    
def change_main_path( self ):
    """
    cette fonction permet de changer l'adresse des chansons
    """
    self.path_to_file = ""
    self.check_adress()
    self.load_songs()
     
     
def mani_file(self):
    """
    cette fonction permet de supprimer , deplacer(dans les dossiers connu)
    et renommer le fichier actuel
    """
    if self.song != None:
        word = self.ask_list( [ "delete ", "move", "rename", "convert"] )
        if all_numbers( word, 3 ):
            if int( word ) == 0:
                choice = self.ask( "are you sure (y/n)" )
                
                if choice == "y":
                    rm_file( self.song )
                
            if int( word ) == 1:
                choice = self.ask_list( [ self.dirs[ x ][ 0 ] for x in range( len( self.dirs ) ) ] )
                
                if all_numbers( choice, len( self.dirs ), mode = 1 ):
                    mv_file( self.song, self.dirs[ int( choice ) ][ 0 ] + "/" + self.song.rsplit( "/", 1 )[ 1 ] )
                
            if int( word ) == 2:
                choice = self.ask( "new_name :" )
                mv_file( self.song, self.song.rsplit( "/",1 )[ 0 ] + choice + "." + self.song.rsplit( ".",1 )[ 1 ])
            
            if int( word ) == 3:
                self.change_extension()
                
            self.load_songs()
            
def get_words(self):
    self.words = []
    if self.song != None :
        file = self.song.rsplit( ".", 1 )[ 0 ] + ".lrc"
        print( isfile( file ) )
        if isfile( file ):
            data = getfile( file )
            data = data.split("[" )
            data = data[1:]
            
            for x in range(len(data)):
                data[x] = replace(data[x],'\n').split("]",1)
            
            new_data = []
            for x in range(len(data)):
                if  ":" in data[x][0] and  '.' in data[x][0] and len(data[x][0]) == 8:
                    new_data.append(data[x])
                    
            data = new_data
            for x in range(len(data)):        
                data[x][0] = int(data[x][0][:2]) * 60 + int(data[x][0][3:5]) + int(data[x][0][6:8]) / 100 
            
            self.words = data
            
def change_extension(self):
    white()
    option = [".mp3", ".m4a", ".wav" , ".flac" ]
    word = self.ask_list( option )
    if all_numbers( word, len( option ), 1 ):
        confirm = self.ask( "delete original (y/n)?" )
        new = self.song.rsplit( ".",1 )[ 0 ] + option[ int( word ) ]
        self.external_call(f"ffmpeg -i '{self.song}' '{new}' " , shell = True)
        if confirm == "y":
            rm_file(self.song)

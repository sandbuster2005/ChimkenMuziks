#made by sand
from random import randint
from .utils import *
from .ffiles import *
import libs.midi2audio as midi2audio
from os import listdir
from os.path import isfile, splitext, dirname
from libs.tinytag import TinyTag
def init_song( self ):
    #SONG variables
    self.song = None# son actuelle
    self.last_word = -1 
     
def choose_song( self ):
    """
    cette fonction permet de:
    choisir une chanson aléatoire : mode 0
    choisit la chanson qui suit dans la liste : mode 1 
    """
    if self.playlist:
        if self.playlist_files:
            files = self.playlist_files
    
    elif self.play_favorite:
        if self.favorite:
            files = self.favorite
            
        else:
            self.play_favorite = 0
            files = self.files
            input(" no favorite press any button to continue")
        
    else:
        files = self.files
        
    if self.mode == 1:
        if self.fchoose and self.favorite and self.song not in self.favorite and not self.exterior and not self.playlist:
            num = randint(1 , min(100 , 50 + len(self.favorite)*5) )
            
            if num > 50:
                files = self.favorite
                
        self.song = files[ randint( 0, len( files ) - 1 ) ]#chanson aleatoire
        
                
        
    if self.mode == 0:
        
        if self.song == None:
            self.song = files[ 0 ]# si pas de chanson joué avant prendre la premiére
            
        else:
            if self.song not in files:
                files = self.files
            self.song = files[ ( files.index( self.song ) + 1 ) % len( files ) ]#chanson suivante : index+1
        


def load_songs( self ):
    """
    cette fonction permet de charge en memoire les chanson de la playlist selectionné/toute
    et de remmetre a 0 le lecteur
    """
    if self.exterior:
        self.files = self.get_file( self.exterior, [] )
    
    else:    
        self.files = self.get_file( self.path_to_file, [] )
        
    self.indexs = self.get_index_data( self.files )
    self.files = [ [self.indexs[x] ,self.files[x]] for x in range( len(self.indexs) ) ]
    self.song = None


def play_song( self ,choose = 1):
    """
    cette fonction lance le choix de chanson et la joue
    """
    
    if len( self.files ) != 0:
        #self.bar = None
        if choose:
            self.choose_song()
            
        self.get_words()
        
        if self.song[-4:] ==".mid":
            self.suspend("play_midi")
        
        self.play()
        self.pause = 0
    
    
def play( self ):
    """
    cette fonction lance la musique actuel ,l'ajoute a l'historique et affiche l intérface
    
    limite:
    une musique doit étre selectionné au préalable 
    """
    if self.played == []:
        self.played.append(  self.song  )# ajoute a l'historique
        
    elif self.played[ -1 ] != self.song :# ajoute a l'historique si la chanson a changé
        self.played.append(  self.song  )
    
    if ".mid" in self.song[1] :
        self.player.set_mrl( "appdata/cache/" + self.song[1].rsplit( ".", 1 )[ 0 ].rsplit("/",1)[1] + ".wav" )
     
    else:
        self.player.set_mrl( self.song[1] )# charge la chanson
        
    self.player.play()
    self.suspend( "display" )# affiche
    
    
def play_last( self ):
    """
    cette fonction permet de jouer la chanson precedante a condition qu'il y en est une
    """
    if len(self.played) > 1:
        self.played.pop()
        self.song = self.played[ -1 ]
        self.play_song(choose = 0)
        
        
def historic( self ):
    """
    cette fonction affiche l'historique d'écoute de la session 
    """
    self.show_list( [ f"{ self.played[ x ][ 0 ] }: {  self.played [ x ][ 1 ].rsplit( '/',1 )[ -1 ] }" for x in range( len( self.played ) ) ], num = False )# index : nom  

def select( self ):
    """
    cette fonction permet de chercher une chanson dans la liste chargé de chanson et l'affiche
    
    limite:
    cette fonction demande une chaine de charactére a rechercher dans les données de l'utilisateur
    """
    self.search = True
    white( 1 )
    INPUT = self.ask( "rechercher dans la liste de chanson :" )
    result = self.find_file( str( INPUT ) )#recherche dans les fichiers
    self.show_list( [ f"{ result[ x ][ 1 ] } :{ result[ x ][ 0 ] }" for x in range( len( result ) ) ], num = False )

def play_midi(self):
    """
    cette fonction permet de produire un fichier mp3 a partir un fichier midi selectionner et un codec selectionné
    """
    outs = listdir("appdata/midi_codec")
    word = self.ask_list(outs)
    
    if all_numbers( word, len( outs ), 1 ):
        print("appdata/midi_codec/" + outs[int(word)])
        self.convert_midi(  )
        
def convert_midi(self,soundmap = ""  , destination = "appdata/cache/" ):
    """
    cette fonction permet de stocker temporairement un fichier mp3 crée a partir d'un fichier midi
    """
    if soundmap == "":
        soundmap = self.base_soundmap
        
    destination = destination + self.song.rsplit( ".", 1 )[ 0 ].rsplit("/",1)[1] + ".wav"
    
    if not isfile(destination) :
        fs = midi2audio.FluidSynth(soundmap)
        fs.midi_to_audio(self.song ,destination )
        
def default_midi(self):
    """
    cette fonction permet a l'utillisteur de selectionner un codec par defaut pour les fichier midi pour eviter les interuptions futur
    """
    choice = listdir( "appdata/midi_codec" )
    word = self.ask_list(choice)
    
    if all_numbers( word, len(choice) , 1):
        self.base_soundmap = f"appdata/midi_codec/{ choice[ int( word ) ] }"
        
def get_metadata(self):
    """
    cette fonction permet de recuperer la miniature d'un fichier si elle existe 
    """
    tag = TinyTag.get(self.song[1] , image = True)
    artist = tag.artist
    image = tag.images.any
    
    if image != None :
        image = image.data
        write_file("appdata/cache/preview", image , mode = "wb")
        image = "appdata/cache/preview"
        
    elif tag.album != None:
        for j in [splitext(self.song[1] )[0], dirname(self.song[1])+self.separator+tag.album]:
            for i in [j+'.jpg', j+'.jpeg', j+'.png']:
                if isfile(i):
                    file = open(i, 'rb')
                    write_file("appdata/cache/preview", file.read(), mode = "wb")
                    image = "appdata/cache/preview"
                    file.close()
                    
    self.thumbnail = image
    

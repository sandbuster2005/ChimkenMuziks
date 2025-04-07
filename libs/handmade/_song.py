#made by sand
from random import randint
from .utils import *
from .ffiles import *
import libs.midi2audio as midi2audio
from os import listdir
from os.path import isfile
from libs.tinytag import TinyTag

def init_song( self ):
    #SONG variables
    self.song = None# son aactuelle
    self.mode = 1# 1:aleatoire 0:dans'l'ordre
    self.base_soundmap = "appdata/midi_codec/default.sf2"   
        
def choose_song( self ):
    """
    cette fonction permet de:
    choisir une chanson aléatoire : mode 0
    choisit la chanson qui suit dans la liste : mode 1 
    """
    if self.mode == 1:
        self.song = self.files[ randint( 0, len( self.files ) - 1 ) ]#chanson aleatoire
        
    if self.mode == 0:
        if self.song == None:
            self.song = self.files[ 0 ]# si pas de chanson joué avant prendre la premiére
            
        else:
            self.song = self.files[ ( self.files.index( self.song ) + 1 ) % len( self.files ) ]#chanson suivante : index+1


def load_songs( self ):
    """
    cette fonction permet de charge en memoire les chanson de la playlist selectionné/toute
    et de remmetre a 0 le lecteur
    """     
    self.files = self.get_file( self.path_to_file, [] )
    self.song = None


def play_song( self ):
    """
    cette fonction lance le choix de chanson et la joue
    """
    if len( self.files ) != 0:
        self.bar = None
        self.choose_song()
        self.get_words()
        if self.song[-4:] ==".mid":
            self.suspend("play_midi")
        print(self.song)
        self.play()
        self.pause = 0
    
    
def play( self ):
    """
    cette fonction lance la musique actuel ,l'ajoute a l'historique et affiche l intérface
    
    limite:
    une musique doit étre selectionné au préalable 
    """
    
    if self.played == []:
        self.played.append( self.files.index( self.song ) )# ajoute a l'historique
        
    elif self.played[ -1 ] != self.files.index( self.song ):# ajoute a l'historique si la chanson a changé
        self.played.append( self.files.index( self.song ) )
        
    if ".mid" in self.song :
        self.player.set_mrl( "appdata/cache/" + self.song.rsplit( ".", 1 )[ 0 ].rsplit("/",1)[1] + ".wav" )
    else:
        self.player.set_mrl( self.song )# charge la chanson
    self.player.play()
    self.suspend( "display" )# affiche
    
    
def play_last( self ):
    """
    cette fonction permet de jouer la chanson precedante a condition qu'il y en est une
    """
    if len(self.played) > 1:
        self.played.pop()
        self.song = self.files[ self.played[ -1 ] ]
        self.play()
        
        
def historic( self ):
    """
    cette fonction affiche l'historique d'écoute de la session 
    """
    self.show_list( [ f"{ self.played[ x ] }: { self.files[ self.played [ x ] ].rsplit( '/',1 )[ -1 ] }" for x in range( len( self.played ) ) ], num = False )# index : nom  

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
        
    self.get_input()

def play_midi(self):
    outs = listdir("appdata/midi_codec")
    word = self.ask_list(outs)
    if all_numbers( word, len( outs ), 1 ):
        print("appdata/midi_codec/" + outs[int(word)])
        self.convert_midi(  )
        
def convert_midi(self,soundmap = ""  , destination = "appdata/cache/" ):
    if soundmap == "":
        soundmap = self.base_soundmap
    destination = destination + self.song.rsplit( ".", 1 )[ 0 ].rsplit("/",1)[1] + ".wav"
    if not isfile(destination) :
        fs = midi2audio.FluidSynth(soundmap)
        fs.midi_to_audio(self.song ,destination )
        
def default_midi(self):
    choice = listdir( "appdata/midi_codec" )
    word = self.ask_list(choice)
    if all_numbers( word, len(choice) , 1):
        self.base_soundmap = f"appdata/midi_codec/{ choice[ int( word ) ] }"
        
def get_metadata(self):
    tag = TinyTag.get(self.song , image = True)
    artist = tag.artist
    image = tag.images.any
    if image != None :
        image = image.data
        write_file("appdata/cache/preview", image , mode = "wb")
        image = "appdata/cache/preview"
    self.thumbnail = image
    

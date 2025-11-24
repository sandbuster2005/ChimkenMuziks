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
    self.song = None# currently playing song
    self.last_word = -1 # pos in current lyrics if there are

def load_songs( self ):
    """
    cette fonction permet de charge en memoire les chanson de la playlist selectionné/toute
    et de remmetre a 0 le lecteur
    """
    #use arg from exterior
    if self.exterior:
        self.files = self.get_file( self.exterior, [] )
    
    else:    
        self.files = self.get_file( self.path_to_file, [] )
        
    self.indexs = self.get_index_data( self.files )
    self.files = [ [self.indexs[x] ,self.files[x]] for x in range( len(self.indexs) ) ]# [index in database , song file]
    self.song = None


def play_song( self ,choose = 1):
    """
    cette fonction lance le choix de chanson et la joue
    """
    
    if len( self.files ) != 0: # if there are song

        if choose:
            self._choose_song()
            
        self.get_words()# check if there are a lyric file
        
        if self.song[-4:] ==".mid": # if its a midi comvert it with a midi codec to a playable version
            self.play_midi()

        if not self.played:#if list is empty
            self.played.append(self.song)# add to historic

        elif self.played[-1] != self.song:  # add to historic if song as changed
            self.played.append(self.song)# add to historic
            self.song_saved = False # tell backend is can save a play in the database

        self._play() #send song to the player

        self.pause = 0


def _choose_song(self):
    """
    cette fonction permet de:
    choisir une chanson aléatoire : mode 0
    choisit la chanson qui suit dans la liste : mode 1
    """
    if self.playlist:# choose in playlist if there one
        if self.playlist_files:
            files = self.playlist_files

    elif self.play_favorite: #choose in favorite if the option is on
        if self.favorite:
            files = self.favorite

        else:# check if theres file in favorite
            self.play_favorite = 0
            files = self.files

    else: #normal files
        files = self.files

    if self.mode == 1: # random
        if self.fchoose and self.favorite and self.song not in self.favorite and not self.exterior and not self.playlist:
            num = randint(1, min(100, 50 + len(self.favorite) * 5))

            if num > 50:
                files = self.favorite

        self.song = files[randint(0, len(files) - 1)]  # chanson aleatoire

    if self.mode == 0: # in order

        if not self.song:# if its first song playing
            self.song = files[0]

        else:
            if self.song not in files: # if >there's a problem fall back to global
                files = self.files

            self.song = files[(files.index(self.song) + 1) % len(files)]  # chanson suivante : index+1
    
def _play( self ):
    """
    cette fonction lance la musique actuel ,l'ajoute a l'historique et affiche l intérface
    
    limite:
    une musique doit étre selectionné au préalable 
    """

    if ".mid" in self.song[1]:# if its a midi played converted version
        self.player.set_mrl("appdata/cache/" + self.song[1].rsplit(".", 1)[0].rsplit("/", 1)[1] + ".wav")

    else:
        self.player.set_mrl( self.song[1] )# load song
    
    self.bar = None # reset bar
    self.player.play()
    self.display()
    
    
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
    self.search = True
    self.show_list( [ f"{ self.played[ x ][ 0 ] }: {  self.played [ x ][ 1 ].rsplit( '/',1 )[ -1 ] }" for x in range( len( self.played ) ) ], num = False )# index : nom

def select( self ):
    """
    cette fonction permet de chercher une chanson dans la liste chargé de chanson et l'affiche
    
    limite:
    cette fonction demande une chaine de charactére a rechercher dans les données de l'utilisateur
    """
    self.search = True
    INPUT = self.ask( "rechercher dans la liste de chanson :" )
    result = self.find_file( str( INPUT ) )#recherche dans les fichiers
    if result:
        self.show_list( [ f"{ result[ x ][ 1 ] } :{ result[ x ][ 0 ] }" for x in range( len( result ) ) ], num = False )
    else:
        self.out("no song corresponding")

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
    
    if image :
        image = image.data
        write_file("appdata/cache/preview", image , mode = "wb")
        image = "appdata/cache/preview"
        
    elif tag.album :
        for j in [splitext(self.song[1] )[0], dirname(self.song[1])+self.separator+tag.album]:
            for i in [j+'.jpg', j+'.jpeg', j+'.png']:
                if isfile(i):
                    file = open(i, 'rb')
                    write_file("appdata/cache/preview", file.read(), mode = "wb")
                    image = "appdata/cache/preview"
                    file.close()
                    
    self.thumbnail = image
    

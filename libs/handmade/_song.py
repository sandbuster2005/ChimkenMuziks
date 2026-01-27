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
    self.new_logger("song")

def load_songs( self ):
    """
    cette fonction permet de charge en memoire les chanson de la playlist selectionné/toute
    et de remmetre a 0 le lecteur
    """


    #use arg from exterior
    if self.exterior:
        self.logger["song"].info(f"loading song from {self.exterior}")
        self.files = self.get_file( self.exterior, [] )
    
    else:
        self.logger["song"].info(f"loading song from {self.path_to_file}")
        self.files = self.get_file( self.path_to_file, [] )

    self.update_song_database( self.files )

    self.indexs = self.get_index_data( self.files )
    self.logger("song").debug(f"loaded indexes : {self.index}")
    
    self.files = [ [self.indexs[x] ,self.files[x]] for x in range( len(self.indexs) ) if isfile(self.files[x]) ]# [index in database , song file]
    self.song = None
    self.logger["song"].info(f"loaded {len( self.files)} song in memory")
    self.logger["song"].trace(f"file : { self.files }")
    
    self.load_favorite_database()


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
            self.logger["song"].info(f"added {self.song} to historic")

        elif self.played[-1] != self.song:  # add to historic if song as changed
            self.played.append(self.song)# add to historic
            self.logger["song"].info(f"added {self.song} to historic")

        self._play() #send song to the player

        self.pause = 0


def _choose_song(self):
    """
    cette fonction permet de:
    choisir une chanson aléatoire : mode 0
    choisit la chanson qui suit dans la liste : mode 1
    """
    self.logger["song"].info("choosing song")
    if self.playlist:# choose in playlist if there one
        if self.playlist_files:
            files = self.playlist_files
            self.logger["song"].debug("choosing song in playlist")

    elif self.play_favorite: #choose in favorite if the option is on
        if self.favorite:
            files = self.favorite
            self.logger["song"].debug("choosing song in favorite")

        else:# check if theres file in favorite
            self.play_favorite = 0
            files = self.files
            self.logger["song"].debug("choosing song in files")

    else: #normal files
        files = self.files
        self.logger["song"].debug("choosing song in files")

    if self.mode == 1: # random
        self.logger["song"].debug("choosing randomly")

        if self.fchoose and self.favorite and self.song not in self.favorite and not self.exterior and not self.playlist:
            self.logger["song"].debug("choosing via favorite biased method:")
            num = randint(1, min(100, 50 + len(self.favorite) * 5))

            if num > 50:
                files = self.favorite
                self.logger["song"].debug("choosing in favorite")

        self.song = files[randint(0, len(files) - 1)]  # chanson aleatoire


    if self.mode == 0: # in order
        self.logger["song"].debug("choosing via order:")

        if not self.song:# if its first song playing
            self.song = files[0]

        else:
            if self.song not in files: # if there's a problem fall back to global
                files = self.files

            self.song = files[(files.index(self.song) + 1) % len(files)]  # chanson suivante : index+1

    self.logger["song"].debug(f"chose {self.song}")

def _play( self ):
    """
    cette fonction lance la musique actuel ,l'ajoute a l'historique et affiche l intérface
    
    limite:
    une musique doit étre selectionné au préalable 
    """

    self.logger["song"].info(f"playing {self.song[1]}")

    if ".mid" in self.song[1]:# if its a midi played converted version
        self.logger["song"].info(f"playing midi file")
        self.player.set_mrl("appdata/cache/" + self.song[1].rsplit(".", 1)[0].rsplit("/", 1)[1] + ".wav")

    else:
        self.player.set_mrl( self.song[1] )# load song

    self.song_saved = False  # tell backend is can save a play in the database
    self.bar = None # reset bar
    self.player.play()
    self.display()
    
    
def play_last( self ):
    """
    cette fonction permet de jouer la chanson precedante a condition qu'il y en est une
    """
    if len(self.played) > 1:
        self.logger["song"].info(f"launching previous song ")
        self.played.pop()
        self.song = self.played[ -1 ]
        self.play_song(choose = 0)
        
        
def historic( self ):
    """
    cette fonction affiche l'historique d'écoute de la session 
    """
    self.logger["song"].info("showing played song to user")
    self.logger["song"].debug(f"played : {self.played }")
    self.search = True
    self.show_list( [ f"{ self.played[ x ][ 0 ] }: {  self.played [ x ][ 1 ].rsplit( '/',1 )[ -1 ] }" for x in range( len( self.played ) ) ], num = False )# index : nom

def old_select( self ):
    """
    #cette fonction permet de chercher une chanson dans la liste chargé de chanson et l'affiche
    
    #limite:
    #cette fonction demande une chaine de charactére a rechercher dans les données de l'utilisateur
    """
    self.search = True
    INPUT = self.ask( "rechercher dans la liste de chanson :" )
    result = self.find_file( str( INPUT ) )#recherche dans les fichiers
    if result:
        self.show_list( [ f"{ result[ x ][ 1 ] } :{ result[ x ][ 0 ] }" for x in range( len( result ) ) ], num = False )
    else:
        self.out("no song corresponding")



def _select_song( self , file_list , display_list = None , text = ""):
    white()
    if display_list == None:
        display_list = [ f"{ str( x[ 0 ] ) }: {x[ 1 ].rsplit( '/', 1 )[ 1 ] }" for x in file_list ]

    self.logger["song"].info("showing select song menu to user")
    self.logger["song"].debug(f"display menu : {', '.join( display_list ) }")
    self.logger["song"].debug(f"file list : { file_list }")

    song = self.asker.menu_deroulant( display_list , self.update_logic, text = text ,  search = True )

    if song < len( file_list ):
        self.song = file_list[ song ]
        self.play_song( choose = 0 )

    self.display()

def select( self ):
    self.logger["song"].info("showing song gallery to the User")
    self._select_song( self.files, text = "song library" )
    """
    white()
    song = self.asker.menu_deroulant([ f"{ str(x[0]) }: {x[1].rsplit('/',1)[1]}" for x in self.files ] , self.update_logic , search = True)

    if song < len(self.files):
        self.song = self.files[song]
        self.play_song(choose = 0)

    self.display()
    """

def select_fav( self ):
    self.logger["song"].info("showing favorite song to the User")
    self._select_song( self.favorite, text = "favorite songs" )

    """
    white()
    song = self.asker.menu_deroulant([ f"{ str(x[0]) }: {x[1].rsplit('/',1)[1]}" for x in self.favorite ] , self.update_logic , search = True)

    if song < len(self.favorite):
        self.song = self.favorite[song]
        self.play_song(choose = 0)

    self.display()
    """

def most_played( self ):
    liste = self.played_database()
    display_list = [ f"{ str(x[2]) }: {x[1].rsplit('/',1)[1]}" for x in liste ]
    liste = [ [ x[0], x[1] ] for x in liste ]
    self.logger["song"].info("showing most played song to the User")
    self._select_song( liste , display_list, "most played")
    """
    white()
    song = self.asker.menu_deroulant([f"{str(x[0])}: {x[1].rsplit('/', 1)[1]}" for x in liste],self.update_logic, search=True)

    if song < len(liste):
        self.song = liste[song]
        self.play_song( choose = 0 )

    self.display()
    """
def play_midi(self):
    """
    cette fonction permet de produire un fichier mp3 a partir un fichier midi selectionner et un codec selectionné
    """
    outs = listdir("appdata/midi_codec")
    word = self.asker.menu_deroulant(outs,self.update_logic)
    
    if  word < len( outs ):
        self.convert_midi( "appdata/midi_codec/" + outs[ word ] )
        
def convert_midi(self,soundmap = ""  , destination = "appdata/cache/" ):
    """
    cette fonction permet de stocker temporairement un fichier mp3 crée a partir d'un fichier midi
    """
    #TODO test the fonction
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
    word = self.asker.menu_deroulant( choice )
    self.logger["song"].info("User selecting default midi codec")

    if  word < len(choice):
        self.base_soundmap = f"appdata/midi_codec/{ choice[ int( word ) ] }"

    self.logger["song"].debug(f"new base soundmap : {self.base_soundmap}")
        
def get_metadata(self):
    """
    cette fonction permet de recuperer la miniature d'un fichier si elle existe 
    """
    self.logger["song"].info("checking song metadata")
    tag = TinyTag.get(self.song[1] , image = True)
    artist = tag.artist
    image = tag.images.any
    
    if image :
        self.logger["song"].info("found img")
        image = image.data
        write_file("appdata/cache/preview", image , mode = "wb")
        image = "appdata/cache/preview"
        
    elif tag.album :
        for j in [splitext(self.song[1] )[0], dirname(self.song[1])+self.separator+tag.album]:
            for i in [j+'.jpg', j+'.jpeg', j+'.png']:
                if isfile(i):
                    self.logger["song"].info("found img")

                    with open(i, mode = "rb") as file:
                        write_file("appdata/cache/preview", file.read(), mode = "wb")
                        image = "appdata/cache/preview"
                    
    self.thumbnail = image
    

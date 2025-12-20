#made by sand
from time import sleep,monotonic
from libs.progress.bar import Bar
from math import floor,ceil
from time import sleep,strftime
from os import listdir
from os import name as sysname
from .utils import *
from .ffiles import *
from .terminal import *
import libs.vlc as vlc
import threading
import random
import platform
import os

def init_main( self, directory, song ):
    #process arg passed with the start command
    self.exterior = directory
    self.exterior_song = song
    
    #check problem with windows
    self.sysname = sysname
    
    if sysname == 'nt':
        self.separator = '\\'
        
    else:
        self.separator = '/'
        
    self.sys_architecture = platform.machine()
    self.stay = True  # False pour quiter le lecteur
    self.pause = 0  # pour mettre en pause le lecteur+la barre
    self.bar = None   # la barre de progression du temps de la chanson 
    self.search = False   # pour mettre en pause l afichhage le temps de finir une recherche
    os.environ["VLC_VERBOSE"] = str("-1") # retire les message de warning vlc cassant l affichage
    self.player = vlc.MediaPlayer()  # lecteur
    self.played = []  # historique
    self.timer = None
    self.words = None # parole si existante
    self.input = ReadChar() # systeme d'input 
 
   
def main( self ):
    """
    cette fonction est la fonction d'initialisation du programme et de fonctionnement 
    """
    self.get_param()#get param from file if it exist else create it
    self.get_img( self.path_to_img,start = 1 )#scan all image in repertory
    self.check_adress()#see if current file adress exist
    self.update_song_database()
    self.load_songs()#try to load the song
    self.load_script()
   
    while len( self.files ) == 0:# if folder is empty
        self.out( "no song in folder" )
        self.change_main_path()
        self.load_songs()

    if self.sound_manager != "base":#base sound manager need a media playing to get volume
        self.start_sound()
        self.display()
    
    if self.exterior: # if an argument was pasted from command line
        if self.exterior_song:
            self.exterior_song = clear_adjacent( self.exterior_song, [ "/" ], 2 )
            self.exterior_song = "//".join( self.exterior_song.rsplit( "/", 1 ) )
            self.song = [ self.get_index_data( [ self.exterior_song ] )[ 0 ], self.exterior_song ]
            self.play_song(0)
    
    else:
        if self.playlist: #load playlist if there one
            self.load_playlist()
        
        if self.last_song and self.auto_last_song: #launch last played sont if configured to 
            self.last_song[ 0 ] = int( self.last_song[ 0 ] )
            self.song = self.last_song
            self.play_song(0)
        
    while self.stay:
        self.get_input()#interface

    self.end()
        
def n_input(self):
    """
    cette fonction permet de garder une méme ligne pour l'input 
    """
    lup()
    wipe_line()


def display( self , space = False ):
    """
    cette fonction affiche l'image ,recupére la durée de la chanson ainsi que le nom de la chanson en cours,
    le volume de la musique ainsi que creer la bar de progression si besoin
    
    limite:
    il est nécessaire qu'une chanson soit selectionné
    """
    if space:
        self.changed.append("space")

    if self.song:
        if not "display" in self.changed:
            self.changed.append("display")# previens l'affichage d'un changement
        if not "bar" in self.changed:
            self.changed.append("bar")
        if self.word and self.words != [] and self.last_word != -1:
            if not "word" in self.changed:
                self.changed.append("word") #previens l"affichage d'un changement


    
    
    
def get_input( self ):
    """
    cette fonction est le menu principal qui permet a l'utilisateur d'interagir avec le programme
    """
    got = ninput( self.update_logic, self.update_display, error = False, text = "" , before = ":",condition = self.is_finished , escape = None )
    lup()# permet d'eviter de recharger l ecran a chaque impur en conservant la ligne

    if got == None:
        self.stay = False
        return

    if all_numbers( got, len( self.files ), 1 ):#chanson selectionné
            self.find_song_database(int(got))
            self.play_song( 0 )
            
    if self.search:#recherche terminé
        self.display()
        self.search = False
        
    if not got and self.song:#pause
        self.wind( 6 )
        
    x = 0
    stop = False
    while x < len( self.commands) and not stop:#executer la première commande contenu dans la chaine donné par l utilisateur
        if   self.commands[ ( index := self.command_pos[ x ] ) ][0] in got:#prenant en compte les modification de l'utilisateur et eviter que les plus petite command shadow les plus grande
            self.commands[ index ][1]( *self.commands[ index ][2] )#lancer la function souhaité
            
            stop = True
            
        x+=1
    
    
def load_all( self ):
    """
    cette fonction permet de recharger toute les images ainsi que toute les chanson et
    remmetre a 0 le lecteur en passant
    """
    self.player.stop()
    self.load_songs()
    self.load_favorite_database()
    self.get_img( self.path_to_img, start = 1 ) #charge toute les image en memoire
    self.check_favorite()
    self.write_param()
    
def wind( self, mode, pause = False  ):
    """
    cette fonction permet de:
    avancer de 10 seconde : mode 1
    reculer de 10 seconde : mode 2
    augmenter le volume de 10% : mode 3
    baisser le volume de 10% : mode 4
    couper/reactiver le son : mode 5
    mettre la musique en pause : mode 6
    afficher/cacher les image : mode 7
    jouer la chanson en boucle : mode 8
    de jouer en aleatoire/dans l'ordre : mode 9
    et actualise l'affichage a chaque fois
    
    limite:
    le volume du son est compris entre 0 et 100%
    """
    if mode == 1: # avance de 10 seconde
        if  self.bar:
            self.player.set_time( min( self.player.get_length() - 1000, self.player.get_time() + 10000 ) )
            
    if mode == 2:# recule de 10 seconde
        if self.bar:
            self.player.set_time( max( 0, self.player.get_time() - 10000 ) )

    if mode == 3: # augmente le volume de 5
        self.volume = min( 100, self.volume + 5 )
        self.set_volume()
        if not "volume" in self.changed: #si l'affichage n'a pas deja ete prevenu
            self.changed.append("volume")#previens l'affichage que le volume a changer

        sleep(0.001)
        
        
    if mode == 4:# baisse le volume de 5
        self.volume = max( 0, self.volume - 5 )
        self.set_volume()
        if not "volume" in self.changed:#si l'affichage n'a pas deja ete prevenu
            self.changed.append("volume")#previens l'affichage que le volume a changer
            
        sleep(0.001)
        
        
    if mode == 5:# mute the music
        self.deafen()
        
    if mode == 6:# pause the music
        self.pause = 1 - self.pause
        self.player.pause()

    if mode == 7:# quit the player
        self.stay = False

    if mode == 15:# go back to music start
        self.player.set_time( 0 )
        self.bar.index = 0
        
def set_timer( self ):
    """
    cette fonction permet de demander a l'utilisateur un temps avant l'arrêt en minute
    """
    word = self.asker.menu_deroulant( [ "quit", "mute", "pause" ] ,self.update_logic)# timer modes
    if  word < 3:
        self.timer_mode = word
        
        self.out( "enter nothing to delete current timer" )
        choice = self.ask( "shutdown in  x minutes :" )
    
        if all_numbers( choice ):
            self.timer = [ 1, int( choice ), monotonic() ]# [elapsed time (m), time remaining (m) , starting time]
        
        else:
            self.timer = None
        
    else:
         self.timer = None 
        
    self.display()

def param_center( self ):
    """
    cette fonction permet de gérer les différents paramétre boolean
    """
    word = 0
    white()
    #tooltip , name , type
    param = [ [x[ 1 ],x[ 0 ],x[ 3 ] ]  for x in self.params if x[ 4 ] ]
    
    while word < len( param ) :
        tooltip = [ [ x[ 0 ], getattr( self, x[ 1 ] ) ] for x in param ]

        word = self.asker.menu_deroulant( [ f"{x[0]} : {bool(x[1])}" for x in tooltip ] ,self.update_logic, cursor = word, search = True)
        lup()
        out( " " * ( len( tooltip ) + 3 ) )
        ldown()
        
        
        if word < len( tooltip ):
                setattr(self,param[  word  ][ 1 ], 1 - tooltip[  word  ][ 1 ] ) # if choice is a param , edit it

    self.display()
                
def manager_manager(self):
    pass

def reset_settings(self):
    """
    cette fonction permet a l'utilisateur de supprimer ses paramétre apres une CONFIRMATION
    """
    a = self.ask(" are you sure you want to reset your setting ? (o/n)")
    if a == "o" or a == "1" or a == "y":
        self.reset()

def clear_cache(self):
    """
    cette fonction permet de suprimer les fichier temporaire (thumbnail , fichier généré a partir de midi...)
    """
    for f in listdir( "appdata/cache" ):
        rm_file( "appdata/cache/" + f )
        
    self.display()

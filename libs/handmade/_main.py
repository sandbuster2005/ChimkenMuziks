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
    self.exterior = directory
    self.exterior_song = song
    
    self.sysname = sysname
    
    if sysname == 'nt':
        self.separator = '\\'
        
    else:
        self.separator = '/'
        
    self.sys_architecture = platform.machine()
    self.stay = True  # False pour quiter le lecteur
    self.pause = 0  # pour mettre en pause le lecteur+la barre
    self.bar = None   # la barre de progression du temps de la chanson 
    self.search = False   # True pour cacher l'affichage
    self.player = vlc.MediaPlayer()  # lecteur
    self.played = []  # historique
    self.MainThread = threading.currentThread()
    self.timer = None
    self.words = None
 
   
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

    if self.sound_manager != "base":#base sound manager need a media playing to get voulme
        self.start_sound()
        self.display()
        
    progress = threading.Thread( target = self.update )#create update thread
    progress.start()
    
    if self.exterior:
        if self.exterior_song:
            self.exterior_song = clear_adjacent( self.exterior_song, [ "/" ], 2 )
            self.exterior_song = "//".join( self.exterior_song.rsplit( "/", 1 ) )
            self.song = [ self.get_index_data( [ self.exterior_song ] )[ 0 ], self.exterior_song ]
            self.play()
    
    else:
        if self.playlist:
            self.load_playlist()
        
        if self.last_song and self.auto_last_song:
            self.last_song[ 0 ] = int( self.last_song[ 0 ] )
            self.song = self.last_song
            self.play()
        
    while self.stay != False:
        self.get_input()#interface
        
        if not progress.is_alive():#if update thread crashed quit main thread
           self.stay = False
            
    self.player.stop()#end
    
    if self.save_param:
        self.write_param()#sauvegarde des parametres
    
    
def update( self ):
    """
    cette fonction afiche la bar de progression et la mettre a jour ainsi que
    passer a la chason suivant a la fin de l'actuel 
    """
    time_check = [ False, 0, 0, 0 ]
    time_changed = False
    save_cooldown = 0
    self.term_size = os.get_terminal_size()
    self.volume_changed = False
    self.display_changed = False
    self.word_changed = False
    timer_changed = False
    timer = None
    last_update = monotonic()
    tick = 0
    base_time = strftime( '%H %M' ).split( " " )
    stop = 0
    
    while self.stay:
        tick += 1
        time = self.player.get_time()#temps actuel
        
        if not self.MainThread.is_alive():
            self.stay = False
            self.player.stop()#end
            
            if self.save_param:
                self.write_param()#sauvegarde des parametres
            
        if self.timer != None:
            
            if self.timer[ 1 ] < 1:
                if self.timer_mode == 0:
                    self.stay = False
                    self.player.stop()#end
                    
                    if self.save_param:
                        self.write_param()
                
                if self.timer_mode == 1:
                    self.wind( 5 )
                    
                if self.timer_mode == 2:
                    self.wind( 6 )
         
        if not time_changed :
            if base_time != strftime( '%H %M' ).split( " " ):
                base_time = strftime( '%H %M' ).split( " " )
                time_changed = True
            
        if self.timer != None:
            
            if not timer_changed:
                if monotonic() > self.timer[ 2 ] + ( self.timer[ 0 ] * 60 ):
                    self.timer[ 0 ] += 1
                    self.timer[ 1 ] -= 1
                    timer_changed = True
                
        if self.sound_manager == "alsa":
            
            if self.volume != self.get_volume():
                self.volume = self.get_volume()
                self.volume_changed = True
       
        if self.song != None and not self.search:#chanson demarré
            
            if self.bar != None:
                
                if self.bar.max != floor( self.player.get_length() / 1000 ):
                    
                    if self.color :
                        color = random.randint( 0, 252 )
                        color += 3 - ( color % 3 )
                    
                    else:
                        color = "white"
                        
                    Max = self.player.get_length()
                    down()
                    save()
                    wipe_line()
                    self.bar = Bar( f"", max=floor( Max/1000 ), color = color, addaptative_bar = self.addaptive_bar ,center = self.center)
                    load()
          
            elif self.player.get_length() > 0:
                
                if self.color:
                    color = random.randint( 0, 252 )
                    color += 3 - ( color % 3 )
                
                else:
                    color = "white"
                    
                Max = self.player.get_length()
                down()
                save()
                wipe_line()
                self.bar = Bar( f"", max=floor( Max/1000 ), color = color, addaptative_bar = self.addaptive_bar , center = self.center)
                load()
         
        if self.bar != None and not self.search and self.song != None:#chanson en cours et pas de pause/suspension     
            
            if self.term_size != ( _ := os.get_terminal_size() ) :
                self.term_size = _
                self.display()
            
            if not save_cooldown and self.bar.index == int( self.bar.max/2 ):
                save_cooldown = monotonic() + 5
                self.write_song_database( self.song[ 1 ] )
                
            if save_cooldown:
                if save_cooldown - monotonic() <0:
                    save_cooldown = 0
            
            if time_check[ 3 ]:
                time_check[ 3 ] -= 1
            
            if time == self.player.get_time() and not time_check[ 3 ]:
                time_check[ 0 ] = True
                time_check[ 1 ] = self.player.get_time()
                time_check[ 2 ] = monotonic()
                
                
            if time / 1000 > self.bar.max:#idk really
                continue
            
            if self.bar.index < 0:##en cas de reculer en desosus du debut
                self.bar.index = 0
                
            if time < 0:#en cas de reculer en dessous du debut
                time = 0
                
            if last_update + 0.5 < monotonic() :
                last_update += 0.5
                self.bar.index = floor( time / 1000 )
                save()
                up()
                self.bar.update()
                load()
                
                
                
            if time_check and not self.pause:
                
                if time_check[ 2 ] + 5 < monotonic():
                    
                    if self.player.get_time() == time_check[ 1 ]:
                        
                        self.play_song( ( 1 - self.repeat ) )
                        out( ":" )
                        continue
                    
                    else:
                        time_check=[ False, 0, 0, 60 ]
           
            if self.word:
                if self.words:
                    
                    if self.words != []:
                        
                        if  ( close := closest( time / 1000, [ x[ 0 ] for x in self.words ] ) ) != self.last_word and self.words[close][0] - time / 1000 < 1:
                            self.last_word = close
                            self.word_changed = True
            
            
            if self.word_changed:
                lyrics = self.words[ self.last_word ][ 1 ]
                space = floor( self.term_size.columns / 2 - len( lyrics ) / 2 )
                save()
                lup( 4 )
                wipe_line()
                out( f"{' '*space * self.center}{ lyrics }" )
                load()
                self.word_changed = False
                
            if time_changed or timer_changed or self.volume_changed or self.display_changed:
        
                if self.show:
                    white()
                    self.display_img()
                    
                ldown( 3 )
                
                time_string = f"{ base_time[ 0 ] }:{base_time[ 1 ]}"
                
                self.volume = self.get_volume()
                volume_string = f"{ self.volume }%"
               
                if self.volume < 10:
                     volume_string = "0" + volume_string
                
                if self.timer :
                    timer_string = f"timer :{ self.timer[1] } mins"
            
                string = time_string + "   " + volume_string
                
                if self.playlist:
                    string = self.playlist + "   " + string
                    
                if self.timer:
                    string += "   " + timer_string
                
                space = floor( ( self.term_size.columns - len( string ) ) / 2 ) 
                
                if os.name == 'nt':
                    a = '\\'
                else:
                    a = '/'
                
                name = self.song[ 1 ].rsplit( a, 1 )[ 1 ]
                if self.song in self.favorite:
                    name = "*" + name + "*"
                space_name = floor( ( self.term_size.columns - len( name ) ) / 2 )
                
                self.bar.center = self.center
                
                save()
                lup( 3 )
                
                out(f"{' ' * space * self.center}{string}")
                
                ldown()
                
                out( f"{' ' * space_name * self.center}{name}" )
                
                load()
                out( ":" )
    
                time_changed = False
                timer_changed = False
                self.volume_changed = False
                self.display_changed = False
            
            if stop != 0:
                stop -= 1
                
            if self.img_script != None and stop == 0 and self.img_mode == "script" and not self.search:
                
                if int( monotonic() ) % self.Screen.framerate == 0:
                    save()
                    home()
                    self.Screen.update()
                    load()
                    stop = 10
                    
            if ceil( time / 1000 ) >= self.bar.max : #la chanson est fini# la chason est bien fini et ne vien pas de commencer
                
                self.play_song( ( 1 - self.repeat ) )

def u_bar(self):
    """
    cette fonction permet de mettre la bar a jour sans casser l'ecran
    """
    if self.bar:
        save()
        up()
        self.bar.update()
        load()
        
def n_input(self):
    """
    cette fonction permet de garder une méme ligne pour l'input 
    """
    lup()
    wipe_line()

def display( self ):
    """
    cette fonction affiche l'image ,recupére la durée de la chanson ainsi que le nom de la chanson en cours,
    le volume de la musique ainsi que creer la bar de progression si besoin
    
    limite:
    il est nécessaire qu'une chanson soit selectionné
    """
    lup()
    
    if self.song != None:
        sleep( 0.1 )  
        self.display_changed = True
        if self.word and self.words != [] and self.last_word != -1:
            self.word_changed = True
                 
    ldown(3)

    
    
    
def get_input( self ):
    """
    cette fonction est le menu principal qui permet a l'utilisateur d'interagir avec le programme
    """
    got = self.ask( ":" ).lower()#ignorer les majuscules
    self.n_input()
    
    if all_numbers( got, len( self.files ), 1 ):#chanson selectionné
            self.song = self.files[ int( got ) ]
            self.search = True
            self.play_song( 0 )
            
    if self.search:#recherche terminé
        self.suspend("display")
        self.search = False
        
        
    if got == "" and self.song != None:#pause 
        self.wind( 6 )
        
    x = 0
    stop = False
    
    while x < len( self.holders ) and not stop:#executer la premier commande contenu dans la chaine donné par l utilisateur
        if self.holders[ self.command[ x ] ] in got:#prenant en compte les modification de l'utilisateur 
            if self.commands[ self.command[ x ] ] == "+":
                command = "plus_f"
                
            elif self.commands[ self.command[ x ] ] == "-":
                command = "minus_f"
                
            else:
                command = self.commands[ self.command[ x ] ] + "_f"
                
            getattr( self, command )()#lancer la function souhaité
            
            stop = True
            
        x+=1
    
    
def load_all( self ):
    """
    cette fonction permet de recharger toute les images ainsi que toute les chanson et
    remmetre a 0 le lecteur en passant
    """
    self.player.stop()
    self.load_songs()
    self.get_img( self.path_to_img, start = 1 )
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
    self.search = True
    if mode == 1:
        if self.bar	!= None: 
            self.player.set_time( min( self.player.get_length() - 1000, self.player.get_time() + 10000 ) )
            self.bar.index = min( self.bar.max - 1, self.bar.index + 10 )
            self.u_bar()
            
    if mode == 2:
        if self.bar != None:
            self.player.set_time( max( 0, self.player.get_time() - 10000 ) )
            self.bar.index = max( 0, self.bar.index - 10 )
        
    
    if mode == 3:
        self.volume = min( 100, self.volume + 5 )
        self.set_volume()
        
        self.volume_changed = True
        
        
    if mode == 4:
        self.volume = max( 0, self.volume - 5 )
        self.set_volume()
        self.volume_changed = True
        
        
        
    if mode == 5:
        self.deafen()
        
    if mode == 6:
        self.pause = 1 - self.pause
        self.player.pause()

    if mode == 15:
        self.player.set_time( 0 )
        self.bar.index = 0
    
    self.search = False
    
    if pause:
        self.suspend( "display" )
        
def set_timer( self ):
    """
    cette fonction permet de demander a l'utilisateur un temps avant l'arrêt en minute
    """
    word = self.ask_list( [ "quit", "mute", "pause" ] )
    if all_numbers( word, 3, 1 ):
        self.timer_mode = int( word ) 
        
        self.out( "enter nothing to delete current timer" )
        choice = self.ask( "shutdown in  x minutes :" )
    
        if all_numbers( choice ):
            self.timer = [ 1, int( choice ), monotonic() ]
        
        else:
            self.timer = None
        
    else:
         self.timer = None 
        
    self.display()

def param_center( self ):
    """
    cette fonction permet de gérer les différents paramétre boolean
    """
    word = "0"
    white()
    #tooltip , name , type
    param = [ [x[ 1 ],x[ 0 ],x[ 3 ] ]  for x in self.params if x[ 4 ] ]
    
    while all_numbers( word ):
        tooltip=[ [ x[ 0 ], getattr( self, x[ 1 ] ) ] for x in param ]
        
        up( len( tooltip ) + 1 )
        word = self.ask_list( tooltip )
        lup()
        out( " " * ( len( tooltip ) + 3 ) )
        ldown()
        
        
        if all_numbers( word , len( tooltip ), 1 ):
                setattr(self,param[ int ( word ) ][ 1 ], 1 - tooltip[ int ( word ) ][ 1 ] )
                
def manager_manager(self):
    pass

def clear_cache(self):
    """
    cette fonction permet de suprimer les fichier temporaire (thumbnail , fichier généré a partir de midi...)
    """
    for f in listdir( "appdata/cache" ):
        rm_file( "appdata/cache/" + f )
        
    self.display()

#made by sand
from time import sleep,monotonic
from libs.progress.bar import Bar
from math import floor,ceil
from time import sleep,strftime
from os import listdir
from .utils import *
from .ffiles import *
from .terminal import *
import libs.vlc as vlc
import threading
import platform
import os

def init_main( self ):
    self.sys_os = platform.system().lower()
    self.sys_architecture = platform.machine()
    self.repeat = 0 #1 pour repeter en boucle la chanson
    self.stay = True  # False pour quiter le lecteur
    self.pause = 0  # pour mettre en pause le lecteur+la barre
    self.bar = None   # la barre de progression du temps de la chanson 
    self.search = False   # True pour cacher l'affichage
    self.player = vlc.MediaPlayer()  # lecteur
    self.played = []  # historique
    self.MainThread = threading.currentThread()
    self.timer = None
    self.word = 1
    self.words = None
   
def main( self ):
    """
    cette fonction est la fonction d'initialisation du programme et de fonctionnement 
    """
    self.get_param()#get param from file if it exist else create it
    self.get_img( self.path_to_img,start = 1 )#scan all image in repertory
    self.check_adress()#see if current file adress exist
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
    time = threading.Thread( target = self.check_time )
    time.start()
    progress.start()
    
    while self.stay != False:
        self.get_input()#interface
        
        if not progress.is_alive():#if update thread crashed quit main thread
           self.stay = False
            
    self.player.stop()#end
    self.write_param()#sauvegarde es parametre
    
    
def update( self ):
    """
    cette fonction afiche la bar de progression et la mettre a jour ainsi que
    passer a la chason suivant a la fin de l'actuel 
    """
    time_changed = False
    volume_changed = False
    timer_changed = False
    timer = None
    base_time=strftime( '%H %M' ).split( " " )
    stop = 0
    
    while self.stay:
        time = self.player.get_time()#temps actuel
        if not self.MainThread.is_alive():
            self.stay = False
            self.player.stop()#end
            self.write_param()#sauvegarde es parametre
            
        if self.timer != None:
            if self.timer < 1:
                self.stay = False
                self.player.stop()#end
                self.write_param()
         
        if self.song != None:#chanson demarré
            sleep(0.1)
            
            if self.bar != None:
                if self.bar.max != floor( self.player.get_length() / 1000 ):
                    Max = self.player.get_length()
                    down()
                    save()
                    self.bar = Bar( "time(s)", max=floor( Max/1000 ), fill="■" )
                    load()
            else:
                Max = self.player.get_length()
                down()
                save()
                self.bar = Bar( "time(s)", max=floor( Max/1000 ), fill="■" )
                load()
        
        if base_time != strftime( '%H %M' ).split( " " ):
            base_time = strftime( '%H %M' ).split( " " )
            time_changed = True
            
            if self.timer != None:
                self.timer -= 1
        
        if self.timer != timer:
            timer = self.timer
            timer_changed = True
            
        if self.sound_manager == "alsa":
            if self.volume != self.get_volume():
                self.volume = self.get_volume()
                volume_changed = True
         
        if self.bar != None and not self.search :#chason en cours et pas de pause/suspension     
            if time/1000 > self.bar.max:#idk really
                continue
            
            if self.bar.index < 0:##en cas de reculer en desosus du debut
                self.bar.index = 0
                
            if time < 0:#en cas de reculer en desosus du debut
                time = 0
                
            if time/1000 > self.bar.index:#la chanson a avancer
                self.bar.index = floor( time/1000 )
                save()
                up()
                self.bar.update()
                load()
                
            if self.word:
                if self.words != []:
                    if self.words[0][0] < time/1000 and self.words[0][0]:
                        save()
                        lup( 4 )
                        wipe_line()
                        out( self.words[0][1] )
                        load()
                        self.words.remove(self.words[0])
                
                
            if time_changed:
                time_changed = False
                save()
                lup( 3 )
                out( f"{ base_time[ 0 ] }:{base_time[ 1 ]}" )
                load()
            
            if timer_changed:
                timer_changed = False
                save()
                lup( 3 )
                right( 20 )
                out(f" timer :{ self.timer } mins ")
                load()
                
            if volume_changed:
                volume_changed = False
                save()
                lup( 3 )
                right( 16 )
                
                if self.volume < 10 :
                    out( f"0{ self.volume }%" )
                    
                else:
                    out( f"{ self.volume }%" )
                    
                load()
            
            if stop != 0:
                stop -= 1 
            if self.img_script != None and stop == 0 and self.img_mode == "script":
                if int( monotonic() ) % self.Screen.framerate == 0:
                    save()
                    home()
                    self.Screen.update()
                    load()
                    stop = 10
                    
            if ceil( time/1000 ) >= self.bar.max : #la chanson est fini# la chason est bien fini et ne vien pas de commencer
                
                if not self.repeat:
                    self.choose_song()
                    
                self.bar = None
                self.get_words()
                if self.song[-4:] ==".mid":
                    self.suspend("convert_midi")
                self.play()
                sys.stdout.write(":")
                sys.stdout.flush()
        
        
def check_time(self):
    
    while self.MainThread.is_alive() and self.stay :
        if self.song != None :
            time0 = self.player.get_time()# temps actuel
            sleep( 0.5 )
            time = self.player.get_time()#temps actuel
            
            if time == time0:
                sleep(5)
                time = self.player.get_time()
                
                if time == time0 and not self.search and not self.pause:
                    if not self.repeat:
                        self.choose_song()
            
                    self.play()
                    lup(0)
                    sys.stdout.write(":")
                    sys.stdout.flush()


def display( self ):
    """
    cette fonction affiche l'image ,recupére la durée de la chanson ainsi que le nom de la chanson en cours,
    le volume de la musique ainsi que creer la bar de progression si besoin
    
    limite:
    il est nécessaire qu'une chanson soit selectionné
    """
    lup()
    if self.song != None:
        a = "/"
        sleep( 0.10 )
        white()
        self.volume = self.get_volume()
        
        time=strftime( "%H %M" ).split( " " )# affiche l'heure au format standard
        if self.show:
            self.display_img()
            
        print( f"{ time[ 0 ] }:{ time[ 1 ] }   volume: { self.volume }%  " )# heure,volume
            
        print( f"Song: { self.files.index( self.song ) }:{ self.song.rsplit( a, 1 )[ 1 ] }" )# playlist,index,chanson
        if self.timer != None:
            save()
            lup( 2 )
            right( 20 )
            out(f" timer :{ self.timer } mins ")
            load()
        
    else:
        if self.sound_manager != "base":
            print( f"volume :{self.volume}" )
    ldown()
    #load()
    
    
    
    
def get_input( self ):
    """
    cette fonction est le menu principal qui permet a l'utilisateur d'interagir avec le programme
    """
    got = self.ask( ":" ).lower()#ignorer les majuscules
    
    if all_numbers( got, len( self.files ), 1 ):#chanson selectionné
            white()
            self.search = False
            self.bar = None
            self.song = self.files[ int(got) ]
            self.get_words()
            if self.song[-4:] ==".mid":
                self.suspend("convert_midi")
            self.play()
            
    if self.search:#recherche terminé
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
                
            getattr( self,command )()#lancer la function souhaité
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
    
    
def wind( self, mode, pause = True  ):
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
    if mode == 1:
        if self.bar	!=	None: 
            self.player.set_time( min( self.player.get_length()-1000, self.player.get_time() + 10000 ) )
            self.bar.index = min( self.bar.max-1, self.bar.index + 10 )
        
    if mode == 2:
        if self.bar != None:
            self.player.set_time( max( 0, self.player.get_time() - 10000 ) )
            self.bar.index = max( 0, self.bar.index - 10 )
    
    if mode == 3:
        self.volume = min( 100, self.volume + 5 )
        self.set_volume()
        
    if mode == 4:
        self.volume = max( 0, self.volume - 5 )
        self.set_volume()
        
    if mode == 5:
        self.deafen()
    
    if mode == 6:
        self.pause = 1 - self.pause
        self.player.pause()
    
    if mode == 7:
        self.show = 1 - self.show
    
    if mode == 8:
        self.repeat = 1 - self.repeat
    
    if mode == 9:
        self.mode = 1 - self.mode
    
    if mode == 10:
        self.word = 1 - self.word
        
    if mode == 11:
        self.player.set_time(0)
        self.bar.index = 0
        
    if pause:
        self.suspend( "display" )
        
def set_timer( self ):
    self.out("enter nothing to delete current timer")
    choice = self.ask( "shutdown in  x minutes :" )
    
    if all_numbers( choice ):
        self.timer = int( choice )
        
    else:
        self.timer = None 
        
    self.display()

def param_center( self ):
    word = "0"
    while all_numbers( word ):
        white()
        tooltip=[[ "afficher l'image ", self.show ],
                 [ "jouer en boucle ", self.repeat ],
                 [ "jouer en random ", self.mode ],
                 [ "afficher les fichier paroles", self.word ]
                ]
        word = self.ask_list( tooltip )
        if all_numbers( word , len (tooltip ), 1 ):
                self.wind( 7 + int( word ), pause = False )
                
def manager_manager(self):
    pass

def clear_cache(self):
    for f in listdir("appdata/cache"):
        rm_file("appdata/cache/" + f)
    self.display()

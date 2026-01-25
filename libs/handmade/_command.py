#made by sand

from .utils import *
from .terminal import *

def init_command( self ):
        #command , linked fonction , fonction arg , tooltip in help
    self.commands = [
         ["h", self.help_menu, {} , "Show the help menu"], #pour afficher le menu help
         ["q", self.wind, { 7 : "mode" }, "Close the program"], #pour quitter le lecteur
         ["r", self.select, {}, "Search for a song in the gallery"], #pour rechercher un son dans le catalogue
         ["g", self.change_sound_manager, {}, "Change the volume controller"], #changer de gestionnaire de volume
         ["i", self.historic, {}, "Show song history"], #pour afficher l'historique
         ["j", self.select_img, {}, "Select an image in the gallery"], #pour selectionner une image dans la galerie
         ["o", self.default_midi, {}, "Select default instruments for .midi files"], #pour selectionner l'instrumental par defaut des .midi
         ["n", self.play_song, {}, "Go to next song"], #pour aller a la chanson suivante
         ["k", self.clear_cache, {}, "Empty the cache"], #pour vider la cache
         ["+", self.wind, {1: "mode"}, "Skip forward 10 seconds"], #pour avancer de 10 seconde
         ["-", self.wind, {2: "mode"}, "Rewind 10 seconds"], #pour reculer de 10 seconde
         ["p", self.wind, {3: "mode"}, "Raise volume by 5%"], #pour monter le son de 5%
         ["m", self.wind, {4: "mode"}, "Lower volume by 5%"], #pour baisser le son de 5%
         ["d", self.wind, {5: "mode"}, "Mute/unmute sound"], #pour mute/unmute le son
         ["s", self.param_center, {}, "Go to settings"], #centre parametre
         ["a", self.load_all, {}, "Reload song and image gallery"], #pour recharger le catalogue de chanson et d'image
         ["c", self.edit_dirs, {}, "Enable/disable folders"], #pour activer/desactiver des dossiers
         ["b", self.play_last, {}, "Go back to previous song"], #pour charger la chanson précédente
         ["y", self.change_main_path, {}, "Change base directory"], #pour changer le repertoire d'origine
         ["l", self.display, { 1 : "space" }, "Reload the display"], #pour actualiser l'affichage
         ["t", self.screen_mode, {}, "Select display mode"], #pour selectionner le mode d'affichage
         ["u", self.write_param, {}, "Save current settings"], #pour sauvegarder les parametre actuel
         ["v", self.edit_command, {}, "Edit a command"], #pour modifier une commande
         ["w", self.reset_settings, {}, "Reset settings"], #pour remetre les paramètre a 0
         ["x", self.dl_yt_playlist, {}, "Download a Youtube playlist"], #pour télécharger une playlist youtube
         ["dl", self.yt_search, {}, "Search on Youtube and download"], #pour rechercher sur youtube
         ["z", self.mani_file, {}, "Delete, move or rename a file"], #pour supprimer/deplacer/renommer un fichier
         ["e", self.change_confirmation, {}, "Change choice message"], #pour changer le message de choix
         ["f",  self.set_timer , {}, "Set a timer"], #pour mettre un timer
         ["bb", self.wind, { 15 : "mode" }, "Rewind to start of the song"], #pour la musique en cours a 0
         ["pl", self.playlist_manager, {}, "Go to playlist menu"], #permet de gerer les playlist
         ["add", self.add_to_playlist, {}, "Add song to favorites/to a playlist"], #permet d'ajouter la chanson a une playlist / au favoris
         ["played", self.most_played, {} , "Display most played songs" ], #affiche la liste des chanson les plus joué
         ["fav", self.select_fav, {}, "Search song in favorites" ] #pour rechercher une chanson dans les favoris
         ]
    #abcdefghijklmnopqrstuvwxyz+- :list des commande utilisé de base
    #dl bb pl add
    self.new_logger("command")
    
def sort_command( self ):
    """
    cette fonction permet de trier les commandes modifié par l'utilisateur
    en fonction de leur taille puis alphabétiquement en gardant le h(help) en priorité dans l'alphabet
    """
    # all this THING sort commands by lenght then by alphabetical order and put the h on top of the alphabet
    base = [x[0] for x in self.commands ]
    self.logger["command"].debug(f"received commands : {base}")
    command = base[1:]
    command = sorted( command, key = lambda s: ( -len( s ) ) )
    x = 0
    missing = ""
    
    while x < len( command ) and missing == "":
        
        if len( command[ x ] ) == 1:
            missing = command[ x ]
            
        x += 1
        
    command=[ command[ x ] * ( 1 - ( ( len( command[ x - 1 ] ) > 1 ) == ( len( command[ x ] ) == 1 ) == ( len( command[ x + 1 ] ) == 1 ) == True ) ) + "h" * ( ( len( command [ x - 1 ] ) > 1 ) == (len ( command[ x ] ) == 1 ) == ( len( command[ x + 1 ] ) == 1 ) ==  True ) for x in range( len( command ) ) ]
    
    if "h" in command:
        command = command[ :command.index( "h" ) + 1 ]+[ missing ] + command[ command.index( "h" ) + 1 :]
        
    elif len( command[0] ) == 1 :
        command = [ "h" ] + command
        
    elif len( command[ 0 ] ) > 1:
        command += [ "h" ]
        
    command = [ base.index(command[x]) for x in range(len(command) ) ]


    self.command_pos = command
    self.logger["command"].debug(f"emmited commands : {self.command_pos}")

def edit_command( self ):
    """
    cette fonction permet de de modifier les commande du programme a
    l'exception de h(help)
    """
    cmd = "0"
    a = ""
    while cmd:
        commands = [ x[0] for x in self.commands ]
        self.help_menu()#show current commands
        print(a)#show last message
        cmd = self.ask("enter current command call :")
        
        if cmd == "h":
            self.out( "help cannot be modified" ) # in case the user forget the change
            return
        
        if cmd in commands:
            self.logger["command"].debug(f"selected : {cmd}")
            key = self.ask( "new command call :" )
            
            if not all_numbers( key ) and key != "":
                 if key not in commands:#if key don't already exist
                     a = f"{  self.commands[ commands.index( cmd ) ][0] } changed to {key}"
                     self.logger["command"].debug(f"changed to {key}")
                     self.commands[ commands.index( cmd ) ][0] = key # set key
                     self.write_param()
                     self.sort_command()
                     
            wipe()


def help_menu( self ):
    """
    cette fonction se sert du dico qui contient les info pour renvoier une
    liste de toute les info
    """
    self.logger["command"].debug("showing help menu")
    menu =  [ "Input a number to play corresponding song", "Press enter to pause/unpause song" ] + [ f"{ self.commands[ x ][0] } : { self.commands[ x ][3] }" for x in range( len( self.commands ) )  ] + [" "] #entrer un nombre pour lancer la chanson correspondante / ne rien rentrer pour mettre pause
    self.show_list(menu , num = False)
    self.search = True


#made by sand
from .ffiles import *

def init_param( self ):
    self.param = "appdata/param.txt"#fichier de sauvegarde des paramétre
    self.new_logger("param")

    #              [ param name, tooltip ,defaut value ,type ,param center ?]
    self.params =  [
                   [ "path_to_file", "chemin vers le dossier source musique", "" ,"str", False ],
                   [ "path_to_img", "chemin vers le dossier source image", "appdata/image/", "str" , False ],
                   [ "mode", "jouer en random", 0 , "bool" , True ],
                   [ "sound_manager", "gestionnaire de son", "base", "str", False ],
                   [ "img", "image actuel" ,"" , "str", False ],
                   [ "repeat", "jouer en boucle ", 0 , "bool", True ],
                   [ "dirs" ,"liste des dossiers / sous dossiers", [], "list", False ],
                   [ "play_favorite", "joue les favoris", 0 , "bool", True],
                   ["fchoose", "augmente la frequence des favoris", 0 , "bool" , True],
                   [ "holders", "commandes", -1 , "list", False ],
                   [ "graphic_manager", "mode d'affichage", "base" , "str", False ],
                   [ "confirmation", "message de choix", "Your choice", "str", False ],
                   [ "show", "afficher l'image ", 1 , "bool", True ],
                   [ "word", "afficher les fichier paroles", 1 , "bool", True ],
                   [ "base_soundmap", "codec midi par default" , "appdata/midi_codec/default.sf2" , "str", False ],
                   [ "addaptive_bar", "taille de la bar proportionnel", 1, bool, True ],
                   [ "color", "la bar change de couleur", 0 , "bool", True ],
                   [ "true_color", "passe les image en true color", 1 ,"bool", True ],
                   [ "nearest", "utilise nearest neighbor pour accélérer l'affichage de l'image", 0, "bool", True ],
                   [ "invert", "inverse les couleurs des images", 0, "bool", True],
                   [ "center", "centrer les paroles et l'image", 1 ,"bool", True ],
                   [ "autoaddapt", "adapte l affichage a la taille du terminal ", 1, "bool", True ],
                   [ "last_song", "derniere chanson joué", "", "str", False ],
                   [ "auto_last_song", "joue la dernier chanson au retour", 1,"bool", True ],
                   [ "playlist" , "nom de la playlist actuel", "", "str", False ],
                   [ "save_param", "sauvegarder les parametres en quitant", 1, "bool" , True],
                   [ "playlist_type","type de playlist", "", "str" , False],
                   [ "quickselect" , "remove need for confirmation when possible", 0, "bool", True ]
                   ]
    
    for x in self.params:
        if x[ 2 ] != -1:
            setattr(self,x[ 0 ], x[ 2 ] )

def get_param( self , param = ""):
    """
    cette fonction permet de recuperer les variables cité dans le fichier  param si presence de celle si
    """
    self.logger["param"].info("loading param")
    data = get_data( self.param, [ "\n", ",,,", "###", ";;;" ] )
    data = remove_list( data )
    co = [ data[ x ][ 0 ] for x in range( len( data ) ) ]
    param = [ x[ 0 ] for x in self.params ]
    for y,x in enumerate( co ):

        if data[ y ][ 1 ] =="":
            continue

        if x == "holders":
            for z in range( len ( data[y][1] ) ):
                self.commands[z][0] = data[y][1][z]
                continue

        #print(data[y],type(data[y][1]),self.params[param.index(x)][3] )
        self.logger["param"].debug(f"{x} : {data[y]} ")
        if self.params[ param.index( x ) ][ 3 ] == "list" and type( data[ y] [ 1 ] ) != list:
            setattr( self, x, [ data[ y ][ 1 ] ])
        
        elif data[ y ][ 1 ] == "0" or data[ y ][ 1 ] == "1":
            setattr( self, x, int( data[ y ][ 1 ] ) )
           
        else:
            setattr( self, x, data[ y ][ 1 ] )
    
    self.load_favorite_database()
    self.sort_command()

def write_param( self , param = ""):
    """
    cette fonction permet d'enregistrer les variable cité dans le fichier param
    """
    if not self.stay:
        if type( self.song ) == list:
            self.last_song = self.song
            
        else:
            self.last_song = ""
    
    data = [ [ x, str( getattr( self, x ) ) ] if type( getattr( self, x ) ) is int else [ x, getattr( self , x ) ] for x in [ x[ 0 ] for x in self.params ] if x != "holders" ]
    data += [ ["holders" ,[x[0] for x in self.commands] ] ]
    data = join_list( data, [ "\n", ",,,", "###", ";;;" ] )
    write_file( self.param, data )
    self.logger["param"].info("saved param")

def reset( self ):
    """
    cette fonction permet de remmetre a 0 les parrametre actuel et
    se enregistrer dans le fichier param
    """
    self.logger["param"].info("reset")
    self.__init__()#remise a 0
    self.write_param()




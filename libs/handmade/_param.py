#made by sand
from .ffiles import *
import sqlite3

def init_param( self ):
    self.param = "appdata/param.txt"#fichier de sauvegarde des paramétre
    #              [ param name, tooltip ,defaut value ,type ,param center ?]
    self.params =  [
                   [ "path_to_file", "chemin vers le dossier source musique", "" ,"str", False ],
                   [ "path_to_img", "chemin vers le dossier source image", "appdata/image/", "str" , False ],
                   [ "mode", "jouer en random", 0 , "bool" , True ],
                   [ "sound_manager", "gestionnaire de son", "base", "str", False ],
                   [ "img", "image actuel" ,"" , "str", False ],
                   [ "repeat", "jouer en boucle ", 0 , "bool", True ],
                   [ "dirs" ,"liste des dossiers / sous dossiers", [], "list", False ],
                   [ "favorite", "liste des favoris", [], "list", False],
                   [ "play_favorite", "joue les favoris", 0 , "bool", True],
                   [ "holders", "commandes", -1 , "list", False ],
                   [ "graphic_manager", "mode d'affichage", "base" , "str", False ],
                   [ "confirmation", "message de choix", "Your choice", "str", False ],
                   [ "show", "afficher l'image ", 1 , "bool", True ],
                   [ "word", "afficher les fichier paroles", 1 , "bool", True ],
                   [ "base_soundmap", "codec midi par default" , "appdata/midi_codec/default.sf2" , "str", False ],
                   [ "addaptive_bar", "taille de la bar proportionnel", 1, bool, True ],
                   [ "color", "la bar change de couleur", 0 , "bool", True ],
                   [ "true_color", "passe les image en true color", 1 ,"bool", True ],
                   [ "nearest", "utilise nearest neighbor pour accélérer l'affichage de l'image", 0, b"ool", True ],
                   [ "invert", "inverse les couleurs des images", 0, "bool", True],
                   [ "center", "centrer les paroles et l'image", 1 ,"bool", True ],
                   [ "autoaddapt", "adapte l affichage a la taille du terminal ", 1, "bool", True]
                   ]
    for x in self.params:
        if x[2]!= -1:
            setattr(self,x[0],x[2])

def get_param( self , param = ""):
    """
    cette fonction permet de recuperer les variables cité dans le fichier  param si presence de celle si
    """
    data = get_data( self.param, [ "|||", ",,,", "###", ";;;" ] )
    data = remove_list( data )
    co = [ data[ x ][ 0 ] for x in range( len( data ) ) ]
    param = [ x[0] for x in self.params]
    print("param :",co)
    for y,x in enumerate(co):
        
        if data[y][1] =="":
            continue
        
        print(data[y],type(data[y][1]),self.params[param.index(x)][3] )
        if self.params[param.index(x)][3] == "list" and type(data[y][1]) != list:
            setattr(self,x, [ data[y][1] ])
        
        elif data[y][1] =="0" or data[y][1] =="1":
            setattr(self,x,int(data[y][1]))
           
        else:
            setattr(self,x,data[y][1])
    
def write_param( self , param = ""):
    """
    cette fonction permet d'enregistrer les variable cité dans le fichier param
    """
    data = [ [ x, str( getattr( self, x ) ) ] if type( getattr( self, x ) ) is int  else [ x, getattr( self , x ) ] for x in [ x[ 0 ] for x in self.params ] ]
    
    data = join_list( data, [ "|||", ",,,", "###", ";;;" ] )
    write_file( self.param, data )
    self.sort_command()

def reset( self ):
    """
    cette fonction permet de remmetre a 0 les parrametre actuel et
    se enregistrer dans le fichier param
    """
    self.__init__()#remise a 0
    self.write_param()


def write_song_database(self,song):
    self.create_song_database()
    base =  sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    requete = """
    insert into song
    Values( ?,"1")
    ON CONFLICT(nom)
    DO UPDATE  SET played = played +1
    """
    cursor.execute(requete,[ song ])
    base.commit()
    base.close()

def create_song_database(self):
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    cursor.execute("create table if not exists song(nom UNIQUE NOT NULL ,played INTEGER NOT NULL)")
    base.commit()
    base.close()

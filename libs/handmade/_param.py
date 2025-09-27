#made by sand
from .ffiles import *
import sqlite3

def init_param( self ):
    self.param = "appdata/param.txt"#fichier de sauvegarde des paramétre
    #              [ param name, tooltip ,defaut value ,type ,param center ?]
    self.params =  [
                   [ "path_to_file", "chemin vers le dossier source musique", "" ,"folder", False ],
                   [ "path_to_img", "chemin vers le dossier source image", "appdata/image/", 'folder', False ],
                   [ "mode", "jouer en random", 0 , "bool" , True ],
                   [ "sound_manager", "gestionnaire de son", "base", "string", False ],
                   [ "img", "image actuel" ,"" , "file", False ],
                   [ "repeat", "jouer en boucle ", 0 , "bool", True ],
                   [ "dirs" ,"liste des dossiers / sous dossiers", [], "list", False ],
                   [ "holders", "commandes", -1 , "list", False ],
                   [ "graphic_manager", "mode d'affichage", "base" , "string", False ],
                   [ "confirmation", "message de choix", "Your choice", "message", False ],
                   [ "show", "afficher l'image ", 1 ,"bool", True ],
                   [ "word", "afficher les fichier paroles", 1 ,"bool", True ],
                   [ "base_soundmap", "codec midi par default" , "appdata/midi_codec/default.sf2" ,"file", False ],
                   [ "addaptive_bar", "taille de la bar proportionnel", 1, "bool", True ],
                   [ "color", "la bar change de couleur", 0 , "bool", True ],
                   [ "true_color", "passe les image en true color", 1 ,"bool", True ],
                   [ "nearest", "utilise nearest neighbor pour accélérer l'affichage de l'image", 0, "bool", True ],
                   [ "invert", "inverse les couleurs des images", 0, "bool", True]
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
    print("param :",co)
    for y,x in enumerate(co):
        
        if data[y][1] !="0" and data[y][1] !="1":
            setattr(self,x,data[y][1])
            
        else:
            setattr(self,x,int(data[y][1]))
    
def write_param( self , param = ""):
    """
    cette fonction permet d'enregistrer les variable cité dans le fichier param
    """
    data = [ [ x, str( getattr( self, x ) ) ] if type( getattr( self, x ) ) is int else [ x, getattr( self , x ) ] for x in [ x[ 0 ] for x in self.params ] ]
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
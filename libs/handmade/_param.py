#made by sand
from .ffiles import *


def init_param( self ):
    self.param = "appdata/param.txt"#fichier de sauvegarde des paramétre
    self.params = ["path_to_file","path_to_img","mode","sound_manager", "img","repeat", "dirs", "holders", "graphic_manager", "confirmation", "show", "word", "base_soundmap","addaptive_bar","color"]
    

def get_param( self , param = ""):
    data = get_data( self.param, [ "|||" , ",,," , "###" ,";;;"] )
    data = remove_list(data)
    co = [data[x][0] for x in range(len(data))]
    
    for y,x in enumerate(co):
        
        if data[y][1] !="0" and data[y][1] !="1":
            setattr(self,x,data[y][1])
            
        else:
            setattr(self,x,int(data[y][1]))
    
def write_param( self , param = ""):
    data = [[x,str(getattr(self,x))] if type(getattr(self,x)) is int else [x,getattr(self,x)] for x in self.params]
    data = join_list( data,[ "|||", ",,,", "###",";;;"] )
    write_file( self.param, data )
    self.sort_command()
"""  
def get_param( self ):

    data = get_data( self.param, [ "|" , "," , "#" ] )# pour extraire les donné
    if data == [] or len( data ) != 13:# si les donné sont corrompu ou n'existe pas
        self.write_param()
        self.show_list(self.help_menu(), num=False )
        
    else:# attribution des parametre
        self.path_to_file = data[ 0 ][ 0 ][ 0 ]
        self.path_to_img = data[ 1 ][ 0 ][ 0 ]
        self.mode = int( data[ 2 ][ 0 ][ 0 ][ 0 ] )
        self.sound_manager = data[ 3 ][ 0 ][ 0 ]
        self.img = data[ 4 ][ 0 ][ 0 ]
        self.repeat = int( data[ 5 ][ 0 ][ 0 ] )
        self.dirs = data[ 6 ]
        self.holders  = [ data[ 7 ][ x ][ 0 ] for x in range( len( data[ 7 ] ) ) ]
        self.graphic_manager = data[ 8 ][ 0 ][ 0 ]
        self.confirmation = data[ 9 ][ 0 ][ 0 ]
        self.show = int( data[ 10 ][ 0 ][ 0 ] )
        self.word = int( data[ 11 ][ 0 ][ 0 ] )
        self.base_soundmap = data[ 12 ][ 0 ][ 0 ] 
        self.sort_command()
        self.show_list(self.help_menu(), num=False )
    
    
def write_param( self ):

    cette fonction permet d'ecrire les parametre actuel en memoire
    dans le fichier param
    data = [ str( self.path_to_file ), str( self.path_to_img ), str( self.mode ), self.sound_manager, str( self.img ), str( self.repeat ), self.dirs, self.holders, self.graphic_manager, self.confirmation, str(self.show), str(self.word) , self.base_soundmap ]# tout les parametre a stocker
    data = join_list( data,[ "|", ",", "#" ] )# formatage pour l'ecriture
    write_file( self.param, data )
    self.sort_command()
"""    
def reset( self ):
    """
    cette fonction permet de remmetre a 0 les parrametre actuel et
    se enregistrer dans le fichier param
    """
    self.__init__()#remise a 0
    self.write_param()

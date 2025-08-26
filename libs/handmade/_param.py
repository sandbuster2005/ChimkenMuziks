#made by sand
from .ffiles import *


def init_param( self ):
    self.param = "appdata/param.txt"#fichier de sauvegarde des paramétre
    self.params =  [
                   "path_to_file",
                   "path_to_img",
                   "mode",
                   "sound_manager",
                   "img",
                   "repeat",
                   "dirs",
                   "holders",
                   "graphic_manager",
                   "confirmation",
                   "show",
                   "word",
                   "base_soundmap",
                   "addaptive_bar",
                   "color",
                   "true_color",
                   "nearest"
                   ]
    

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
    data = [ [ x, str( getattr( self, x ) ) ] if type( getattr( self, x ) ) is int else [ x, getattr( self , x ) ] for x in self.params ]
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

#made by sand
import subprocess
from .utils import export

@export
def init_external(self):
    pass


@export
def external_call( self, arg, shell = False ):
    """
    cette fonction permet d'executer des commandes dans le cmd avec ou sans
    shell
    """
    if shell == False :
        subprocess.Popen(arg).wait()
        
    elif shell == True:
        subprocess.Popen( arg, shell = True ).wait()

@export
def external_return ( self, args:list ):
    return subprocess.check_output( args )
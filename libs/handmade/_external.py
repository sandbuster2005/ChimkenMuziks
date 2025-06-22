#made by sand
import subprocess

def external_call( self, arg, shell = False ):
    """
    cette fonction permet d'executer des commandes dans le cmd avec ou sans
    shell
    """
    if shell == False :
        subprocess.Popen(arg).wait()
        
    elif shell == True:
        subprocess.Popen( arg, shell = True ).wait()

def external_return ( self, args:list ):
    return subprocess.check_output( args )
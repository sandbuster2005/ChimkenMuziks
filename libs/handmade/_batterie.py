#made by sand
#not used anymore

def init_battery( self ):
    self.battery = [ 0, 0 ]#valeur brut de la batterie et moment du relevé
    self.battery_life = None# temps restant estimé
    self.battery_exist = self.battery_check()


def battery_check( self ):
    """
    cette fonction permet de verifier si l'appareil posséde une batterie
    afin de l'afficher plus tard
    """
    try:
        with open( "/sys/class/power_supply/BAT0/capacity", "r" ) as f:# emplacement des info batterie 
            value = f.read()
            
    except:
        self.battery_exist = False
        
    else:
        self.battery_exist = True
    
    
def get_battery( self ):
    """
    cette fonction permet d'obtenir le pourcentage de batterie restant
    """
    with open( "/sys/class/power_supply/BAT0/capacity", "r" ) as f:# emplacement des info batterie 
        value = f.read()
        
    return value.split( "\n", 1 )[ 0 ]


def get_battery_life( self ):
    """
    cette fonction permet de calculer le temps d'utilisation de l'ordinateur
    restant par rapport a sa consommation (plutôt aproximatif)
    """
    with open( "/sys/class/power_supply/BAT0/energy_now", "r" ) as f:# emplacement des info batterie 
        value = int( f.read() )
        
    if self.battery[ 0 ] != 0:
        delta = self.battery[ 0 ] - value#differance de batterie
        
        if delta != 0 :
            life = ( value / delta )*( monotonic() - self.battery[ 1 ] )# calcul du temps restant
            
            if monotonic() - self.battery[ 1 ] > 180:
                self.battery = [ value, monotonic() ]# modification de la valeur de referance toute le 3 minute
            
            self.battery_life = round( ( life / 3600 ) * 1.4, 2 )# x1.4 pour approcher la valeur reel
    
    else:
        self.battery = [ value, monotonic() ]# initialisation de la fonction

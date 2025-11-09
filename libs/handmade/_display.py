from ..readchar import readchar
from math import ceil,floor
from .utils import white
def init_display( self ):
    pass
    
def out( self, text ):
    """
    cette fonction permet d'afficher un message text a l'utilisateur
    """
    if self.graphic_manager == "base":
        print( text )


def ask( self, text ):
    """
    cette fonction permet de demander une valeur a l'utilisateur
    en lui demandant text
    """
    if self.graphic_manager == "base":
        return input( f"{ text }" )


def show_list( self, liste, num = True , start = 0):
    """
    cette fonction permet d afficher les elements d'une liste un
    par un ,numeroté ou non
    """
    if self.graphic_manager == "base":
        if num == True:
            for x in range( len( liste ) ):
                print( x + start, liste[x] )
        
        else:
            for x in liste:
                print( x )
  
  
def ask_list( self, liste, text = "" , num = True ):
    """
    cette fonction affiche a l'utilisateur une liste et lui demande
    une valeur a l'aide d un prompt text
    """
    if text == "":
        text = self.confirmation
        
    if self.graphic_manager == "base":
        if len( liste ) > self.term_size.lines:
            n = 0
            word = "n"
            size = self.term_size.lines
            
            while word == "n" or word == "p":
                self.show_list( liste[ n * (size-2) : ( n + 1 ) * (size - 2)] , start = n*(size - 2 ) )
                self.show_list(["p : previous page","n : next page"], num = False)
                word = self.ask( f"{ text }" )
                white()
                if word == "n":
                    n = min(n+1, ceil( len(liste) / (size-2) ) - 1 )
                    
                if word == "p":
                    n = max(n-1,0)
                    
            return word
        
        else:
            self.show_list( liste, num )
            
            if len( liste ) < 11:
                return readchar()    
            
            else:
                return self.ask( f"{ text }" )
    


def change_confirmation( self ):
    """
    cette fonction permet de changer le prompt par defaut de
    la fonction ask_list
    """
    self.confirmation = self.ask( "new choice prompt" )
    
    

from ..readchar import readchar

def init_display( self ):
    self.graphic_manager = "base"
    self.confirmation = "your choice: "
    
    
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


def show_list( self, liste, num = True ):
    """
    cette fonction permet d afficher les elements d'une liste un
    par un ,numeroté ou non
    """
    if self.graphic_manager == "base":
        if num == True:
            for x in range( len( liste ) ):
                print( x, liste[x] )
        
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
    
    

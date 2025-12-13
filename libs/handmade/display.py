import os
from math import ceil,log
from .terminal import *
from collections.abc import Callable

def white( n = 40 ):
    for x in range( n ):
        print( "\n" )

class Display:
    def __init__(self):
        self.term_size = os.get_terminal_size()
        self.graphic_manager = "base"
        self.confirmation = "your choice"

    def ask(self, text: str , *arg , **kwargs) -> str | None :
        """
        cette fonction permet de demander une valeur a l'utilisateur
        en lui demandant text
        """
        if self.graphic_manager == "base":
            return ninput( text = f"{ text }",*arg , **kwargs )

        else:
            return None


    def show_list(self, liste , show_num = True, start : int = 0 , quick = False ) -> None :
        """
        cette fonction permet d afficher les elements d'une liste un
        par un ,numeroté ou non
        """
        if self.graphic_manager == "base":
            if quick:
                length = ceil ( log( len ( liste ), 10 ) )
            else:
                num_of_zero = 0

            if show_num :
                for x in range( len( liste ) ):
                    if quick:
                        num_of_zero =  length - ceil ( log( x , 10 ) )

                    print(num_of_zero * "0"  + str(x + start), liste[ x ] )


            else:
                for x in liste:
                    print( x )

    def ask_list(self, liste , text  = "", show_num = True , quick = True , *arg , **kwargs ) -> str | None :
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
                size = self.term_size.lines - 2

                while word == "n" or word == "p":

                    self.show_list(liste[ n * size: (n + 1) * size ], start = n * size )

                    self.show_list( [ "p : previous page", "n : next page" ], show_num = False )

                    word = self.ask( f"{ text }", *arg , **kwargs )
                    white()

                    if word == "n":
                        n = min(n + 1, ceil( len( liste ) / size ) - 1)

                    if word == "p":
                        n = max( n - 1 , 0)

                return word

            elif quick:
                self.show_list( liste , quick = True)
                return self.ask(f"{ text }", quick = ceil( log(  len( liste ), 10 ) ) )  # auto return when enough number where entered

            else:
                self.show_list( liste)
                return self.ask( f"{ text }", *arg , **kwargs )

        else:
            return None

    def menu_deroulant(self , menu ,text ="" ,cursor = 0 ):
        if self.graphic_manager == "base":
            word = "start"
            text += "\n"
            while word != "":

                out( text )
                for x in range( len (menu ) ) :
                    if x == cursor:
                        out(">")
                        tforeground(0,0,255,menu[x])
                        out( "\n" )

                    else:
                        print( " " + menu[x] )

                word = ninput(text = "", error = None , chrs = [ Key.UP, Key.DOWN] , quick = 1 ,escape = None )
                if  word == None :
                    return len(menu) + 1

                elif word == Key.DOWN:
                    cursor = min( len(menu) - 1 , cursor + 1 )
                    lup(2)

                elif word == Key.UP:
                    cursor = max(0 , cursor - 1 )

                lup( len (menu) + text.count("\n") )
                wipe()

            ldown( len(menu) )
            return cursor

        return None


    def change_confirmation(self) -> None:
        """
        cette fonction permet de changer le prompt par defaut de
        la fonction ask_list
        """
        self.confirmation = self.ask( "new choice prompt" )

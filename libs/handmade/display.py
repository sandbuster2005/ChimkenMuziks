import os
from math import ceil
from .terminal import ninput
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


    def show_list(self, liste : list , num : bool = True, start : int = 0 , iterable = range) -> None :
        """
        cette fonction permet d afficher les elements d'une liste un
        par un ,numeroté ou non
        """
        if self.graphic_manager == "base":
            if num :
                for x in iterable( len( liste ) ):
                    print(x + start, liste[ x ] )

            else:
                for x in liste:
                    print( x )


    def ask_list(self, liste : list, text : str = "", num : bool = True , iterable = range , *arg : Callable , **kwargs : str | list[ str ] ) -> str | None :
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
                    self.show_list(liste[n * ( size - 2 ): (n + 1) * ( size - 2 ) ], start = n * ( size - 2) , iterable = iterable )
                    self.show_list( [ "p : previous page", "n : next page" ], num = False , iterable = iterable )
                    word = self.ask( f"{ text }", *arg , **kwargs )
                    white()

                    if word == "n":
                        n = min(n + 1, ceil( len( liste ) / ( size - 2 ) ) - 1)

                    if word == "p":
                        n = max( n - 1 , 0)

                return word

            else:
                self.show_list( liste, num , iterable = iterable )
                return self.ask( f"{ text }", *arg , **kwargs )

        else:
            return None

    def change_confirmation(self) -> None:
        """
        cette fonction permet de changer le prompt par defaut de
        la fonction ask_list
        """
        self.confirmation = self.ask( "new choice prompt" )

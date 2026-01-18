import os
from math import ceil, log, floor
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
                return self.ask(f"{ text }", quick = ceil( log(  len( liste ), 10 ) ), *arg , **kwargs )  # auto return when enough number where entered

            else:
                self.show_list( liste)
                return self.ask( f"{ text }", *arg , **kwargs )

        else:
            return None

    def menu_deroulant(self, menu, *args, text="", cursor=0, search=False, word_search = "" ):

        if self.graphic_manager == "base":

            size = floor(os.get_terminal_size().lines / 2)
            lenght = os.get_terminal_size().columns
            chrs_search = [chr(x) for x in range(32, 127)] + [ Key.BACKSPACE ]
            chrs = [Key.SHIFT_UP, Key.UP, Key.DOWN, Key.SHIFT_DOWN, Key.CONTROL_DOWN, Key.CONTROL_UP]

            word = ""
            text += "\n"

            global_pos = cursor
            temp_menu = [ x for x in menu if word_search.lower() in "".join(x).lower() ]

            while word != Key.ENTER:

                out( text )

                out(f"{len(temp_menu)} items\n")

                if word_search != "":
                    out("search: ")

                out(word_search + "\n" )

                if len(temp_menu) < size and None == True: # unused
                    for x in range(len(temp_menu)):

                        if x == cursor:
                            tforeground(0, 0, 255, ">" + val[1:] )
                            out("\n")

                        else:
                            print( val )
                else:

                    before = cursor - size
                    after = cursor + size

                    for x in range( max(0, before - 1  ), max( 0, before + min( after * -1 , len( temp_menu ) ) ) + min( after + max(0, before * -1 ) -5 , len( temp_menu ) ) ):
                        val = " " + "".join(temp_menu[x])

                        if len(val) > lenght:
                            val = val[: (lenght - 3) ] + "..."

                        if x == cursor:
                            tforeground(0, 0, 255, ">" + val[1:] )
                            out("\n")

                        else:
                            print( val )

                word = ninput(text="", error=None, simple=True, quick=1, escape=None, *args)

                if search:

                    if word in chrs_search:
                        white()

                        if word == Key.BACKSPACE:
                            word_search = word_search[ :-1 ]

                        else:
                            word_search += word

                        if temp_menu != []:
                            global_pos = menu.index( temp_menu[ cursor ] )

                        temp_menu = [x for x in menu if word_search.lower() in "".join( x ).lower() ]

                        if menu[ global_pos ] in temp_menu:
                            cursor = temp_menu.index( menu[ global_pos ] )

                        else:
                            cursor = 0

                if word == Key.ESC:
                    return len(menu) + 1

                elif word == Key.DOWN:
                    cursor = min(len(temp_menu) - 1, cursor + 1)
                    # lup(2)

                elif word == Key.CONTROL_DOWN:
                    cursor = len(temp_menu) - 1


                elif word == Key.SHIFT_DOWN:
                    cursor = min(len(temp_menu) - 1, cursor + (size - 1))

                elif word == Key.UP:
                    cursor = max(0, cursor - 1)

                elif word == Key.CONTROL_UP:
                    cursor = 0

                elif word == Key.SHIFT_UP:
                    cursor = max(0, cursor - (size - 1))

                lup(len(menu) + text.count("\n") )
                wipe()

            if temp_menu != []:
                global_pos = menu.index(temp_menu[cursor])
            else:
                return len(menu) + 1
            # ldown( len(menu) )
            return global_pos

        return None


    def change_confirmation(self) -> None:
        """
        cette fonction permet de changer le prompt par defaut de
        la fonction ask_list
        """
        self.confirmation = self.ask( "new choice prompt" )

import termios
import sys
from collections.abc import Callable
from copy import copy
from select import select
from io import StringIO
from libs.readchar import ReadChar,key as Key


def ninput(*arg : Callable , **kwarg) -> str:

    chrs : list[str] = [  chr( x ) for x in range( 32, 127 ) ]
    escape : any = ""
    text : str =  "input: "
    error : str  = "value not recognized / not acceptable"
    before : str = ""
    condition : Callable | None = None
    quick : int = 0
    value : str = ""
    simple : bool = False
    pos = len(value)

    for k,x in kwarg.items():

        if k == "chrs":
            chrs = x
        if k == "text":
            text = x
        if k == "error":
            error = x
        if k == "before":
            before = x
        if k == "condition":
            condition = x
        if k == "quick":
            quick = x
        if k== "value":
            value = x
        if k == "escape":
            escape = x
        if k == "simple":
            simple = x

    stop = False
    le = len(before)

    if text:
        print(text)

    if error:
        print("")

    out(before)

    with ReadChar() as Ninput:
        while not stop:
            a = Ninput.key()

            if simple and a:
                return a


            if a == Key.ENTER:
                stop = True

            elif a == Key.LEFT:
                pos = max( 0 , pos - 1 )
                line_start()

                if pos != 0:
                    right(pos)

            elif a == Key.RIGHT:
                pos = min( len( value ) , pos + 1)
                line_start()
                right(pos)

            elif a == Key.SUPR:
                pos = 0
                value = ""
                line_start()
                wipe_line()
                out(before)

            elif a == Key.BACKSPACE:
                line_start()
                value = value[ : max ( 0, pos - 1) ] + value [ pos: ]

                if pos:
                    pos -= 1

                wipe_line()
                out(before + value)
                line_start()

                if pos:
                    right(pos + le)

            elif a == Key.ESC:
                return escape

            elif a in chrs:
                lup()

                if error:
                    wipe_line()

                ldown()

                value = value[ : pos  ] + a + value [ pos   : ]
                pos += 1

                wipe_line()
                out( before + value )
                line_start()
                right( pos + le )

            elif a == "":
                pass

            else:
                if error:
                    lup()
                    print(error )
                if pos:
                    right(pos)

            for func in arg:
                func()

            if condition:
                if condition():
                    return ""
            
            if quick:
                if len(value) >= quick:
                    stop = True
    print("")
    return value

#pretty sure your not dumb if you see this so it can go without comment for now

def out( text ):
    sys.stdout.write( text )
    sys.stdout.flush()

def up( x = 1 ):
    out( f'\x1b[{ x }A' )
    
def lup( x = 1 ):
    out( f'\x1b[{ x }F' )
    
def down( x = 1):#dont work for now it seem
    out ( f'\x1b[{ x }B' )

def ldown( x = 1 ):
    out( '\n'*x )

def left( x = 1 ):
    out( f'\x1b[{ x }D' )
    
def right( x = 1 ):
    out( f'\x1b[{ x }C' )

def home():
    out( '\x1b[H' )

def wipe():
    out( '\x1b[2J' )
    
def wipe_line():
    out( '\x1b[2K' )

def save():
    out( "\x1b7" )
    
def load():
    out( "\x1b8" )

def line_start():
    lup()
    ldown()
#true color (24bit)
def tforeground(r,g,b,text):
    out(f"\x1b[38;2;{r};{g};{b}m{text}")
    out("\033[0m")

def tbackground(r,g,b,text):
    out(f"\x1b[48;2;{r};{g};{b}m{text}")
    out("\033[0m")

#0-255
def foreground(idd,text):
    out(f"\x1b[38;5;{idd}m{text}")
    out("\033[0m")

def background(idd,text):
    out(f"\x1b[48;5;{idd}m{text}")
    out("\033[0m")

#The table starts with the original 16 colors (0-15).
#The proceeding 216 colors (16-231) or formed by a 3bpc RGB value offset by 16, packed into a single value.
#The final 24 colors (232-255) are grayscale starting from a shade slighly lighter than black, ranging up to shade slightly darker than white.
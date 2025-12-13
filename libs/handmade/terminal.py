import termios
import sys
from collections.abc import Callable
from copy import copy
from select import select
from io import StringIO


class Key:
    def __init__(self):
        raise "static class should not be turned into instance"

    LF = "\x0a"
    CR = "\x0d"
    SPACE = "\x20"
    ESC = "\x1b"
    TAB = "\x09"

    # CTRL
    CTRL_A = "\x01"
    CTRL_B = "\x02"
    CTRL_C = "\x03"
    CTRL_D = "\x04"
    CTRL_E = "\x05"
    CTRL_F = "\x06"
    CTRL_G = "\x07"
    CTRL_H = "\x08"
    CTRL_I = TAB
    CTRL_J = LF
    CTRL_K = "\x0b"
    CTRL_L = "\x0c"
    CTRL_M = CR
    CTRL_N = "\x0e"
    CTRL_O = "\x0f"
    CTRL_P = "\x10"
    CTRL_Q = "\x11"
    CTRL_R = "\x12"
    CTRL_S = "\x13"
    CTRL_T = "\x14"
    CTRL_U = "\x15"
    CTRL_V = "\x16"
    CTRL_W = "\x17"
    CTRL_X = "\x18"
    CTRL_Y = "\x19"
    CTRL_Z = "\x1a"

    # common
    BACKSPACE = "\x7f"

    # cursors
    UP = "\x1b\x5b\x41"
    DOWN = "\x1b\x5b\x42"
    LEFT = "\x1b\x5b\x44"
    RIGHT = "\x1b\x5b\x43"

    # navigation keys
    INSERT = "\x1b\x5b\x32\x7e"
    SUPR = "\x1b\x5b\x33\x7e"
    HOME = "\x1b\x5b\x48"
    END = "\x1b\x5b\x46"
    PAGE_UP = "\x1b\x5b\x35\x7e"
    PAGE_DOWN = "\x1b\x5b\x36\x7e"

    # function keys
    F1 = "\x1b\x4f\x50"
    F2 = "\x1b\x4f\x51"
    F3 = "\x1b\x4f\x52"
    F4 = "\x1b\x4f\x53"
    F5 = "\x1b\x5b\x31\x35\x7e"
    F6 = "\x1b\x5b\x31\x37\x7e"
    F7 = "\x1b\x5b\x31\x38\x7e"
    F8 = "\x1b\x5b\x31\x39\x7e"
    F9 = "\x1b\x5b\x32\x30\x7e"
    F10 = "\x1b\x5b\x32\x31\x7e"
    F11 = "\x1b\x5b\x32\x33\x7e"
    F12 = "\x1b\x5b\x32\x34\x7e"

    # SHIFT+_
    SHIFT_TAB = "\x1b\x5b\x5a"

    # other
    CTRL_ALT_SUPR = "\x1b\x5b\x33\x5e"

    # ALT+_
    ALT_A = "\x1b\x61"

    # CTRL+ALT+_
    CTRL_ALT_A = "\x1b\x01"

    # aliases
    ENTER = LF
    DELETE = SUPR


class ReadChar:
    """
    A ContextManager allowing for keypress collection without requiring the user to
    confirm presses with ENTER. Can be used non-blocking while inside the context.
    """

    def __init__(self) -> None:
        self.interrupt_key = ["\x03"]  #ctrl C
        self._buffer = StringIO()

    def __enter__(self) -> "ReadChar":
        self.fd = sys.stdin.fileno()
        term = termios.tcgetattr(self.fd)
        self.old_settings = copy(term)

        term[3] &= ~(
                termios.ICANON  # don't require ENTER
                | termios.ECHO  # don't echo
                | termios.IGNBRK
                | termios.BRKINT
        )
        term[6][termios.VMIN] = 0  # immediately process every input
        term[6][termios.VTIME] = 0
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, term)
        return self

    def __exit__(self, type, value, traceback) -> None:
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_settings)

    def __update(self) -> None:
        """
        check stdin and update the internal buffer if it holds data
        """
        if sys.stdin in select([sys.stdin], [], [], 0)[0]:
            pos = self._buffer.tell()
            data = sys.stdin.read()
            self._buffer.write(data)
            self._buffer.seek(pos)

    @property
    def key_waiting(self) -> bool:
        """
        True if a key has been pressed and is waiting to be read. False if not.
        """
        self.__update()
        pos = self._buffer.tell()
        next_byte = self._buffer.read(1)
        self._buffer.seek(pos)
        return bool(next_byte)

    def char(self) -> str:
        """
        Reads a single char from the input stream and returns it as a string of
        length one. Does not require the user to press ENTER.
        """
        self.__update()
        return self._buffer.read(1)

    def key(self) -> str:
        """
        Reads a keypress from the input stream and returns it as a string. Key-pressed
        consisting of multiple characters will be read completely and be returned as a
        string matching the definitions in `key.py`.
        Does not require the user to press ENTER.
        """
        self.__update()

        c1 = self.char()

        if c1 in self.interrupt_key:
            raise KeyboardInterrupt

        if c1 != "\x1B":
            return c1

        c2 = self.char()
        if c2 not in "\x4F\x5B":
            return c1 + c2

        c3 = self.char()
        if c3 not in "\x31\x32\x33\x35\x36":
            return c1 + c2 + c3

        c4 = self.char()
        if c4 not in "\x30\x31\x33\x34\x35\x37\x38\x39":
            return c1 + c2 + c3 + c4

        c5 = self.char()
        return c1 + c2 + c3 + c4 + c5


def ninput(*arg : Callable , **kwarg) -> str:

    chrs : list[str] = [  chr( x ) for x in range( 32, 127 ) ]
    escape : any = ""
    text : str =  "input: "
    error : str  = "value not recognized / not acceptable"
    before : str = ""
    condition : Callable | None = None
    quick : int = 0
    value : str = ""
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
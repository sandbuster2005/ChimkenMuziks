import sys
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

#true color (24bit)
def Tforeground(r,g,b,text):
    out(f"\x1b[38;2;{r};{g};{b}m{text}")
def Tbackground(r,g,b,text):
    out(f"\x1b[48;2;{r};{g};{b}m{text}")
    
#0-255
def foreground(ID,text):
    out(f"\x1b[38;5;{ID}m{text}")
def background(ID,text):
    out(f"\x1b[48;5;{ID}m{text}")

#The table starts with the original 16 colors (0-15).
#The proceeding 216 colors (16-231) or formed by a 3bpc RGB value offset by 16, packed into a single value.
#The final 24 colors (232-255) are grayscale starting from a shade slighly lighter than black, ranging up to shade slightly darker than white.
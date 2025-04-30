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

    
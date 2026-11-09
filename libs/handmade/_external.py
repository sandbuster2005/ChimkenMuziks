#made by sand
from libs.readchar import key as Key
import subprocess
import threading
from .utils import export

@export
def init_external(self):
    pass


@export
def external_call( self, arg, shell = False ):
    """
    cette fonction permet d'executer des commandes dans le cmd avec ou sans
    shell
    """
    if shell == False :
        subprocess.Popen(arg).wait()

    elif shell == True:
        subprocess.Popen( arg, shell = True ).wait()

@export
def external_return ( self, args:list ):
    return subprocess.check_output( args )

@export
def launch_mpris(self):
    self.dbus_command = {
        "QUIT":       [ self.end, {} ],
        "PLAY":       [ self._unpause, {} ],
        "PAUSE":      [ self._pause, {} ],
        "PLAY_PAUSE": [ self.wind, { 6 : "mode" } ] ,
        "NEXT":       [ self.play_song, {1 - self.repeat : "choose"}],
        "PREVIOUS":   [ self.play_last, {} ]
    }

    if self.MPRIS:
        self.MPRIS_server = threading.Thread( target = self.MPRIS.run)
        self.MPRIS_server.daemon = True
        self.MPRIS_server.start()

@export
def send_to_dbus(self, property, value):
    if self.MPRIS:
        self.MPRIS.update_queue.append( (property, value) )



@export
def parse_input(self, input ):
    self.logger["external"].debug(f"parsing {input}")
    input = list( input.split(":",1)[-1] )
    if "%" in input :
        input[ input.index("%") ] = Key.LF
    if "<" in input:
        input[ input.index("<") ] = Key.DOWN
    if ">" in input:
        input[ input.index(">") ] = Key.UP

    return input

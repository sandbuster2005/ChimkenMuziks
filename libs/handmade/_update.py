import os
import random
from time import strftime, monotonic, sleep
from libs.progress.bar import Bar
from math import floor,ceil
from .terminal import *
from .utils import closest, white
def current_time():
    return strftime('%H %M').split(" ")

def init_update(self):
    self.term_size = os.get_terminal_size()
    self.changed = []
    self.song_saved = False
    self.current_time = current_time()
    self.time = False
    self.time_check = [False, 0, 0, 0]



def update_logic(self):
    if self.timer:
        if self.timer[1] < 1:
            if self.timer_mode == 0:
                self.end()

            elif self.timer_mode == 1:
                self.wind(5)

            elif self.timer_mode == 2:
                self.wind(6)

    if not "time" in self.changed:
        if self.current_time != current_time():
            self.current_time = current_time()
            self.changed.append("time")

    if self.timer:

        if not "timer" in self.changed:
            if monotonic() > self.timer[2] + ( self.timer[0] * 60 ):
                self.timer[0] += 1
                self.timer[1] -= 1
                self.changed.append("timer")


    if self.sound_manager == "alsa":

        if self.volume != self.get_volume():
            self.volume = self.get_volume()
            self.changed.append("volume")



    if self.song:
        if not self.bar:
            if self.player.get_length() > 0:
                sleep(0.01)
                if self.color:
                    color = random.randint(0, 252)
                    color += 3 - (color % 3)
                else:
                    color = "white"

                lenght = self.player.get_length()
                self.bar = Bar(f"", max = floor(lenght / 1000), color = color, addaptative_bar = self.addaptive_bar,
                               center = self.center)


        else:
                    
            self.time = self.player.get_time()

            if self.bar.index  < floor( self.time / 1000 ):# or self.bar.index > floor( self.time / 1000 ) :
                self.bar.index = floor( self.time / 1000 )
                if not "bar" in self.changed:
                    self.changed.append("bar")

            if self.word:
                if self.words:
                    if ( close := closest( int( self.time / 1000 ), [x[0] for x in self.words])) != self.last_word and self.words[close][0] - self.time / 1000 < 1:
                            self.last_word = close
                            if not "word" in self.changed:
                                self.changed.append("word")
                    
            if self.time < 0:  # en cas de reculer en dessous du debut
                self.time = 0

            if self.bar.index < 0:  ##en cas de reculer en desosus du debut
                self.bar.index = 0


            if self.term_size != ( _ := os.get_terminal_size() ) :
                self.term_size = _
                if not "display" in self.changed:
                    self.changed.append("display")


            if not self.song_saved and self.bar.index * 2 > self.bar.max:
                self.song_saved = True
                self.write_song_database( self.song[ 1 ] )

            """
            if self.time_check[3]:
                self.time_check[3] -= 1

            if not self.time_check[0] and not self.time_check[3]:
                self.time_check[0] = True
                self.time_check[1] = self.player.get_time()
                self.time_check[2] = monotonic()

            if self.time_check[0] and not self.pause:

                if self.time_check[2] + 5 < monotonic():

                    if self.player.get_time() == self.time_check[1]:

                        self.play_song( (1 - self.repeat ) )
                        self.display()

                    else:
                        self.time_check = [False, 0, 0, 60]
            """

            if self.bar:
                if not self.player.is_playing() and not self.pause:   # la chanson est fini# la chason est bien fini et ne vien pas de commencer
                    self.play_song((1 - self.repeat))
                    self.display()


def update_display(self):
    if "space" in self.changed and not self.search:
        wipe()
        self.changed.remove("space")

    if "word" in self.changed:
        lyrics = self.words[self.last_word][1]
        space = floor(self.term_size.columns / 2 - len(lyrics) / 2)
        save()
        lup(4)
        wipe_line()
        out(f"{' ' * space * self.center}{lyrics}")
        load()
        self.changed.remove("word")

    if self.song:
        if "time" in self.changed or "timer" in self.changed or "volume" in self.changed or "display" in self.changed:
            if self.show and "display" in self.changed:
                white()
                self.display_img()
                ldown(3)

            time_string = f"{ self.current_time[0] }:{ self.current_time[1] }"

            self.volume = self.get_volume()
            volume_string = f"{self.volume}%"

            if self.volume < 10:
                volume_string = "0" + volume_string

            string = time_string + "   " + volume_string

            if self.playlist:
                string = self.playlist + "   " + string

            if self.timer:
                string += "   " + f"timer :{self.timer[1]} mins"

            space = floor((self.term_size.columns - len(string)) / 2)

            if os.name == 'nt':
                a = '\\'
            else:
                a = '/'

            name = self.song[1].rsplit(a, 1)[1]

            if self.song in self.favorite:
                name = "*" + name + "*"

            space_name = floor((self.term_size.columns - len(name)) / 2)

            if self.bar:
                self.bar.center = self.center

            save()
            lup(3)
            wipe_line()
            out(f"{' ' * space * self.center}{string}")

            ldown()
            wipe_line()
            out(f"{' ' * space_name * self.center}{name}")

            load()
            wipe_line()
            out(":")
            if "time" in self.changed:
                self.changed.remove("time")

            if "timer" in self.changed:
                self.changed.remove("timer")

            if "volume" in self.changed:
                self.changed.remove("volume")

            if "display" in self.changed:
                self.changed.remove("display")

        if "bar" in self.changed and not self.search and self.bar:
            save()
            up()
            self.bar.update()
            load()
            self.changed.remove("bar")

def is_finished(self):
    if not self.stay:
        return True
    return False

def end(self):
    self.stay = False
    self.player.stop()
    if self.save_param:
        self.write_param()

a = Bar(f"", max = 8)
a.index = 2
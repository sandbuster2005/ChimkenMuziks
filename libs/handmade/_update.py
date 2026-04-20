import os
import random
from time import strftime, monotonic, sleep , time as timeS
from libs.progress.bar import Bar
from math import floor,ceil
from pypresence import  Presence, ActivityType, StatusDisplayType
from .terminal import *
from .utils import closest, white



def current_time():
    return strftime('%H %M').split(" ")

def init_update(self):
    self.term_size = os.get_terminal_size()
    self.changed = []
    self.song_saved = False
    self.current_time = current_time()
    self.time = {"vlc": 0 , "python": 0 }
    self.time_check = [False, 0, 0, 0]

def update_logic(self):
    if self.timer:
        if self.timer["remaining"] < 1 and self.timer["update_mode"] == "time":
            self.logger["update"].info("timer finished")
            self.end_timer()

    if not "time" in self.changed:
        if self.current_time != current_time():
            self.current_time = current_time()
            self.logger["update"].trace("time as changed")
            self.changed.append("time")

    if self.pause:
        self.logger["update"].bullshit("player is paused")

    if self.timer:

        if not "timer" in self.changed:

            if monotonic() > self.timer["start"] + ( self.timer["elapsed"] * 60 ) and self.timer["update_mode"] in [ "time","time-song" ]:
                self.timer["elapsed"] += 1
                self.timer["remaining"] -= 1
                self.logger["update"].debug(f"timer as changed : {self.timer}")
                self.changed.append("timer")


    if self.sound_manager == "alsa":

        if self.volume != self.get_volume():
            self.logger["update"].info("global volume")
            self.volume = self.get_volume()
            self.changed.append("volume")



    if self.song:
        if not self.bar:
            if self.player.get_length() > 0:
                sleep(0.01)
                self.logger["update"].info("creating new bar")
                if self.color:
                    color = random.randint(0, 252)
                    color += 3 - (color % 3)
                else:
                    color = "white"

                lenght = self.player.get_length()
                self.bar = Bar(f"", max = floor( lenght / 1000 ), color = color, addaptative_bar = self.addaptive_bar,
                               center = self.center)
                
                if self.discord and self.discordRP:
                   self.update_discord_status()


        else:
            time = self.player.get_time()

            if self.time["vlc"] != time :
                self.time["vlc"] = time
                self.time["python"] = monotonic()

            if self.time["vlc"] > 0:
                if self.pause:
                    time = self.time["vlc"]
                    self.time["python"] = monotonic()
                else:
                    time = self.time["vlc"] + monotonic() * 1000 - self.time["python"] * 1000
            else:
                time = 0

            self.logger["update"].bullshit( f" UPDATE LOOP : time : { time  } , vlc time : {self.time['vlc'] }")

            if self.bar.index  < floor( time / 1000 ):# or self.bar.index > floor( self.time / 1000 ) :
                self.bar.index = floor( time / 1000 )
                if not "bar" in self.changed:
                    self.changed.append("bar")
                    self.logger["update"].trace("bar changed ")

            if self.word:

                if self.words:

                    if self.last_word != len( self.words ) -1 :

                        if self.words[self.last_word][0] + ( self.words[self.last_word + 1][0] - self.words[self.last_word][0] ) / 1.2 < time  / 1000:
                                self.last_word += 1

                                if not "word" in self.changed:
                                    self.logger["update"].debug(f"lyric changed : { self.words[self.last_word] }")
                                    self.changed.append( "word" )

            if time < 0:  # en cas de reculer en dessous du debut
                self.time["vlc"] = 0
                self.time["python"] = monotonic()
                self.logger["update"].warning("time went under 0")

            if self.bar.index < 0:  ##en cas de reculer en desosus du debut
                self.bar.index = 0
                self.changed.append("bar")
                self.logger["update"].warning("bar went under 0")


            if self.term_size != ( _ := os.get_terminal_size() ) :
                self.term_size = _

                if not "display" in self.changed:
                    self.changed.append("display")

                self.logger["update"].debug(f"terminal size changed to {self.term_size}")
                
            if self.discordRP and not self.discord_connected and self.discord:
                self.connect_to_discord()
                self.update_discord_status()
                self.discord_connected = True
                
            if not self.discordRP and self.discord_connected and self.discord:
                self.RPC.clear()
                self.RPC.close()
                self.discord_connected = False
            
            


            if not self.song_saved and self.bar.index * 2 > self.bar.max:
                self.song_saved = True
                self.write_song_database( self.song.file )

            if self.bar:
                if not self.player.is_playing() and not self.pause and self.stay:
                    self.logger["update"].info("song finished, next one")
                    self.play_song((1 - self.repeat))
                    self.display()
            


def update_display(self, value ):
    self.logger["update"].bullshit("display loop")
    if "space" in self.changed and not self.search:
        wipe()
        self.logger["update"].trace("cleared screen")
        self.changed.remove("space")

    if "word" in self.changed:
        lyrics = self.words[self.last_word][1]
        space = floor(self.term_size.columns / 2 - len(lyrics) / 2)
        save()
        lup(4)
        wipe_line()
        out(f"{' ' * space * self.center}{lyrics}")
        load()

        self.logger["update"].trace("updated lyric")
        self.changed.remove("word")

    if self.song:
        if "time" in self.changed or "timer" in self.changed or "volume" in self.changed or "display" in self.changed:
            if self.show and "display" in self.changed:
                white()
                self.display_img()
                self.logger["update"].debug("printed image ")
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
                string += "   " + f"timer :{self.timer['remaining']} {self.timer['display']}"

            space = floor((self.term_size.columns - len(string)) / 2)

            name = self.song.name

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
            line_start()
            out( value )
            if "time" in self.changed:
                self.changed.remove("time")

            if "timer" in self.changed:
                self.changed.remove("timer")

            if "volume" in self.changed:
                self.changed.remove("volume")

            if "display" in self.changed:
                self.changed.remove("display")

            self.logger["update"].trace("updated main display")

        if "bar" in self.changed and not self.search and self.bar:
            save()
            lup()
            self.bar.update()
            load()
            wipe_line()
            line_start()
            out(value)
            self.logger["update"].trace("updated bar")
            self.changed.remove("bar")


def connect_to_discord(self):
    self.discord = True
    self.discord_connected = False
    
    if self.discordRP:
        client_id = "1495534597419700264"
        try:
            self.RPC = Presence( client_id )
            self.RPC.connect()
            
        except:
            self.discord = False
            self.discord_connected = False
            
        else:
            self.discord_connected = True    



def update_discord_status(self):
    self.RPC.update(
        activity_type = ActivityType.LISTENING,
        status_display_type = StatusDisplayType.NAME ,
        name = self.song.name,
        state = "ChimkenMuziks",
        start = timeS() - self.bar.index,
        end = timeS() + self.bar.max - self.bar.index   
        )

def pause_discord_status(self):
    self.RPC.update(
        activity_type = ActivityType.LISTENING,
        status_display_type = StatusDisplayType.NAME ,
        name = "Paused",
        state = "ChimkenMuziks", 
        )
            
            
def is_finished(self):
    if not self.stay:
        return True
    return False


def end(self):
    self.stay = False
    self.logger["update"].info("EXITING APP")
    self.player.stop()
    if self.discord_connected:
        self.RPC.clear()
        self.RPC.close()
        
    if self.save_param:
        self.write_param()

from .utils import export
from pypresence import  Presence, ActivityType, StatusDisplayType
from youtube_search import YoutubeSearch
from time import time as timeS
@export
def init_discord(self):
    self.discord = True
    self.discord_connected = False


@export
def connect_to_discord(self):
    self.logger["discord"].debug("connecting to discord...")
    if self.discordRP:
        client_id = "1495534597419700264"
        try:
            self.RPC = Presence( client_id )
            self.RPC.connect()
            
        except:
            self.logger["discord"].debug("connection failed")
            self.discord = False
            
            self.discord_connected = False
            
        else:
            self.logger["discord"].debug("connected")
            self.discord_connected = True    


@export
def update_discord_status(self):        
    try :
        self.logger["discord"].debug("updating status...")
        if self.url:
            self.RPC.update(
                activity_type = ActivityType.LISTENING,
                status_display_type = StatusDisplayType.DETAILS ,
                details = self.song.name,
                details_url = self.url,
                state = "ChimkenMuziks",
                start = timeS() - self.bar.index,
                end = timeS() + self.bar.max - self.bar.index,
                )
        else:
            self.RPC.update(
                activity_type = ActivityType.LISTENING,
                status_display_type = StatusDisplayType.DETAILS ,
                details = self.song.name,
                state = "ChimkenMuziks",
                start = timeS() - self.bar.index,
                end = timeS() + self.bar.max - self.bar.index,
                )

            
    except:
        self.logger["discord"].debug("update failed")
        self.discord = False
        self.discord_connected = False
            

    else:
        self.logger["discord"].debug("updated status")
        self.discord_connected = True           

@export
def pause_discord_status(self):
    try :
        self.logger["discord"].debug("pausing status...")
        self.RPC.update(
            activity_type = ActivityType.LISTENING,
            status_display_type = StatusDisplayType.NAME ,
            name = "Paused",
            state = "ChimkenMuziks", 
            )
    except:
        self.logger["discord"].debug("pausing failed")
        self.discord = False
        self.discord_connected = False

    else:
        self.logger["discord"].debug("status paused")
        self.discord_connected = True

@export
def exit_discord(self):
    if self.discord_connected:
        self.RPC.clear()
        self.RPC.close()
        
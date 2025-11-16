#made by sand
try :
    import alsaaudio
except:
    pass

def init_sound( self ):
    self.mute = 0
    
    try :
        import alsaaudio
        
    except:
        self.audio_linux=False
        
    else:
        self.audio_linux=True
    
def start_sound( self ):
    """
    cette fonction permet de demmarer les gestionnaire de son externe
    qui le nécessite
    """
    if self.sound_manager == "alsa":
        self.mixer = alsaaudio.Mixer()
        
    self.volume = self.get_volume()
    
  
def change_sound_manager( self ):
    """
    cette fonction permet de changer le gestionnaire
    """
    choice = self.ask_list( [ "base inclued in vlc", "alsaaudio , use global volume ONLY on linux" ] )
    
    if choice == "0":
        self.sound_manager = "base"
        
    if choice == "1": 
        if self.audio_linux:
            self.mixer = alsaaudio.Mixer()
            self.volume = self.get_volume()
            self.sound_manager = "alsa"
            self.display()
    
    
def get_volume( self ):
    """
    cette fonction renvoie le volume actuel
    """
    if self.sound_manager == "base":
       volume = self.player.audio_get_volume()
       return volume
    
    if self.sound_manager == "alsa":
        volume = self.mixer.getvolume()[ 0 ]
        return volume
        
        
def set_volume(self):
    """
    cette fonction permet de mettre le volume a une valeur predéfini
    """
    if self.sound_manager == "base":
        self.player.audio_set_volume( self.volume )
        
    if self.sound_manager == "alsa":
        self.mixer.setvolume( self.volume )
       
       
def deafen(self):
    """
    cette fonction permet de rendre audible/mettre en sourdine 
    """
    if self.sound_manager == "base":
        self.mute = 1 - self.mute
        self.player.audio_set_mute( self.mute )
        
    if self.sound_manager== "alsa":
        self.mute = 1 - self.mute
        self.mixer.setmute( self.mute )
        
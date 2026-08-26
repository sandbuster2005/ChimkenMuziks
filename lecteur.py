#!/bin/python
#made by sand
import argparse
import sys
import logging
import datetime
import os 
from ChimkenJournalism import Journal
from appdirs import AppDirs



#debug levels :
    #NOTSET : 0
    # [CUSTOM] BULLSHIT : 1
    # [CUSTOM] TRACE : 5
    #DEBUG : 10
    #INFO : 20
    #WARNING : 30
    #ERROR : 40
    #CRITICAL : 50


class App:
    def __init__( self, song = "", logging_level = logging.DEBUG ):

        self.appdirs = AppDirs("ChimkenMuziks","sand")
        try:
            os.mkdir(self.appdirs.user_data_dir)
            os.mkdir(self.appdirs.user_cache_dir)
            os.mkdir(self.appdirs.user_log_dir)
            os.mkdir(self.appdirs.user_config_dir)
        
        except:
            pass
        
        if os.path.isfile('appdata/param.txt') and not os.path.isfile(AppDirs("ChimkenMuziks","sand").user_config_dir+'/param.txt'):
            os.rename('appdata/param.txt', AppDirs("ChimkenMuziks","sand").user_config_dir+'/param.txt')
        
        if os.path.isfile('appdata/cache/data.db')and not os.path.isfile(AppDirs("ChimkenMuziks","sand").user_data_dir+'/data.db'):
            os.rename('appdata/cache/data.db', AppDirs("ChimkenMuziks","sand").user_config_dir+'/data.db')
            
        
        
        conf ={
            "default" :{
                "level": logging_level,
                "format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
                "loggers": ["main", "param", "command", "file", "image", "download", "song", "data", "update", "discord"],
                "handlers":[
                    {
                    "name" : f"{self.appdirs.user_log_dir}/{str(datetime.datetime.now()).replace(':','_')}.log",
                    "type" : "file",
                    "level": 0
                    }      
                    ]
            }
        }
        
        self.logger = Journal( conf )
        self.logger.add_level("TRACE",5)
        self.logger.add_level("BULLSHIT",1)
        
        self.logger["main"].info("APP STARTED")

        self.logger["main"].debug("initializing methods")
        
        
        self.init_param()
        self.init_main(song)
        self.init_sound()
        self.init_battery()
        self.init_command()
        self.init_file()
        self.init_image()
        self.init_download()
        self.init_song()
        self.init_display()
        self.init_printer()
        self.init_data()
        self.init_playlist()
        self.init_update()
        self.logger["main"].info("initiated methods")

    from libs.handmade._external import external_call, external_return
    from libs.handmade._display import init_display, out, ask, ask_list, show_list, change_confirmation
    from libs.handmade._sound import init_sound, start_sound, change_sound_manager, get_volume, set_volume, deafen
    from libs.handmade._batterie import init_battery, battery_check, get_battery, get_battery_life
    from libs.handmade._command import init_command, sort_command, edit_command, help_menu      
    from libs.handmade._param import init_param, get_param, write_param, reset
    from libs.handmade._files import init_file, get_file, select_dir, switch_dir, find_file, check_adress, change_main_path, get_words, change_extension, edit_dirs, create_dirs_links, nselect_dir
    from libs.handmade._image import init_image ,get_img, display_img, select_img, load_script, screen_mode,gen_image
    from libs.handmade._download import init_download, yt_search, dl_yt_playlist, thread_loop 
    from libs.handmade._song import init_song, _choose_song, load_songs, play_song, play_last, historic, select, _play, play_midi, convert_midi, default_midi, get_metadata, most_played, select_fav,_select_song,play_now,get_url
    from libs.handmade._main import init_main, main, get_input, load_all, wind, display, set_timer, param_center, clear_cache, n_input, reset_settings, end_timer
    from libs.handmade._printimage import print_image_to_screen, init_printer, gen_image_data
    from libs.handmade._data import init_data, write_song_database, create_song_database, update_song_database, get_index_data, update_favorite_database, load_favorite_database, add_song_database, add_column, drop_column, get_column, load_playlist_database, is_in_playlist, update_playlist_database, get_albums, get_artists, load_album_database, load_artist_database, get_song_database, find_song_database, played_database, update_song_metadata_info, exec_sql_request,get_playlist  
    from libs.handmade._playlist import init_playlist, playlist_manager , add_to_playlist, get_song_info, load_playlist, remove_playlist, load_new_playlist,clear_playlist, add_new_playlist, show_playlist, edit_playlist,gen_playlist_menu
    from libs.handmade._update import init_update , is_finished , update_logic , update_display,update_discord_status,connect_to_discord,pause_discord_status,end,preload_song
    import colorama.__init__ as colorama
    colorama.init()

    class Song:
        def __init__(self, index , file , separator , metadata = {}):
            self.index = index
            self.file = file
            self.filepathname, self.extension = self.file.rsplit( ".",1 )
            self.filepath, self.filename = self.file.rsplit( separator, 1 )
            self.name = self.filename.rsplit( ".",1 )[0]
            self.metadata = metadata
            
            # Default values for mandatory metadata entries:
            if 'track' not in self.metadata:
                self.metadata['track'] = 0
            
        def __str__(self):
            return self.file
        
        def __repr__(self):
            return self.file
        
        def __eq__(self, other):            
            return self.index == other.index
    
    class Image:
        def __init__(self, height , width, name, image = "" ):
            self.name = name
            self.image = image
            self.height = height
            self.width = width
            
    
    
    
    
    

parser = argparse.ArgumentParser()
parser.add_argument("--song")
#parser.add_argument("--dir", required="--song" in sys.argv)

args = parser.parse_args()
if args.song:
    app = App(args.song)
    
else:
    app = App()
    
app.main()


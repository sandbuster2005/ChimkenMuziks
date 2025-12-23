#!/bin/python
#made by sand
import argparse
import sys
from mimetypes import inited


class App:
    def __init__( self, directory = "" , song = ""):
        self.init_param()
        self.init_main( directory , song)
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



    from libs.handmade._external import external_call, external_return
    from libs.handmade._display import init_display, out, ask, ask_list, show_list, change_confirmation
    from libs.handmade._sound import init_sound, start_sound, change_sound_manager, get_volume, set_volume, deafen
    from libs.handmade._batterie import init_battery, battery_check, get_battery, get_battery_life
    from libs.handmade._command import init_command, sort_command, edit_command, help_menu      
    from libs.handmade._param import init_param, get_param, write_param, reset
    from libs.handmade._files import init_file, get_file, select_dir, switch_dir, find_file, check_adress, change_main_path, mani_file, get_words, change_extension, edit_dirs
    from libs.handmade._image import init_image ,get_img, display_img, select_img, load_script, screen_mode
    from libs.handmade._download import init_download, yt_search, dl_yt_playlist  
    from libs.handmade._song import init_song, _choose_song, load_songs, play_song, play_last, historic, select, _play, play_midi, convert_midi, default_midi, get_metadata
    from libs.handmade._main import init_main, main, get_input, load_all, wind, display, set_timer, param_center, clear_cache, n_input, reset_settings
    from libs.handmade._printimage import print_image_to_screen, init_printer
    from libs.handmade._data import init_data, write_song_database, create_song_database, update_song_database, get_index_data, update_favorite_database, load_favorite_database, add_song_database, add_column, drop_column, get_column, load_playlist_database, is_in_playlist, update_playlist_database, get_albums, get_artists, load_album_database, load_artist_database, get_song_database,find_song_database
    from libs.handmade._playlist import init_playlist, playlist_manager , add_to_playlist, get_song_info, load_playlist
    from libs.handmade._update import init_update , is_finished , update_logic , update_display,end
    import libs.colorama.__init__ as colorama
    colorama.init()

parser = argparse.ArgumentParser()
parser.add_argument('-s', "--song")
parser.add_argument("--dir", required="--song" in sys.argv)

args = parser.parse_args()
if args.dir:
    app = App(args.dir,args.song)
    
else:
    app = App()
    
app.main()


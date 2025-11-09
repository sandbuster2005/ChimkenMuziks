#!/bin/python
#made by sand
import argparse
import sys
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
        
    from libs.handmade._external import external_call,external_return
    from libs.handmade._display import init_display,out,ask,ask_list,show_list,change_confirmation
    from libs.handmade._sound import init_sound,start_sound,change_sound_manager,get_volume,set_volume,deafen
    from libs.handmade._batterie import init_battery,battery_check,get_battery,get_battery_life
    from libs.handmade._command import init_command,sort_command,edit_command,help_menu      
    from libs.handmade._param import init_param,get_param,write_param,reset
    from libs.handmade._files import init_file,get_file,select_dir,switch_dir,find_file,check_adress,change_main_path,mani_file,get_words,change_extension,edit_dirs,check_favorite
    from libs.handmade._image import init_image,get_img,display_img,select_img,load_script,screen_mode
    from libs.handmade._download import init_download,yt_search,dl_yt_playlist  
    from libs.handmade._song import init_song,choose_song,load_songs,play_song,play_last,historic,select,play,play_midi,convert_midi,default_midi,get_metadata
    from libs.handmade._main import init_main,main,update,get_input,load_all,wind,display,set_timer,param_center,clear_cache,u_bar,n_input
    from libs.handmade._printimage import print_image_to_screen, init_printer
    from libs.handmade._data import init_data,write_song_database,create_song_database,update_song_database,get_index_data,update_favorite_database,load_favorite_database,add_song_database,add_column,drop_column,get_column,load_playlist_database,is_in_playlist,update_playlist_database,get_albums,get_artists,load_album_database,load_artist_database,get_song_database
    from libs.handmade._playlist import init_playlist, playlist_manager , add_to_playlist, get_song_info,load_playlist
    import libs.colorama.__init__ as colorama
    colorama.init()

    def suspend( self, fonction):
        """
        cette fonction met en pause l'affichage le temps que la fonction
        fonction s'execute
        """
        self.search = 1
        getattr( self, fonction )()
        self.search = 0

    #les fonctions sont relié a self.commands
    def q_f( self ):
        self.stay = False


    def r_f( self ):
        self.select()


    def g_f( self ):
        self.suspend( "change_sound_manager" )


    def i_f( self ):
        self.search = True
        self.historic()
        self.get_input()

    def j_f( self ):
        self.suspend( "select_img" )


    def n_f( self ):
        self.suspend("play_song")

    def e_f( self ):
        self.change_confirmation()
        
    def f_f( self ):
        self.suspend( "set_timer" )

    def plus_f( self ):
        self.wind( 1 )


    def minus_f( self ):
        self.wind( 2 )


    def p_f( self ):
        self.wind( 3 )


    def m_f( self ):
        self.wind( 4 )


    def d_f( self ):
        self.wind( 5 )
      
    def bb_f( self ):
        self.wind( 15 )
        
    def t_f( self ):
        self.suspend("screen_mode")
     
     
    def o_f( self ):
        self.suspend("default_midi")


    def s_f( self ):
        self.suspend( "param_center" )
        self.suspend( "display" )

    def a_f( self ):
        self.load_all()


    def c_f( self ):
        self.suspend( "edit_dirs")
        self.load_songs()


    def b_f( self ):
        self.suspend("play_last")


    def dl_f( self ):
        self.suspend("yt_search")


    def l_f( self ):
        self.suspend( "display" )


    def u_f( self ):
        self.write_param( )


    def v_f( self ):
        self.suspend( "edit_command" )


    def w_f( self ):
        self.search = True
        a = input(" are you sure you want to reset your setting ? (o/n)")
        if a == "o" or a=="1" or a=="y":
            self.reset()
        self.search = False


    def x_f( self ):
        self.suspend("dl_yt_playlist")
        self.pause = True


    def y_f( self ):
        self.suspend("change_main_path")


    def z_f( self ):
        self.suspend( "mani_file" )
     

    def k_f( self ):
        self.clear_cache()
        
    def h_f( self ):
        self.search = True
        self.show_list( self.help_menu(), num=False )
        self.get_input()
    
    def pl_f( self ):
        self.suspend("playlist_manager")
    
    def add_f( self ):
        self.suspend("add_to_playlist")
parser = argparse.ArgumentParser()
parser.add_argument('-s', "--song")
parser.add_argument("--dir", required="--song" in sys.argv)



args = parser.parse_args()
if args.dir:
    app = App(args.dir,args.song)
else:
    app = App()
app.main()


#!/bin/python
#made by sand
class App:
    def __init__( self ):
        self.init_main()
        self.init_sound()
        self.init_battery()
        self.init_command()
        self.init_file()
        self.init_image()
        self.init_download()
        self.init_song()
        self.init_display()
        self.init_param()
        #self.init_letter()
    from libs.handmade._external import external_call,external_return
    from libs.handmade._display import init_display,out,ask,ask_list,show_list,change_confirmation
    from libs.handmade._sound import init_sound,start_sound,change_sound_manager,get_volume,set_volume,deafen
    from libs.handmade._batterie import init_battery,battery_check,get_battery,get_battery_life
    from libs.handmade._command import init_command,sort_command,edit_command,help_menu      
    from libs.handmade._param import init_param,get_param,write_param,reset
    from libs.handmade._files import init_file,get_file,select_dir,switch_dir,find_file,check_adress,change_main_path,mani_file,get_words,change_extension
    from libs.handmade._image import init_image,get_img,display_img,select_img,load_script,screen_mode
    from libs.handmade._download import init_download,yt_search,dl_yt_playlist  
    from libs.handmade._song import init_song,choose_song,load_songs,play_song,play_last,historic,select,play,play_midi,convert_midi,default_midi,get_metadata
    from libs.handmade._main import init_main,main,update,get_input,load_all,wind,display,set_timer,param_center,clear_cache,u_bar,n_input
    #from libs.handmade._letter import init_letter,suspend,a_f,b_f,c_f,d_f,e_f,f_f,g_f,h_f,i_f,j_f,k_f,l_f,m_f,n_f,o_f,p_f,q_f,r_f,s_f,t_f,u_f,v_f,w_f,x_f,y_f,z_f,plus_f,minus_f,dl_f,bb_f
    def suspend( self, fonction ):
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
        self.play_song()

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
        self.suspend( "select_dir" )
        self.load_songs()


    def b_f( self ):
        self.play_last()


    def dl_f( self ):
        self.suspend("yt_search")


    def l_f( self ):
        self.suspend( "display" )


    def u_f( self ):
        self.write_param( )


    def v_f( self ):
        self.suspend( "edit_command" )


    def w_f( self ):
        self.reset()


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



app = App()
app.main()


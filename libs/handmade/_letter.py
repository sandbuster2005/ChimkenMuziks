#made by sand


def init_letter( self ):
    pass

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
    self.suspend( "historic" )


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
    self.change_main_path()


def z_f( self ):
    self.suspend( "mani_file" )
 

def k_f( self ):
    self.clear_cache()
    
def h_f( self ):
    self.show_list( self.help_menu(), num=False )


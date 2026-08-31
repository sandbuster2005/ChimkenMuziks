from .utils import *
from .terminal import *
from tinytag import TinyTag

@export
def init_playlist(self):
    pass

@export
def add_to_playlist(self):
    if self.song in self.favorite:
        fav = "remove from favorite"
        
    else:
        fav = "add to favorite"
    
    tooltip = [ fav ]
    
    if self.get_column():
        tooltip.append("add to playlist")
        
    word = self.asker.menu_deroulant( tooltip,self.update_logic )
        
    if word < len( tooltip ):
        if word == 0:
             if not self.song in self.favorite:
                self.favorite.append( self.song )
                self.update_favorite_database(1)
                
             else:
                self.favorite.remove( self.song )
                self.update_favorite_database(0)
            
        elif word == 1:
            white()
            playlists = self.get_column()
            tooltip = []
            value = []
            
            for x in playlists:
                value.append(1 - self.is_in_playlist(x) )
                tooltip.append( f": { 'not'* value[-1] } in {x}")
                    
            new = self.asker.menu_deroulant( tooltip,self.update_logic , search = True )
            
            if new < len( playlists ):
                self.update_playlist_database(playlists[  new ], value[ new  ] )

    self.display()

@export
def gen_playlist_menu(self):
    playlists = self.get_column()
    
    sub_menu_select = {
    "show" : [ self.show_playlist , {1 : "ptype" , 2 : "playlist" } ] ,
    "select" : [ self.load_new_playlist, { 1 : "ptype" , 2 : "playlist" } ]
    }


    menu = {
      "return to file mode": self.clear_playlist,
      "select playlist":
      {
          "album" :
          { album : sub_menu_select for album in self.get_albums() },
          
          "artist" :
          { artist : sub_menu_select for artist in self.get_artists() },
          
          "playlist" :
          { playlist : sub_menu_select for playlist in playlists }
          
      },
      "manage playlist":
      {
          "create playlist": self.add_new_playlist,
          
          "remove playlist":
          { playlist : [  self.remove_playlist , { 2 : "playlist" } ] for playlist in playlists },
          
          "add song to playlist":
          { playlist : [ self.edit_playlist, { 2 : "playlist" } ] for playlist in playlists },

          "export playlist":
          { playlist : [ "self.export_playlist", { 2 : "playlist" } ] for playlist in playlists }
       }

            }
    
    return menu

@export
def playlist_manager(self):
        
    self.asker.dynamic_recursive_menu(self.gen_playlist_menu, self.update_logic , text = "test" )
    
    self.display()
    

@export
def edit_playlist(self,playlist):
    indexes = { song.index : self.is_in_playlist(playlist, song.file ) for song in self.files }
    files = [ song for song in self.files ]
    res = 0
    
    while res < len(self.files):
        menu = [ f"\x1b[38;2;0;255;0m{ str( song.index ) }: *{ song.filename }*\033[0m"  if indexes[ song.index ] else f"{ str( song.index ) }: { song.filename }" for song in self.files ]
        res = self.asker.menu_deroulant(menu , self.update_logic, search = True, cursor = res )
        
        if res < len(self.files):
            song = files[ res ]
            indexes[ song.index ] = 1 - indexes[ song.index ]
            self.update_playlist_database( playlist , indexes[ song.index ], song.file )

@export
def show_playlist(self, playlist ,ptype):
    if ptype != "playlist":
        input("not yet supported press any key to continue")
        return 2
    
    self._select_song(self.get_playlist(playlist) ,text = playlist , play_next = True )
    return 2

@export
def add_new_playlist(self):
    white()
    word = self.ask( "new playlist name:" )

    if word.lower() not in ( self.get_column() + ["id_song","nom","played","favorite",""]   ):
        self.add_column( word.lower() )
    
    return 2

@export
def clear_playlist(self):
    self.playlist = ""
    return 1

@export
def load_new_playlist(self,playlist, ptype):
    self.playlist = playlist
    self.playlist_type = ptype
    self.load_playlist()
    self.song = None
    self.play_song()
    return 1
    
@export
def remove_playlist(self, playlist):
    self.drop_column( playlist )
    return 2



@export
def get_song_info(self,song):
    try:
        tag = TinyTag.get(song , image = True)
        
    except:
        return [ None , None ]
    
    else:
        return [tag.artist , tag.album]

@export
def load_playlist(self):
    if self.playlist_type == "playlist":
        self.load_playlist_database()
        
    if self.playlist_type == "album":
        self.load_album_database()
        
    if self.playlist_type == "artist":
        self.load_artist_database()
    
    

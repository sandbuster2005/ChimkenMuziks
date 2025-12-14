from .utils import *
from libs.tinytag import TinyTag
def init_playlist(self):
    pass


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
            
            
def playlist_manager(self):
    word = self.asker.menu_deroulant( ["select playlist","add playlist","remove playlist","return to file mode"], self.update_logic)
    
    if  word < 4:
        playlists = self.get_column()
        
        if word == 3:
            self.playlist = ""
        
        elif word == 1:
            white(4)
            word = self.ask( "new playlist name:" )
            
            if word.lower() not in ( playlists + ["id_song","nom","played","favorite",""]   ):
                self.add_column( word.lower() )
                
        elif word == 0:
            albums = self.get_albums()
            albums = remove_list ( [ x.split("/") for x in albums] )
            albums = [ x  for y,x in enumerate( albums )  if x not in albums[:y] ]

            artists = self.get_artists()
            artists = remove_list ( [ x.split("/") for x in artists ] )
            artists = [ x  for y,x in enumerate( artists)  if x not in artists[:y] ]
            
            self.tooltips = []
            
            if playlists or albums or artists:
                white()
                new = self.asker.menu_deroulant(["playlist","album","artist"],self.update_logic)
                
                if new < 3:
                    
                    if new == 0 and playlists:
                        res = self.asker.menu_deroulant( playlists,self.update_logic,search = True )
                        white()
                        if res < len(playlists):
                            self.playlist = playlists[  res ]
                            self.playlist_type = "playlist"
                            self.load_playlist()
                            self.song = None
                            self.play_song()
                    
                    elif new == 1 and albums:
                        res = self.asker.menu_deroulant( albums ,self.update_logic , search = True)
                        white()
                        if res < len( albums ):
                            self.playlist = albums[  res ]
                            self.playlist_type = "album"
                            self.load_playlist()
                            self.song = None
                            self.play_song()
                        
                    elif new == 2 and artists:
                        res = self.asker.menu_deroulant( artists,self.update_logic,search = True )
                        white()
                        if res < len( artists ):
                            self.playlist = artists[  res  ]
                            self.playlist_type = "artist"
                            self.load_playlist()
                            self.song = None
                            self.play_song()
       
        elif word == 2:
            white()
            new = self.asker.menu_deroulant( playlists,self.update_logic , search = True )
            
            if new < len( playlists ):
                 if self.playlist!= playlists [ new ]:
                    self.drop_column( playlists[ new ] )
                
            else:
                print("no playlist")
                input("press any key to continue")
            
        
    self.display()
                
def get_song_info(self,song):
    try:
        tag = TinyTag.get(song , image = True)
        
    except:
        return [ None , None ]
    
    else:
        return [tag.artist , tag.album]

def load_playlist(self):
    if self.playlist_type == "playlist":
        self.load_playlist_database()
        
    if self.playlist_type == "album":
        self.load_album_database()
        
    if self.playlist_type == "artist":
        self.load_artist_database()
    
    

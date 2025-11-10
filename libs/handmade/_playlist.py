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
        
    word = self.ask_list( tooltip )
        
    if all_numbers( word, len( tooltip ), 1 ):
        if int( word ) == 0:
             if not self.song in self.favorite:
                self.favorite.append( self.song )
                self.update_favorite_database(1)
                
             else:
                self.favorite.remove( self.song )
                self.update_favorite_database(0)
            
        elif int( word ) == 1:
            white()
            playlists = self.get_column()
            tooltip = []
            value = []
            
            for x in playlists:
                value.append(1 - self.is_in_playlist(x) )
                tooltip.append( f": { 'not'* value[-1] } in {x}")
                    
            new = self.ask_list( tooltip )
            
            if all_numbers(new, len( playlists ), 1):
                self.update_playlist_database(playlists[ int( new ) ], value[ int( new ) ] )
                
    self.display()
            
            
def playlist_manager(self):
    word = self.ask_list( ["select playlist"," add playlist","remove playlist","return to file mode"])
    
    if all_numbers( word, 4 ,1):
        playlists = self.get_column()
        
        if word == "3":
            self.playlist = ""
        
        elif word == "1":
            white(4)
            word = self.ask( "new playlist name:" )
            
            if word.lower() not in ( playlists + ["id_song","nom","played","favorite",""]   ):
                self.add_column( word.lower() )
                
        elif word =="0":
            albums = self.get_albums()
            albums = remove_list ( [ x.split("/") for x in albums] )
            
            artists = self.get_artists()
            artists = remove_list ( [ x.split("/") for x in artists ] )
            
            self.tooltips = []
            
            if playlists or albums or artists:
                white()
                new = self.ask_list(["playlist","album","artist"])
                
                if all_numbers(new , 3 , 1):
                    
                    if new == "0" and playlists:
                        res = self.ask_list( playlists )
                        white()
                        if all_numbers(res , len(playlists) , 1):
                            self.playlist = playlists[ int( res ) ]
                            self.playlist_type = "playlist"
                            self.load_playlist()
                            self.song = None
                            self.n_f()
                    
                    elif new == "1" and albums:
                        res = self.ask_list( albums )
                        white()
                        if all_numbers(res , len( albums ) , 1):
                            self.playlist = albums[ int( res ) ]
                            self.playlist_type = "album"
                            self.load_playlist()
                            self.song = None
                            self.n_f()
                        
                    elif new == "2" and artists:
                        res = self.ask_list( artists )
                        white()
                        if all_numbers(res , len( artists ) , 1):
                            self.playlist = artists[ int( res ) ]
                            self.playlist_type = "artist"
                            self.load_playlist()
                            self.song = None
                            self.n_f()
       
        elif word =="1":
            white()
            new = self.ask_list( playlists )
            
            if all_numbers(new , len( playlists ) , 1):
                 if self.playlist!= playlist [ int( new ) ]:
                    self.drop_column( playlists[ int( new ) ] )
                
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
    
    

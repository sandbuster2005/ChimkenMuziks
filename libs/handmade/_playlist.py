from .utils import *
from tinytag import TinyTag
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
    playlists = self.get_column()
    match self.asker.menu_deroulant( ["select playlist","add playlist","remove playlist","return to file mode","add to playlist","show playlist"], self.update_logic) :
        
        
        case 0:
            
            albums = self.get_albums()
            artists = self.get_artists()
            
            albums = remove_list ( [ x.split("/") for x in albums] )
            artists = remove_list ( [ x.split("/") for x in artists ] )
            
            if not type(albums) == list:
                albums = [ albums ]
            if not type(artists) == list:
                artists = [ artists ]
            
            albums = [ x  for y,x in enumerate( albums )  if x not in albums[:y] ]
            artists = [ x  for y,x in enumerate( artists )  if x not in artists[:y] ]
            
            total = [ playlists, albums, artists, [ ] ]
            tooltip = ["playlist","album","artist"]
            
            white()
            choice = self.asker.menu_deroulant( tooltip ,self.update_logic)
            
            if total[ choice ]:
                white()
                res = self.asker.menu_deroulant( total[choice], self.update_logic, search = True )
            
                if res < len( total[choice] ):
                    self.playlist = total[choice][  res ]
                    self.playlist_type = tooltip[choice]
                    self.load_playlist()
                    self.song = None
                    self.play_song()

            
        case 1:
            white(4)
            word = self.ask( "new playlist name:" )
        
            if word.lower() not in ( playlists + ["id_song","nom","played","favorite",""]   ):
                self.add_column( word.lower() )
                
                     
        case 2:
            white()
            word = self.asker.menu_deroulant( playlists,self.update_logic , search = True )
        
            if word < len( playlists ):
                 if self.playlist != playlists[ word ] :
                    self.drop_column( playlists[ word ] )

            else:
                print("no playlist")
                input("press any key to continue")
                      
    
    
        case 3:
            self.playlist = ""
            
            
            
        case 4:
            playlist = self.asker.menu_deroulant(playlists, self.update_logic, search = True )
            
            indexes = { song.index : self.is_in_playlist(playlists[playlist], song.file ) for song in self.files }
            files = [ song for song in self.files ]
            res = 0
            
            while res < len(self.files):
                menu = [ f"{ str( song.index ) }: *{ song.filename }*"  if indexes[ song.index ] else f"{ str( song.index ) }: { song.filename }" for song in self.files ]
                res = self.asker.menu_deroulant(menu , self.update_logic, search = True, cursor = res )
                
                if res < len(self.files):
                    song = files[ res ]
                    indexes[ song.index ] = 1 - indexes[ song.index ]
                    self.update_playlist_database( playlists[playlist] , indexes[ song.index ], song.file )
                    
                    
                        
        case 5:
            playlist = self.asker.menu_deroulant(playlists, self.update_logic, search = True )
            files = [ song for song in self.files if self.is_in_playlist(playlists[playlist], song.file ) ]
            self._select_song(files ,text = playlists[playlist] , play_next = True )
    
 
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
    
    

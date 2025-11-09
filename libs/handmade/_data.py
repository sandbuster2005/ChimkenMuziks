import sqlite3
from .utils import *

def init_data(self):
    pass

def write_song_database(self,song):
    self.create_song_database()
    base =  sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    requete = """
    UPDATE song
    SET played = played +1
    WHERE nom = ?
    """
    cursor.execute(requete,[ song ])
    base.commit()
    base.close()

def create_song_database(self):
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    requete = """
    create table if not exists song(
    id_song INTEGER UNIQUE NOT NULL,
    nom TEXT UNIQUE NOT NULL ,
    played INTEGER NOT NULL,
    favorite INTEGER NOT NULL,
    artist TEXT ,
    album TEXT,
    PRIMARY KEY(id_song AUTOINCREMENT)
    )
    """
    cursor.execute(requete)
    base.commit()
    base.close()

def add_song_database(self, song):
    self.create_song_database()
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    s = clear_adjacent(song,["/"],2)
    s= "//".join( s.rsplit("/",1) )
    cursor.execute( ' INSERT OR IGNORE INTO song (nom,played,favorite) VALUES (?,"0","0")',[s])        
    base.commit()
    cursor.execute( " SELECT id_song,nom FROM song WHERE nom = ?", [s])
    result = cursor.fetchall()
    return [result[ 0 ][0],result[ 0 ][1]]

def update_song_database(self):
    self.create_song_database()
    base = sqlite3.connect("appdata/cache/data.db")
    
    cursor = base.cursor()
    
    if self.exterior:
        for x in self.get_file( self.exterior, [] ):
            cursor.execute( ' INSERT OR IGNORE INTO song (nom,played,favorite,artist,album) VALUES (?,"0","0",?,?)',[ x, artist, album ])
    else:
        for x in self.get_file( self.path_to_file, [] ):
            artist,album = self.get_song_info(x)
            cursor.execute( ' INSERT OR IGNORE INTO song (nom,played,favorite,artist,album) VALUES (?,"0","0",?,?)',[ x, artist, album ])
        
    base.commit()
    base.close()
    
def update_favorite_database(self,mode):
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    cursor.execute( "UPDATE song SET favorite = ? where nom = ?",[ mode, self.song[ 1 ] ] )
    base.commit()
    base.close()
    
def load_favorite_database(self):
    self.create_song_database()
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    cursor.execute( " SELECT id_song,nom FROM song WHERE favorite = '1'")
    result = cursor.fetchall()
    self.favorite = [  [ x[0],x[1] ] for x in result ]
    base.commit()
    base.close()
    
def get_index_data(self,nom):
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    result = []
    for x in nom:
        cursor.execute("SELECT id_song FROM song WHERE nom = ?" ,[x])
        result.append(cursor.fetchone()[0])
    return result

def add_column(self,column):
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    cursor.execute(f"ALTER TABLE song ADD COLUMN {column} INTEGER")
    base.commit()
    base.close()
    
def drop_column(self,column):
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    cursor.execute(f"ALTER TABLE song DROP COLUMN {column} ")
    base.commit()
    base.close()

def load_playlist_database(self):
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    cursor.execute(f" SELECT id_song,nom FROM song WHERE {self.playlist} = '1' ")
    result = cursor.fetchall()
    base.commit()
    base.close()
    self.playlist_files =  [  [ x[0],x[1] ] for x in result ]

def update_playlist_database(self, playlist, value):
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    cursor.execute( f"UPDATE song SET {playlist} = ? where nom = ?",[ value, self.song[ 1 ] ] )
    base.commit()
    base.close()

def is_in_playlist(self,playlist):
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    cursor.execute(f" select {playlist} FROM song where nom = ? ",[ self.song[ 1 ] ] )
    result =  cursor.fetchone()[0]
    base.commit()
    base.close()
    if result == 1:
        return 1
    
    else:
        return 0
    
def get_column(self):
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    cursor.execute("select name from pragma_table_info('song') as tblInfo")
    result = cursor.fetchall()
    base.commit()
    base.close()
    return [ x[0]for x in result ][6:]

def get_albums(self):
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    cursor.execute("SELECT DISTINCT album FROM song WHERE album IS NOT NULL")
    result =  cursor.fetchall()
    base.commit()
    base.close()
    return [ x[0] for x in result]

def load_album_database(self):
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    cursor.execute("SELECT id_song,nom FROM song WHERE album = ?",[self.playlist])
    result =  cursor.fetchall()
    base.commit()
    base.close()
    self.playlist_files = [  [ x[0],x[1] ] for x in result ]


def get_artists(self):
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    cursor.execute("SELECT DISTINCT artist FROM song WHERE artist IS NOT NULL")
    result = cursor.fetchall()
    base.commit()
    base.close()
    return [ x[0] for x in result]

def load_artist_database(self):
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    cursor.execute("SELECT id_song,nom FROM song WHERE artist = ?",[self.playlist])
    result =  cursor.fetchall()
    base.commit()
    base.close()
    self.playlist_files =  [  [ x[0],x[1] ] for x in result ]
import sqlite3

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
    PRIMARY KEY(id_song AUTOINCREMENT)
    )
    """
    cursor.execute(requete)
    base.commit()
    base.close()
    

def update_song_database(self):
    self.create_song_database()
    base = sqlite3.connect("appdata/cache/data.db")
    cursor = base.cursor()
    
    for x in self.get_file( self.path_to_file, [] ):
        print(x)
        cursor.execute( ' INSERT OR IGNORE INTO song (nom,played) VALUES (?,"0")',[x])
        
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
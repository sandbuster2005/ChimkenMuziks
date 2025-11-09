#made by sand
from os import listdir
from os.path import isdir,isfile
from .ffiles import *
from .ffiles import get_file as getfile
from .utils import *
from .terminal import up,wipe,out
from ..readchar import readchar
import re

def init_file( self ):
    self.files = []# chanson chargé
        
def get_file( self, path, files = [] ):
    """
    cette fonction permet de récuperer tout les fichier waw,mp3 et m4a dans un dossier et sous dossiers,
    elle remet aussi a 0 l'historique ,stop toute chanson en cours de lecture et ajoute a la liste des dossiers
    le dossiers et les sous dossiers si il n'y sont pas
    
    limite:
    path est un chemin d'accés auquel l'utilisateur peut accéder
    files est une liste qui peut contenir des chemin d'accés auquel l'utilisateur peut accéder au préalable
    renvoie les ficher déja inclus et ceux du dossier scanné
    """

    self.song = None
    self.played = []
    self.player.stop()
    
    for f in listdir( path ):
        if isdir( path + f ):
            
            if [ path + f, '1' ] in self.dirs:# le dossier est activé
                files += self.get_file( path + f + self.separator, [] )
            
            elif [ path + f, '0' ] in self.dirs:# le dossier est desactivé 
                continue
            
            else:# le dossier n'est pas repertorié
                files += self.get_file( path + f + self.separator, [] )
                self.dirs.append( [ path + f, '1' ] )
                
        if f[ -4: ] == ".mp3"  or f[ -4: ] == ".m4a" or f[ -4: ] == ".wav" or f[ -5: ] == ".flac" or f[ -4: ] == ".mid" or f[ -4: ] == ".ogg":#le fichier est un audio
            files.append( path + self.separator + f )
            
    return sorted( files ,key = lambda x: x.rsplit( self.separator, 1 )[ 1 ].lower() )


def edit_dirs(self):
    """
    cette fonction permet a l'utilisateur d'activer/desactiver des dossiers
    en suivant l'architecture de dossier en partant de la racine
    """
    self.select_dir( self.switch_dir )

def select_dir( self ,func =print , lim = -1 , retour = 0):
    """
    cette fonction permet d'activer/desactiver des dossiers de la liste de dossier sous dossier
    pour oculter les chanson qu'il contient
    
    limite:
    demande une valeur numérique a l'utilisateur pour selectionner un dossier/sous dossiers
    """
    count = 0
    mode = "standard"
    base = self.path_to_file.count( self.separator )
    bottom = 0
    select = []
    
    for x in self.dirs:
        print( x )
        if self.path_to_file in x[ 0 ]:
            bottom = max( bottom ,x[ 0 ].count( self.separator ) - base )
            select.append( [ x[ 0 ].count( self.separator ) - base ,x[ 0 ],x[ 1 ] ] )
            
        else:
            pass
        
    choose = []
    for y in range(bottom + 1):
        choose.append( [ [ x[ 1 ],x[ 2 ] ] for x in select if x[ 0 ] == y ] )
        
    folder = self.path_to_file + ""
    pos = 0
    word = "0"
    temp = choose[ 0 ]
    while word and count != lim :
        white()
        print(f"mode : { str( mode ) }")
        print("   " + folder.split( self.path_to_file )[ 1 ] )
        
        for x in range( len( temp ) ):
            print( str(x) + ":", temp[x][0].split(folder,1)[1] ,int(temp[x][1]) * "  on" + (1 - int(temp[x][1])) * "off" )
            
        print("(b) to go back")
        print("(s) switch mode")
        
        if len( temp )< 11:
            out("select folder")
            word = readchar()
        
        else:
            word = input( "select folder " )
        
        if all_numbers( word, len( temp ), 1 ):
            if mode == "switch":
                if temp[ int( word ) ][ 1 ] == "1":
                        
                        if retour:
                            return self.dirs.index( [ temp[ int( word ) ][ 0 ], "1" ] )
                        
                        else:
                            temp[ int( word ) ][ 1 ] = "0"
                            func( self.dirs.index( [ temp[ int( word ) ][ 0 ], "1" ] ) )
                            count += 1
                        
                else:
                        
                        if retour:
                            return self.dirs.index([ temp[ int( word ) ][ 0 ], "0" ])
                        
                        else:
                            temp[ int( word ) ][ 1 ] = "1"
                            func( self.dirs.index( [ temp[ int( word ) ][ 0 ], "0" ] ) )
                            count += 1    
            
            if mode == "standard":
                wipe()
                print( int( word ), temp[ int( word ) ][ 0 ].split( folder, 1 )[ 1 ] )
                print("")
                print("1: select folder")
                print("2: enter folder ")
                out("select option")
                nword = readchar()
                
                if "1" in nword :
                    
                    if temp[ int( word ) ][ 1 ] == "1":
                        
                        if retour:
                            return self.dirs.index( [ temp[ int( word ) ][ 0 ], "1" ])
                        
                        else:
                            temp[int(word)][1] = "0"
                            func( self.dirs.index( [ temp[ int( word ) ][ 0 ], "1" ] ) )
                            count += 1
                        
                    else:
                        
                        if retour:
                            return self.dirs.index( [temp[ int( word ) ][ 0 ], "0" ] )
                        
                        else:
                            temp[ int( word) ][ 1 ] = "1"
                            func( self.dirs.index( [ temp[ int( word ) ][ 0 ], "0" ]) )
                            count += 1
                
                elif "2" in nword:
                    if pos != bottom:
                        pos += 1
                        folder = temp[ int( word ) ][ 0 ] + self.separator
                        temp = [ x for x in choose[ pos ] if folder in x[ 0 ] ]
                
            
        elif "s" in word:
            if mode != "switch":
                mode = "switch"
            
            else:
                mode = "standard"
        
        elif "b" in word :
            
            if pos!=0:
                folder = folder.rsplit( self.separator, 2 )[ 0 ] + self.separator
                pos -= 1
                temp = [ x for x in choose [pos ] if folder in x[ 0 ] ]
            
            else:
                word = ""
                print("")
        
        else:
            word = ""
            print("")

def switch_dir( self, word ):
    """
    cette fonction permet d'activer ou desactiver un dossier de la liste
    """
    self.dirs[ word ][ 1 ] = str( 1 - int( self.dirs[ word ][ 1 ] ) )
  
  
def find_file( self, word ):
    """
    cette fonction renvoie une liste contentant toute les chaine de charactères de la liste de chanson chargés
    contenant une chaine de charactère word
    
    limite:
    toute les charactère sont considérée comme minuscule
    """
    files = [ [ self.files[ x ][ 1 ].rsplit( self.separator )[ -1 ], x ] for x in range(len(self.files)) if word.lower() in self.files[ x ][ 1 ].lower().rsplit( self.separator, 1 )[ -1 ] ]#cherche dans la liste de son en ignorant les majuscules      
    
    if len(files) < 10 and len(word) > 3:
        for y in range( len( word ) ):
            for i,x in enumerate( self.files ):
                if [x[1].rsplit( self.separator )[ -1 ], i ] not in files:
                    if re.search( "".join( [x * ( i != y ) + "."*( i == y ) for i,x in enumerate( word ) ] ), x[ 1 ].lower() ):
                        files.append( [ x [1] .rsplit( self.separator )[ -1 ], i ] )
    
    return sorted(files,key = lambda x: x[1] )

def check_adress( self ):
    """
    cette fonction permet de verifier si l'adresse existe et est un dossier
    """
    if not isdir( self.path_to_file ) or self.path_to_file == "":
        while not isdir( self.path_to_file ):
            
            try:
                self.path_to_file = str( self.external_return( [ "xplr" ], ) )[ 2:-3 ] + self.separator
            
            except:
                self.path_to_file = input( "chemin du dossier musique: " )
                
                if self.path_to_file[-1] != self.separator:
                    self.path_to_file += self.separator
    
    self.write_param()
    
    
def change_main_path( self ):
    """
    cette fonction permet de changer l'adresse des chansons
    """
    self.path_to_file = ""
    self.check_adress()
    self.load_songs()
     
     
def mani_file(self):
    """
    cette fonction permet de supprimer , deplacer(dans les dossiers connu)
    et renommer le fichier actuel
    """
    if self.song != None:
        index = self.files.index( self.song )
        
        tooltip = [ "delete ", "move", "rename", "convert"]
        
        if self.get_column():
            tooltip.append("add to playlist")
        
        word = self.ask_list( tooltip )
        
        if all_numbers( word, len( tooltip ), 1 ):
            
            if int( word ) == 0:
                choice = self.ask( "are you sure (y/n)" )
                
                if choice == "y":
                    rm_file( self.song[ 1 ] )
                    self.files.remove( self.song )
                
            elif int( word ) == 1:
                choice = str( self.select_dir( retour = 1 ) )
                
                if all_numbers( choice, len( self.dirs ), mode = 1 ):
                    mv_file( self.song[ 1 ], self.dirs[ int( choice ) ][ 0 ] + self.separator + self.song.rsplit( self.separator, 1 )[ 1 ] )
                    self.files[index] = self.dirs[ int( choice ) ][ 0 ] + self.separator + self.song.rsplit( self.separator, 1 )[ 1 ]

            elif int( word ) == 2:
                choice = self.ask( "new_name :" )
                mv_file( self.song[ 1 ], self.song.rsplit( self.separator,1 )[ 0 ] + choice + "." + self.song.rsplit( ".",1 )[ 1 ])
                self.files[ index ] = self.song.rsplit( self.separator,1 )[ 0 ] + choice + "." + self.song.rsplit( ".",1 )[ 1 ]
                
            elif int( word ) == 3:
                self.change_extension()
                 
            if int(word) < 4 : 
                self.song = None
                self.played = self.played[:-1]
                self.player.stop()
                print("")
            
            else:
                self.display()
        
        else:
            self.display()
            
def get_words(self):
    """
    cette fonction permet de recuperer les paroles d'un fichier .lrc et de les passer
    au lecteur
    """
    self.last_word = -1
    self.words = []
    
    if self.song != None :
        file = self.song[1].rsplit( ".", 1 )[ 0 ] + ".lrc"
        
        if isfile( file ):
            data = getfile( file )
            data = data.split("[" )
            data = data[ 1: ]
            
            for x in range( len( data ) ):
                data[ x ] = replace( data[ x ], '\n' ).split("]", 1 )
            
            new_data = []
            
            for x in range(len(data)):
                if  ":" in data[ x ][0] and  '.' in data[ x ][ 0 ] and (len(data[ x ][ 0 ] ) == 8 or len(data[ x ][ 0 ] ) == 9):
                    new_data.append( data[ x ] )
                    
            data = new_data
            
            for x in range( len( data ) ): 
                data[ x ][ 0 ] = int(data[ x ][ 0 ][ :2 ] ) * 60 + int( data[ x ][ 0 ][ 3:5 ] ) + int( data[ x ][ 0 ][ 6:8 ] ) / 100 
                
                # enlever espace au début
                if data[x][1][0] == ' ':
                    data[x][1] = data[x][1][1:]
                           
            self.words = data
            
def change_extension(self):
    """
    cette fonction permet de convertir les fichier musique a l'aide de ffmpeg
    """
    white()
    option = [".mp3", ".m4a", ".wav" , ".flac" ]
    word = self.ask_list( option )
    
    if all_numbers( word, len( option ), 1 ):
        confirm = self.ask( "delete original (y/n)?" )
        new = self.song.rsplit( ".",1 )[ 0 ] + option[ int( word ) ]
        self.external_call(f"ffmpeg -i '{self.song}' '{new}' " , shell = True)
        
        if confirm == "y":
            rm_file( self.song )

def check_favorite(self):
    self.favorite = [ x for x in self.favorite if x in self.files]
    

                
            
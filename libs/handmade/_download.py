#made by sand
from libs.youtube_search import YoutubeSearch
from .utils import *
from os import listdir, makedirs
from os.path import isdir
def init_download( self ):
    pass


def yt_search( self ):
    """
    cette fonction permert de faire une recherche sur youtube et de télécharger l'audio d'une video,
    elle propose les 10 premiers resultat
    
    limite:
    la fonction demande 2 valeur a l'utilisateur: une recherche ,une valeur numérique entre 0 et 9
    ou aucune valeur et affiche les 10 resultat obtenu de youtube
    certain charactère du titre seront supprimé pour le bon fonctionnement du programme
    """
    self.search = True
    word = self.ask("votre recherche : ")
    results = YoutubeSearch( word, max_results = 10 ).to_dict()#10 premier resultat de la recherche youtube     
    word = self.asker.menu_deroulant( [ results[ x ].get( "title" ) for x in range ( len( results ) ) ], self.update_logic)# see titles of vid
    
    if  word < 10 :
        option = ["mp3", "m4a"]# dowload format
        words = self.asker.menu_deroulant( option,self.update_logic )
        
        if words < len( option ):
            extension = option[ words ] # user choice
            title = replace( results[  word  ].get( "title" ), [ "(", "'", '"', ")", " ", ":", "|", "&","/"] , "_")#formatage pour eviter les crash
            title = clear_adjacent(title,["-","_"],2)
            title = replace(title ,["_"],"\ ")# replace _ by spaces
            link = "https://www.youtube.com" + results[ word ].get( "url_suffix" ) # video url
            print( link )
            
            if not isdir( self.path_to_file + "download/"):
                makedirs(self.path_to_file + "download/")
                
            path = replace(self.path_to_file," ","\ ")
            self.external_call( [ f"yt-dlp -x --embed-thumbnail --audio-format { extension } -o { path }download/{ title } { link } " ], shell = True )# telechargement en externe en .mp3


def dl_yt_playlist( self ):
    """
    cette fonction permet d'enregistre une chanson/ playlist de chanson  a partir de son url
    elle verifie aussi si toute les chanson on été télécharger sans probléme
    """
    playlist = self.ask( "playlist/song url:" )
    lenght = self.ask( "lenght of playlist:" )
    new_lenght = 0
    
    if all_numbers( lenght ):
        lenght = int( lenght )
        
        if not isdir( self.path_to_file + "download/"):
                makedirs(self.path_to_file + "download/")
        
        path = replace(self.path_to_file," ","\ ")
        
        for f in listdir( f"{ self.path_to_file }/download" ):#count file before
            lenght += 1
           
        self.external_call( [ f"yt-dlp -x --embed-thumbnail --audio-format mp3 -P /{ path }download/ { playlist } " ], shell = True ) # telechargement chanson / playlist en .mp3
        
        for f in listdir( f"{ self.path_to_file }/download" ):#count file after
            new_lenght += 1
        
        if new_lenght!=lenght:
            self.out( f"{ lenght-new_lenght } songs don't seem to have been downloaded" )
            







#made by sand
from libs.youtube_search import YoutubeSearch
from .utils import *
from os import listdir

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
    word = self.ask_list( [ results[ x ].get( "title" ) for x in range ( len( results ) ) ])
    
    if all_numbers( word, 10, 1 ):
        option = ["mp3", "m4a"]
        word = self.ask_list( option )
        
        if all_numbers( word, len( option ), 1 ):
            extension = option[ int( word ) ]
            title = replace( results[ int( word ) ].get( "title" ), [ "(", "'", '"', ")", " ", ":", "|", "&"] , "_")#formatage pour eviter les crash
            link = "https://www.youtube.com" + results[ int( word ) ].get( "url_suffix" )
            print( link ) 
            self.external_call( [ f"./yt-dlp -x --embed-thumbnail --audio-format { extension } -o { self.path_to_file }download/{ title } { link } " ], shell = True )# telechargement en externe en .mp3


def dl_yt_playlist( self ):
    """
    cette fonction permet d'enregistre une chanson/ playlist de chanson  a partir de son url
    elle verifie aussi si toute les chanson on été télécharger sans probléme
    """
    playlist = self.ask( "playlist/song url:" )
    lenght = self.ask("lenght of playlist:")
    new_lenght=0
    if all_numbers( lenght ):
        lenght = int( lenght )
        for f in listdir( f"{ self.path_to_file }/download" ):
            lenght += 1
            
        self.external_call( [ f"./yt-dlp -x --embed-thumbnail --audio-format mp3 -P /{ self.path_to_file }download/ { playlist } " ], shell = True ) # telechargement chanson / playlist en .mp3
        
        for f in listdir( f"{ self.path_to_file }/download" ):
            new_lenght += 1
        
        if new_lenght!=lenght:
            self.out( f"{ lenght-new_lenght } songs don't seem to have been downloaded" )
            







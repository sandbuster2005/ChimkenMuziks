===============================
ChimkenMuziks Devellopement Doc
===============================


external
========
  
 .. py:method:: external_call(self ,arg, shell = False)

  execute code in the terminal outside off python  

 :param arg: the command with it's argument to be executed 
 :type arg: str
 :param shell: whether it should be excuted in shell or not
 :type shell: bool 

 .. danger::

  shell should not be used as it is depracated and a security risk    

 .. py:method:: external_return(self, args)

 allow to execute code in the terminal and return the output

 :param args: the command with the argument that should be used
 :type args: list

--------


Command
=======
 
    .. py:method:: init_command(self)

     allow to load necessary variables for the command methods before starting

    .. py:method:: sort_command(self)

     sort command from longest to shortest and then by alphabetical

     .. tip::

      this allow to make sure there are no command overshadowing another  

  
    .. py:method:: edit_command(self)
    
     allow the user to modify the exting command for new ones

     .. tip::
    
      it check to see if command already exist and doesn't allow to modify help command
  
    .. py:method:: help_menu(self)
      
      show the user all the commands

----------

Param
=====
  
    .. py:method:: init_param(self)

       allow to load necessary variables for the param methods before starting


    .. py:method:: get_param(self)
       
     read param file and set the corresponding variable accordingly

     .. caution::
      a field should not be removed once added , it would render all previous param file obsolete

    .. py:method:: write_param(self)
      
     write the current params to file for next launch

    .. py:method:: reset(self)
     
     set all params to default value

     .. warning:: 
      it doesn't ask for confirmation and directly save them , proceed with caution

Files
=====
   
   .. py:method:: init_file(self)
	
    allow to load necessary variables for the file methods before starting

   .. py:method:: get_file(self,path,file=[])

     craw through folders and return a list of all contained music files

     :param path: the folder path from which the program should start
     :type path: str
     :param file: starting file that will be returned with the found file
     :type file: list

     .. note::
      file is used in the first place as a recursive argument and should not be modified  

   .. py:method:: edit_dirs(self)
      
    allow user to select folder to ignore in crawling

   .. py:method:: create_dirs_links(self)
    
     create dict to recognize which folder each one contains

   .. py:method:: nselect_dir(self, display_dict={} , start="")
	
	allow user to select a folder by walking through them and allow to see aditionnal information 

     :param display_dict: additionnal content to be display for each folder optionnally
     :type display_dict: dict
     :param start: allow to start from a specific folder if wanted , default to media folder root 
     :type start: str

   .. py:method:: select_dir(self, func=print ,lim=-1 , retour=0)

    allow user to select folder to enable/disable

    .. error:: 
     This Function is deprecated and should not be used

   .. py:method:: switch_dir(self,word)
	
     change the state of a folder 
	
     :param word: the index inhte list of the folder to switch
     :type word: int

   .. py:method:: find_file(self,word)

     return the list of file countaining a special string

     :param word: the string to search in all the songs name
     :type word: str

   .. py:method:: check_adress(self)

    check if media folder path countain at least one media else ask the user to change until it does

   .. py:method:: change_main_path( self )
    
    makes the user reselect media folder path and reload the songs
    
   .. py:method:: get_word( self )
    
    extract song lyrics from corresponding file 

   .. py:method:: change_extension(self,song)
    
    use ffmpeg to convert media to another format then reload the songs , also prompting the user to remove the original file 

-------

Image
=====

   .. py:method:: init_image(self)

     allow to load necessary variables for the image methods before starting

   .. py:method:: get_img(self)

     craws through the default image folder and save the files in memory

   .. py:method:: gen_img(self)
     
    chose between thumbnail if it exist or default image and launch a thread to generatr it for the current terminal size

   .. py:method:: display_img(self)
 
    chose between thumbnail if it exist or default image and directly ask to print it
   
   .. py:method:: select_img(self)
    
    allow user to chose a default picture to be used or keep it random when there are no thumbnail 

   .. py:method:: load_script(self)

    WIP : currently does nothing

   .. py:method:: screen_mode(self)

    WIP : should not be used 


-------

Download
========

   .. py:method:: init_download(self)
    
    allow to load necessary variables for the download methods before starting

   .. py:method:: yt_search(self)

    allow user to search on youtube and select from the first 10 result a media to download , then load it

   .. py:method:: dl_yt_playlist(self)

    allow user to enter a youtube link and to download song/playlist + check all have been download

    .. note::
     a thread is created while it's downloading to keep the player up and running

   .. py:method:: thread_loop(self)

     run the update logic of the player while downloading playlist

-------

Song
====

   .. py:method:: init_song(self)

    allow to load necessary variables for the download methods before starting

   .. py:method:: load_songs(self,reset=1)

    load all songs in memory including favorites ,playlist also create dirs_link and update the database

    :param reset: if the screen and player should be stopped 
    :type reset: Bool
  
    :calls:
     * :py:meth:`get_file <get_file>`
     * :py:meth:`create_dirs_links <create_dirs_links>`
     

    .. note::
     when deleting a song for exemple you should reset to avoid error from unknown file
   
   
   .. py:method:: play_song(self , choose=1)

    chose a song if necessary , loads lyrics , convert midi to playable , add song to played song and update the timer if necessary 
    
    then launch :py:meth:`_play <_play>`

    :param choose: tell the method if it should select a new song
    :type choose: Bool

   .. py:method:: _choose_song(self)

     choose a song depending on waiting list, current playlist , favorite and options 

   .. py:method:: _play(self)

     subsitute file path to converted midi path if needed , then send it to vlc to be played and ask to gen image


   .. py:method:: play_last(self)
 
     launch previous played song if there's one

   .. py:method:: historic(self)

     show user the list of played song 


   .. py:method:: _select_song(self,file_list,display_list=None,text="",play_next=False)

     allow user to select song from media list and to modify or play it 

     :param file_list: the list of song media available
     :type file_list: list
     :param display_list: the list of what should be displayed for each song
     :type display_list: list
     :param text: the text to be displayed above the display
     :type text: str
     :param play_next: should song be played directly without displaying option menu
     :type play_next: bool

   .. py:method:: select(self)
     
     allow user to select song from media list


   .. py:method:: select_fav(self)

     allow user to select song from favorite media list 

   
   .. py:method:: most_played(self)

     allow user to select song from all time played media list


   .. py:method:: play_now(self)
     
     allow user to select song from waitinglist and immediatly play it

   .. py:method:: play_midi(self)

     allow to create a mp3 file with a midi and a codec selected by the user

   .. py:method:: convert_midi(self,soundmap="",destination="appdata/cache/")

     convert song to mp3 file and save it in cache using selected codec

     :param soundmap: the codec to be used filepath
     :type soundmap: str
     :param destination: the folder where the converted file will be kept
     :type destination: str

   .. py:method:: default_midi(self)
   
    allow user to select default codec to be used with midi

   .. py:method:: get_metadata(self)

    check if there a thumbnail embedded in file and extract it if possible

------

main
====

  .. py:method:: init_main(self,directory,song)

   allow to load necessary variables for the download methods before starting

   :param directory: directory passed through at class creation
   :type directory: str
   :param song: song passed through at class creation
   :type song: str

  .. py:method:: main(self)

   start the system , initiating everything



  .. py:method:: n_input(self)

   go up one line and clear it


  .. py:method:: display(self)

   tell the update loop to update the display when possible

   :param space: if it also tell to put space
   :type space: bool


  .. py:method:: get_input(self)
  
   read the user input and execute corresponding command

  .. py:method:: load_all(self)

   launch all the loading functions

  .. py:method:: wind(self,mode,pause = False)

   execute various simple task

   :mode: 
    | 1  : forward 
    | 2  : rewind 
    | 3  : volume up 
    | 4  : volume down
    | 5  : deafen
    | 6  : pause 
    | 7  : quit
    | 15 : rewind to start

  .. py:method:: set_timer(self)

   allow user to set a timer with multiple option see [TIMER]

  .. py:method:: end_timer(self)

   execute end instruction fo timer , see [TIMER]

  .. py:method:: param_center(self)
   
   allow user to modify supported parameter

  .. py:method:: reset_settings(self)

   ask user if he want to reset setting and respond accordingly

-------

printimage
==========

  .. py:method:: init_printer(self)

   allow to load necessary variables for the printimage methods before starting

  .. py:method:: closest(colors,color)   

   depracated ans should not be used

  .. py:method:: gen_image_data(self,path,top_offset=0)

   generate unique string to be printed to show the chosen image

   :param path: path to image
   :type path: str
   :param top_offset: how many line should not be counted from terminal size
   :type top_offset: int

  .. py:method:: print_image_to_screen(self,path,top_offset=0)

   directly print chosen image to screen

   :param path: path to image
   :type path: str
   :param top_offset: how many line should not be counted from terminal size
   :type top_offset: int

   .. warning::
    this method is depracated , it should not be used 

-------

playlist
========

  .. py:method:: init_playlist(self)

   allow to load necessary variables for the playlist methods before starting

  .. py:method:: add_to_playlist(self)

   allow user to add current song to a playlist including favorites

  .. py:method:: playlist_manager(self)

   allow user to manage playlists

  .. py:method:: get_song_info(self,song)
   
   read metadata of song , return artist and album

   :param song: song to check
   :type song: str

  .. py:method:: load_playlist(self)

   load file corresponding to playlist type see [playlist]
  

-------


update
======

  .. py:function:: current_time()
   
   return time to format hour:minute

  .. py:method:: init_update(self)

   allow to load necessary variables for the update methods before starting

  .. py:method:: update_logic(self)

   the update loop for all the logic

  .. py:method:: update_display(self)

   the update loop for all the display parts

  .. py:method:: connect_to_discord(self)

   try to connect to discord with rich presence

  .. py:method:: update_discord_status(self)

   try to update rich presence with current song

  .. py:method:: pause_discord_status(self)

   try to update rich presence with current song paused 

  .. py:method:: is_finished(self)

   return state of program

  .. py:method:: end(self)

   end sequence of the program 

------

Data
====

  .. py:method:: init_data(self)

   allow to load necessary variables for the download methods before starting

  .. py:method:: write_song_database(self,song)

    add one to played count of selected song in database

   :param song: the name of the song to be updated
   :type song: str

  .. py:method:: create_song_database(self)

    create song table in database if it don't exist already

  .. py:method:: exec_sql_request(self,request)
   
    execute given request and save the change in the database
    
    :param request: request to be executed
    :type request: list
    
  .. py:method:: add_song_database(self, song)
  
    add individual song in the database and return with newly created index see [SONG]
    
    :param song: file to add to database
    :type song: str
    
  .. py:method:: update_song_database(self , file)
  
    add list of songs to the database and ask to read metadata to add album and playlist later
    
    :param file: list of songs to add to database
    :type file : list
    
  
  .. py:method:: update_song_metadata_info(self,file)
  
   get artist and album info of file , then add a request to queue to add info into database
   
   :param file: song to process
   :type file: str
   
  .. py:method:: get_song_database(self)
  
   return the list of all song's name with their corresponding artist and album
  
  
  .. py:method:: find_song_database(self,num)
  
   return song ( see [SONG] ) corresponding to index
   
   :param num: the index of song you're searching
   :type num: int
   
  .. py:method:: played_database(self)
  
   return list of all song already played ordered by most played 
   
  .. py:method:: update_favorite_database(self)
  
   change favorite state of current song in database
   
   :param mode: new favorite state
   :type mode: bool
   
  .. py:method:: load_favorite_database(self)
  
   return list of all favorite songs ( see [SONG] ) in database
   
  .. py:method:: get_index_data(self,nom)
  
   return index of song with corresponding name
   
   :param nom: the song you're searching
   :type nom: str
  
  .. py:method:: add_column(self,column)
  
   add a column to song table corresponding to a new playlist
   
   :param column: name of the new column
   :type column: str
   
  .. py:method:: drop_column(self,colum)
  
   remove a column to song table coresponding to an old playlist
   
   :param column: name of the existing column
   :type column: str
   
  .. py:method:: load_playlist_database(self)
  
   if there is a selected playlist load the corresponding songs
   
  .. py:method:: update_playlist_database(self,playlist,value,song=None)
  
   update corresponsing playlist status for selected song
   
   :param playlist: the choosen playlist 
   :type playlist: str
   :param value: the new state of the song for the playlist
   :type value: bool
   :param song: the selected song name
   :type song: str
   
  .. py:method:: is_in_playlist(self,playlist,song=None)
  
   check if selected song is in a specific playlist
   
   :param playlist: playlist to check
   :type playlist: str
   :param song: selected song
   :type song: str
   
  
  .. py:method:: get_column(self)
  
   return list of playlist names in database
   
  .. py:method:: get_album(self)
  
   return list off all album in database
  
  .. py:method:: load_album_database(self)
  
   load list of songs corresponding to current album
   
  .. py:method:: get_artists(self)
  
   return lsit of all artist in database
   
  .. py:method:: load_artist_database(self)
   
   load all song corresponding to current 

   
    
 








   


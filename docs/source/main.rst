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




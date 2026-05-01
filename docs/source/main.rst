===============================
ChimkenMuziks Devellopement Doc
===============================

.. py:class:: App
  
  .. py:method:: __init__(self, directory="" , song="", logging_level=10)
  
  initialize the logger and load all the methods
  
  :param song: indicate a song to be played when lauching the program
  :type song: str
  :param directory: where the song is located 
  :type directory: str
  :param logging_level: indicate from which level log will be written
  :type logging_level: int


  -------------


  In external
  ===========
  
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

  ----------

  In Command
  ==========
 
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

  In Param
  ========    
  
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









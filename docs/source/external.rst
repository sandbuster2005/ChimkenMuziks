========
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
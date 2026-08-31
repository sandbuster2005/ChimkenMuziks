#!/bin/python
#made by sand
import argparse
import sys
import logging
import datetime
import os
import importlib
from ChimkenJournalism import Journal
from appdirs import AppDirs



#debug levels :
    #NOTSET : 0
    # [CUSTOM] BULLSHIT : 1
    # [CUSTOM] TRACE : 5
    #DEBUG : 10
    #INFO : 20
    #WARNING : 30
    #ERROR : 40
    #CRITICAL : 50

class App:
    def __init__( self, song = "", logging_level = logging.DEBUG ):
             #from libs.handmade._external import external_call, external_return
        
        import colorama.__init__ as colorama
        colorama.init()
        
        self.exterior_song = song
        
        self.load_methods()
        
        self.load_appdirs()
        
        self.load_logger(logging_level)
        
        self.init_all()
    
    
    
    
    def load_methods(self):
        
        self.libs = [
            "external", "display", "sound", "batterie",
            "command", "param", "files", "image",
            "download", "song", "main", "printimage",
            "data", "playlist", "update", "discord"
            ]
        
        for lib in self.libs:
            setattr(self,f"{ lib }_lib", importlib.import_module( f".._{lib}", f"libs.handmade._{ lib }" ) )

        for lib_name in self.libs:
            
            lib = getattr(self,f"{lib_name}_lib")
            
            for method in lib.__all__:
                
                method = getattr(lib,method)
                setattr( self, method.__name__, method.__get__( self ) )
    
    
    def load_appdirs(self):
        self.appdirs = AppDirs("ChimkenMuziks","sand")
        try:
            os.mkdir(self.appdirs.user_data_dir)
            os.mkdir(self.appdirs.user_cache_dir)
            os.mkdir(self.appdirs.user_log_dir)
            os.mkdir(self.appdirs.user_config_dir)
        
        except:
            pass
        
        if os.path.isfile('appdata/param.txt') and not os.path.isfile(AppDirs("ChimkenMuziks","sand").user_config_dir+'/param.txt'):
            os.rename('appdata/param.txt', AppDirs("ChimkenMuziks","sand").user_config_dir+'/param.txt')
        
        if os.path.isfile('appdata/cache/data.db')and not os.path.isfile(AppDirs("ChimkenMuziks","sand").user_data_dir+'/data.db'):
            os.rename('appdata/cache/data.db', AppDirs("ChimkenMuziks","sand").user_config_dir+'/data.db')
       
       
    def load_logger(self, logging_level):
        conf ={
            "default" :{
                "level": logging_level,
                "format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
                "loggers": ["main", "param", "command", "file", "image", "download", "song", "data", "update", "discord"],
                "handlers":[
                    {
                    "name" : f"{self.appdirs.user_log_dir}/{str(datetime.datetime.now()).replace(':','_')}.log",
                    "type" : "file",
                    "level": 0
                    }      
                    ]
            }
        }
        
        self.logger = Journal( conf )
        self.logger.add_level("TRACE",5)
        self.logger.add_level("BULLSHIT",1)
        
        self.logger["main"].info("APP STARTED")

        self.logger["main"].debug("initializing methods")
     
     
    
    def init_all(self):
        for lib in self.libs:
            getattr(self,f"init_{lib}")()
        
        self.logger["main"].info("initiated methods")
                
                
                
                
                
    
    class Song:
        def __init__(self, index , file , separator , metadata = {}):
            self.index = index
            self.file = file
            self.filepathname, self.extension = self.file.rsplit( ".",1 )
            self.filepath, self.filename = self.file.rsplit( separator, 1 )
            self.name = self.filename.rsplit( ".",1 )[0]
            self.metadata = metadata
            
            # Default values for mandatory metadata entries:
            if 'track' not in self.metadata:
                self.metadata['track'] = 0
            
        def __str__(self):
            return self.file
        
        def __repr__(self):
            return self.file
        
        def __eq__(self, other):            
            return self.index == other.index
    
    
    
    
    
    class Image:
        def __init__(self, height , width, name, image = "" ):
            self.name = name
            self.image = image
            self.height = height
            self.width = width
            
    
    
    
    
    

parser = argparse.ArgumentParser()
parser.add_argument("--song")
#parser.add_argument("--dir", required="--song" in sys.argv)

args = parser.parse_args()
if args.song:
    app = App(args.song)
    
else:
    app = App()
    
app.main()







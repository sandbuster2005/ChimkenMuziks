import logging
import datetime

# conf exemple
# you always need a default config with all the field 
conf = {
    "default" :
        {
        "level": 0,
        "format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        "loggers": ["main" ,"sub" ],
        "handlers":
          [
            {
            "name" : "main.log",
            "type" : "file",
            "level": 0
            },
            
            {
            "name" : "warning.log",
            "type" : "file",
            "level": 30
            }         
          ]
        },
    
    "backup" :
        {
        "loggers" : ["backup"],
        "handlers":
          [
            {
            "name" : "backup.log",
            "type" : "file",
            "level" : 0
            }
          ]
        }      
       }



class Journal:
    
    def __init__(self, config = conf ):
        
        logging.getLogger().setLevel(0)
        
        self._levels = { 10 : "DEBUG" ,20 : "INFO"  ,30: "WARNING" ,40: "ERROR" ,50 : "CRITICAL" }
        self._logger = {}
        self._handlers = []
        self._configs = config
        print(self._configs)
        
        self.add_log("_JOURNAL_")
        
        for config in self._configs.keys():
            for logger in self._configs[config]["loggers"]:
                self.add_log( logger , config )
        
        
        
        
        
    def __getitem__(self, index):
        
        if index in self._logger.keys():
            return self._logger[index]
        
        else:
            self.add_log( index )
            self._logger["_JOURNAL_"].warning(f"{index} log do not exist and should be manually created before next time")
            
            return self._logger[index]
        
        
        
            
    
    def __repr__(self):
        
        return self.loggers()
    
    
    
    
    
    def _create_file_handler( self, filehandler , template ):
        
        handler = logging.FileHandler( filehandler["name"] )
        handler.setLevel( filehandler["level"] )
        handler.setFormatter ( template ) 
        self._handlers.append( handler )
        
        return handler
    
    
    
    
    
    def _create_log_formatter(self , config = "defaut" ):
        
        if "format" in self._configs[config].keys():
            return logging.Formatter(fmt = self._configs[config]["format"] )
        
        else:
            return logging.Formatter(fmt = self._configs["default"]["format"] )
        
        
        
        
    
    def add_log(self, name , config = "default" ):
        
        self._logger[ name ] = logging.getLogger( name )
        
    
        if "level" in self._configs[config].keys():
            self._logger[ name ].setLevel( self._configs[config]["level"] )
            
        else:
            self._logger[ name ].setLevel( self._configs["default"]["level"] )
        
        
        template = self._create_log_formatter( config )  
        
        if "handlers" in self._configs[config].keys() :
            handlers = self._configs[config]["handlers"]
        
        else:
            handlers = self._configs["default"]["handlers"]
       
        for handler in handlers:
            if handler["type"] == "file":
                 self._logger[ name ].addHandler( self._create_file_handler( handler , template ) )
        
        
        self._logger[ name ].propagate = False
    
    def add_level(self, level_name, level_num, erase = False ):
        if level_num in self._levels.keys() and not erase:
            raise Exception("log level already exist")
        
        
        method_name = level_name.lower()
        level_name = level_name.upper()

        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(level_num):
                self._log(level_num, message, args, **kwargs)

        def logToRoot(message, *args, **kwargs):
            logging.log(level_num, message, *args, **kwargs)
        
        self._levels[level_num] = level_name
        
        logging.addLevelName(level_num, level_name)

        setattr(logging, level_name, level_num)
        setattr(logging.getLoggerClass(), method_name, logForLevel)
        setattr(logging, method_name, logToRoot)
        
        
    def loggers(self):
        return  "loggers : " + " ,".join( [ x for x in self._logger.keys() ] )
    
    def levels(self):
        return "\n".join( [ f"{ self._levels[x] } : {x} " for x in sorted(self._levels) ] ) 
    
    def handlers(self):
        return self._handlers
    
    
journal = Journal()
journal.add_level("test",15)
journal["test"].test("this is a teste")
journal.add_log("screen" ,"backup")
journal["screen"].test("its working")
journal["main"].warning("this is normal")
print(journal.loggers() )
print( journal.levels() )
print( journal._logger["screen"].handlers)
print(journal)
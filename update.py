import subprocess
import shutil
from os.path import isdir,exists
from os import listdir,makedirs,remove,rmdir

mode = "o"
depth = 1
#a:add o:overwrite


def external_call( arg, shell = False ):
    """
    cette fonction permet d'executer des commandes dans le cmd avec ou sans
    shell
    """
    if shell == False :
        subprocess.Popen(arg).wait()
        
    elif shell == True:
        subprocess.Popen( arg, shell = True ).wait()
        
def external_return ( args:list ):
    return subprocess.check_output(args)

def get_file(path, newpath="", files = [] ,end=1, depth=0):
    """
    cette fonction permet de récuperer tout les fichier waw,mp3 et m4a dans un dossier et sous dossiers,
    elle remet aussi a 0 l'historique ,stop toute chanson en cours de lecture et ajoute a la liste des dossiers
    le dossiers et les sous dossiers si il n'y sont pas
    
    limite:
    path est un chemin d'accés auquel l'utilisateur peut accéder
    files est une liste qui peut contenir des chemin d'accés auquel l'utilisateur peut accéder au préalable
    renvoie les ficher déja inclus et ceux du dossier scanné
    """
    dirs = []
    depth-=1
    for f in listdir( path + newpath ):
        if isdir( path + newpath + f ) and depth!=0:
                newf,newd = get_file( path , files = [], newpath = newpath + f + "/", depth=depth-1 )
                files+=newf
                dirs+=newd
                dirs.append( newpath + f+ "/" )
                
        elif not isdir(path + newpath + f):    
            files.append( newpath + f )
            
    if depth==0:
        return files
    
    return files,dirs


try:
    source = str(external_return(["xplr"],))[2:-3]+"/"
except:
    source = input("chemin du dossier  source: ")

try:
    destination = str(external_return(["xplr"],))[2:-3]+"/"
except:
    destination = input("chemin du dossier  source: ")


start_depth = destination.count("/")

if not isdir(source):
   raise ValueError(f"{source} not a directory")
    
if not isdir(destination):
    raise ValueError(f"{destination} not a directory")

files,dirs = get_file(source)
nfiles = []
efiles,dirs2 = get_file(destination,files = []) #existing file in destination
edirs = []

print(f"{len(files)} files")



dirs = [x for x in dirs if x.count("/") <= depth ]

for x in files:
    if x.count("/") <=  depth:
        nfiles.append(x)
    
    elif x.count("/") - depth <=0:
        nfiles.append(x.rsplit("/")[-1])
        print(x.rsplit("/")[-1])
    
    else:
        nfiles.append("/".join( x.rsplit("/")[:depth]) + "/" + x.rsplit("/")[-1])                                  
        print("/".join( x.rsplit("/")[:depth]) + "/" + x.rsplit("/")[-1] )



print(nfiles,len(nfiles))
for f in dirs:
    if not exists(destination + f):
        print(f"{destination + f} dosn't exist creating")
        makedirs(destination + f)
   
    else:
        print(destination+f)
        efiles += get_file(destination,newpath=f,depth=1,files = [])

for f in dirs2:
    if f not in dirs:
        efiles += get_file(destination,newpath=f,depth=1,files = [])
        edirs.append(f)


if mode =="o":
    for f in efiles:
        if f not in files:
            remove(destination+f)
            print(f"removed {f}")
    for f in edirs:
        rmdir(destination+f)
    

for x in range(len(nfiles)):
    if nfiles[x] not in efiles:
        shutil.copy(source+files[x],destination+nfiles[x])
        print(f"sucefully copied {nfiles[x]}")


#print(source,destination)

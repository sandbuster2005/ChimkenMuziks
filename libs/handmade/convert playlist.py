#made by sand
from utils import replace
from os import listdir
import os
path="/home/sand/Musique/musique/download"
for f in listdir(path):
    print(f)
    extension="."+f.rsplit(".",1)[1]
    #print(extension)
    file=f.rsplit("[",1)[0]
    #print(file)
    #file=replace(file,["(","'",'"',")"," ",":","|","&","[","]"],"_")
    #print(path+"/"+file+extension)
    #print(path+"/"+f)
    #input()
    os.rename(path+"/"+f,path+"/"+file+extension)
#made by sand
import os
from os.path import isfile
def write_file(file:str,data="", mode = "w",encoding="utf-8")-> None:
    """
    cette fonction permet de creer un fichier file et otionnement ecrire un texte data dans le fichier
    """
    if not "b" in mode:
        with open(file,mode,encoding = encoding ) as f:
            f.write(data)
    else :
       with open(file,mode ) as f:
            f.write(data)

def get_file(file:str ,encoding="utf-8")-> str:
    """
    cette fonction permet de recuperer le contenu d'un fichier texte
    """
    with open(file,"r",encoding=encoding) as f:
        result=f.read()
    return result

def get_info(data:str,chrs:[str])-> list:
    """
    cette fonction permet de transforer une chaine de charactére avec des separateur en liste de profondeur maximal egal
    au nombre de caractére dans chrs 
    """
    data=data.split(chrs[0])
    new_data=[]
    for x in range(len(data)):
        if len(chrs)>1:
            new_data.append(get_info(data[x],chrs[1:]))
    if new_data!=[]:
        return new_data
    else:
        return data

def get_data(file:str,chrs:[str])-> list:
    """
    cette fonction permet de recupérer les valeur d'un fichier a separateur et de le transformer en liste
    """
    if isfile(file):
        data=get_file(file)
        data=get_info(data,chrs)
        return(data)
    else:
        write_file(file)
        return []
def edit_data(file,chrs,edit:str,position:[int])-> None:
    """
    cette fonction permet avec la position dans la liste créer grace a get_data de modifier une valeur et de l'enregistrer
    """
    data=get_data(file,chrs)
    data.remove([""])
    if data!=[]:
        new_data=["" for x in range(len(position)+1)]
        new_data[0]=data
        for x in range(1,len(position)+1):
            new_data[x]=new_data[x-1][position[x-1]]
        new_data[-1]=edit
        for x in range(len(new_data)-1,0,-1):
            new_data[x-1][position[x-1]]=new_data[x]
        data=join_list(data,chrs)
        write_file(file,data)
        
def join_list(data:str,chrs:[str],depth:int=0,lenght:int=0)-> str:
    """
    cette fonction permet a partir d'une liste de former une chaine de caractére avec des separateurs 
    """
    new_data=""
    for x in range(len(data)):
        if type(data[x])==list:
            new_data+=join_list(data[x],chrs,depth+1,len(data)-(x+1))
        else:
            new_data+=data[x]+(chrs[0+depth]*(x!=len(data)-1))
    return new_data+(chrs[depth-1]*(lenght!=0))
def rm_file(file):
    os.remove(file)
    
def mv_file(file,newfile):
    os.rename(file,newfile)
    
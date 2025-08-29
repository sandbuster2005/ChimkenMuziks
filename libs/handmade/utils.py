#made by sand
from math import ceil
def white(x:int=60):
    """
    cette fonction passe un nombre x de ligne
    """
    for z in range(x):
        print("")

def replace(word:str,chrs:list,new:str="") -> str:
    return "".join([word[x]*(1-(word[x] in chrs))+ new*(word[x] in chrs) for x in range(len(word))])

def all_numbers(word,lim=0,mode=0):
    """
    cette fonction permet de :
    verifier si une chaine de charactère est un nombre : mode 0
    verifier si une chaine de charactère est un nombre strictement inferieur a un seuil lim : mode 1
    verifier si une chaine de charactére est un nombre  inferieur ou égal a un seuil lim : mode 2
    
    limite:
    word doit étre une chaine de charactére
    lim doit étre strictement supérieur a 1
    mode doit étre compris entre 0 et 1 inclut
    """
    
    return all(test in "0123456789" for test in word)==(word!="")==True==(int("".join([str(max(0,int(ord(word[x])-48))) for x in range(len(word))]))*lim<lim*lim-mode+1)

def str_lowerup(word:str,chrs:[str],mode=0):
    """
    cette fonction permet de mettre en majuscule ou minuscule une liste de chr dans uene chaine de caractére
    word est une chaine de charactere
    chrs est une liste de charactere
    mode 1 pour majuscule
    mode 0 pour mminuscule
    """
    return "".join([word[x]*(1-(word[x].lower() in chrs))+(word[x].lower())*(word[x].lower() in chrs )*(1-mode)+(word[x].upper())*(word[x] in chrs )*(mode) for x in range(len(word))])

def clear_adjacent(word:str,chrs:[str],lenght:int) -> str:
    pos = 0
    if lenght <= 1 :
        raise Exception("lenght should be above 1")
    if not isinstance(word, str):
        raise Exception("word should be a string")
    if isinstance(chrs, str):
        chrs = list(chrs)
    if not isinstance(chrs, list):
        raise Exception("chrs should be a list/string")
    
    for x in range(len(chrs)):
        if not isinstance(chrs[x], str):
            if isinstance(chrs[x], int):
                chrs[x] = chr(chrs[x])
            else :
                raise Exception("inside chrs should be str")
        
        
    
    while pos+  lenght != len(word):
        remove = True
        
        x = 0
        while x < lenght and remove == True:
            if word[pos+x] not in chrs:
                remove = False
            x += 1
        
        if remove :
            replace = len(chrs) - 1
            x = 0
            
            for x in range(lenght):
                replace = min(replace, chrs.index(word[pos + x]))
                
            word = word[:pos] + chrs[replace] + word[pos + lenght:]
            if pos !=0 :
                pos -= 1
        
        else :
            pos += 1
    return word
            
                
        

def ask( self, text ):
    """
    cette fonction permet de demander une valeur a l'utilisateur
    en lui demandant text
    """
    return input( f"{ text }" )

def show_list( liste, num = True ):
    """
    cette fonction permet d afficher les elements d'une liste un
    par un ,numeroté ou non
    """
    if num == True:
        for x in range( len( liste ) ):
             print( x, liste[x] )
        
    else:
        for x in liste:
                print( x )
                
def ask_list(liste, text = "" , num = True ):
    """
    cette fonction affiche a l'utilisateur une liste et lui demande
    une valeur a l'aide d un prompt text
    """
    self.show_list( liste, num )
    return self.ask( f"{ text }" )

def dumb_closest(num:int ,liste:sorted) -> int:
    """
    cette fonction renvoie l'index du nombre le plus proche dans une liste rangé
    """
    while ( pos:= ( ( high := ( high := [ len(liste) if not "high" in ( var := locals() ) else high ][0] ) * ( _ := ( num > liste[ ( pos := [0 if "pos" not in var  else pos ][0] ) ] ) ) + pos * (1 - _) ) + (low := ( low := [ 0 if not "low" in var  else low ][0] ) * (1 - _ ) + pos * _  ) ) // 2) != low :
        pass
            
    return pos
        
def closest(num:int , liste:sorted) -> int:
    pos = 0
    high = len(liste)
    low = 0
    while (pos := (high + low)//2 ) != low:
        
        if liste[pos] > num:
            high = pos
        
        else:
            low = pos
            
    return pos
        
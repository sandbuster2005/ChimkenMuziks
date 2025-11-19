#made by sand
from math import log,floor
def white( x : int = 60 ) -> None:
    """
    cette fonction passe un nombre x de ligne
    """
    for z in range(x):
        print("")
        
def replace( word : str, chrs : list[str], new : str = "" ) -> str:
    """
    cette fonction permet de remplacer dans word les string contenu dans chr par new
    """
    return [ word := f"{ new }".join( word.split( x ) ) for x in chrs ][ -1 ]
    
def all_numbers(word : str ,lim :int = 0,mode : int = 0) -> bool:
    """
    cette fonction permet de :
    verifier si une chaine de charactère est un nombre : mode 0
    verifier si une chaine de charactère est un nombre strictement inférieur a un seuil lim : mode 1
    verifier si une chaine de charactére est un nombre  inferieur ou égal a un seuil lim : mode 2
    
    limite:
    word doit étre une chaine de charactére
    lim doit étre strictement supérieur a 1
    mode doit étre compris entre 0 et 1 inclut
    """
    
    return all(test in "0123456789" for test in word)==(word!="")==True==(int("".join([str(max(0,int(ord(str(word)[x])-48))) for x in range(len(str(word)))]))*lim<lim*lim-mode+1)

def str_lowerup( word : str, chrs : list[ str ], mode : int = 0 ) -> str:
    """
    cette fonction permet de mettre en majuscule ou minuscule une liste de chr dans une chaine de caractére
    word est une chaine de charactere
    chrs est une liste de charactere
    mode 1 pour majuscule
    mode 0 pour minuscule
    """
    return "".join( [word[x]*(1-(word[x].lower() in chrs))+(word[x].lower())*(word[x].lower() in chrs )*(1-mode)+(word[x].upper())*(word[x] in chrs ) * mode for x in range(len(word))])

def clear_adjacent( word : str, chrs : list[ str ], lenght : int ) -> str:
    """
    cette fonction permet de supprimer les charactère adjacent de lenght individu
    contenu dans chrs de word
    """
    pos = 0
    if lenght <= 1 :
        raise Exception( "lenght should be above 1" )
    
    if not isinstance( word, str ):
        raise Exception( "word should be a string" )
    
    if isinstance( chrs, str ):
        chrs = list( chrs )
        
    if not isinstance( chrs, list ):
        raise Exception( "chrs should be a list/string" )
    
    for x in range( len( chrs ) ):
        if not isinstance( chrs[ x ], str ):
            if isinstance( chrs[ x ], int ):
                chrs[ x ] = ord( chrs[ x ] )
                
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
            change = len( chrs ) - 1
            
            for x in range( lenght ):
                change = min( change, chrs.index( word[ pos + x ] ) )
                
            word = word[:pos] + chrs[ change ] + word[ pos + lenght: ]
            
            if pos !=0 :
                pos -= 1
        
        else :
            pos += 1
            
    return word

#please don't use that
def dumb_closest(num : int ,liste : list ) -> int:
    """
    cette fonction renvoie l'index du nombre le plus proche dans une liste rangé
    """
    while ( pos:= ( ( high := ( high := [ len(liste) if not "high" in ( var := locals() ) else high ][0] ) * ( _ := ( num > liste[ ( pos := [0 if "pos" not in var  else pos ][0] ) ] ) ) + pos * (1 - _) ) + (low := ( low := [ 0 if not "low" in var  else low ][0] ) * (1 - _ ) + pos * _  ) ) // 2) != low :
        pass
            
    return pos
        
def closest(num : int , liste :  list ) ->  int:
    """
    cette fonction renvoie l'index de la valeur la plus proche de num
    liste doit étre rangé par ordre croissant / decroissant
    """

    high = len(liste)
    low = 0
    
    while (pos := ( high + low ) // 2 ) != low:
        
        if liste[ pos ] > num:
            high = pos
        
        else:
            low = pos
            
    return pos

def remove_list( liste : list ) -> list:
    """
    cette fonction permet de retirer les étages de liste inutile (contenant 1 element)
    """
    if type(liste) is not list:
        return liste
    
    if len(liste) == 1:
        
        if type(liste[0]) is not list:
            return liste[0]
        
        else:
            return remove_list(liste[0])
        
    else:
        return [remove_list(x) for x in liste]
    
def rotate_tableau(liste : list , add : bool = True, val = None) -> list :
    """
    cette fonction permet de tourner le tableau de 90°
    """
    lenght = max( [ len( x ) for x in liste ] )
    result = [ [] for _ in range( len( liste ) ) ]
    
    for index in range( lenght ):
        for elem in liste:
            if len( elem ) > index:
                result[ index ].append( elem[ index ] )
                
            elif add:
                 result[ index ].append( val )
                 
    return result

def convertion( number : int ,precision : int = 4,extension : str = "b", base : int = 1000 , names : list = [" ","K","M","G","T","P","E","Z","Y","R","Q"] ) -> str:
    power = floor( log( number ,base) )
    num = number / base ** power

    a = f"{ round( number / base ** power , precision -  ( floor( log(num , 10) ) + 1  ) ) }"
    spaces = max (0, 5 - len( a ) ) * " "
    if power <= len( names ):
        return f"{ a } {spaces}{ names[ power ] }{ extension }"

    else:
        raise "value too big for provided notation"

def get_perm( num : int|str ) -> list :
    """
    cette fonction renvoie les permission (rwx) d un fichier a partir du nombre
    """
    result = ""
    for x in str( num ):
        y = int( x )

        if y >= 4:
            result += "r"
        else:
            result += "-"

        if y in [2,3,6,7]:
            result += "w"
        else:
            result += "-"

        if y % 2 == 1:
            result += "x"
        else:
            result += "-"

    return result

def scroll_text( text : str , pos : int, size : int, direction : int) -> str:
    """
    cette fonction permet de faire defiller un string pour pouvoir l afficher sur l'ecran
    direction = 1 : gauche
    direction = -1 : droite
    """
    #direction 1 : left | -1 : right
    result = text[ max( 0, direction + pos ) : size + direction + pos ]
    print( result )
    return result
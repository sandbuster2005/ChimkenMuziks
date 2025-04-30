import os
#il faut absolument une classe Screen avec une methode display et update + self.framerate
#elle sont appellé par le code principal
class Screen:
    def __init__(self):
        self.framerate = 5# le nombre de frame par seconde
        self.count = 0
    
    def display(self):#la fonction qui serra appeller quand il faut redesinner toute l'image
        width,height = os.get_terminal_size() #l'affichage sera la taille du terminal -4 ligne puissque le lecteur affiche 4 ligne
        for x in range(height-4):
            print(x)
    
    def update(self):#la fonction sera executer self.framerate frame par seconde
        print(self.count)
        self.count += 1
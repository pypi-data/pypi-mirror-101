class File:
    def __init__(self):
        self.file = []
    def enfiler(self,item):
        self.file.append(item)
    def defiler(self):
        if len(self.file) > 0:
            item = self.file.pop(0)
            return item
        else:
            return "file vide !"
    def vider(self):
        self.file = []
    def informations(self):
        print(self.file)
    def to_list(self):
        return self.file
    def est_vide(self):
        if len(self.file)>0:
            return False
        else:
            return True
class Pile:
    def __init__(self):
        self.pile = []
    def empiler(self, *args):
        for arg in args:
            self.pile.append(arg)
    def depiler(self):
        if len(self.pile) > 0:
            item = self.pile.pop(len(self.pile)-1)
            return item
        else:
            return "pile vide !"
    def vider(self):
        self.pile = []
    def informations(self):
        print(self.pile)
    def to_list(self):
        return self.pile
    def est_vide(self):
        if len(self.pile)>0:
            return False
        else:
            return True
class Graph:
    def __init__(self):
        self.graph = {}
    def definition(self,**kwargs):
        '''
        :param:  Noeud = " Suc1 , Suc2 .. "
         Example : definition(a=" b , c " , b = "" )
         c-t-d : la racine : a , les succs de a = [ b , c ]
        '''
        for key, value in kwargs.items():
            if "," in value:
                val = value.split(",")
                succs = [ x.upper() for x in val]
                if len(succs)>1:
                    self.graph[key.upper()] = succs
                else:
                    self.graph[key.upper()] = []
            else:
                if value != "":
                    self.graph[key.upper()] = [value.upper()]
                else:
                    self.graph[key.upper()] = []
    def get_sucss(self,noeud):
        '''
        :param noeud:
        :return les successeurs de noeud:
        '''
        try:
            sucss = self.graph[noeud.upper()]
        except:
            sucss = []
        finally:
            return sucss
    def informations(self):
        if len(list(self.graph.keys()))>0 :
            feuilles = [ key for key in list(self.graph.keys()) if len(self.get_sucss(key)) == 0 ]
            print(f"-Racine = {list(self.graph.keys())[0]} \n-Les feuilles : {feuilles}  \n-Graph: {self.graph}")
        else:
            print("Graph est Vide !")
    def vider(self):
        self.graph = {}
    def to_dict(self):
        '''
        :return le graph sous forme d'un dict python:
        '''
        return self.graph






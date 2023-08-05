from Amkdev_mia_tools import File,Pile,Graph
###################################### FUNCTIONS #################################################
def BFS(graph,start,but):
    start = start.upper();but = but.upper();closed = File();open = File();parent = {};parent[start] = start;find = False
    open.enfiler(start)
    while not open.est_vide():
        current = open.defiler()
        if current == but:
            find = True
            break
        else:
            closed.enfiler(current)
        succs_de_current = graph.get_sucss(current)
        for suc in succs_de_current:
            if suc not in parent:
                parent[suc]=current
            open.enfiler(suc)
    if find :
        # tracé le chemin
        goal=but
        chemain = [goal]
        # trace the path back till we reach start
        while goal != start:
            goal = parent[goal]
            # ajouter a la position 0 le goal bah tji tabda mn START ll BUT
            chemain.insert(0, goal)
        print(f"j'ai trouvé le but '{but}' \nNœuds explorés : {closed.to_list()} \nfile d'attente :{open.to_list()} \nLe chemin trouvé : {chemain} ")
    else:
        print(f"Tous les noeuds a été exploré mais aucun chemin trouvé")
def DFS(graph,start,but):
    start = start.upper();but = but.upper();closed = File();open = Pile();parent = {};parent[start]=start;find=False
    open.empiler(start)
    while not open.est_vide():
        current=open.depiler()
        if current == but:
            find = True
            break
        else:
            if current not in closed.to_list():
                closed.enfiler(current)
        sucs_of_current = graph.get_sucss(current)
        for suc in reversed(sucs_of_current):
            parent[suc]=current
            open.empiler(suc)

    if find :
        goal=but
        chemain = [goal]
        while goal != start:
            goal = parent[goal]
            chemain.insert(0, goal)
        print(f"j'ai trouvé le but '{but}' \n Nœuds explorés : {closed.to_list()} \n file d'attente : {open.to_list()} \n le chemin trouvé : {chemain} ")
    else:
        print(f"Tous les noeuds a été exploré mais aucun chemin trouvé {open.to_list()} ,{closed.to_list()}")
def DLS(graph,start,but,niveau,limite):
    start = start.upper();but = but.upper();closed = File();parent = {};parent[start] = start
    def DLS_0(start, but, niveau, limite):
        closed.enfiler(start)
        if start == but: return niveau
        if niveau == limite: return False
        succs = graph.get_sucss(start)
        for suc in succs:
            parent[suc] = start
            if DLS_0(suc, but, niveau + 1, limite): return True
    if DLS_0(start, but, niveau, limite):
        goal = but
        chemin = [but]
        while but != start:
            but = parent[but]
            chemin.insert(0, but)
        print(f"j'ai trouvé le But {goal} : \n- les noeuds explorés : {closed.to_list()} "
              f"\n- le chemin trouvé : {chemin} \n- niveau de but {len(chemin)}"
              f"\n- niveau maximum : {limite} ")
    else:
        print(f" but non trouvé \n- les noeuds explorés : {closed.to_list()} "
              f"\n- chemin non trouvé \n- niveau de but : non trouvé "
              f"\n- niveau maximum : {limite} ")
def IDS(graph,start,but,profondeur_maximale):
    closed = File();start = start.upper();but = but.upper();parent ={};parent[start] = start;find=False
    def DFS(start, but, profondeur_maximale):
        closed.enfiler(start)
        if start == but:
            return True
        if profondeur_maximale <= 0:
            return False
        succs = graph.get_sucss(start)
        for suc in succs:
            parent[suc] = start
            if DFS(suc, but, profondeur_maximale - 1):
                return True
        return False

    def IterativeDFS(start, but, profondeur_maximale):
        for i in range(profondeur_maximale):
            if DFS(start, but, i):
                return True
        return False

    if IterativeDFS(start, but, profondeur_maximale):
        goal = but
        chemin = [but]
        while but != start:
            but = parent[but]
            chemin.insert(0, but)
        print(f"j'ai trouvé le But {goal} : \n- les noeuds explorés : {closed.to_list()} "
              f"\n- le chemin trouvé : {chemin} \n- niveau de but {len(chemin)}"
              f"\n- profondeur_maximale ( L ) : {profondeur_maximale} ")
    else:
        print(f" but non trouvé \n- les noeuds explorés : {closed} "
              f"\n- chemin non trouvé \n- niveau de but : non trouvé "
              f"\n- profondeur_maximale : {profondeur_maximale} ")





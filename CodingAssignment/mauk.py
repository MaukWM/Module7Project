from graph_io import *
from graph import *
import collections

# Central program

def RunIsomophismProgram(name,autos,decision):
    with open(name) as f:
        L = load_graph(f, read_list=True)

    # Initial colouring
    AList = CreateVertexList(L)
    SetInitialColour(AList)
    # preparation
    thing = BuildDict(AList)
    kaas = thing[0]
    max = thing[1]
    # Refining
    changed = True
    while changed:
        stuff = Refine(kaas, max)
        changed = stuff[0]
        max = stuff[1]
    # arrived at first stable colouring branching starts here:

    dicts = []
    for graph in L[0]:
        dicts.append(BuildDict(graph.vertices)[0])

    a = len(dicts)

    if autos:
        n = 0
        for graph in L[0]:
            findAutoMorphism(graph,n)
            n = n + 1

    for x in range(0,a):
        for y in range(x + 1,a):
            something = [dicts[x],dicts[y]]
            print("graph " + str(x) + " graph " + str(y) + " have " + str(CountIsomorphism(dicts[x],dicts[y],True,decision)) + " isomorphism(s)")



# writing to dot file
    i = 0
    for G in L[0]:
        name = 'mygraph' + str(i) + '.dot'
        with open(name, 'w') as f:
            write_dot(G, f)
        i += 1



# Color Refinement

def CreateVertexList(DataSet) -> list:
    """"Create a list with all vertices"""
    VertexList = []
    for graph in DataSet[0]:
        VertexList.extend(graph.vertices)
    return VertexList

def SetInitialColour(List):
    """"Set initial colour (e.g. degree of vertex is colour)"""
    for vertex in List:
        vertex.colornum = vertex.degree

def BuildDict(List) -> list:
    """"Build dict of the form {colour,list[vertices]}"""
    Dict = {}
    max = 0
    for vertex in List:
        if vertex.colornum in Dict:
            Dict.get(vertex.colornum).append(vertex)
        else:
            Dict[vertex.colornum] = [vertex]
            if vertex.colornum > max:
                max = vertex.colornum
    return [Dict, max]

def Neighbourhood(Node) -> list:
    """Find the neighbourhood of one Node and return it as a list
    example: [1,1,1,1,3,4,5,6,1,5,2,3,6]"""
    colour = []
    for neighbour in Node.neighbours:
        colour.append(neighbour.colornum)
    return sorted(colour)

def Refine(Dict, max) -> list:
    """" Four every colour check whether the neighbourhood of each node is the same as that of the first vertex
    For all nodes that do not have this property add them in a list to the list changing in the form:
    [key, node1, node2, ...]
    In the end, give all the changing nodes new colours
    return whether something has changed with the new max colour"""
    changed = False
    changing = []
    index = -1
    # iterating over colours
    for key in Dict.keys():
        # setting variables
        nodes = Dict[key]
        neighbourhoodOne = sorted(Neighbourhood(nodes[0]))
        colourchanged = False
        for node in nodes:
            if neighbourhoodOne != sorted(Neighbourhood(node)):
                if changed == False:
                    changed = True

                if colourchanged == False:
                    changing.append([key])
                    index += 1
                    colourchanged = True

                changing[index].append(node)


    for list in changing:
        dictlist = Dict[list[0]]
        list.pop(0)
        max = max + 1
        Dict[max] = list
        for node in list:
            dictlist.remove(node)
            node.colornum = max
    return [changed, max]

# Branching Starts here

def BasicChecks(Dict1, Dict2) -> bool:
    for key in Dict2:
        if Dict1.get(key) == None or Dict2.get(key) == None or len(Dict1.get(key)) == 0 or len(Dict2.get(key)) == 0:
            return 0.5

    for key in Dict1:
        if Dict1.get(key) == None or Dict2.get(key) == None or len(Dict1.get(key)) == 0 or len(Dict2.get(key)) == 0:
            return 0.5
        if len(Dict1.get(key)) != len(Dict2.get(key)):
            return 0.5
        elif len(Dict1.get(key)) > 1:
            return key
    return 1.5

    """
    Checks if :var Dict1 and :var Dict2 have the same length, if not :return False
    Checks if array of all corresponding values is same length, if not :return False
    else :return True
    
    if len(Dict1) != len(Dict2):
        return False
    for key in Dict1.keys():
        if Dict2.get(key) == None:
            return False
        if len(Dict1.get(key)) != len(Dict2.get(key)):
            return False
    return True
    """

def isIsomorphism(Dict1, Dict2) -> list:
    """"
    only call this if BasicChecks(Dict1,Dict2) :returns True
    Are graphs Dict1 and Dict2 Isomorphic
    :return key if not
    :return True if yes
    """
    a = []
    kaas = False
    for key in Dict1.keys():
        if len(Dict1.get(key)) != 1 or len(Dict2.get(key)) != 1:
            a = key
            kaas = True
    if kaas:
        return [False, a]
    return [True, 0]

def RestoreColours(Dict1):
    for key in Dict1.keys():
        vertexlist = Dict1.get(key)
        for vertex in vertexlist:
            vertex.colornum = key

def DeepcopyDict(Dict1) -> dict:
    A = {}
    for key in Dict1.keys():
        a = []
        vertexlist = Dict1.get(key)
        for vertex in vertexlist:
            a.append(vertex)
        A[key] = a
    return A

def findStableColouring(dict1, dict2):
    while True:
        newColour1 = max(dict1.keys())
        newColour2 = max(dict2.keys())
        newColour = max([newColour1, newColour2]) + 1
        worst = False
        A = []
        B = []
        for key in dict1.keys():
            a = []
            b = []
            kaas = False
            Ham = False

            vertex1 = dict1.get(key)[0]
            neighbourhoodV1 = Neighbourhood(vertex1)

            for vertex in dict1.get(key):
                if Neighbourhood(vertex) != neighbourhoodV1:
                    a.append(vertex)
                    dict1.get(key).remove(vertex)
                    kaas = True
                    worst = True
            for vertex in dict2.get(key):
                if Neighbourhood(vertex) != neighbourhoodV1:
                    b.append(vertex)
                    dict2.get(key).remove(vertex)
                    Ham = True
                    worst = True
            if kaas:
                A.append(list(a))
            if Ham:
                B.append(list(b))

        #         Recolouring
        if worst:
            x = newColour
            y = newColour
            for entry in A:
                for vertex in entry:
                    vertex.colornum = x
                dict1[x] = entry
                x += 1

            for entry in B:
                for vertex in entry:
                    vertex.colornum = y
                dict2[y] = entry
                y += 1
        else:
            break

def CountIsomorphism(dict1, dict2, first, decicion):
    if not first:
        findStableColouring(dict1,dict2)
    kaas = BasicChecks(dict1,dict2)

    if kaas == 1.5:
        return 1
    elif kaas == 0.5:
        return 0
    key = kaas

    dict1Old = DeepcopyDict(dict1)
    dict2Old = DeepcopyDict(dict2)

    vertex1 = dict1Old.get(key)[0]
    num = 0
    for vertex2 in dict2Old.get(key):
        # restore colours
        RestoreColours(dict1Old)
        RestoreColours(dict2Old)
        dict1 = DeepcopyDict(dict1Old)
        dict2 = DeepcopyDict(dict2Old)

        newkey = max(dict1Old.keys())

        dict1.get(key).remove(vertex1)
        dict2.get(key).remove(vertex2)
        dict1[newkey + 1] = [vertex1]
        dict2[newkey + 1] = [vertex2]
        num = num + CountIsomorphism(dict1, dict2, False,decision)


        if decision:
            if num > 0:
                return 1
    return num

def copyGraph(graph):
    A = graph.vertices
    newGraph = Graph(False,len(A),False)
    B = newGraph.vertices
    for vertex in A:
        index = A.index(vertex)
        for vertex2 in vertex.neighbours:
            index2 = A.index(vertex2)
            if index2 > index:
                f = Edge(B[index],B[index2])
                newGraph.add_edge(f)

    return newGraph

def findAutoMorphism(Graph1, n):
    Graph2 = copyGraph(Graph1)
    vertexList = []
    for vertex in Graph1.vertices:
        vertexList.append(vertex)
    for vertex in Graph2.vertices:
        vertexList.append(vertex)
    SetInitialColour(vertexList)

    thing = BuildDict(vertexList)
    kaas = thing[0]
    max = thing[1]
    # Refining
    changed = True
    while changed:
        stuff = Refine(kaas, max)
        changed = stuff[0]
        max = stuff[1]
    # arrived at first stable colouring branching starts here:

    dict1 = BuildDict(Graph1.vertices)[0]
    dict2 = BuildDict(Graph2.vertices)[0]

    print("Graph " + str(n) + " has " + str(CountIsomorphism(dict1, dict2, True, False)) + " automorphisms")


name = 'basicGI1.grl'
autos = True
decision = False
RunIsomophismProgram(name,autos,decision)
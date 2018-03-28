from graph_io import *
from graph import *
import collections

# Central program

def RunIsomophismProgram(name):
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

    # Cycling every possible comparison
    GraphNumbers = len(L[0]) + 1
    for x in range(1,GraphNumbers):
        dict1 = BuildDict(L[0][x].vertices)
        for y in range(x + 1,GraphNumbers):
            # Prep
            dict2 = BuildDict(L[0][y].vertices)
            BranchingNeeded = False
            # Comparing Graphs
            if BasicChecks(dict1, dict2):
                if isIsomorphism(dict1, dict2):
                    print('graph ' + str(x) + ' and graph ' + str(y) + ' are isomorphic')
                else:
                    BranchingNeeded = True
            else:
                print('graph ' + str(x) + ' and graph ' + str(y) + ' are not isomorphic')
            # Brancing
            while BranchingNeeded:
                BranchingNeeded = False






    # writing to dot file
    i = 0
    for G in L[0]:
        name = 'mygraph' + str(i) + '.dot'
        with open(name, 'w') as f:
            write_dot(G, f)
        i += 1

# Color Refinement

def CreateVertexList(DataSet) -> list:
    VertexList = []
    for graph in DataSet[0]:
        VertexList.extend(graph.vertices)
    return VertexList

def SetInitialColour(List):
    for vertex in List:
        vertex.colornum = vertex.degree

def BuildDict(List) -> list:
    Dict = {}
    max = 0
    for vertex in List:
        if Dict.__contains__(vertex.colornum):
            Dict.get(vertex.colornum).append(vertex)
        else:
            Dict[vertex.colornum] = [vertex]
            if vertex.colornum > max:
                max = vertex.colornum
    return [Dict, max]

def Neighbourhoods(Node) -> list:
    colour = []
    for neighbour in Node.neighbours:
        colour.append(neighbour.colornum)
    return colour

def Refine(Dict, max) -> list:
    changed = False
    changing = []
    index = -1
    # iterating over colours
    for key in Dict.keys():
        # setting variables
        nodes = Dict[key]
        neighbourhoodOne = sorted(Neighbourhoods(nodes[0]))
        colourchanged = False
        for node in nodes:
            if neighbourhoodOne != sorted(Neighbourhoods(node)):
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
    if len(Dict1) != len(Dict2):
        return False
    for key in Dict1.keys():
        if len(Dict1.get(key)) != len(Dict2.get(key)):
            return False
    return True

def isIsomorphism(Dict1, Dict2):
    for key in Dict1:
        if len(Dict1.get(key)) != 1 or len(Dict2.get(key)) != 1:
            return key
    return True

def BranchingCheck(Dict1, Dict2, key) -> bool:
    a = 10
#     something happens


name = 'colorref_smallexample_2_49.grl'
RunIsomophismProgram(name)
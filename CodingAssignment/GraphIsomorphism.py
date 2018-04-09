from graph_io import *
from graph import *
import collections



def runProgram(namecolloref):
    with open(namecolloref) as f:
        L = load_graph(f, read_list=True)

    # Creating a vertex list of all vertices
    AList = CreateVertexList(L)
    # Setting initial colours and returning the maximum color
    max = SetInitialColour(AList)
    # Building a dictionary sorted on colours Dict(colour,list(nodes))
    kaas = BuildDict(AList)
    # While stuff is being changed in the dictionary do this:
    changed = True
    while changed:
        # Look for violations of neighbourhoods in colorsets
        stuff = Refine(kaas, max)
        # see whether something changed
        changed = stuff[0]
        # assign new max color
        max = stuff[1]

    i = 0
    for G in L[0]:
        name = 'mygraph' + str(i) + '.dot'
        with open(name, 'w') as f:
            write_dot(G, f)
        i += 1

def CreateVertexList(DataSet) -> list:
    VertexList = []
    for graph in DataSet[0]:
        VertexList.extend(graph.vertices)
    return VertexList

def SetInitialColour(List) -> int:
    max = 0
    for vertex in List:
        number = vertex.degree
        vertex.colornum = number
        if number > max:
            max = number
    return max

def BuildDict(List) -> dict:
    Dict = {}
    for vertex in List:
        if Dict.__contains__(vertex.colornum):
            Dict.get(vertex.colornum).append(vertex)
        else:
            Dict[vertex.colornum] = [vertex]
    return Dict

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

def BasicChecks(Dict1, Dict2) -> bool:
    if len(Dict1) != len(Dict2):
        return False
    for key in Dict1.keys():
        if len(Dict1.get(key)) != len(Dict.get(key)):
            return False

def BranchIsomorphism(Dict1, Dict2):





namecolloref = 'colorref_smallexample_4_16.grl'
runProgram(namecolloref)
from graph_io import *
from graph import *
import collections

with open('colorref_smallexample_2_49.grl') as f:
    L = load_graph(f, read_list = True)



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


AList = CreateVertexList(L)
max = SetInitialColour(AList)
kaas = BuildDict(AList)
changed = True
while changed:
    stuff = Refine(kaas,max)
    changed = stuff[0]
    max = stuff[1]

i = 0
for G in L[0]:
    name = 'mygraph' + str(i) + '.dot'
    with open(name,'w') as f:
        write_dot(G,f)
    i += 1
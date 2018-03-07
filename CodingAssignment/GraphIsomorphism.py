from graph_io import *
from graph import *

with open('colorref_smallexample_4_7.grl') as f:
    L = load_graph(f, read_list = True)

def compare_graphs(L):
    for x in L[0]:
        for y in x.vertices:
            y.colornum = len(y.incidence)
            print('node ' + str(y) + ' has ' + str(y.colornum) + ' connections')



compare_graphs(L)

G = L[0][0]
with open('mygraph.dot', 'w') as f:
    write_dot(G, f)
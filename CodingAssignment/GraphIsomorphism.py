from graph_io import *
from graph import *

with open('colorref_smallexample_4_7.grl') as f:
    L = load_graph(f, read_list = True)

def compare_graphs(L):
    
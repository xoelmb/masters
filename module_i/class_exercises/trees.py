from graphviz import Digraph

graph = Digraph('G', filename="my_graph", format="png", engine='dot')
graph.edge("A","C")
graph.edge("C","D")
graph.edge("C","E")
graph.edge("A","E")
graph.render()
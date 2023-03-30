from PIL import Image
import numpy as np
import networkx as nx

def load_image():
	size = 28, 28 # downsampling for easier computations

	# make sure that brain.tf is in the same directory as this file
	im = Image.open('brain.tif').convert('L')
	im.thumbnail(size, Image.Resampling.LANCZOS)
	print("Importing 'brain.tif' file for processing...\n")
	print(f"Downsizing to {size} pixels for sake of example\n")
	return im 

def create_graph(im):
	imarray = np.array(im).astype(float)

	height, width = imarray.shape

	graph = nx.Graph()

	print("Creating graph from pixels values \n")

	# add each pixel to the graph
	for i in range(height):
	    for j in range(width):
	        node = (i,j)
	        graph.add_node(node)

	# add edges to graph
	for i in range(height):
	    for j in range(width):
	        if i < height - 1:
	            weight = abs(imarray[i][j] - imarray[i+1][j])
	            graph.add_edge((i,j), (i+1,j), weight=weight)
	        if j < width - 1:
	            weight = abs(imarray[i][j] - imarray[i][j+1])
	            graph.add_edge((i,j), (i+1,j), weight=weight)

	# turn the nx graph into an adjacency list
	print("Converting graph to adjaceny list format \n")
	adj = {}
	for node in graph.nodes():
	    adj[node] = {}
	    for neighbor, weight in graph[node].items():
	        adj[node][neighbor] = weight["weight"]

	return adj


def prim_mst(adj):
	start = (0,0)

	MST = {start: None}

	print("Beginnig Prim's algorithm \n")

	#dictionary to keep track of the min edge weights for each node (start with all but start weights at inf)
	min_weights = {node: float('inf') for node in adj}
	min_weights[start] = 0

	unvisited_nodes = set(adj.keys())


	while unvisited_nodes:
	    
	    # minimum edge weight path
	    curr = min(unvisited_nodes, key=lambda node: min_weights[node])
	    
	    unvisited_nodes.remove(curr)
	    
	    MST[curr] = min_weights[curr]
	    
	    for neighbor, weight in adj[curr].items():
	        if neighbor in unvisited_nodes and weight < min_weights[neighbor]:
	            min_weights[neighbor] = weight
	print("Printing the MST: (format is node 1 -- weight -- node 2 ... node n)\n")
	for node, weight in MST.items():
	    if weight is not None:
	        print(node, " -- ", weight)



if __name__ == "__main__":
   brain_image = load_image()
   adjacency_list = create_graph(brain_image)
   prim_mst(adjacency_list)

   print("Program complete.")



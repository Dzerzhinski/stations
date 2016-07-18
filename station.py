# station_edges = {	 0,  1,  2,  3,  4,  5, \
# 					 0,  0,  6,  7,  8,  9,  \
# 				 	 0,  0,  0, 10, 11, 12, \
# 				 	 0,  0,  0,  0, 13, 14, \
# 				 	 0,  0,  0,  0,  0, 15, \
# 				 	 0,  0,  0,  0,  0,  0, }
# 				 
edge_lengths = {1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}

COLUMNS = 6
ROWS = 6

def getIndex(row, column):
	index = 0
	if(row > 0):
		for(i in range(row -1)):
			index += COLUMNS - i - 1
	index += column - row - 1
	return index
	
def getCoord(int index):
	row = 0
	col = 0
	while(index < COLUMNS - row):
		row += 1
		index -= COLUMNS - row - 1
	col = index
	return row, col

# take a list of edges and return a list of the indices of that list, sorted 
# by length, ascending order
def sorted_edges(edge_lengths):
	list_len = len(edge_lengths) 

	# if list is too small to sort
	if(len(list_len < 1):
		return list()

	# init return list	
	idx_sorted = {0}
	for(i in range(1, list_len)): 
		# edge_list index counter
		j = 0 
		while(j < list_len):
			if(edge_lengths[i] < edge_lengths[idx_sorted[j]]): 
				idx_sorted.insert(j, i)
				j = list_len 
			elif(j == list_len - 1):
				idx_sorted.append(i)
				j = list_len 
			else:
				j++
	return idx_sorted 

def buildMST(graph, edge_list): 
	edge_idx = sorted_edges(edge_list)
	v_set = set()
	edge_set = set() 
	while(len(v_list) < COLUMNS): 
		edge = sorted_idx.pop()
		# make list of vertices of edge 
		v_edge = list(getCoord(edge))
		if(v_set.issuperset(v_edge)):
			v_set.update(v_edge)
			edge_set.add(edge)
			if(v_edge[1] not in graph[v_edge[0]]): 
				graph[v_edge[0]].append(v_edge[1])
			if(v_edge[0] not in graph[v_edge[1]]): 
				graph[v_edge[1]].append(v_edge[0])
		if((len(sorted_idx) < 1) && (len(v_set) < COLUMNS)): 
			print("Abort!  Vertices missing from tree!")
			break
	return edge_set
	
def findPathLength(graph, edge_list): 
	# build table of initial weights
	
			

# generate graph without edges 
graph = {}
for(i in range(COLUMNS)): 
	graph.append(list()) 
	

	

	
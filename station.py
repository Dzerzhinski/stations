"""Matrix of edges i.e. the distances of routes between bus stops.  They 
    follow this key: 
            1  ::  Montlake Station
            2  ::  Green Lake P+R
            3  ::  Northgate Transit Center
            4  ::  Beacon Hill
            5  ::  Columbia City
            6  ::  Rainier Beach Stn
            7  ::  University of WA Stn
            8  ::  NW 54th + 30th (Ballard)
            9  ::  63rd Ave SW + SW Admiral Way
            10 ::  Capital Hill Stn
            11 ::  I District Stn
            12 ::  Westlake Stn
            13 ::  Denny Way + 2nd Ave
            14 ::  West Viewmont Way W + W Bertona St
            15 ::  W Nickerson St + 6th Ave W 
    Repeat entries are replaced with zeroes for convenience."""
EDGE_LENGTHS = [ \
                [0, 2.8, 4.9, 5.4, 6.5, 9.9, 10.5, 5.5, 10.2, 2.8, 4.5, 3.8, 4.3, 6.4, 3.8], \
                [0, 0, 2.0, 7.1, 8.6, 11.3, 2.4, 4.3, 12.2, 4.1, 5.9, 4.8, 5.1, 5.7, 3.9], \
                [0, 0, 0, 9.2, 10.6, 13.4, 4.4, 5.3, 14.3, 6.2, 7.9, 7.3, 7.5, 8.3, 5.7], \
                [0, 0, 0, 0, 2.0, 4.6, 5.7, 8.3, 6.6, 2.9, 1.7, 3.0, 3.9, 8.7, 6.8], \
                [0, 0, 0, 0, 0, 2.6, 6.8, 11.0, 8.1, 5.0, 3.7, 4.7, 5.7, 10.6, 8.3], \
                [0, 0, 0, 0, 0, 0, 10.2, 13.2, 9.5, 7.5, 6.4, 7.5, 8.4, 13.4, 11.5], \
                [0, 0, 0, 0, 0, 0, 0, 5.1, 11.8, 3.2, 5.3, 4.3, 4.9, 6.1, 3.8], \
                [0, 0, 0, 0, 0, 0, 0, 0, 12.8, 6.1, 6.9, 5.7, 5.6, 4.2, 2.7], \
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 9.6, 6.6, 7.7, 8.6, 13.1, 11.3], \
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.7, 1.0, 2.0, 6.8, 4.3], \
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.9, 6.7, 4.6], \
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 5.9, 3.4], \
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4.8, 3.4], \
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.2], \
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Ratio for cost benefit analysis.  See description in report.
RATIO = 7

# Dimensions of the array of edges
COLUMNS = 15
ROWS = 15

def convertEdgeArray(): 
    """Convert a matrix of edges to an indexed list of edges.
    
        Using the global variable matrix of distances between nodes (bus 
        stops), it returns the elements rearranged as an indexed list.  
        Entries are ordered left to right, top to bottom, and zeroes are 
        ignored."""
    # initialize return ovject.
    edges_list = list() 
    # populate list
    for i in range(0, ROWS - 1): 
        for j in range(i + 1, COLUMNS): 
            edges_list.append(EDGE_LENGTHS[i][j])
    return edges_list 

def getIndex(row, column):
    """Get index from row and column. 
    
        Taking the row and column of an element of the matrix of edges, it 
        returns the corresponding index of the edge from the list of edges.
        """
    index = 0
    if(row > 0):
        for i in range((row - 1)): 
            index += COLUMNS - i - 1
    index += column - row - 1
    return index
    
def getCoord(index):
    """Get coordinates from index.
    
        Taking the index of an edge from the list of edges, it returns the 
        row and column of the corresponding edge from the matrix of edges.  
        The row and column correspond to the two vertices, or stations, of 
        the route."""
    row = 0
    col = 0
    # The first column of the matrix is a zero vector, so the beginning of 
    # the list of edges doesn't correspond to the first element of the 
    # matrix.
    while(index > COLUMNS - row - 2):
        index -= COLUMNS - row - 1
        row += 1
    col = index + 1 + row
    return row, col
    
def getEdgeLength(v1, v2, edges):
    """Get length of an edge from its coordinates.
    
        I don't know why this would be useful.  It takes two vertices 
        (stations) and a list of edges as parameters, and returns the element 
        of the list, and edge, that corresponds to those two vertices."""
    # Row cannot be higher than the columns, based on the triangular nature 
    # of the matrix.
    if(v2 < v1): 
        temp = v1
        v1 = v2
        v2 = temp
    return edges[getIndex(v1, v2)] 

def sortedEdges(edges_list, edge_table):
    """Sort list of edges.
    
    This takes a list of integers representing edges (edge_list) and these 
    integers are indices for the list of edge weights, edge_table.  It returns 
    a list that is edge_list elements, sorted by the weights of the 
    corresponding edges, in descending order.  This is a necessary helper 
    function for Kruskal's algorithm in buildMST function."""
    list_len = len(edges_list) 

    # if list is too small to sort
    if(list_len < 1):
        return list()

    # initialize return list    
    idx_sorted = [edges_list[0]]
    # edge is the integer identifying the edge, and an index of edge_table
    for edge in edges_list[1:]: 
        # index of element of sorted list to test against edge
        j = 0 
        while(j < len(idx_sorted)):
            # insert case
            if(edge_table[edge] > edge_table[idx_sorted[j]]): 
                idx_sorted.insert(j, edge)
                j = len(idx_sorted) 
            # end of list case
            elif(j == len(idx_sorted) - 1):
                idx_sorted.append(edge)
                j = len(idx_sorted)  
            else:
                j += 1
    # debug variable
    idx_sorted_str = str([edge_table[i] for i in idx_sorted])
    return idx_sorted 
    
def hasCircuit(graph, addl_v): 
    """Return true if the graph includes a circuit. 
    
        This takes a graph, a list of lists where each outer list element 
        corresponds to a node of the graph, and each element of the inner 
        list represents nodes adjacent.  It also takes a list of two more 
        nodes representing a new edge to the graph.  It parses the graph 
        recursively and returns True if a circuit exists in the graph.  It 
        is implied that there is no circuit before the edge between the 
        elements of addl_v is added to the graph."""
    def trace(source, dest, vertex): 
        """Recurse and return True if a circuit exists.  
        
            This recurses through the nodes of the graph, which exists in the 
            scope inherited from the outer function.  It takes the source, 
            which is the node that was previously examined, the destination, 
            which is the node being examined now, and the vertex that 
            represents the start of the search for the circuit.  It is 
            implied that there is no circuit before the new edge (the edge 
            between the vertices of addl_v) is added to the graph.  It returns 
            True if there is a circuit detected, and False if the branch ends 
            without finding a circuit."""
        # Recursion limit
        if(vertex in graph[dest]): 
            return True
        else: 
            # recurse over adjacent nodes
            for v in graph[dest]: 
                # the first part of the Boolean expression ensures that the 
                # edge that was previously recursed over isn't traversed 
                # again, the second is the recursive call.
                if((v != source) and trace(dest, v, vertex)): 
                    return True
            return False
    # begin the recursion
    return trace(addl_v[0], addl_v[1], addl_v[0]) 
    

def buildMST(graph, edge_list): 
    """Build the minimal spanning tree.
    
        Use Kreskal's algorithm to build the tree from the list of edges 
        (edge_list parameter) and populate the graph (passed by reference) 
        with the tree.  Also returns a set of of the edges that make up the 
        graph."""
    # produce a sorted list of edges
    sorted_idx = sortedEdges(list(range(len(edge_list))), edge_list)
    # debug print    
    #print(sorted_idx) 
    # initiallie the set to return
    edge_set = set() 
    # build tree
    while(len(edge_set) < COLUMNS - 1): 
        if(len(sorted_idx) < 1): 
            print("Emergency! Tree ran out of edges!")
            break
        edge = sorted_idx.pop()
        # make list of vertices of edge 
        v_edge = list(getCoord(edge))
        # test if the new edge is valid
        if(not hasCircuit(graph, v_edge)):
            # add to graph and set representing edges of tree
            edge_set.add(edge)
            # debug variable
            e_str = str(edge_set)
            graph[v_edge[0]].append(v_edge[1])
            graph[v_edge[1]].append(v_edge[0])
    # debug variables
    size = len(edge_set)
    g_str = str(graph)
    e_str = str(edge_set)
    length_str = str([edge_list[i] for i in edge_set])
    # yaaaay
    return edge_set
    
def findPathLength(graph, edge_list, start, dest): 
    """Find the length of the shortest path. 
        
        Use Dijkstra's algorigthm to find the shortest path and calculate the 
        length of that path.  Takes the graph (showing adjacency of nodes) and 
        edge_list (showing length of edges).  Also takes as parameters the 
        starting and ending nodes.  Retuns the overall length, a floating 
        point number."""
    # build table of initial weights
    table = list()
    # build visited table
    # no need to check predecessors -- we need the length of the path, not 
    # the path itself.
    visited = list(range(COLUMNS))  
    # populate table of weights
    for i in range(COLUMNS):
        table.append(float('infinity'))
    table[start] = 0 
    current = start
    # counter for debug and error-checking
    counter = 0
    while(current != dest): 
        if(counter > COLUMNS): 
            # error handling
            print("Abort! Path search is broken!") 
            return float('infinity') 
        # update weights of nodes
        for i in graph[current]: 
            if(i in visited): 
                table[i] = table[current] + \
                    getEdgeLength(i, current, edge_list)
        # update visited list
        visited.remove(current) 
        if(len(visited) < 1): 
            # error handling
            print("Abort! No path to destination!")
            break
        # find node for next iteration
        current = visited[0] 
        for i in range(1, len(visited)): 
            if(table[visited[i]] < table[current]): 
                current = visited[i]
        # update debug counter
        counter += 1
    return table[current]
    
def calcMileage(graph, edge_table, addl_edge = None): 
    """Calculate rider-mileage of graph.
    
        Assuming that there is an equal amount of bidirectional traffic from 
        each node to every other node, we make this a unit of traffic.  So 
        considering the shortest path from one node to another multiplied by 
        the distance of that path, we have a "rider-mile" measurement of the 
        cost of travel over the graph.  Comparing two graphs, we can measure 
        the advantage of one graph over another by comparing this mileage.  
        This function accepts a graph as a parameter and returns the mileage 
        of that graph.  The indexed list of edge lengths is another required 
        parameter.  There is an optional parameter, addl_edge, that represents 
        an edge that could potentially be added to the graph, and the mileage 
        is calculated as if this edge were added.  This function is necessary 
        for the addBranch function which adds to the graph according to a 
        simple cost-benefit analysis.  It is dependent upon the 
        findPathLength function to calculate overall mileage."""
    # add optional additional edge
    if(addl_edge is not None): 
        # make a temporary copy so we can add the additional edge without 
        # mutating the graph
        temp_graph = graph.copy()
        v_list = list(getCoord(addl_edge)) 
        temp_graph[v_list[0]] = graph[v_list[0]].copy() 
        temp_graph[v_list[1]] = graph[v_list[1]].copy() 
        temp_graph[v_list[0]].append(v_list[1]) 
        temp_graph[v_list[1]].append(v_list[0]) 
    # if not using addl_edge parameter, use reference to original graph
    else: 
        temp_graph = graph
    # iterate over possible routes and add mileage
    mileage = 0
    for start in range(COLUMNS - 1): 
        for dest in range(start + 1, COLUMNS): 
            mileage += findPathLength(temp_graph, edge_table, start, dest)
    return mileage
    
def addBranches(graph, edge_table, branches, threshold): 
    expand = True 
    unused = [i for i in range(len(edge_table)) if i not in branches] 
    while(expand): 
        base_miles = calcMileage(graph, edge_table) 
        new_miles = list()
        cba_ratio = list() 
        high_idx = 0
        for i in range(len(unused)): 
            if(i > len(edge_table)): 
                print("Oh shit I'm out of bounds!") 
            new_miles.append(calcMileage(graph, edge_table, unused[i]))
            cba_ratio.append((base_miles - new_miles[i]) / edge_table[unused[i]])
            if(cba_ratio[i] > cba_ratio[high_idx]): 
                high_idx = i
        if(cba_ratio[high_idx] > threshold): 
            # add branch to graph 
            branches.add(unused[high_idx]) 
            v_list = list(getCoord(unused[high_idx])) 
            graph[v_list[0]].append(v_list[1]) 
            graph[v_list[1]].append(v_list[0]) 
            unused.pop(high_idx) 
        else: 
            expand = False 

def main(): 
    edge_table = convertEdgeArray() 
    
    # generate graph without edges 
    graph = list()
    for i in range(COLUMNS): 
        graph.append(list()) 
    
    tree_set = buildMST(graph, edge_table) 
    print(graph) 
    print(calcMileage(graph, edge_table)) 
    
    # Assuming that populations and traffic are evenly distributed across the 
    # city, such that there are equal numbers of riders originating from 
    # every node, and 1/14th of the of the riders from a specific node will 
    # travel to any other node.  So we will assume 14 "units" of bidirectional 
    # traffic will come/go from any individual node.
    # This gives us a rough estimate of the value.  If 14 rider-units will 
    # benefit from adding a mile of raod, it is cost-effective.  Taking that 
    # further, if one mile of bike-friendly road will save a rider (or rather, 
    # one unit of bidirectional bike traffic) 14 miles of travel, the road 
    # improvement can be considered cost-effective.
    # So, we consider the sum of miles traveled by each rider unit, divide it 
    # by the cost of the network, and provided this ratio is above fourteen, 
    # it is a cost-effective improvement.  
    addBranches(graph, edge_table, tree_set, RATIO)    
    num_rte = str(len(tree_set))
    print(graph) 
    print(calcMileage(graph, edge_table)) 
    
main() 

foo = getCoord(90)
bar = getCoord(0)
    

    

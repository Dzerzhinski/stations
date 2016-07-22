import locale 
import networkx as nx
import matplotlib.pyplot as plt 
locale.setlocale(locale.LC_ALL, '') 

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
    
STATIONS_SHORT = ["Montlake", \
                    "Greenlake", \
                    "Northgate", \
                    "Beacon Hill", \
                    "Columbia City", \
                    "Rainier Beach", \
                    "UW", \
                    "Ballard", \
                    "West Seattle", \
                    "Capitol Hill", \
                    "I District", \
                    "Westlake", \
                    "Lower Queen Anne", \
                    "Magnolia", \
                    "N Queen Anne"]
                    
STATIONS_POS = [(47.644766, -122.302764), \
                    (47.676527, -122.320804), \
                    (47.702234, -122.327502), \
                    (47.579491, -122.311751), \
                    (47.559884, -122.292623), \
                    (47.522491, -122.279673), \
                    (47.649796, -122.303808), \
                    (47.668685, -122.394782), \
                    (47.576149, -122.413351), \
                    (47.619921, -122.320346), \
                    (47.598317, -122.328144), \
                    (47.611644, -122.337146), \
                    (47.618822, -122.353437), \
                    (47.650616, -122.409524), \
                    (47.651807, -122.364491)]
    
STATIONS = ["Montlake Station", \
                "Green Lake Park and Ride", \
                "Northgate Transit Center", \
                "Beacon Hill Station", \
                "Columbia City Station", \
                "Rainier Beach Station", \
                "University of Washington Station", \
                "NW 54th and 30th", \
                "63rd Ave SW and SW Admiral Way", \
                "Capitol Hill Station", \
                "International District Station", \
                "Westlake Station", \
                "Denny Way and 2nd Ave", \
                "West Viewmont Way W and Bertona St", 
                "W Nickerson St and 6th Ave W"]
EDGE_LENGTHS = [ \
                [0,  2.8,  4.9,  5.4,  6.5,  9.9, 10.5,  5.5, 10.2,  2.8,  4.5,  3.8,  4.3, 6.4, 3.8], \
                [0,    0,  2.0,  7.1,  8.6, 11.3,  2.4,  4.3, 12.2,  4.1,  5.9,  4.8,  5.1, 5.7, 3.9], \
                [0,    0,    0,  9.2, 10.6, 13.4,  4.4,  5.3, 14.3,  6.2,  7.9,  7.3,  7.5, 8.3, 5.7], \
                [0,    0,    0,    0,  2.0,  4.6,  5.7,  8.3,  6.6,  2.9,  1.7,  3.0,  3.9, 8.7, 6.8], \
                [0,    0,    0,    0,    0,  2.6,  6.8, 11.0,  8.1,  5.0, 3.7, 4.7, 5.7, 10.6, 8.3], \
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

# cost per mile of adding bike lanes
COST_PER_MILE = 10000

def normStationPos(station_list): 
    lat_avg = 0
    long_avg = 0
    for i in station_list: 
        lat_avg += i[0] 
        long_avg += i[1] 
    lat_avg = lat_avg / len(station_list) 
    long_avg = long_avg / len(station_list) 
    norm_list = []
    for i in station_list: 
        lat = i[0] - lat_avg
        long = i[1] - long_avg
        norm_list.append((long, lat)) 
    return norm_list

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

#def getIndex(row, column):
#    """Get index from row and column. 
#    
#        Taking the row and column of an element of the matrix of edges, it 
#        returns the corresponding index of the edge from the list of edges.
#        """
#    if(row > column): 
#        r = column
#        c = row
#    else: 
#        r = row
#        c = column
#    index = 0
#    if(r > 0):
#        for i in range(r): 
#            index += COLUMNS - i - 2
#    index += c - r - 1
#    return index
#    
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
    
#def getEdgeLength(v1, v2, edges):
#    """Get length of an edge from its coordinates.
#    
#        I don't know why this would be useful.  It takes two vertices 
#        (stations) and a list of edges as parameters, and returns the element 
#        of the list, and edge, that corresponds to those two vertices."""
#    # Row cannot be higher than the columns, based on the triangular nature 
#    # of the matrix.
#    if(v2 < v1): 
#        temp = v1
#        v1 = v2
#        v2 = temp
#    return edges[getIndex(v1, v2)] 

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
                    getEdge(i, current)
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
    """Add branches to tree as is cost-effective. 
    
        Assuming that the graph is minimally spanning, this function examines 
        unused edges and adds them to the graph.  It does so iteratively, 
        first adding the edge that has the most gain to the cost-benefit 
        analysis, and ending when it cannot find an edge whose cost-benefit 
        ratio that exceeds the parameter threshold.  The graph to which 
        branches are added is passed by reference in parameter graph, the 
        indexed list of edge lengths is passed in parameter edge_table, the 
        list of edges that compose the graph is passed by reference in 
        parameter branches.  It is dependent upon the calcMileage function."""
    expand = True 
    # build list of unused edges
    unused = [i for i in range(len(edge_table)) if i not in branches] 
    # iterate until there is no cost-benefit advantage to adding additional 
    # branches
    while(expand): 
        # calculate rider-miles of graph in its current state 
        base_miles = calcMileage(graph, edge_table) 
        # initialize variables
        new_miles = list()
        cba_ratio = list() 
        # index of edge within list of unused edges with highest advantage
        # note: the indexed element is itself an index to edge_table 
        high_idx = 0
        # iterate over unused edges
        for i in range(len(unused)): 
            # error/debug handling
            if(i > len(edge_table)): 
                print("Oh shit I'm out of bounds!") 
            # calculate rider-mile total of graph with this edge 
            new_miles.append(calcMileage(graph, edge_table, unused[i])) 
            # calculate advantage of adding this edge: 
            # advantage is ratio of difference in total rider-miles by adding 
            # new edge over length (cost) of new edge
            cba_ratio.append((base_miles - new_miles[i]) / edge_table[unused[i]])
            # test advantage             
            if(cba_ratio[i] > cba_ratio[high_idx]): 
                high_idx = i
        # add the edge that gives the most benefit to tree, providing it meets 
        # the threshold of cost-benefit advantage 
        if(cba_ratio[high_idx] > threshold): 
            # add branch to graph 
            branches.add(unused[high_idx]) 
            v_list = list(getCoord(unused[high_idx])) 
            graph[v_list[0]].append(v_list[1]) 
            graph[v_list[1]].append(v_list[0]) 
            unused.pop(high_idx) 
        # end iteration 
        else: 
            expand = False 

def getEdge(n1, n2): 
    if(n1 > n2): 
        row = n2
        column = n1
    else: 
        row = n1
        column = n2
    return EDGE_LENGTHS[row][column]

def printGraph(graph, edge_table): 
    """Print graph.
    
        Prints the graph with each station listing its adjacent stations.  
        Takes graph (by reference) as parameter."""
    for stn in range(len(graph)): 
        str_routes = str(STATIONS[stn]) + " => "
        if(len(graph[stn]) > 0): 
            for adj in graph[stn][:-1]:  
                str_routes += str(STATIONS[adj]) + \
                        " ({0}), ".format(getEdge(stn, adj))
            str_routes += str(STATIONS[graph[stn][-1]]) + \
                            " ({0})".format(getEdge(stn, graph[stn][-1]))
        print(str_routes) 
        
def sumEdges(tree, edge_table): 
    """Sum the weight of edges in a tree.
    
        Helper function to calculate total weight of all edges in the graph.  
        Takes the tree to be summed and a table of edge weights as 
        parameters.  Returns the total weight.  In this case, the "weight" of 
        edges correspond to the length of the routes they represent."""
    ttl = 0
    for edge in tree: 
        ttl += edge_table[edge] 
    return ttl

def main(): 
    """Execute algorithm generate trees.
    
        Overall process managed through main function for convenience."""
    # convert matrix of edge lengths to indexed list 
    edge_table = convertEdgeArray() 
    
    # generate graph without edges
    # each element index corresponds to a node.  Each element is a list of 
    # nodes adjacent to the indexed node.  Initialied to nodes without edges 
    graph = list()
    for i in range(COLUMNS): 
        graph.append(list()) 
    
    # generate minimum spanning tree solution 
    tree_set = buildMST(graph, edge_table) 
    tree_str = str(tree_set)
    print("Minimum Spanning Tree: ") 
    printGraph(graph, edge_table) 
    length_mst = sumEdges(tree_set, edge_table) 
    print("Total length of all routes: {0:.2f} miles".format(length_mst)) 
    print("Total cost of plan: {}".format( \
                    locale.currency((COST_PER_MILE * length_mst), \
                    grouping = True)))
                    
    # draw using NetworkX 
    g = nx.Graph() 
    g_labels = {} 
    for i in range(COLUMNS): 
        g.add_node(i, name = STATIONS_SHORT[i])
        g_labels[i] = STATIONS_SHORT[i]
    for v in range(len(graph)): 
        for a in graph[v]: 
            if(a > v): 
                g.add_edge(v, a) 
    g_pos = normStationPos(STATIONS_POS) 
    nx.draw(g, pos = g_pos, labels = g_labels)
    plt.savefig("mst.png")    
    plt.show()
    
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
    print("Advantageous Tree: ") 
    printGraph(graph, edge_table) 
    length_addl = sumEdges(tree_set, edge_table) 
    print("Total length of all routes: {0:.2f} miles".format(length_addl)) 
    print("Total cost of plan: {}".format( \
                    locale.currency((COST_PER_MILE * length_addl), \
                    grouping = True)))
    # draw using NetworkX 
    g = nx.Graph() 
    g_labels = {} 
    for i in range(COLUMNS): 
        g.add_node(i, name = STATIONS_SHORT[i])
        g_labels[i] = STATIONS_SHORT[i]
    for v in range(len(graph)): 
        for a in graph[v]: 
            if(a > v): 
                g.add_edge(v, a) 
    g_pos = normStationPos(STATIONS_POS) 
    nx.draw(g, pos = g_pos, labels = g_labels)
    plt.savefig("full.png")    
    plt.show()


main() 

foo = getCoord(90)
bar = getCoord(0)
    
for i in range(len(EDGE_LENGTHS)): 
    line = str(i + 1)
    for j in range(len(EDGE_LENGTHS[i])): 
        line += " & " + str(EDGE_LENGTHS[i][j]) 
    line += " \\\\"
    print(line) 

    

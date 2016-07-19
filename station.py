# station_edges = {     0,  1,  2,  3,  4,  5, \
#                      0,  0,  6,  7,  8,  9,  \
#                       0,  0,  0, 10, 11, 12, \
#                       0,  0,  0,  0, 13, 14, \
#                       0,  0,  0,  0,  0, 15, \
#                       0,  0,  0,  0,  0,  0, }
# edge_lengths = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
#                  

# A    -
# B   2.8   - 
# C   4.9  2.0   -
# D   5.4  7.1  9.2   -
# E   6.5  8.6 10.6  2.0   -
# F   9.9 11.3 13.4  4.6  2.6   -
# G  10.5  2.4  4.4  5.7  6.8 10.2   -
# H   5.5  4.3  5.3  8.3 11.0 13.2  5.1   -
# I  10.2 12.2 14.3  6.6  8.1  9.5 11.8 12.8   -
# J   2.8  4.1  6.2  2.9  5.0  7.5  3.2  6.1  9.6   -
# K   4.5  5.9  7.9  1.7  3.7  6.4  5.3  6.9  6.6  1.7   -
# L   3.8  4.8  7.3  3.0  4.7  7.5  4.3  5.7  7.7  1.0  1.0   -
# M   4.3  5.1  7.5  3.9  5.7  8.4  4.9  5.6  8.6  2.0  1.9  1.0   -
# N   6.4  5.7  8.3  8.7 10.6 13.4  6.1  4.2 13.1  6.8  6.7  5.9  4.8   -
# O   3.8  3.9  5.7  6.8  8.3 11.5  3.8  2.7 11.3  4.3  4.6  3.4  3.4  3.2   -



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






COLUMNS = 15
ROWS = 15

def convertEdgeArray(): 
    edges_list = list() 
    for i in range(0, ROWS): 
        for j in range(i + 1, COLUMNS - 1): 
            edges_list.append(EDGE_LENGTHS[i][j])
    return edges_list 

def getIndex(row, column):
    index = 0
    if(row > 0):
        for i in range((row - 1)): 
            index += COLUMNS - i - 1
    index += column - row - 1
    return index
    
def getCoord(index):
    row = 0
    col = 0
    while(index > COLUMNS - row):
        row += 1
        index -= COLUMNS - row - 1
    col = index
    return row, col
    
def getEdgeLength(v1, v2, edges):
    if(v2 < v1): 
        temp = v1
        v1 = v2
        v2 = temp
    return edges[getIndex(v1, v2)] 

# take a list of edges and return a list of the indices of that list, sorted 
# by length, ascending order
def sortedEdges(edges_list, edge_table):
    list_len = len(edges_list) 

    # if list is too small to sort
    if(list_len < 1):
        return list()

    # init return list    
    idx_sorted = [edges_list[0]]
    # n is the element to insert into sorted list
    for edge in edges_list[1:]: 
        # index of element of sorted list to test against i
        j = 0 
        while(j < len(idx_sorted)):
            # insert case
            if(edge_table[edge] < edge_table[idx_sorted[j]]): 
                idx_sorted.insert(j, edge)
                j = len(idx_sorted) 
            # end of list case
            elif(j == len(idx_sorted) - 1):
                idx_sorted.append(edge)
                j = len(idx_sorted)  
            else:
                j += 1
    return idx_sorted 

def buildMST(graph, edge_list): 
    sorted_idx = sortedEdges(list(range(len(edge_list))), edge_list)
    print(sorted_idx) 
    v_set = set()
    edge_set = set() 
    while(len(v_set) < COLUMNS): 
        edge = sorted_idx.pop()
        # make list of vertices of edge 
        v_edge = list(getCoord(edge))
        if(not v_set.issuperset(v_edge)):
            v_set.update(v_edge)
            edge_set.add(edge)
            e_str = str(edge_set)
            if(v_edge[1] not in graph[v_edge[0]]): 
                graph[v_edge[0]].append(v_edge[1])
            if(v_edge[0] not in graph[v_edge[1]]): 
                graph[v_edge[1]].append(v_edge[0])
        if((len(sorted_idx) < 1) and (len(v_set) < COLUMNS)): 
            print("Abort!  Vertices missing from tree!")
            break
    size = len(edge_set)
    v_str = str(v_set)
    e_str = str(edge_set)
    return edge_set
    
def findPathLength(graph, edge_list, start, dest): 
    # build table of initial weights
    table = list()
    visited = list(range(COLUMNS))  
    for i in range(COLUMNS):
        table.append(float('infinity'))
    table[start] = 0 
    current = start
    counter = 0
    while(current != dest): 
        print(current) 
        if(counter > COLUMNS): 
            print("Abort! Path search is broken!") 
            return float('infinity') 
        for i in graph[current]: 
            if(i in visited): 
                table[i] = table[current] + \
                    getEdgeLength(i, current, edge_list)
        print(current) 
        visited.remove(current) 
        if(len(visited) < 1): 
            print("Abort! No path to destination!")
            break
        current = visited[0] 
        for i in range(1, len(visited)): 
            if(table[visited[i]] < table[current]): 
                current = visited[i]
        counter += 1
    return table[current]
    
def calcMileage(graph, edge_table, addl_edge = None): 
    if(addl_edge is not None): 
        temp_graph = graph.copy()
        v_list = list(getCoord(addl_edge)) 
        temp_graph[v_list[0]] = graph[v_list[0]].copy() 
        temp_graph[v_list[1]] = graph[v_list[1]].copy() 
        temp_graph[v_list[0]].append(v_list[1]) 
        temp_graph[v_list[1]].append(v_list[0]) 
    else: 
        temp_graph = graph
    mileage = 0
    for start in range(COLUMNS - 1): 
        for dest in range(start + 1, COLUMNS): 
            mileage += findPathLength(graph, edge_table, start, dest)
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
            new_miles.append(calcMileage(graph, edge_table, unused[i]))
            cba_ratio.append((new_miles[i] - base_miles) / edge_table[unused[i]])
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
    addBranches(graph, edge_table, tree_set, 14)    
    print(graph) 
    print(calcMileage(graph, edge_table)) 
    
main() 

    
    

    

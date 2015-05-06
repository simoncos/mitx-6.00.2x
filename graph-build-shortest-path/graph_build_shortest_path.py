# -*- coding: utf-8 -*-
# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    print "Loading map from file..."
    g = WeightedDigraph()
    inFile = open(mapFilename,'r',0)
    while 1:
        line = inFile.readline()
        if not line:
            break
        edgeDataList = string.split(line)    
        try:
            g.addNode(Node(edgeDataList[0]))            
        except:
            pass
        try:
            g.addNode(Node(edgeDataList[1]))            
        except:
            pass
        g.addEdge(WeightedEdge(Node(edgeDataList[0]),Node(edgeDataList[1]),int(edgeDataList[2]),int(edgeDataList[3])))
    return g
    

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    global validPaths # 储存所有两点间路径，在递归算法DFSFindValidPath里无法实现，只能用全局变量
    validPaths = []
    DFSFindValidPath(digraph,start,end)
    satisfingPaths = validPaths[:]
    #print satisfingPaths
    # 去除超过阈值的路径,若阈值内路径数为0，raise异常
    for v in validPaths:
        if calculatePathDistance(digraph,v)[0] > maxTotalDist or \
        calculatePathDistance(digraph,v)[1] > maxDistOutdoors:
            satisfingPaths.remove(v)
    #print satisfingPaths    
    if satisfingPaths == []:
        raise ValueError("No Valid Paths")
    # 寻找最短路径
    leastTotalDistance = None
    shortestPath = None
    for s in satisfingPaths:
        pathTotalDist = calculatePathDistance(digraph,s)[0]
        if leastTotalDistance == None or \
            pathTotalDist < leastTotalDistance:
            leastTotalDistance = pathTotalDist
            shortestPath = s

    shortestPath_str = []       
    for node in shortestPath:
        shortestPath_str.append(str(node))
    return shortestPath_str # 将path中的数据从Node转为string，以满足题目输出要求

def DFSFindValidPath(digraph, start, end, path = []):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    path = path + [Node(start)] # path中存储的是Node类型
    #print 'Current dfs path:', path
    if Node(start) == Node(end):
        validPaths.append(path)
    for node in digraph.childrenOf(Node(start)):
        if node not in path: #avoid cycles # 若path中类型不是Node，此行会报错
            newPath = DFSFindValidPath(digraph,node,end,path)
            if newPath != None:
                return newPath

def calculatePathDistance(digraph, path):  #计算一条path的总距离及户外总距离
    totalDistance = 0
    totalOutdoorDistance = 0
    for i in range(len(path)-1): 
        #{a: [ [b,(2,1)], [c,(3,2)]], b: [[c,(4,2)]], c:[] }
        for edgeData in digraph.edges[path[i]]:
            if edgeData[0] == path[i+1]:
                totalDistance += float(edgeData[1][0])
                totalOutdoorDistance += float(edgeData[1][1])
                break
    return totalDistance,totalOutdoorDistance

# g=load_map('mit_map.txt')
# print bruteForceSearch(g, '32', '36', 100, 100)

#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    #If you come across a path that is longer than your shortest path found so far, 
    #then you know that this longer path cannot be your solution, 
    #so there is no point in continuing to traverse its children and 
    #discover all paths that contain this sub-path.

    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    global leastTotalDistance_a, shortestPath_a # 与bruteForceSearch()中的变量区分 # global????
    leastTotalDistance_a = max
    shortestPath_a = []
    DFSFindShortestPath(digraph,start,end,maxTotalDist,maxDistOutdoors)
    if shortestPath_a == []:
        raise ValueError("No Valid Paths")

    shortestPath_str = []       
    for node in shortestPath_a:
        shortestPath_str.append(str(node))
    return shortestPath_str # 将path中的数据从Node转为string，以满足题目输出要求

def DFSFindShortestPath(digraph, start, end, maxTotalDist, maxDistOutdoors, path = []):
    global leastTotalDistance_a, shortestPath_a # global????
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    path = path + [Node(start)] # path中存储的是Node类型
    #print 'Current dfs path:', path
    if Node(start) == Node(end):
        totalDistance,totalOutdoorDistance = calculatePathDistance(digraph,path)
        if totalDistance <= maxTotalDist and totalOutdoorDistance <= maxDistOutdoors:
            if totalDistance < leastTotalDistance_a:
                shortestPath_a = path
                leastTotalDistance_a = totalDistance
    for node in digraph.childrenOf(Node(start)):
        if node not in path: #avoid cycles # 若path中类型不是Node，此行会报错
            newPath = DFSFindShortestPath(digraph,node,end,maxTotalDist,maxDistOutdoors,path)
            if newPath != None:
                if calculatePathDistance(newPath)[0] >= leastTotalDistance_a:
                    break
                return newPath    

g = load_map('mit_map.txt')
print directedDFS(g, '32', '36', 100, 100)

# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
# if __name__ == '__main__':
#     Test cases
#     mitMap = load_map("mit_map.txt")
#     print isinstance(mitMap, Digraph)
#     print isinstance(mitMap, WeightedDigraph)
#     print 'nodes', mitMap.nodes
#     print 'edges', mitMap.edges


#     LARGE_DIST = 1000000

#     Test case 1
#     print "---------------"
#     print "Test case 1:"
#     print "Find the shortest-path from Building 32 to 56"
#     expectedPath1 = ['32', '56']
#     brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
#     dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath1
#     print "Brute-force: ", brutePath1
#     print "DFS: ", dfsPath1
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

#     Test case 2
#     print "---------------"
#     print "Test case 2:"
#     print "Find the shortest-path from Building 32 to 56 without going outdoors"
#     expectedPath2 = ['32', '36', '26', '16', '56']
#     brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
#     dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
#     print "Expected: ", expectedPath2
#     print "Brute-force: ", brutePath2
#     print "DFS: ", dfsPath2
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
#     print "---------------"
#     print "Test case 3:"
#     print "Find the shortest-path from Building 2 to 9"
#     expectedPath3 = ['2', '3', '7', '9']
#     brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath3
#     print "Brute-force: ", brutePath3
#     print "DFS: ", dfsPath3
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
#     print "---------------"
#     print "Test case 4:"
#     print "Find the shortest-path from Building 2 to 9 without going outdoors"
#     expectedPath4 = ['2', '4', '10', '13', '9']
#     brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
#     dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
#     print "Expected: ", expectedPath4
#     print "Brute-force: ", brutePath4
#     print "DFS: ", dfsPath4
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

#     Test case 5
#     print "---------------"
#     print "Test case 5:"
#     print "Find the shortest-path from Building 1 to 32"
#     expectedPath5 = ['1', '4', '12', '32']
#     brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath5
#     print "Brute-force: ", brutePath5
#     print "DFS: ", dfsPath5
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
#     print "---------------"
#     print "Test case 6:"
#     print "Find the shortest-path from Building 1 to 32 without going outdoors"
#     expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
#     brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
#     dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
#     print "Expected: ", expectedPath6
#     print "Brute-force: ", brutePath6
#     print "DFS: ", dfsPath6
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
#     print "---------------"
#     print "Test case 7:"
#     print "Find the shortest-path from Building 8 to 50 without going outdoors"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr

#     Test case 8
#     print "---------------"
#     print "Test case 8:"
#     print "Find the shortest-path from Building 10 to 32 without walking"
#     print "more than 100 meters in total"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr

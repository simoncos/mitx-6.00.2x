# -*- coding: utf-8 -*-
# 6.00.2x Problem Set 5
# Graph optimization
#
# A set of data structures to represent graphs
#

class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method
        # Think: Why would we want to do this?
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)

class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[Node(k)]: #注意是Node(key)而非str(key)
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]

class WeightedEdge(Edge):
    def __init__(self,src,dest,weight1,weight2):
        Edge.__init__(self,src,dest)
        self.weight1=weight1
        self.weight2=weight2
    def getTotalDistance(self):
        return self.weight1
    def getOutdoorDistance(self):
        return self.weight2
    def __str__(self):
        # a->b (15, 10)
        return str(self.src) + '->' + str(self.dest) + ' (' + str(self.weight1) + ',' + str(self.weight2) + ')' 
    
class WeightedDigraph(Digraph):
    def _init_(self,nodes,edges):
        Digraph.__init__(self,nodes,edges)
    def addEdge(self,edge):
        src = edge.getSource()
        dest = edge.getDestination()
        weight1 = edge.getTotalDistance()
        weight2 = edge.getOutdoorDistance()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in WeightedGraph')
        # {a: [ [b,(2,1)], [c,(3,2)]], b: [[c,(4,2)]], c:[] }
        self.edges[src].append([dest,(weight1,weight2)])
    def childrenOf(self,node):
        children = []
        for edge in self.edges[node]:
            children.append(edge[0])
        return children
    def __str__(self):
        '''
        a->b (15.0, 10.0)
        a->c (14.0, 6.0)
        b->c (3.0, 1.0)
        '''
        res = ''
        for key in self.edges:
            for data in self.edges[Node(key)]: #注意是Node(key)而非str(key)
                # 将 每次循环生成的res后面新增一行数据
                res = '{0}{1}->{2} ({3},{4})\n'.format(res, key, data[0], float(data[1][0]),float(data[1][1]))
        return res[:-1] #去掉最后一行（\n带来的空行）


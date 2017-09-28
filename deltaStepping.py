#!usr/bin/env python

'''
Delta Stepping Algorithm implementation of SSSP

Author : Prateek Srivastava
Date Created : 09-23-2017

Acknowledgements:
Special Thanks to Marcin J Zalewski

Paper :
@article{meyer_-stepping:_2003,
       title = {Δ-stepping: a parallelizable shortest path algorithm},
       volume = {49},
       issn = {0196-6774},
       shorttitle = {Δ-stepping},
       url = {http://www.sciencedirect.com/science/article/pii/S0196677403000762},
       doi = {10.1016/S0196-6774(03)00076-2},
'''

import sys
from collections import defaultdict, OrderedDict
from math import ceil


class Graph:
    """ Graph creation courtesy : https://gist.github.com/econchick/4666413 """

    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}
        self.delta = int(sys.argv[1])
        self.propertyMap = {}
        self.workItems = []
        self.sourceVertex = int(sys.argv[2])
        self.infinity = 999999999
        self.B = OrderedDict()

    def add_node(self, node_label):
        self.nodes.add(node_label)

    def add_edge(self, from_node, to_node, distance):

        if from_node not in self.nodes:
            self.add_node(from_node)
        if to_node not in self.nodes:
            self.add_node(to_node)

        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance

    def readGraphFile(self, filename):
        with open(filename) as f:
            fileList = list(f)
            fileList = [[int(i) for i in x.strip('\n').split()] for x in fileList]
        for edge in fileList:
            self.add_edge(edge[0], edge[1], edge[2])

    def relax(self, w, x):

        """
        This function relaxes a bucket i.e. if the distance of a vertex is less than the already existing distance in
        the property map then, the vertex is removed from the bucket and reinserted in the new bucket

        x is the distance of the vertex and w is the index of the vertex in the property map
        """

        if x < self.propertyMap[w]:

            # check if there is an entry of w in the dictionary B
            if self.propertyMap[w] != self.infinity:
                if w in self.B[ceil(self.propertyMap[w] / self.delta)]:
                    # check if the vertex is in the wrong bucket
                    if ceil(x / self.delta) != ceil(self.propertyMap[w] / self.delta):
                        self.B[ceil(self.propertyMap[w] / self.delta)].remove(w)
                    else:
                        self.B[ceil(x / self.delta)].append(w)

            # if the dictionary entry does not exist
            else:
                self.B[ceil(x / self.delta)] = [w]

            # update the property map
            self.propertyMap[w] = x

    def findRequests(self, vertices):
        tmp = {}
        edgeVectors = []
        for u in vertices:
            for v in self.edges[u]:
                tmp[v] = self.propertyMap[u] + self.distances[(u, v)]
        return tmp

    def relaxRequests(self, request):
        for key, value in request.items():
            self.relax(key, value)

    def deltaStepping(self):

        
        # initialize property map
        for node in self.nodes:
            self.propertyMap[node] = self.infinity
        self.relax(self.sourceVertex, 0)
        while self.B:
            i = min(self.B.keys())
            iValue = self.B[i]
            del self.B[i]
            Req = self.findRequests(iValue)
            self.relaxRequests(Req)


def main():
    g = Graph()
    g.readGraphFile('sampleGraph.txt')
    g.deltaStepping()
    print("The shortest path from ", g.sourceVertex, " is ", g.propertyMap)


if __name__ == '__main__':
    main()

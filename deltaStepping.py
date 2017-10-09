#!/usr/bin/env python

"""
This code is implementation of sequential Delta Stepping

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
"""

import sys
from collections import defaultdict, OrderedDict
from math import ceil


class Graph:
    """ Graph creation courtesy : https://gist.github.com/econchick/4666413 """

    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}
        self.delta = 5
        self.propertyMap = {}
        self.workItems = []
        self.sourceVertex = 0
        self.infinity = 999999999
        self.totalNodes = 0
        self.totalEdges = 0
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

    def readGRFile(self, filename):
        ctr = -1
        with open(filename, 'r') as f:
            for line in f:
                if ctr == -1:
                    ctr += 1
                    tmp = [int(x) for x in line.strip('\n').split()]
                    if int(tmp[2]) == 1:
                        self.totalNodes = int(tmp[0])
                        self.totalEdges = int(tmp[1])
                        for x in range(0,self.totalNodes):
                            self.add_node(x)
                    else:
                        print("Error Can't print this type of a graph")
                        exit(1)
                else:
                    tmp = [int(x) for x in line.strip('\n').split()]
                    for num in range(0, len(tmp), 2):
                        self.add_edge(ctr, tmp[num], tmp[num + 1])
                    ctr += 1

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

    def findRequests(self, vertices, kind):

        tmp = {}
        for u in vertices:
            for v in self.edges[u]:
                edgeWeight = self.propertyMap[u] + self.distances[(u, v)]
                if kind == 'light':
                    if edgeWeight <= self.delta:
                        tmp[v] = edgeWeight
                elif kind == 'heavy':
                    if edgeWeight > self.delta:
                        tmp[v] = edgeWeight
                else:
                    return "Error: No such kind of edges " + kind
        return tmp

    def relaxRequests(self, request):
        for key, value in request.items():
            self.relax(key, value)

    def deltaStepping(self):
        """ This is the main function to implement the algorithm """
        for node in self.nodes:
            self.propertyMap[node] = self.infinity
        self.relax(self.sourceVertex, 0)
        while self.B:
            i = min(self.B.keys())
            r = []
            while i in self.B:
                req = self.findRequests(self.B[i], 'light')
                r += self.B[i]
                del self.B[i]
                self.relaxRequests(req)
            req = self.findRequests(r, 'heavy')
            self.relaxRequests(req)


def main():
    g = Graph()
    # g.readGraphFile('sampleGraph.txt')
    g.readGRFile('file11.gr')
    g.deltaStepping()
    print("The shortest path from ", g.sourceVertex, " is ", g.propertyMap)


if __name__ == '__main__':
    main()

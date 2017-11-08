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

from math import ceil
import networkx as nx


class algorithm:
    def __init__(self):
        self.distances = {}
        self.delta = 5
        self.propertyMap = {}
        self.workItems = []
        self.sourceVertex = 0
        self.infinity = 999999999
        self.totalNodes = 0
        self.totalEdges = 0
        self.B = {}

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

    def findRequests(self, vertices, kind, G):

        tmp = {}
        for u in vertices:
            for v in G.neighbors(u):
                edgeWeight = self.propertyMap[u] + G.get_edge_data(u, v)['weight']
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

    def deltaStepping(self, G):
        """ This is the main function to implement the algorithm """
        for node in G.nodes():
            self.propertyMap[node] = self.infinity

        self.relax(self.sourceVertex, 0)
        while self.B:
            i = min(self.B.keys())
            r = []
            while i in self.B:
                req = self.findRequests(self.B[i], 'light', G)
                r += self.B[i]
                del self.B[i]
                self.relaxRequests(req)
            req = self.findRequests(r, 'heavy', G)
            self.relaxRequests(req)

    def metisReader(self, filename, G):
        ctr = -1
        with open(filename, 'r') as f:
            for line in f:
                if ctr == -1:
                    ctr += 1
                    tmp = [int(x) for x in line.strip('\n').split()]
                    if int(tmp[2]) == 1:
                        self.totalNodes = int(tmp[0])
                        self.totalEdges = int(tmp[1])

                    else:
                        print("Error Can't print this type of a graph")
                        exit(1)
                else:
                    tmp = [int(x) for x in line.strip('\n').split()]
                    for num in range(0, len(tmp), 2):
                        G.add_edge(ctr, tmp[num] - 1, weight=tmp[num + 1])
                    ctr += 1

    def readEdgeList(self, filename, G):
        with open(filename, 'r') as f:
            fileList = list(f)
            fileList = [[int(i) for i in x.strip('\n').split()] for x in fileList]
        for edge in fileList:
            G.add_edge(edge[0], edge[1], weight=edge[2])

    def validate(self, G):
        p = nx.single_source_dijkstra(G, 0)
        if p[0] == self.propertyMap:
            return True
        else:
            for k, v in p[0].items():
                print(k,v)
                # if p[0][k] != self.propertyMap[k]:
                #     print(k, " value in ground truth is ", p[0][k], " and value in delta stepping is ", self.propertyMap[k])
            return False


def main():
    G = nx.path_graph(0)
    # filename = 'file11.gr'
    # filename = 'sampleGraph.gr'
    filename = 'graph1.gr'
    a = algorithm()
    a.metisReader(filename, G)
    a.deltaStepping(G)
    if not a.validate(G):
        print("Error : The algorithm is incorrect")
    else:
        print("The shortest path from ", a.sourceVertex, " is ", a.propertyMap)


if __name__ == '__main__':
    main()

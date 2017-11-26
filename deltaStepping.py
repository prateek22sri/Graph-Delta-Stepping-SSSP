#!/usr/bin/env python

"""
This code is implementation of sequential Delta Stepping

Author : Prateek Srivastava
Date Created : 09-23-2017

Base DeltaStepping Algorithm Acknowledgements:
Marcin J Zalewski - marcin.zalewski@pnnl.gov

Paper :
@article{meyer_-stepping:_2003,
       title = {Δ-stepping: a parallelizable shortest path algorithm},
       volume = {49},
       issn = {0196-6774},
       shorttitle = {Δ-stepping},
       url = {http://www.sciencedirect.com/science/article/pii/S0196677403000762},
       doi = {10.1016/S0196-6774(03)00076-2},
"""

from math import floor, sqrt
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint


class Algorithm:
    """

    """

    def __init__(self):
        """

        """
        self.distances = {}
        self.delta = 5
        self.property_map = {}
        self.workItems = []
        self.source_vertex = 2
        self.infinity = float("inf")
        self.totalNodes = 0
        self.totalEdges = 0
        self.B = {}

    def relax(self, w, x):
        """
        This function relaxes a bucket i.e. if the distance of a vertex is less than the already existing distance in
        the property map then, the vertex is removed from the bucket and reinserted in the new bucket

        x is the distance of the vertex and w is the index of the vertex in the property map
        """
        # print("w=", w, "x=", x)
        if x < self.property_map[w]:
            # check if there is an entry of w in the dictionary B
            if self.property_map[w] != self.infinity:
                if w in self.B[floor(self.property_map[w] / self.delta)]:
                    # check if the vertex is in the wrong bucket
                    if floor(x / self.delta) != floor(self.property_map[w] / self.delta):
                        self.B[floor(self.property_map[w] / self.delta)].remove(w)
                self.B[floor(x / self.delta)].append(w)

            # if the dictionary entry does not exist
            else:
                if floor(x / self.delta) not in self.B:
                    self.B[floor(x / self.delta)] = [w]
                else:
                    if w not in self.B[floor(x / self.delta)]:
                        self.B[floor(x / self.delta)].append(w)

            # update the property map
            self.property_map[w] = x

    def find_requests(self, vertices, kind, g):
        """
        returns a dictionary of neighboring edges with their weights but according to the kind i.e. light or heavy

        :param vertices:
        :param kind:
        :param g:
        :return:
        """

        tmp = {}
        # print("vertices=", vertices, "kind=", kind)
        for u in vertices:
            for v in g.neighbors(u):
                # print(u, self.property_map[u], g.get_edge_data(u, v)['weight'])
                edge_weight = self.property_map[u] + g.get_edge_data(u, v)['weight']
                if kind == 'light':
                    if g.get_edge_data(u, v)['weight'] <= self.delta:
                        if v in tmp:
                            if edge_weight < tmp[v]:
                                tmp[v] = edge_weight
                        else:
                            tmp[v] = edge_weight
                elif kind == 'heavy':
                    if g.get_edge_data(u, v)['weight'] > self.delta:
                        if v in tmp:
                            if edge_weight < tmp[v]:
                                tmp[v] = edge_weight
                        else:
                            tmp[v] = edge_weight
                else:
                    return "Error: No such kind of edges " + kind
        # print("tmp=", tmp)
        return tmp

    def relax_requests(self, request):
        """

        :param request:
        :return:
        """
        for key, value in request.items():
            self.relax(key, value)

    def delta_stepping(self, g):
        """
        This is the main function to implement the algorithm

        :param g:
        :return:
        """
        for node in g.nodes():
            self.property_map[node] = self.infinity
        self.relax(self.source_vertex, 0)
        # print(self.B, self.property_map)
        ctr = 0
        while self.B:
            # print("Parent Iteration=", ctr)
            # print("bucket=", self.B)
            i = min(self.B.keys())
            sub_ctr = 0
            r = []

            while i in self.B:
                # print("Child Iteration=", sub_ctr)
                # print("B[i]=", self.B[i])
                req = self.find_requests(self.B[i], 'light', g)
                # print("req=", req)
                r += self.B[i]
                del self.B[i]
                self.relax_requests(req)
                sub_ctr += 1
                # print(self.B)
            # print("child ends")
            # print("r=", r)
            req = self.find_requests(r, 'heavy', g)
            self.relax_requests(req)
            ctr += 1

    def validate(self, g):
        """

        :param g:
        :return:
        """
        self.property_map = {k: v for k, v in self.property_map.items() if v != self.infinity}
        p = nx.single_source_dijkstra(g, self.source_vertex)
        if p[0] == self.property_map:
            return True
        else:
            print("Error: The algorithm is faulty!!!")
            for k, v in p[0].items():
                if p[0][k] != self.property_map[k]:
                    print("vertex ", k, " value in ground truth is ", p[0][k], " and value in delta stepping is ",
                          self.property_map[k])
            return False


def main():
    make_graph = False
    g = nx.read_edgelist('sample2', nodetype=int, data=(('weight', int),), create_using=nx.DiGraph())

    print("\nGraph Information..")
    print("===================\n")
    print(nx.info(g))
    print("\nCalculating shortest path..")
    a = Algorithm()
    a.source_vertex = 2
    a.delta_stepping(g)
    print("\nValidating Solution..")
    if not a.validate(g):
        exit(1)
    else:
        print("\nThe shortest path from ", a.source_vertex, " is:")
        pprint(a.property_map)

    # visualize the graph
    if make_graph:
        pos = nx.spring_layout(g, k=5 / sqrt(g.order()))
        nx.draw_networkx(g, pos)
        edge_labels = dict([((u, v,), d['weight'])
                            for u, v, d in g.edges(data=True)])
        nx.draw_networkx_edge_labels(g, pos=pos, edge_labels=edge_labels, label_pos=0.3, font_size=7)
        plt.show(block=False)
        plt.savefig("sample1_graph.png")


if __name__ == '__main__':
    main()

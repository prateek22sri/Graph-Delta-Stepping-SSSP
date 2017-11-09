#!usr/bin/env python

from collections import defaultdict

# https://gist.github.com/econchick/4666413
class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

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


def dijkstra(graph, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:

            weight = current_weight + graph.distances[(min_node, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path


def main():
    g = Graph()
    with open('sample2') as f:
        fileList = list(f)
        fileList = [[int(i) for i in x.strip('\n').split()] for x in fileList]
    for edge in fileList:
        g.add_edge(edge[0],edge[1],edge[2])
    print(dijkstra(g, 0))


if __name__ == '__main__':
    main()

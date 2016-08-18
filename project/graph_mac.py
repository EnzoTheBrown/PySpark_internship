from Heap import myHeap

import pickle

pickle_in = open('../data/listener.pickle', 'rb')
data = pickle.load(pickle_in) 


class Node:
    def __init__(self, mac, visited = False):
        self.mac = mac
        self.neighbors = []
        self.visited = visited
        self.parent = None

    def add_neighbor(self, node, distance):
        self.neighbors.append([node, distance])

    def find_neighbor(self, address):
        for n in self.neighbors:
            if n[0].mac == address:
                return n
        else:
            print('no such adddress')

    def is_neighbor(self, n):
        for node in self.neighbors:
            if node[0] is not None:
                print(node[0].mac)
            if n[0] == node:
                return True
        return False

    def display_neighbors(self):
        for n in self.neighbors:
            print([n[0], n[1]])


class Heap(myHeap):
    @staticmethod
    def compare(left, right):
        if (left[1] > right[1]):
            return True
        return False


class Graph:
    def __init__(self):
        self.nodes = []
        for d in data:
            self.nodes.append(Node(d[0]))
        i = 0
        for node in self.nodes:
            for add in data[i][1]:
                n = self.find_node(add[1])
                if n is not None:
                    node.add_neighbor(self.find_node(n.mac), add[0])
            i += 1

    def find_node(self, mac):
        for node in self.nodes:
            if mac in node.mac:
                return node
        return None

    def is_correct(self, mac1, mac2):
        n1 = self.find_node(mac1)
        n2 = self.find_node(mac2)
        if n1 is not None and n2 is not None:
            return n1.is_neighbor(n2)
        return False

    def dijkstra(self, start, goal):#node, node
        candidates = Heap()

        def push_neighbors(pop):
            for n in pop[0].neighbors:
                if not n[0].visited:
                    n[0].visited = True
                    candidates.push([n[0], n[1] + pop[1]])
                    n[0].parent = pop[0]

        candidates.push([start, 0])
        start.visited = True
        popped = candidates.pop()
        while popped[0].mac != goal.mac:
            push_neighbors(popped)
            popped = candidates.pop()
        for n in self.nodes:
            n.visited = False

        node = goal
        while node.parent is not None:
            print([node.mac[:-1], node.parent.find_neighbor(node.mac)[1]])
            node = node.parent

g = Graph()
g.dijkstra(g.find_node('e8:50:8b:5d:b1:8d'), g.find_node('2c:54:cf:fa:7f:09'))

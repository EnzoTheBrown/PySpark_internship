import pickle

pickle_in = open('listener.pickle', 'rb') 
data = pickle.load(pickle_in) 


class Node:
    def __init__(self, mac):
        self.mac = mac
        self.neighbors = []

    def add_neighbor(self, node):
        self.neighbors.append(node)

    def is_neighbor(self, n):
        for node in self.neighbors:
            if n == node:
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
                node.add_neighbor(self.find_node(add))
            i += 1
        print len(self.nodes)

    def find_node(self, mac):
        for node in self.nodes:
            if node.mac == mac:
                return node
        return None

    def is_correct(self, mac1, mac2):
        n1 = self.find_node(mac1)
        n2 = self.find_node(mac2)
        return n1.is_neighbor(n2)


g = Graph()
print(g.is_correct('00:19:07:8d:ed:53', '34:bb:26:ff:e6:c2'))


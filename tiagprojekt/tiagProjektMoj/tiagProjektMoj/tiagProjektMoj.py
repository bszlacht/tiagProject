import networkx as nx
import matplotlib.pyplot as plt
import pydot



class Graph(nx.Graph):  # wierzcholki numerowane od 0..n-1

    def get_index_from_label(self, label):
        for key, value in nx.get_node_attributes(self, "label").items():
            if value == label:
                return key
        return None

    # zwraca z kompatybilnymi indeksami
    # last_idx to najwyzszy index wezla w grafie na ktorym przeprowadzam transformacje
    # vertex_idx to index wezla lewej strony produkcji
    def map_idx(self, last_idx, vertex_idx):
        mapping = {}
        for i in self.nodes():
            if i == 0:
                mapping[i] = vertex_idx
            else:
                mapping[i] = i + last_idx

        return nx.relabel_nodes(self, mapping)

    # stosuje produkcje na grafie, zwraca statystyki jesli produkcje da sie wykonac- false w przeciwnym razie
    # vertex - label wierzcholka lewej strony produkcji
    # G - graf prawej strony produkcji
    # transformation - transformacja osadzenia w postaci slownika np. "a" : "b" - zwisajaca krawedz z wierzcholka a polaczyc z b po prawej stronie produkcji
    # zakładam że rightG numerowany od 0..n-1
    def produce(self, vertex: str, G, transformation: dict):
        vertex_idx = self.get_index_from_label(vertex)
        if vertex_idx != None:
            neighbors = [(i, self.nodes[i]["label"]) for i in self.neighbors(vertex_idx)]

            G = G.map_idx(len(self) - 1, vertex_idx)

            self.remove_node(vertex_idx)
            self.add_nodes_from(G.nodes(data=True))
            self.add_edges_from(G.edges(data=True))

            for idx, label in neighbors:
                join_to_label = transformation[label]
                join_to_idx = G.get_index_from_label(join_to_label)
                if join_to_idx == None:
                    join_to_idx = self.get_index_from_label(join_to_label)
                if join_to_idx != None:
                    self.add_edge(idx, join_to_idx)

            return self.generate_stats()
        else:
            return False

    def print_with_labels(self):
        labelsdict = {k: self.nodes[k]["label"] for k in self.nodes}
        nx.draw(self, with_labels=True, labels=labelsdict)
        plt.show()

    def generate_stats(self):
        stat = {"Liczba węzłów": self.number_of_nodes(),
                "Liczba krawędzi": self.number_of_edges(),
                "Liczba składowych spójnych": nx.number_connected_components(self),
                "Średni stopień wierzchołka": sum([d for _, d in self.degree]) // self.number_of_nodes()}

        atributes = nx.get_node_attributes(self, "label")
        label_degree = {label: 0 for label in atributes.values()}
        label_number = label_degree
        avg_label_degree = {}
        for key, label in atributes.items():
            label_degree[label] += self.degree[key]
            label_number[label] += 1

        for label, degree in label_degree.items():
            avg_label_degree[label] = degree // label_number[label]

        stat["Średni stopień wierzchołka dla etykiet"] = avg_label_degree
        avg = lambda x: sum(x)//len(x)
        stat["Średnia liczba węzłów w składowej spójnej"] = avg([len(c) for c in nx.connected_components(self)])

        return stat

    


    def createValidGraph(self):
        n = len(self.nodes)
        res = Graph()
        nodes = list(self.nodes)
        for idx, label in enumerate(self.nodes):
            res.add_node(idx, label = label)
        for edge in self.edges:
            x_idx = findIndex(self.nodes, edge[0])
            y_idx = findIndex(self.nodes, edge[1])
            res.add_edge(x_idx, y_idx)
        return res

def findIndex(A, toFind):
    for idx, label in enumerate(A):
        if label == toFind:
            return idx
    return -1
         

            

def main():
    #input = Graph(nx.drawing.nx_pydot.read_dot("input.dot"))
    #input = list(input)
    testA = Graph(nx.drawing.nx_pydot.read_dot("A.dot"))
    A = testA.createValidGraph()
    A.print_with_labels()

    #produkcja P1
    testB = Graph(nx.drawing.nx_pydot.read_dot("B.dot"))
    testB = Graph(nx.drawing.nx_pydot.read_dot("B.dot"))
    B = testB.createValidGraph()
    B.print_with_labels()
    
    tr = {"a": "Y", "b": "c", "c": "Y", "d": "a", "X": "c", "Y": "Y"}
    A.produce("X", B, tr)
    A.print_with_labels()
    print(A.generate_stats())



if __name__ == "__main__":
    main()

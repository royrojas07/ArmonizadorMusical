class Node:
    def __init__(self,chord): 
        self.chord = chord
        self.selected_count = 0
        self.neighbors = []

    def get_chord(self):
        return self.chord

    def selected_up(self):
        self.selected_count += 1
    
    def add_neighbor(self,edge):
        self.neighbors.append(edge)

    def get_neighbors(self):
        return self.neighbors

class Edge:
    def __init__(self,nodeA,nodeB):
        self.origen = nodeA
        self.destiny = nodeB
        self.selected_count = 0
        self.probability = 0.0

    def set_probability(self,probability):
        self.probability = probability

    def get_origen(self):
        return self.origen
    
    def selected_up(self):
        self.selected_count += 1
    
    def get_destiny(self):
        return self.destiny

    def get_probability(self):
        return self.probability

class Graph:
    def __init__(self,txt):
        self.graph = []
        self.chords = []
        self.create_graph(self.read_txt(txt))  #llamaria al metodo create con el txt ya leido por el metodo read_txt

    def read_txt(self,txt):
        fd = open(txt,"r")
        line = fd.readline()
        fd.close()
        return line

    #crearia el grafo a partir de lo leido en el metodo read_txt
    def create_graph(self,chords):
        self.chords = chords.split(",")
        for c in self.chords:
            node = Node(c)
            self.graph.append(node)
        
        #cada nodo esta unido con el resto de los acordes
        for nodeA in self.graph:
            for nodeB in self.graph:
                edge = Edge(nodeA,nodeB)
                nodeA.add_neighbor(edge)

    def training(self, txt):
        song = self.read_txt(txt).split(",")
        current_node = None
        for node in self.graph:
	        if(node.get_chord() == song[0]): # get the starting node
		        current_node = node

        for i in range(1,len(song)):
            next_node = None
            current_node.selected_up()
            for edge in current_node.get_neighbors():
                if(edge.destiny.get_chord() == song[i]):
                    edge.selected_up()
                    next_node = edge.destiny
            
                edge.set_probability(edge.selected_count / current_node.selected_count)

            current_node = next_node


    def print_graph(self):
        for nodes in self.graph:
            print("Nodo: ", nodes.get_chord(), "  Selected: ", nodes.selected_count)
            for edge in nodes.get_neighbors():
                print("    Edge to: ",edge.get_destiny().get_chord(), "  Weight: ", edge.get_probability(), "  Selected: ", edge.selected_count)


prueba = Graph("prueba.txt")
prueba.print_graph()
print("--------------------------------")
prueba.training("cancion.txt")
prueba.print_graph()

 



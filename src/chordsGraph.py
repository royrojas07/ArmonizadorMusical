import json

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

    def set_selected_count(self, count):
        self.selected_count = count

class Edge:
    def __init__(self,nodeA,nodeB):
        self.origen = nodeA
        self.destiny = nodeB
        self.selected_count = 0
        self.probability = 0.0

    def set_probability(self,probability):
        self.probability = probability

    def set_selected_count(self, count):
        self.selected_count = count

    def get_origen(self):
        return self.origen
    
    def selected_up(self):
        self.selected_count += 1
    
    def get_destiny(self):
        return self.destiny

    def get_probability(self):
        return self.probability

class Graph:
    def __init__(self, gen_type, filename):
        self.graph = []
        self.chords = []
        self.genre = "classical"

        if(gen_type == 0): #Creado desde 0, un buevo grafo 

            self.create_graph(self.read_txt(filename))  #llamaria al metodo create con el txt ya leido por el metodo read_txt

        else:   #Cargar un grafo ya creado de un archivo JSON
            self.load_graph_from_json(filename)

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
            
                edge.set_probability(round(edge.selected_count / current_node.selected_count, 4))

            current_node = next_node


    def print_graph(self):
        for nodes in self.graph:
            print("Nodo: ", nodes.get_chord(), "  Selected: ", nodes.selected_count)
            for edge in nodes.get_neighbors():
                print("    Edge to: ",edge.get_destiny().get_chord(), "  Weight: ", edge.get_probability(), "  Selected: ", edge.selected_count)


    def  save_graph_to_json(self):
        graph_container = []
        for node in self.graph:
            neighbor_data = {}
            for edge in node.get_neighbors():
                neighbor_data[edge.get_destiny().get_chord()] = [edge.get_probability(), edge.selected_count]

            graph_container.append([[node.get_chord(),node.selected_count], neighbor_data])

        json_file = None
        try:
            json_file = open(self.genre + ".json", "w")
        except:
            print("Can't open the especified file.")
            return

        json_file.write(json.dumps(graph_container))

        json_file.close()

    def load_graph_from_json(self, filename):

        json_file = None
        try:
            json_file = open(filename, "r")
        except:
            print("Can't open the especified file.")
            return

        graph_container = json.loads(json_file.readline())

        json_file.close();

        
        for listitem in graph_container:

            self.chords.append(listitem[0][0])

        counter = 0
        for chord in self.chords:
            node = Node(chord)
            node.set_selected_count( graph_container[counter][0][1])
            self.graph.append(node)
            counter +=1

        
        for i in range(len(self.graph)):

            for j in range(len(self.graph)):

                new_Edge = Edge(self.graph[i], self.graph[j])
                new_Edge.set_probability(graph_container[i][1][self.graph[j].get_chord()][0])
                new_Edge.set_selected_count(graph_container[i][1][self.graph[j].get_chord()][1])
                self.graph[i].add_neighbor(new_Edge)

        




        





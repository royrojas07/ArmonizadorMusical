import json
import random
import math
from SongConversor import *
from TextSongReader import *

class Node:
    def __init__(self,chord,node_type): 
        self.chord = chord
        self.selected_count = 0
        self.neighbors = []
        self.type = node_type

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
    def __init__(self, gen_type, genre, filename = ""):
        self.graph = [[],[],[]]
        self.genre = genre

        if(gen_type == 0): #Creado desde 0, un buevo grafo 

            self.create_graph()  #llamaria al metodo create

        else:   #Cargar un grafo ya creado de un archivo JSON
            self.load_graph_from_json(filename)

    #crearia el grafo a partir de los IDs en el archivo de ChordsId
    def create_graph(self):
        
        inserted_ids = []
        for note in Chord_Notes.keys():
            for variation in Chord_Variations.keys():
                complete_note = note + variation
                if(convert_chord(complete_note) not in inserted_ids):
                    node = Node(convert_chord(complete_note))
                    self.graph.append(node)
                    inserted_ids.append(convert_chord(complete_note))
        
        #cada nodo esta unido con el resto de los acordes
        for nodeA in self.graph:
            for nodeB in self.graph:
                edge = Edge(nodeA,nodeB)
                nodeA.add_neighbor(edge)

    def training(self, song):
        current_node = None

        first_note_found = False
        counter = 0
        while ((not first_note_found) and counter < len(self.graph)):
            if(self.graph[counter].get_chord() == song[0]): # get the starting node
                current_node = self.graph[counter]
                first_note_found = True
            counter += 1

        for i in range(1,len(song)):
            next_node = None
            current_node.selected_up()
            for edge in current_node.get_neighbors():
                if(edge.destiny.get_chord() == song[i]):
                    edge.selected_up()
                    next_node = edge.destiny
            
                edge.set_probability(round(edge.selected_count / current_node.selected_count, 5))

            current_node = next_node

    def create_song(self, song_length, first_note):
        current_node = None
        first_note_id = convert_chord(first_note)
        for node in self.graph[SINGLE]:
            if(first_note_id == node.get_chord()):
                current_node = node

        new_song = []
        for i in range(song_length):
            chord_to_add = None

            if(current_node.type == SINGLE): #Single node
                chord_to_add = current_node.get_chord()
            elif(current_node.type == DOUBLE): #Double node
                chord_to_add = current_node.get_chord()[1]
            else: #Triple node
                chord_to_add = current_node.get_chord()[2]

            new_song.append(chord_to_add)

            decision_probability = random.random()
            closest_option = (math.inf,0)


            neighbors = current_node.get_neighbors()

            if(len(neighbors) == 0):
                if(current_node.type == SINGLE):
                    current_node = graph[DOUBLE][random.randint(0, len(graph[DOUBLE]-1))]
                else:
                    current_node = graph[TRIPLE][random.randint(0, len(graph[TRIPLE]-1))]
            else:
                for i in range(len(neighbors)):
                    if( abs(neighbors[i].get_probability() - decision_probability) < abs(closest_option[0] - decision_probability)):
                        closest_option = (neighbors[i].get_probability(), i)

                current_node = neighbors[closest_option[1]].get_destiny()

        return new_song

    def print_graph(self):
        for node_group in self.graph:
            for node in node_group:
                print("---------------------------------------------------------------")
                print("Nodo: ", node.get_chord(), "  Selected: ", node.selected_count)
                for edge in node.get_neighbors():
                    print("    Edge to: ",edge.get_destiny().get_chord(), "  Weight: ", edge.get_probability(), "  Selected: ", edge.selected_count)


    def  save_graph_to_json(self):
        graph_container = []
        for node_group in self.graph:
            for node in node_group:
                neighbor_data = {}
                for edge in node.get_neighbors():
                    neighbor_data[str(edge.get_destiny().get_chord())] = [edge.get_probability(), edge.selected_count]

                graph_container.append([[node.get_chord(),node.selected_count,node.type], neighbor_data])

        json_file = None
        try:
            json_file = open(self.genre + ".json", "w")
        except:
            print("Can't open the specified file.")
            return

        json_file.write(json.dumps(graph_container))

        json_file.close()

    def load_graph_from_json(self, filename):

        filename += ".json"
        json_file = None
        try:
            json_file = open(filename, "r")
        except:
            print("Can't open the especified file.")
            return 

        graph_container = json.loads(json_file.readline())

        json_file.close();

        node_content = [[],[],[]]
        
        #Extract the node IDs from the file data
        for listitem in graph_container:
            if(listitem[0][2] == SINGLE):
                node_content[SINGLE].append(listitem[0][0])
            elif(listitem[0][2] == DOUBLE):
                node_content[DOUBLE].append(tuple(listitem[0][0]))
            else:
                node_content[TRIPLE].append(tuple(listitem[0][0]))

        #Create the nodes from the extracted data in the file
        counter = 0
        for i in range(3):
            if(i == SINGLE):
                for content in node_content[SINGLE]:
                    node = Node(content, SINGLE)
                    node.set_selected_count(graph_container[counter][0][1])
                    self.graph[SINGLE].append(node)
                    counter +=1
            elif(i == DOUBLE):
                for content in node_content[DOUBLE]:
                    node = Node(content, DOUBLE)
                    node.set_selected_count(graph_container[counter][0][1])
                    self.graph[DOUBLE].append(node)
                    counter +=1  
            else:
                for content in node_content[TRIPLE]:
                    node = Node(content, TRIPLE)
                    node.set_selected_count(graph_container[counter][0][1])
                    self.graph[TRIPLE].append(node)
                    counter +=1        

        #Restore the connections 
        counter = 0
        for k in range(3):
            if(k == SINGLE):
                for i in range(len(self.graph[SINGLE])): #Reconnecting singles to doubles
                    current_node_neighbors = graph_container[counter][1].keys()
                    for j in range(len(current_node_neighbors)):

                        #Find the double node to connect to
                        node_to_connect = None
                        found_key = None
                        found = False
                        node_counter = 0
                        while((not found) and (node_counter < len(current_node_neighbors))):
                            if(str(self.graph[DOUBLE][node_counter].get_chord()) == current_node_neighbors[j]):
                                found = True
                                node_to_connect = self.graph[DOUBLE][node_counter]
                                found_key = current_node_neighbors[j]
                            node_counter +=1

                        if(found):
                            new_Edge = Edge(self.graph[SINGLE][i], node_to_connect)
                            new_Edge.set_probability(graph_container[counter][1][found_key][0])
                            new_Edge.set_selected_count(graph_container[counter][1][found_key][1])
                            self.graph[SINGLE][i].add_neighbor(new_Edge)
                    counter +=1
            if(k == DOUBLE):
                for i in range(len(self.graph[DOUBLE])): #Reconnecting doubles to triples
                    current_node_neighbors = graph_container[counter][1].keys()
                    for j in range(len(current_node_neighbors)):

                        #Find the triple node to connect to
                        node_to_connect = None
                        found_key = None
                        found = False
                        node_counter = 0
                        while((not found) and (node_counter < len(current_node_neighbors))):
                            if(str(self.graph[TRIPLE][node_counter].get_chord()) == current_node_neighbors[j]):
                                found = True
                                node_to_connect = self.graph[TRIPLE][node_counter]
                                found_key = current_node_neighbors[j]
                            node_counter +=1

                        if(found):
                            new_Edge = Edge(self.graph[DOUBLE][i], node_to_connect)
                            new_Edge.set_probability(graph_container[counter][1][found_key][0])
                            new_Edge.set_selected_count(graph_container[counter][1][found_key][1])
                            self.graph[DOUBLE][i].add_neighbor(new_Edge)
                    counter +=1
            else:
                for i in range(len(self.graph[TRIPLE])): #Reconnecting triples to triples
                    current_node_neighbors = graph_container[counter][1].keys()
                    for j in range(len(current_node_neighbors)):

                        #Find the triple node to connect to
                        node_to_connect = None
                        found_key = None
                        found = False
                        node_counter = 0
                        while((not found) and (node_counter < len(current_node_neighbors))):
                            if(str(self.graph[TRIPLE][node_counter].get_chord()) == current_node_neighbors[j]):
                                found = True
                                node_to_connect = self.graph[TRIPLE][node_counter]
                                found_key = current_node_neighbors[j]
                            node_counter +=1

                        if(found):
                            new_Edge = Edge(self.graph[TRIPLE][i], node_to_connect)
                            new_Edge.set_probability(graph_container[counter][1][found_key][0])
                            new_Edge.set_selected_count(graph_container[counter][1][found_key][1])
                            self.graph[TRIPLE][i].add_neighbor(new_Edge)
                    counter +=1
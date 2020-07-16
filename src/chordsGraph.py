import sys
import json
import random
import math
import time
from SongConversor import *
from TextSongReader import *

SINGLE = 0
DOUBLE = 1
TRIPLE = 2

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

    def get_type(self):
        return self.type

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
        single_nodes = [] # lista de nodos simples
        for note in Chord_Notes.keys():
            chord_id = convert_chord(note)
            if chord_id not in inserted_ids:
                single_nodes.append(Node(chord_id, SINGLE))
                inserted_ids.append(chord_id)
        self.graph[0] = single_nodes

        """
        inserted_ids = []
        chords = [] # lista de acordes
        for note in Chord_Notes.keys():
            for variation in Chord_Variations.keys():
                chord_id = convert_chord(note+variation)
                if chord_id not in inserted_ids:
                    chords.append(chord_id)
                    inserted_ids.append(chord_id)

        double_nodes = [] # lista de nodos dobles
        for chord1 in self.graph[SINGLE]:
            for chord2 in chords:
                double_nodes.append(Node((chord1.get_chord(), chord2), DOUBLE))
        self.graph[1] = double_nodes

        triple_nodes = [] # lista de nodos triples
        for chord1 in chords:
            for chord2 in chords:
                for chord3 in chords:
                    triple_nodes.append(Node((chord1, chord2, chord3), TRIPLE))
        self.graph[2] = triple_nodes
        """

    def training(self, song):
        current_node = None

        first_note_found = False
        counter = 0
        
        while ((not first_note_found) and counter < len(self.graph[SINGLE])):
            if self.graph[SINGLE][counter].get_chord() == song[0]: # get the starting node
                current_node = self.graph[SINGLE][counter]
                first_note_found = True
            counter += 1

        for i in range(1,len(song)):
            next_node = None
            current_node.selected_up()
            for edge in current_node.get_neighbors():
                if current_node.type == SINGLE:
                    if edge.destiny.get_chord() == (song[i-1], song[i]):
                        edge.selected_up()
                        next_node = edge.destiny
                else: # nodo doble o triple
                    if edge.destiny.get_chord() == (song[i-2], song[i-1], song[i]):
                        edge.selected_up()
                        next_node = edge.destiny
                edge.set_probability(round(edge.selected_count / current_node.selected_count, 5))
            if next_node == None:
                e = None
                if current_node.type == SINGLE:
                    found = False
                    for double in self.graph[DOUBLE]:
                        if double.get_chord() == (song[i-1], song[i]):
                            e = Edge(current_node, double)
                            current_node.add_neighbor(e)
                            e.selected_up()
                            next_node = e.destiny
                            found = True

                    if(not found):
                        new_node = Node((song[i-1], song[i]), DOUBLE)
                        self.graph[DOUBLE].append(new_node)
                        e = Edge(current_node, new_node)
                        current_node.add_neighbor(e)
                        e.selected_up()
                        next_node = e.destiny
                else:
                    found = False 
                    for triple in self.graph[TRIPLE]:
                        if triple.get_chord() == (song[i-2],
                                song[i-1], song[i]):
                            e = Edge(current_node, triple)
                            current_node.add_neighbor(e)
                            e.selected_up()
                            next_node = e.destiny
                            found = True

                    if(not found):
                        new_node = Node((song[i-2], song[i-1], song[i]), TRIPLE)
                        self.graph[TRIPLE].append(new_node)
                        e = Edge(current_node, new_node)
                        current_node.add_neighbor(e)
                        e.selected_up()
                        next_node = e.destiny

                e.set_probability(round(e.selected_count / current_node.selected_count, 5))
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
                    current_node = self.graph[DOUBLE][random.randint(0, len(self.graph[DOUBLE])-1)]
                else:
                    current_node = self.graph[TRIPLE][random.randint(0, len(self.graph[TRIPLE])-1)]
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
            print("Can't open the specified file.")
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
                    for key in graph_container[counter][1].keys():

                        #Find the double node to connect to
                        node_to_connect = None
                        found_key = None
                        found = False
                        node_counter = 0
                        while((not found) and (node_counter < len(self.graph[DOUBLE]))):
                            if(str(self.graph[DOUBLE][node_counter].get_chord()) == key):
                                found = True
                                node_to_connect = self.graph[DOUBLE][node_counter]
                                found_key = key
                            node_counter +=1

                        if(found):
                            new_Edge = Edge(self.graph[SINGLE][i], node_to_connect)
                            new_Edge.set_probability(graph_container[counter][1][found_key][0])
                            new_Edge.set_selected_count(graph_container[counter][1][found_key][1])
                            self.graph[SINGLE][i].add_neighbor(new_Edge)
                    counter +=1
            elif(k == DOUBLE):
                for i in range(len(self.graph[DOUBLE])): #Reconnecting doubles to triples
                    for key in graph_container[counter][1].keys():

                        #Find the triple node to connect to
                        node_to_connect = None
                        found_key = None
                        found = False
                        node_counter = 0
                        while((not found) and (node_counter < len(self.graph[TRIPLE]))):
                            if(str(self.graph[TRIPLE][node_counter].get_chord()) == key):
                                found = True
                                node_to_connect = self.graph[TRIPLE][node_counter]
                                found_key = key
                            node_counter +=1

                        if(found):
                            new_Edge = Edge(self.graph[DOUBLE][i], node_to_connect)
                            new_Edge.set_probability(graph_container[counter][1][found_key][0])
                            new_Edge.set_selected_count(graph_container[counter][1][found_key][1])
                            self.graph[DOUBLE][i].add_neighbor(new_Edge)
                    counter +=1
            else:
                for i in range(len(self.graph[TRIPLE])): #Reconnecting triples to triples
                    for key in graph_container[counter][1].keys():

                        #Find the triple node to connect to
                        node_to_connect = None
                        found_key = None
                        found = False
                        node_counter = 0
                        while((not found) and (node_counter < len(self.graph[TRIPLE]))):
                            if(str(self.graph[TRIPLE][node_counter].get_chord()) == key):
                                found = True
                                node_to_connect = self.graph[TRIPLE][node_counter]
                                found_key = key
                            node_counter +=1

                        if(found):
                            new_Edge = Edge(self.graph[TRIPLE][i], node_to_connect)
                            new_Edge.set_probability(graph_container[counter][1][found_key][0])
                            new_Edge.set_selected_count(graph_container[counter][1][found_key][1])
                            self.graph[TRIPLE][i].add_neighbor(new_Edge)
                    counter +=1
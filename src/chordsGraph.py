import json
import random
import math
from SongConversor import *
from TextSongReader import *

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
    def __init__(self, gen_type, genre, filename = ""):
        self.graph = []
        self.chords = []
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
        for node in self.graph:
            if(first_note_id == node.get_chord()):
                current_node = node

        new_song = []
        for i in range(song_length):
            new_song.append(current_node.get_chord())

            decision_probability = random.random()
            closest_option = (math.inf,0)

            neighbors = current_node.get_neighbors()
            for i in range(len(neighbors)):
                if( abs(neighbors[i].get_probability() - decision_probability) < abs(closest_option[0] - decision_probability)):
                    closest_option = (neighbors[i].get_probability(), i)

            current_node = neighbors[closest_option[1]].get_destiny()

        return new_song



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
                neighbor_data[int(edge.get_destiny().get_chord())] = [edge.get_probability(), edge.selected_count]

            graph_container.append([[node.get_chord(),node.selected_count], neighbor_data])

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
                new_Edge.set_probability(graph_container[i][1][str(self.graph[j].get_chord())][0])
                new_Edge.set_selected_count(graph_container[i][1][str(self.graph[j].get_chord())][1])
                self.graph[i].add_neighbor(new_Edge)

"""        
newGraph = Graph(0)
#newGraph.print_graph()
reader = TextSongReader()


song_list = reader.read_dir()
for train_count in range (5000):
    random.shuffle(song_list)
    for songs in song_list:
        song = convert_song('C:/Users/Marco/Desktop/UCR/I Semestre 2020/Inteligencia Artificial/Proyecto/Canciones/TXT Acordes/Clásica/' + songs, 'C', '', True)
        newGraph.training(song)

new_song_id = newGraph.create_song(50, "C")
print(new_song_id)

new_song_string = []
for i in range(len(new_song_id)):
    new_song_string.append(get_chord_name(new_song_id[i]))

print(new_song_string)
"""
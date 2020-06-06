import os
from chordsGraph import *
from ChordsId import *
from TextSongReader import *
from SongConversor import *

def main():
	option = 1
	graph = None
	while option != 5:
		print("--------------------------------------------")
		try:
			print("1. Create new graph")
			print("2. Select existing graph")
			print("3. Train current graph")
			print("4. Create new song from current graph")
			print("5. Exit")
			option  = int(input("Choose an option from the menu: "))			
		except:
			option = -1

		if(option == 1):
			graph_name  = input("Write the graph name or genre: ")
			filename = graph_name + ".json"
			if(os.path.exists(filename)):
				print("There's already a graph with that name.")
			else:
				graph = Graph(0, graph_name)
				graph.save_graph_to_json()
				print("Graph created!")
		elif(option == 2):
			graph_name  = input("Write the graph name of the existing graph: ")
			graph = Graph(1, graph_name, graph_name)
			print("Graph loaded!")
		elif (option == 3):
			if(graph != None):
				try:
					iteration_count  = int(input("Write the number of training iterations: "))
					
				except:
					print("Not a valid number, assuming 100")
					iteration_count = 100

				song_directory = input("Write the path of the song directory to be used for training: ")

				print("Starting training...")
				reader = TextSongReader()
				song_list = reader.read_dir(song_directory)
				for i in range (iteration_count):
					random.shuffle(song_list)
					for song_names in song_list:
						song = convert_song( song_directory + "/" + song_names, 'C', '', True)
						graph.training(song)

				print("Training done!")
				graph.save_graph_to_json()
			else:
				print("No graph has been selected or created yet")

		elif(option == 4):
			if(graph != None):

				base_note  = input("Write the base note for the song: ")

				try:
					song_length = int(input("Write the number of chords the song will have: "))
					
				except:
					print("Not a valid number, assuming 15")
					song_length = 15			



				new_song_ids = graph.create_song(song_length, base_note)
	    		
				new_song_chords = []
				for i in range(len(new_song_ids)):
					new_song_chords.append(get_chord_name(new_song_ids[i]))

				print("The chords for this new song are:")
				print(new_song_chords)
			else:
				print("No graph has been selected or created yet")				
		elif(option == 5):
			exit()

main()




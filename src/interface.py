#librerias que se importan
import pygame 
import time
import textwrap
from chordsGraph import *
from ChordsId import *
from TextSongReader import *
from SongConversor import *


#inicializa todos los modulos de pygame
#retorna si la inicializacion fue exitosa o no 
pygame.init()

#va a ser nuestra superficie 
xy_display = (480, 320)
display = pygame.display.set_mode(xy_display) #Resolucion de la ventana

pygame.display.set_caption('Armonizador musical') #titulo de la ventana 

#imagen
image = pygame.image.load(r'piano.jpeg')
image = pygame.transform.scale(image, (220, 100))

#icono
pygame.display.set_icon(image)

myColor = (10,26,56) #fondo
orange = (255,127,80) #botones
white = (255,255,255) #color de letra 

#variable necesaria para los textos
smallfont = pygame.font.SysFont(None,25)
mediumfont = pygame.font.SysFont(None,30)
bigfont = pygame.font.SysFont(None,75)

#Estilo de los textos
def textObjects(text,color,size):
	if size == "small":
		textSurface = smallfont.render(text,True,color)
	if size == "medium":
		textSurface = mediumfont.render(text,True,color)
	if size == "big":
		textSurface = bigfont.render(text,True,color)
	return textSurface, textSurface.get_rect()

#texto de los botones
def textToButton(msg,color,buttonx,buttony,buttonwidth,buttonheight):
	textSurf, textRect = textObjects(msg,color,"small")
	textRect.center = ((buttonx+(buttonwidth/2)),buttony+(buttonheight/2))
	display.blit(textSurf,textRect)
	
#funcion que lee si se le hizo click al boton 
def button(msg,x,y,width,height, graph = None):
	cur = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	time.sleep()
	if x + width > cur[0] > x and y + height > cur[1] > y and click[0] == 1:
		return buttonActions(msg, graph)
		
def label(msg,color,size,x,y):
	textSurf, textRect = textObjects(msg,color,size)
	textRect.center = (x,y)
	display.blit(textSurf,textRect)
	
		
#Acciones de los diferentes botones, cada uno lleva a la funcion definida
def buttonActions(msg, graph = None):
	if msg == "Exit":
		pygame.quit()
		quit()
	if msg == "Create new graph":		
		return create_graph_display(graph)
	if msg == "Create a song":
		create_song_base_note(graph)
	if msg == "Choose graph":		
		return select_graph_display(graph)
	if msg == "Training":
		training_count(graph)			
	if msg == "Return":
		draw_menu_display()
		
def draw_menu_display():
	display.fill(myColor)
	
	#imagen
	display.blit(image,(150,0))
	
	#Uso de draw  eje x, eje y, largo, altura
	
	#Codigo de posiciones de los textos
	textToButton("Create new graph",white,150,100,200,75)
	textToButton("Create a song",white,150,150,200,75)
	textToButton("Choose graph",white,150,200,200,75)
	textToButton("Training",white,150,250,200,75)
	textToButton("Exit",white,340,272,200,75)

	#Aplica los cambios realizados en el fondo
	pygame.display.update()

#metodo de inicializacion 
def init():

	display.fill(myColor)
	
	#imagen
	display.blit(image,(150,0))
	
	
	#Uso de draw  eje x, eje y, largo, altura
	
	#Codigo de posiciones de los textos
	textToButton("Create new graph",white,150,100,200,75)
	textToButton("Create a song",white,150,150,200,75)
	textToButton("Choose graph",white,150,200,200,75)
	textToButton("Training",white,150,250,200,75)
	textToButton("Exit",white,340,272,200,75)

	#Aplica los cambios realizados en el fondo
	pygame.display.update()

	#grafo
	graph = None
	
	time.sleep(0.25)
	mainloop = True
	while mainloop:
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mainloop = False
	
		#espera de los evento de presionar los botones 
		graph = button("Create new graph",150,100,200,75, graph)
		button("Create a song",150,150,200,75, graph)
		graph = button("Choose graph",150,200,200,75, graph)
		button("Training",150,250,200,75, graph)
		button("Exit",340,272,200,75)

def create_graph_display(graph):

	time.sleep(0.25)
	input_graph_name = '' 	
	mainloop = True
	while mainloop:
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mainloop = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					input_graph_name = input_graph_name[:-1]
				elif event.key == pygame.K_RETURN:
					#Aqui se llama el metodo que recomienda -------------
					graph = Graph(0, input_graph_name)
					graph.save_graph_to_json()
					text = "Graph '" + input_graph_name + "' created!" 
					show_text = smallfont.render(text, 1,white)
					display.blit(show_text,(150,100))
					pygame.display.update()
					time.sleep(2)
					draw_menu_display()					
					return graph					
				else:
					input_graph_name += event.unicode

		display.fill(myColor)
		show_input_chord = smallfont.render(input_graph_name, 1,white)
		display.blit(show_input_chord,(342,50))
		text = "Write the graph name or genre: "
		show_text = smallfont.render(text, 1,white)
		display.blit(show_text,(100,0))
		textToButton("Return",white,340,272,200,75)
		button("Return",340,272,200,75)
		pygame.display.update()



def select_graph_display(graph):

	time.sleep(0.25)
	input_graph_name = '' 	
	mainloop = True
	while mainloop:
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mainloop = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					input_graph_name = input_graph_name[:-1]
				elif event.key == pygame.K_RETURN:

					graph = Graph(1, input_graph_name, input_graph_name)
					print(graph)
					text = "Graph '" + input_graph_name + "' loaded!" 
					show_text = smallfont.render(text, 1, white)
					display.blit(show_text,(150,100))
					pygame.display.update()
					time.sleep(2)
					draw_menu_display()	
					return graph

				else:
					input_graph_name += event.unicode

		display.fill(myColor)
		show_graph_name = smallfont.render(input_graph_name, 1,white)
		display.blit(show_graph_name,(342,50))
		text = "Write the graph name you want to select: "
		show_text = smallfont.render(text, 1,white)
		display.blit(show_text,(100,0))
		textToButton("Return",white,340,272,200,75)
		button("Return",340,272,200,75)
		pygame.display.update()
		
#Inicializa el fondo y aplica los valores para mostrar la ventana general	
def create_song_base_note(graph):

	time.sleep(0.25)
	input_base_chord = '' 	
	mainloop = True
	while mainloop:
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mainloop = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					input_base_chord = input_base_chord[:-1]
				elif event.key == pygame.K_RETURN:
					#Aqui se llama el metodo que recomienda -------------													
					create_song_length(input_base_chord, graph)
					#print("Enter")
				else:
					input_base_chord += event.unicode

		display.fill(myColor)
		show_input_chord = smallfont.render(input_base_chord, 1,white)
		display.blit(show_input_chord,(342,0))
		text = "Write your base chord: "
		show_text = smallfont.render(text, 1,white)
		display.blit(show_text,(150,0))
		textToButton("Return",white,340,272,200,75)
		button("Return",340,272,200,75)
		pygame.display.update()

def create_song_length(base_chord, graph):

	time.sleep(0.25)
	input_song_length = '' 
	mainloop = True
	while mainloop:
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mainloop = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					input_song_length = input_song_length[:-1]
				elif event.key == pygame.K_RETURN:
					#Aqui se llama el metodo que recomienda -------------													
					song_recomend_screen(graph.create_song(int(input_song_length), base_chord))
					#print("Enter")
				else:
					input_song_length += event.unicode

		display.fill(myColor)
		show_input_length = smallfont.render(input_song_length, 1,white)
		display.blit(show_input_length,(342,0))
		text = "Write the length of the song: "
		show_text = smallfont.render(text, 1,white)
		display.blit(show_text,(100,0))
		textToButton("Return",white,340,272,200,75)
		button("Return",340,272,200,75)
		pygame.display.update()

def song_recomend_screen(new_song):

	time.sleep(0.25)
	display.fill(myColor)

	textToButton("Return",white,340,272,200,75)

	#ejemplo de como se puede poner una variable en pantalla
	song_text = ""

	for i in range(len(new_song)):
		if(i != len(new_song) - 1):
			song_text += get_chord_name(new_song[i]) + ", "
		else:
			song_text += get_chord_name(new_song[i]) 

	show_song = smallfont.render("Song:", 1,white)
	display.blit(show_song,(225,0)) #permite desplegar e la pos que se le indique en el parametro

	song_text_wrapped = textwrap.fill(song_text, 50)
	song_split = song_text_wrapped.split("\n")

	line_height = 50
	for line in song_split:
		show_line = smallfont.render(line, 1, white)
		display.blit(show_line,(25,line_height))
		
		line_height+=25

	pygame.display.update()

	mainloop = True
	while mainloop:
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mainloop = False

		button("Return",340,272,200,75)

def training_count():
	time.sleep(0.25)
	input_training_count = '' 	
	mainloop = True
	while mainloop:
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mainloop = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					input_training_count = input_training_count[:-1]
				elif event.key == pygame.K_RETURN:
					#Aqui se llama el metodo que recomienda -------------													
					training_display(int(input_training_count))
					draw_menu_display()	
					return
					#print("Enter")
				else:
					input_training_count += event.unicode

		display.fill(myColor)
		show_input_length = smallfont.render(input_training_count, 1,white)
		display.blit(show_input_length,(342,50))
		text = "Write the amount of training iterations: "
		show_text = smallfont.render(text, 1,white)
		display.blit(show_text,(100,0))
		textToButton("Return",white,340,272,200,75)
		button("Return",340,272,200,75)
		pygame.display.update()

def training_display(count):
	time.sleep(0.25)
	current_iteration = 1
	reader = TextSongReader()
	song_list = reader.read_dir()
	while current_iteration <= count:

		display.fill(myColor)
		text = "Iteration count: "
		show_text = smallfont.render(text, 1,white)
		display.blit(show_text,(100,0))

		display.fill(myColor)
		text = str(current_iteration)
		show_text = bigfont.render(text, 1,white)
		display.blit(show_text,(200,50))

		pygame.display.update()

		for song in song_list:
			song = convert_song('C:/Users/Marco/Desktop/UCR/I Semestre 2020/Inteligencia Artificial/Proyecto/Canciones/TXT Acordes/Clásica/' + song, 'C', '', True)
			graph.training(song)

		current_iteration += 1

	text = "Finished! Going back in 3..2..1"
	graph.save_graph_to_json()
	show_text = mediumfont.render(text, 1, white)
	display.blit(show_text,(220,100))
	pygame.display.update()
	time.sleep(3)
	return	

#llama a la funcion que inicializa todo el programa 	
init()
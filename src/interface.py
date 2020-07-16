#librerias que se importan
from pygame import mixer
import pygame
import time
import textwrap
import sys,os
import random
from chordsGraph import *
from ChordsId import *
from TextSongReader import *
from SongConversor import *


#inicializa todos los modulos de pygame
#retorna si la inicializacion fue exitosa o no 
pygame.init()
APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
mixer.init()

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

graph = None
new_song = None
index = None
auto_play = False
cursor = 0
base = 0
tope = 6

Notes_Sound_Files = {
    0:'c.ogg',
    1:'c#.ogg', 
    2:'d.ogg',
    3:'d#.ogg',
    4:'e.ogg', 
    5:'f.ogg', 
    6:'f#.ogg', 
    7:'g.ogg',
    8:'g#.ogg',
    9:'a.ogg',
    10:'a#.ogg', 
    11:'b.ogg',
}

Chord_Individual_Notes = {
    '':[0,4,7],
    'm':[0,3,7],
    '7':[0,4,7,10],
    'm7':[0,3,7,10],
    'maj7':[0,4,7,11],
    'mm7':[0,3,7,11],
    '6':[0,4,7,9],
    'm6':[0,3,7,9],
    '6/9':[0,2,4,7,9],
    '5':[0,7],
    '9':[0,2,4,7,10],
    'm9':[0,2,3,7,10],
    'maj9':[0,2,4,7,11],
    '11':[0,2,4,5,7,10],
    'm11':[0,2,3,5,7,10],
    '13':[0,2,4,5,7,9,10],
    'm13':[0,2,3,5,7,9,10],
    'maj13':[0,2,4,7,9,11],
    'add':[0,2,4,7],
    '7-5':[0,4,6,10],
    '7+5':[0,4,8,10],
    'sus':[0,5,7],
    'dim':[0,3,6],
    'dim7':[0,3,6,9],
    'm7b5':[0,3,6,10],
    'aug':[0,4,8],
    'aug7':[0,4,8,10]
}

Note_Displacement = {
    'B#':0,
    'C':0, 
    'C#':1, 
    'Db':1, 
    'D':2, 
    'D#':3, 
    'Eb':3,
    'E':4,
    'Fb':4,
    'E#':5, 
    'F':5, 
    'F#':6, 
    'Gb':6, 
    'G':7, 
    'G#':8, 
    'Ab':8, 
    'A':9, 
    'A#':10, 
    'Bb':10, 
    'B':11,
    'Cb':11
}

def play_chord (chord_str):

    base_note = ''
    chord_variation = ''
    #Este if y else determina si el acorde es valido
    if len( chord_str ) > 0:
        if (len( chord_str ) > 1 ) and ( chord_str[1] in ['#', 'b']) :
            base_note = chord_str[0].upper() + chord_str[1]

            if len( chord_str ) > 2:
                chord_variation = chord_str[2:].lower()
        else: 
            base_note = chord_str[0].upper()
            if len( chord_str ) > 1:
                chord_variation = chord_str[1:].lower()



    notes = Chord_Individual_Notes[chord_variation]
    
    #Carga primero los sonidos
    sounds = []
    for note in notes:
        displaced_note = ((note + Note_Displacement[base_note])) % 12
        sounds.append(mixer.Sound(os.path.join(APP_FOLDER, 'Sounds/' + Notes_Sound_Files[displaced_note])))

    #Despues los toca
    for sound in sounds:
        sound.play()

    #Delay entre las notas  
    #time.delay(1000)

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
def button(msg,x,y,width,height):
	cur = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x + width > cur[0] > x and y + height > cur[1] > y and click[0] == 1:
		buttonActions(msg)
		
def label(msg,color,size,x,y):
	textSurf, textRect = textObjects(msg,color,size)
	textRect.center = (x,y)
	display.blit(textSurf,textRect)
	
		
#Acciones de los diferentes botones, cada uno lleva a la funcion definida
def buttonActions(msg):
	global index
	global new_song
	global auto_play
	if msg == "Exit":
		pygame.quit()
		quit()
	if msg == "Create new graph":		
		create_graph_display()
	if msg == "Create a song":
		create_song_base_note()
	if msg == "Choose graph":		
		select_graph_display()
	if msg == "Training":
		training_count()
	if msg == "Play":
		play_chord (get_chord_name(new_song[index]))
	if msg == "Auto Play":
		auto_play = True
		index = 0
		for i in range(len(new_song)):
			song_recomend_screen()
			time.sleep(0.7)
			index += 1
		auto_play = False
	if msg == "Begin":
		index = 0
		song_recomend_screen()
	if msg == "Reset":
		create_song_base_note()
	if msg == "Next":
		if index + 1 == len(new_song):
			print("Se excedio del lenght de la cancion")
		else:
			index += 1
		song_recomend_screen()
	if msg == "Prev":
		if index - 1 < 0:
			print("Se excedio del lenght de la cancion")
		else:
			index -= 1
		song_recomend_screen()
	if msg == "Return":
		init()
		
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
	
	time.sleep(0.25)
	mainloop = True
	while mainloop:
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mainloop = False
	
		#espera de los evento de presionar los botones 
		button("Create new graph",150,100,200,75)
		button("Create a song",150,150,200,75)
		button("Choose graph",150,200,200,75)
		button("Training",150,250,200,75)
		button("Exit",340,272,200,75)

def create_graph_display():

	global graph
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
					init()			
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



def select_graph_display():
	global graph
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
					#graph.print_graph()
					text = "Graph '" + input_graph_name + "' loaded!" 
					show_text = smallfont.render(text, 1, white)
					display.blit(show_text,(150,100))
					pygame.display.update()
					time.sleep(2)
					init()
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
def create_song_base_note():
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
					create_song_first_note(input_base_chord)
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

def create_song_first_note(base_note):
	time.sleep(0.25)
	input_first_note = '' 	
	mainloop = True
	while mainloop:
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mainloop = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					input_first_note = input_base_chord[:-1]
				elif event.key == pygame.K_RETURN:
					#Aqui se llama el metodo que recomienda -------------													
					create_song_length(base_note, input_first_note)
					#print("Enter")
				else:
					input_first_note += event.unicode

		display.fill(myColor)
		show_input_chord = smallfont.render(input_first_note, 1,white)
		display.blit(show_input_chord,(342,0))
		text = "Write the first note: "
		show_text = smallfont.render(text, 1,white)
		display.blit(show_text,(150,0))
		textToButton("Return",white,340,272,200,75)
		button("Return",340,272,200,75)
		pygame.display.update()

def create_song_length(base_note, first_note):
	global graph
	global new_song
	global index 
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
					new_song = graph.create_song(int(input_song_length), first_note)	
					index = 0											
					song_recomend_screen()
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

def song_recomend_screen():
	global index
	global new_song
	global auto_play
	global tope
	global base 
	time.sleep(0.25)
	display.fill(myColor)


	#Dibujos de los triangulos
	pygame.draw.polygon(display,orange,((400,100),(460,150),(400,200)))
	pygame.draw.polygon(display,orange,((80,100),(20,150),(80,200)))

	pygame.draw.polygon(display,orange,((225,80),(255,100),(225,120)))
	pygame.draw.polygon(display,orange,((245,80),(275,100),(245,120)))

	#Uso de draw  eje x, eje y, largo, altura
	textToButton("Play",white,150,225,200,75)
	textToButton("Auto Play",white,150,65,200,75)
	textToButton("Next",white,325,112,200,75)
	textToButton("Prev",white,-40,112,200,75)
	textToButton("Reset",white,0,225,200,75)
	textToButton("Begin",white,300,225,200,75)
	textToButton("Return",white,340,272,200,75)

	
	
	show_song = smallfont.render("Song",1,white)
	display.blit(show_song,(225,0)) #permite desplegar e la pos que se le indique en el parametro

	line_x = 25
	if(index > tope / 2 and len(new_song) > tope):
		base += 1
		tope += 1
	elif(index == base and base > 0):
		base -= 1
		tope -= 1
	for i in range(base,tope):
		if(i == index):
			show_line = smallfont.render(get_chord_name(new_song[i]), 1, orange)
		else:
			show_line = smallfont.render(get_chord_name(new_song[i]), 1, white)
		display.blit(show_line,(line_x,50))
		if(i != len(new_song) - 1):
			show_separator = smallfont.render("|", 1, white)
			display.blit(show_separator,(line_x + 60,50))
		line_x +=75


	show_chord = bigfont.render(get_chord_name(new_song[index]),250,white)
	display.blit(show_chord,(230,120))

	pygame.display.update()
	if not auto_play:
		mainloop = True
		while mainloop:
		
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					mainloop = False

			button("Play",150,225,200,75)
			button("Auto Play",150,65,200,75)
			button("Next",325,112,200,75)
			button("Prev",-40,112,200,75)
			button("Reset",0,225,200,75)
			button("Begin",300,225,200,75)
			button("Return",340,272,200,75)
	else:
		play_chord(get_chord_name(new_song[index]))

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
					#draw_menu_display()	
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
	global graph
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

		random.shuffle(song_list)
		for song in song_list:
			c_song = convert_song('TXT Acordes/Clásica/' + song, 'C', '', True)
			#print(song, c_song)
			graph.training(c_song)

		current_iteration += 1

	text = "Finished! Going back in 3..2..1"
	graph.save_graph_to_json()
	show_text = mediumfont.render(text, 1, white)
	display.blit(show_text,(100,100))
	pygame.display.update()
	time.sleep(3)
	init()	

#llama a la funcion que inicializa todo el programa 	
init()
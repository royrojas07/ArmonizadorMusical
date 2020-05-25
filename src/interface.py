#librerias que se importan
import pygame 
import time
from chordsGraph import *


#inicializa todos los modulos de pygame
#retorna si la inicializacion fue exitosa o no 
pygame.init()

#va a ser nuestra superficie 
display = pygame.display.set_mode((480,320)) #Resolucion de la ventana

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
    if msg == "Exit":
        pygame.quit()
        quit()
    if msg == "Start":
        prueba = Graph(0,"prueba.txt")
        print("--------------------------------")
        prueba.training("cancion.txt")
        prueba.print_graph()
        prueba.save_graph_to_json()
    if msg == "Choose graph":
    	prueba = Graph(1, "classical.json")
    	prueba.print_graph()
    if msg == "Training":
        print(msg)
		


#metodo de inicializacion 
def init():

	display.fill(myColor)
	
	#imagen
	display.blit(image,(150,0))
	
	
	#Uso de draw  eje x, eje y, largo, altura
	
	#Codigo de posiciones de los textos
	textToButton("Start",white,150,100,200,75)
	textToButton("Choose graph",white,150,150,200,75)
	textToButton("Training",white,150,200,200,75)
	textToButton("Exit",white,340,272,200,75)

	#Aplica los cambios realizados en el fondo
	pygame.display.update()
	
	time.sleep(0.25)
	
	mainloop = True
	while mainloop:
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mainloop = False
	
		#espera de los evento de presionar los botones 
		button("Start",150,100,200,75)
		button("Choose graph",150,150,200,75)
		button("Training",150,200,200,75)
		button("Exit",340,272,200,75)
	
		
#Inicializa el fondo y aplica los valores para mostrar la ventana general	
def start():
    pass
def training():
    pass
	
	
#llama a la funcion que inicializa todo el programa 	
init()
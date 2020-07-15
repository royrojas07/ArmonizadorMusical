# ArmonizadorMusical
Repositorio con el código fuente del proyecto del curso Inteligencia Artificial (CI-0129)

Actualmente el repositorio cuenta con dos branches, el master donde se piensa implementar el Armonizador Músical con una interfaz gráfica con pygames*, para el master el código todavía no es funcional ya que no se ha adaptado el uso de la interfaz con pygames.

El otro branch "Command-Line-Interface" cuenta con una versión funcional del código pero con una interfaz en línea de comandos que se despliega como un menú de opciones las funciones del programa. Para ejecutar este código, en línea de comandos o terminal se debe ejecutar "main.py" con Python3. Además, este branch cuenta con un archivo .json donde se almacena un grafo ya entrenado con aproximadamente 15000 iteraciones del algoritmo de entrenamiento.

Si el profesor Markus o alguien más desea ver un ejemplo de una canción creada a partir el grafo tiene que seguir el siguiente procedimiento:
 1. Descargar los archivos en el branch "Command-Line-Interface" y descomprimirlos en la carpeta que guste.
 1. Abrir la línea de comandos de Windows o terminal de Linux e ir al directorio del código.
 1. Ejecutar con Python 3 el archivo main.py.
 1. En el menú de opciones: 
    1.  Escoger la opción de "Select existing graph" e ingresar el nombre del grafo "classical" para cargar el grafo.
    1.  Escoger la opción de "Create new song from current graph" 
        1.  Ingresar la nota base de donde quiere que se base la canción, por ejemplo "C" o "D".
        1.  Ingresar la cantidad de acordes que quiere que tenga la canción, por ejemplo 30 o 50.
        1.  Se desplegará una canción creada usando el grafo con Cadenas de Markov.
        

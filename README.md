# Armonizador Musical
Repositorio con el código fuente del proyecto del curso Inteligencia Artificial (CI-0129)

Este proyecto consiste en un armonizador musical que genera una secuencia de acordes con base en diferentes géneros musicales. El repositorio cuenta con 3 diferentes géneros (Jazz, Rock y Classical) por defecto pero se pueden añadir y entrenar más.

## Explicación General
El armonizador utiliza Cadenas de Markov en donde cada nodo del grafo corresponde a una serie de acordes y sus caminos corresponden a la probabilidad de que continue el siguiente nodo dentro de la secuencia de acordes. Para calcular la probabilidad de que un nodo escoja a otro nodo como parte de su secuencia, se calcula la cantidad de veces que se pasó por el nodo origen entre la cantidad de veces que se pasó por la arista destino. 

También, cabe mencionar que se utilizan varios tipos de nodos, simples, dobles y triples en donde cada uno de estos corresponde a un conjunto de acordes pasados (Algo como un tipo de memoria para que el grafo pueda recordar si ya tocó varios acordes en secuencia y no se repita mucho). 

## Iniciar el programa
1. Abrir la terminal ya sea en windows o en linux. 
1. Correr el comando "python interface.py", sí no se tiene instalada la librería pygame por favor hacerlo con el comando "pip install pygame". 

## Generar una canción nueva
1. Primero se debe cargar un grafo con la opción "Choose graph". 
1. Luego se nos pedirá digitar el nombre del grafo que queremos cargar, si elegimos un nombre inválido se indicará en la terminal. 
1. Después se debe presionar la opción "Create a song", en donde se pedirá la tonalidad, primer acorde y longitud de la canción que deseamos.
1. Finalmente se llegará una interfaz en donde el usuario puede reproducir cada acorde creado de manera individual presionando "play" y navegar 
por la canción con los botones "prev" y "next" , o bien reproducirla de forma automática con el botón "autoplay". 
1. Para facilidad en el menú siempre podemos volver al inicio de la canción con begin o crear una canción con otra tonalidad, primer acorde y longitud 
nuevamente con "Reset". 

## Entrenar un grafo
1. Después de ya haber cargado un grafo con "Choose graph" si se desea entrenar se deberá presionar el botón de "Training". 
1. La interfaz mostrada nos pedirá por el número de iteraciones que deseamos para entrenar el grafo. 
1. Por último veremos un contador que irá subiendo hasta nuestro número seleccionado, indicando por cual iteración de entrenamiento 
vamos hasta que esté listo. 
### Nota: 
El grafo busca las canciones en la carpeta con el mismo nombre del grafo dentro de “/src/TXT Acordes”. En esta misma carpeta es donde se deberían guardar los conjuntos de canciones con las que se quiera entrenar el grafo.

## Crear un grafo
1. Para esta acción escogemos la opción "Create new graph".
1. Posteriormente se nos solicitará un nombre para este grafo.
1. Luego con el nombre creado debemos cargarlo con "Choose Graph".
1. Debemos luego entrenarlo con un número de iteraciones razonable.
1. Luego podremos proceder a crear una canción a partir del grafo.

## Formato de las canciones TXT
El conjunto de entrenamiento se compone de las canciones que son básicamente archivos de texto con la secuencia de acordes.
Un archivo de texto con los acordes debe seguir el siguiente formato:
1. Primero, debe tener la nota base o tonalidad de la canción.
1. Luego, todos los acordes de la canción separados por coma, espacios o cada acorde por línea. Cualquier combinación de las diferentes formas de separar los acordes también es válida.


### Notas base válidas:	
* C o B#, C# o Db, D, D# o Eb, E o Fb, F o E#, F# o Gb, G, G# o Ab, A, A# o Bb, B o Cb
### Acordes válidos:	
* Estructura: Nota base + acorde.
* Acordes: Ninguno, m, 7, m7, maj7, mm7, 6, m6, 5, add, dim, aug
* Ejemplos: C, Bm,  Ebm7, C#aug…
* Nota: Existen notas que se escriben diferente pero suenan igual como C y B#, F o E#... (Como se indica en las notas base) entonces se pueden utilizar cualquiera de las 2 notas base.

### Pequeños Bugs
* Puede que a la hora de reproducir una canción, la interfaz se quede pegada hasta que finalice la propia canción. Solo hay que esperar a que termine la canción para que se pueda volver a utilizar la interfaz.
* También, puede que la interfaz se quede pegada en el proceso de entrenamiento un grafo (Alrededor de las 250 iteraciones) y se desbloquea cuando terminar.

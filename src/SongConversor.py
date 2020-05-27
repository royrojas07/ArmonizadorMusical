from ChordsId import *
from TextSongReader import *
from ScaleConversor import *

#este diccionario dice cuales acordes se convierten a cuales
#transforma los id de las variaciones a otros id de otras variaciones
default_conversion_table = {
    0:0, #major
    1:1, #minor
    2:2, # 7
    3:3, # m7
    4:4, #maj7
    5:5, #mm7
    6:6, #6
    7:7, #m6
    8:6, #6/9
    9:9, #5
    10:2, #9
    11:3, #m9
    12:4, #maj9
    13:2, #11 
    14:3, #m11
    15:2, #13
    16:3, #m13
    17:4, #maj13
    18:18, #add
    19:2, #7-5**
    20:2, #7+5**
    21:5, #sus**
    22:22, #dim
    23:22, #dim7
    24:22, #'m7b5
    25:25, #aug
    26:25 #aug7



}

def convert_chord (chord_name_str, conversion_file = ''):
    """
    converts chord depending on the conversion table
    @type conversion_file: str
    @param conversion_file: specifies chord conversion table
    @type chord_name_str: str
    @param chord_name_str: chord name
    @rtype: int
    @return: converted chord
    """
    converted_id = 0

    if conversion_file == '':
        conversion_table = default_conversion_table
    #TODO ELSE DE CONVERSION TABLE

    chord_id = get_chord_id(chord_name_str)
    base_note = math.floor(chord_id/100)
    chord_variation = chord_id - (base_note * 100)
    converted_id = (base_note*100)+ conversion_table[chord_variation]

    return converted_id


def convert_song (song_file_name, base_note = 'C',conversion_file = '', id_option = False):

    """
    converts chord depending on the conversion table
    @type song_dir_name: str
    @param song_file_name: specifies the song file name
    @type base_note: str
    @param base_note: specifies the base note to convert to
    @type conversion_file: str
    @param conversion_file: specifies the conversion file for custom conversion tables
    @rtype: list
    @return: converted song
    """
    returned_song = None
    songReader = TextSongReader()
    scale_conv = ScaleConversor(base_note)

    #obtiene el contenido de la cancion
    song_content = songReader.read(song_file_name)
    
    #lista de canciones con en donde cada cancion tiene sus acordes por id de acorde
    
    converted_song = []
    
    for chord in song_content:
        if is_chord_valid(chord):
            converted_chord = convert_chord (chord, conversion_file)
            #TODO puede ser que desde que aqui se convierta la escala de la cancion
            if (not id_option): 
                converted_chord_str = get_chord_name(converted_chord)
                converted_song.append (converted_chord_str)
            else:
                converted_song.append (converted_chord)

    #le cambia la escala a la cancion
    if (not id_option): 
        converted_scale_song = []
        for chord in scale_conv.convert(converted_song):
            converted_scale_song.append(str(chord))
        returned_song = converted_scale_song
    else: 
        returned_song =  converted_song


    return returned_song

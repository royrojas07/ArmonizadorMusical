import math

Chord_Notes = {
    'B#':1,
    'C':1, 
    'C#':2, 
    'Db':2, 
    'D':3, 
    'D#':4, 
    'Eb':4,
    'E':5,
    'Fb':5,
    'E#':6, 
    'F':6, 
    'F#':7, 
    'Gb':7, 
    'G':8, 
    'G#':9, 
    'Ab':9, 
    'A':10, 
    'A#':11, 
    'Bb':11, 
    'B':12,
    'Cb':12
}

Chord_Variations = {
    '':0,
    'm':1,
    '7':2,
    'm7':3,
    'maj7':4,
    'mm7':5,
    '6':6,
    'm6':7,
    '6/9':8,
    '5':9,
    '9':10,
    'm9':11,
    'maj9':12,
    '11':13,
    'm11':14,
    '13':15,
    'm13':16,
    'maj13':17,
    'add':18,
    '7-5':19,
    '7+5':20,
    'sus':21,
    'dim':22,
    'dim7':23,
    'm7b5':24,
    'aug':25,
    'aug7':26
}


def get_chord_id(chord_str_input):
    """
    gets chord id from a chord name
    @type chord: str
    @param chord: chord name
    @rtype: int
    @return: chord id
    """
    value = -1
    chord_str = chord_str_input.strip()

    base_note = ''
    chord_variation = ''

    #Este if y else determina si el acorde es valido
    if (len( chord_str ) > 1 ) and ( chord_str[1] in ['#', 'b']) :
        base_note = chord_str[0].upper() + chord_str[1]

        if len( chord_str ) > 2:
            chord_variation = chord_str[2:].lower()
    else: 
        base_note = chord_str[0].upper()
        if len( chord_str ) > 1:
            chord_variation = chord_str[1:].lower()

    #si es valido su id es esa formula
    if base_note in Chord_Notes and chord_variation in Chord_Variations: 
        value = ((Chord_Notes[base_note] * 100)) + Chord_Variations[chord_variation]

    return value

def get_chord_name(chord_id):
    """
    Gets the chord name from its id
    @type chord: int
    @param chord: chord_id
    @rtype: str
    @return: chord_str
    """
    chord_str = ''

    has_base_note = False
    has_variation = False
    #Formulas para obtener el valor
    base_note = math.floor(chord_id/100)
    chord_variation = chord_id - (base_note * 100)
    base_note_key = ''
    variation_key = ''

    
    #busca en Chord_Notes la key de la llave y la asigna a base_note_key
    for key, value in Chord_Notes.items() : 
        if base_note == value and has_base_note == False: 
            #print ('asd', key, value, 'ccac', base_note)
            base_note_key = key 
            has_base_note = True


    #busca en Chord_Notes la key de la llave y la asigna a  chord_variation_key
    for key, value in Chord_Variations.items(): 
        if chord_variation == value and has_variation == False:
            
            variation_key = key 
            has_variation = True

    if has_base_note and has_variation:
        chord_str = base_note_key + variation_key

    return chord_str

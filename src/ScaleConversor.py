class Chord:
    def __init__( self, name, value ):
        self.name = name
        self.value = value

    def get_name( self ):
        return self.name
    
    def set_name( self, nname ):
        self.name = nname

    def get_value( self ):
        return self.value
    
    def set_value( self, nvalue ):
        self.value = nvalue

    def __eq__( self, other_chord ):
        return self.value == other_chord.value

class ScaleConversor:
    def __init__( self, base_note ):
        self.base_note = base_note.upper()
        self.basic_chords = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        self.chord_values = {'C':1, 'C#':2, 'Db':2, 'D':3, 'D#':4, 'Eb':4,
                'E':5, 'F':6, 'F#':7, 'Gb':7, 'G':8, 'G#':9, 'Ab':9, 'A':10, 'A#':11, 'Bb':11, 'B':12 }

    def chord_value( self, chord ):
        value = 0
        if chord[0].upper() in self.basic_chords:
            if (len( chord ) > 1) and (chord[1].lower() in ['#', 'b']):
                value = self.chord_values[chord[0:2]]
            else:
                value = self.chord_values[chord[0]]
        return value

    def convert( self, file_name ):
        chord_list = []
        song_file = open( file_name )
        file_base_note = song_file.readline()
        file_chord_buffer = song_file.read()
        chord_sequence_str = chord_sequence_str.split()

        for chord in chord_sequence_str:
            if chord[0].upper() in self.basic_chords::
                chord_list.append( Chord( chord, chord_value( chord ) ) )
        
        if file_base_note != self.base_note: # otherwise conversion is not necessary
            return convert_chord_sequence( file_base_note, chord_list )
        return chord_list
    
    def convert_chord_sequence( self, base_note, sequence ):
        bases_difference = self.chord_values[base_note] - self.chord_values[self.base_note]
        for chord in sequence:
            chord.set_value( chord.get_value() - bases_difference )

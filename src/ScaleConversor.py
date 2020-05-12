class Chord:
    def __init__( self, name, value=None ):
        self.name = name
        self.chord_bases = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.chord_values = {'C':1, 'C#':2, 'Db':2, 'D':3, 'D#':4, 'Eb':4,
                'E':5, 'F':6, 'F#':7, 'Gb':7, 'G':8, 'G#':9, 'Ab':9, 'A':10, 'A#':11, 'Bb':11, 'B':12}
        if value == None:
            self.value = self.chord_value( name )
        else:
            self.value = value

    def get_name( self ):
        return self.name
    
    def set_name( self, nname ):
        self.name = nname

    def get_value( self ):
        return self.value
    
    def set_value( self, nvalue ):
        self.value = nvalue

    def chord_base( self ):
        if ( len( self.name ) > 1 ) and ( self.name[1] in ['#', 'b'] ):
            return self.name[:2]
        else:
            return self.name[0]

    def chord_value( self, chord ):
        value = 0
        if chord[0].upper() in self.chord_bases:
            if ( len( chord ) > 1 ) and ( chord[1].lower() in ['#', 'b'] ):
                value = self.chord_values[chord[0:2]]
            else:
                value = self.chord_values[chord[0]]
        return value

    def __sub__( self, difference ):
        nvalue = ( self.value - difference ) % 12
        nname = self.chord_bases[nvalue-1]
        if len( self.chord_base() ) > 1:
            nname += self.name[2:]
        else:
            nname += self.name[1:]
        return Chord( nname, nvalue )

    def __eq__( self, other_chord ):
        return ( self.value == other_chord.value ) and ( self.name == other_chord.name )
    
    def __str__( self ):
        return "(%s, %d)" % ( self.name, self.value )

class ScaleConversor:
    def __init__( self, base_note ):
        self.base_note = base_note
        self.basic_chords = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

    def convert( self, file_name ):
        chord_list = []
        song_file = open( file_name )
        song_base_note = song_file.readline().rstrip( '\n' )
        chord_sequence_str = song_file.read().split()

        for chord in chord_sequence_str:
            if chord[0].upper() in self.basic_chords:
                chord_list.append( Chord( chord ) )
        
        if song_base_note != self.base_note: # otherwise conversion is not necessary
            return self.convert_chord_sequence( song_base_note, chord_list )
        return chord_list
    
    def convert_chord_sequence( self, base_note, sequence ):
        converted_chord_sequence = []
        bases_difference = Chord( base_note ).get_value() - Chord( self.base_note ).get_value()
        for chord in sequence:
            converted_chord_sequence.append( chord - bases_difference )
        return converted_chord_sequence

def testing():
    """
    this function is only for testing purposes
    """
    chord = Chord( 'F#m7' )
    chord2 = Chord( 'F#m7', 1 )

    if ( chord == chord2 ) == False:
        if chord.chord_base() == 'F#':
            nchord = chord - 10
            print( nchord )

    conversor = ScaleConversor( 'A#' )
    for c in conversor.convert_chord_sequence( 'D', [Chord( 'Dmaj7' ), Chord( 'A7' ), Chord( 'G' ), Chord( 'Bm' )] ):
        print(c)
    
    print( "testing convert()" )
    conversor = ScaleConversor( 'C' )
    for c in conversor.convert( 'xsong.txt' ):
        print(c)

if __name__ == '__main__':
    testing()
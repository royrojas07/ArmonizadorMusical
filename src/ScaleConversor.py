class Chord:
    def __init__( self, name, value=None ):
        self.name = name
        self.root_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        #self.root_notes_values = {'C':1, 'C#':2, 'Db':2, 'D':3, 'D#':4, 'Eb':4,
        #        'E':5, 'F':6, 'F#':7, 'Gb':7, 'G':8, 'G#':9, 'Ab':9, 'A':10, 'A#':11, 'Bb':11, 'B':12}

        self.root_notes_values = {'B#':1,'C':1, 'C#':2, 'Db':2, 'D':3, 'D#':4, 'Eb':4,'E':5,'Fb':5,'E#':6, 'F':6, 
                                    'F#':7, 'Gb':7, 'G':8, 'G#':9, 'Ab':9, 'A':10, 'A#':11, 'Bb':11, 'B':12,'Cb':12}
        if value == None:
            self.value = self.chord_value( name )
        else:
            self.value = value

    def get_name( self ):
        return self.name
    
    def set_name( self, nname):
        self.name = nname

    def get_value( self ):
        return self.value
    
    def set_value( self, nvalue ):
        self.value = nvalue

    def root_note( self ):
        """
        Gets the root note of the chord
        @rtype: str
        @return: root note
        """
        if ( len( self.name ) > 1 ) and ( self.name[1] in ['#', 'b'] ):
            return self.name[:2]
        else:
            return self.name[0]

    def chord_value( self, chord ):
        """
        Gets the chord value
        @type chord: str
        @param chord: name of the chord
        @rtype: int
        @return: chord value
        """
        value = 0
        if chord[0].upper() in self.root_notes:
            if ( len( chord ) > 1 ) and ( chord[1].lower() in ['#', 'b'] ):
                #chord_upper = chord[0:2]
                #value = self.root_notes_values[chord[0:2]]
                value = self.root_notes_values[chord[0].upper() + chord[1]]
            else:
                value = self.root_notes_values[chord[0].upper()]
        return value

    def __sub__( self, semitones ):
        """
        Substracts semitones from the current chord
        @type semitones: int
        @param semitones: number of semitones to substract
        @rtype: Chord
        @return: new Chord with substracted semitones
        """
        nvalue = ( self.value - semitones ) % 12
        nname = self.root_notes[nvalue-1]
        if len( self.root_note() ) > 1:
            nname += self.name[2:]
        else:
            nname += self.name[1:]
        return Chord( nname, nvalue )

    def __eq__( self, other_chord ):
        return ( self.value == other_chord.value ) and ( self.name == other_chord.name )
    
    def __str__( self ):
        #return "(%s, %d)" % ( self.name, self.value )
        return "%s" % ( self.name)

class ScaleConversor:
    def __init__( self, base_note ):
        self.base_note = base_note
        self.notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

    def convert( self, song ):
        chord_list = []
        song_base_note = song[0]
        chord_sequence_str = song[1:]

        for chord in chord_sequence_str:
            #if chord[0].upper() in self.notes:
            if chord[0].upper() in self.notes and len( chord ) > 0:
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
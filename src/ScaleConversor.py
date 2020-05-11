class ScaleConversor:
    def __init__( self, base_chords ):
        self.base_chords = base_chords
    
    def convert( self, file_name ):
        

class Chord:
    def __init__( self, name, value ):
        self.name = name
        self.value = value
    
    def __eq__( self, other_chord ):
        return self.value == other_chord.value
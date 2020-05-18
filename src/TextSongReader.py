class TextSongReader:
    def __init__( self, delimiter=',' ):
        self.delimiters = ['\n', ' ']
        self.delimiters.append( delimiter )
    
    def read( self, song_file_name ):
        """
        Reads the content of a song text file
        @type song_file_name: str
        @param song_file_name: song text file name
        @rtype: list
        @return: file chords list
        """
        song_file = open( song_file_name )
        content = song_file.read()
        return self.split( content )

    def split( self, string ):
        """
        Splits a string by some delimiters
        @type string: str
        @param string: string to split
        @rtype: list
        @return: splitted string by delimiters
        """
        splitted_string = []
        
        str_len = len( string )
        i = 0
        for j in range( str_len ):
            if string[j] in self.delimiters:
                if i != j:
                    splitted_string.append( string[i:j] )
                i = j+1
        
        if i != j:
            splitted_string.append( string[i:j+1] )
        
        return splitted_string
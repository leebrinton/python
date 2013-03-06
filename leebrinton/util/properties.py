import os

class Properties:
    def __init__( self ):
        self._props = dict()


    def getProperty( self, key ):
    	'''Retrieve the value of a property.
    	
    	Keyword argumnents:
    	
    	key -- the property name
    	
    	Returns: the property value or None if the property is undefined
    	'''
    	
        val = None

        try:
            val = self._props[key]
        except KeyError, err:
            pass

        return val


    def getPropertyOrDefault( self, key, defaultValue ):
    	'''Retrieve the value of a property.
    	
    	Keyword arguments:
    		
    	key -- the property name

        defaultValue -- default value of the property
		
        Retuurns: the property value or
                  the default value if the property is undefined
    	'''
    	
        val = self.getProperty( key )

        if val is None:
            val = defaultValue

        return val


    def setProperty( self, key, value ):
    	'''Set the value of a property.
    	
    	Keyword arguments:
    		
    	key -- the property name
    	
    	value -- the property value
    	
    	Returns: the previous value of the property
    	'''
    	
        old = self.getProperty( key )

        self._props[key] = value

        return old


    def haveProperty( self, key ):
    	'''Determine if a property is defined.
    	
    	Keyword arguments:
    	
    	key -- the property name
    	
    	Returns: True if the property is defined otherwise False
    	'''
    	
        result = True
        val = self.getProperty( key )

        if val is None:
            result = False
            
        return result

    def loadFromSequencw( self, seq ):
        '''Set the value of properties from a sequence.

    	Keyword arguments:
    	
    	seq -- a sequence of key=value pairs
    	
    	Returns: The number of properties set.
        '''
        count = 0

        for line in stream:
            line = line.strip()

            if len( line ) == 0:
                continue

            if line[0] == '#':
                continue

            componentList = line.split( "=" )

            if len( componentList ) == 2:
                if not self.getProperty( componentList[0] ):
                    self.setProperty( componentList[0], componentList[1] )
                    count = count + 1

        return count

    def getEnvVar( self, varname ):
    	'''Get the value of an environment variabble without
        throwing an exception.
    	
    	Keyword arguments:
    		
    	varname -- the environment variable name
    		
    	Returns: the environment variable value or
                 None if the environment variable is undefined	
    	'''

        result = None

        try:
            result = os.environ[varname]
        except KeyError, err:
            pass

        return result


    def setPropFromEnv( self, name ):
    	'''Set the value of a property from an environment variable.
    	
    	Keyword arguments:
    		
    	name -- the property name
    	
    	Returns: the previous value of the property
    	'''

    	result = None
        val = self.getEnvVar( name )

        if val is not None:
            result = self.setProperty( name, val )

        return result

    def setPropertiesFromEnv( self, names ):
        '''Set the value of propeties from
           a collection of environment variables.

        Keyword arguments:

        names -- a collection of property names
        '''

        for name in names:
            self.setPropFromEnv( name )


if __name__ == '__main__':
    filehandle = None
    filename = 'webpix.properties'
    props = Properties()

    try:
        try:
            filehandle = open( filename )
            props.load( filehandle )
        
            for key in ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']:
                print props.getProperty( key )
        except Exception, err:
            print 'Error: ', err
    finally:
        if filehandle:
            filehandle.close()

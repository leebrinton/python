import log

def isBaseString( value ):
    return isinstance( value, basestring )

def isString( value ):
    return isinstance( value, str )

def isUnicode( value ):
    return isinstance( value, unicode )

def isEmpty( value ):
    result = False

    if not isBaseString( value ):
        msg = 'Expecting instance of basestring '
        msg += 'but recieved %s' % str(type(value))
        log.error( msg )
        raise TypeError( msg )
    elif value == None:
        result = True
    elif len(value) == 0:
        result = True

    return result

def noneToEmpty( value ):
    result = value

    if value == None:
        result = ''

    return result

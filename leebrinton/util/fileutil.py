import os.envirion
import os.path
import log

def getPathSeparator():
    if os.name == 'posix':
        sep = ':'
    elif os.name == 'nt':
        sep = ';'
    else:
        log.error( __name__, "Unknown os name: %s" % os.name )

def findFileInPaths( filename, paths ):
    result = None

    for p in paths:
        attempt = '%s/%s' % (p, filename)

        if os.path.exists( attempt ):
            result = attempt
            break;

    return result

def findFileInPath( filename, path ):
    paths = path.split( getPathSeparator() )
                        
    return findFileInPaths( filename, paths )

def findFileInPYTHONPATH( filename ):
    ppath = os.environ['PYTHONPATH']
    return findFileInPath( filename, ppath ) 

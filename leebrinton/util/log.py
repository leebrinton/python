import userutil

_haveLogging = False
_haveApacheCommonsLogging = False

_loggingMethod = None
_defaultLevel = None
_levelByLogName = { 'FileChooser': 'debug', 'DBUtil' : 'debug' }

try:
    import logging
    _loggingMethod = 'logging'
    _defaultLevel = logging.DEBUG

    _logFormat = "%(asctime)-15s %(levelname)s %(name)s %(user)-8s %(message)s"
    logging.basicConfig( format=_logFormat, level=_defaultLevel )

    _haveLogging = True
except ImportError:
    try:
        from org.apache.commons.logging import LogFactory
        _haveApacheCommonsLogging = True
        _loggingMethod = 'org.apache.commons.logging'
        _haveLogging = True
    except ImportError:
        try:
            from java.util.logging import Logger
            from java.util.logging import Level
            _loggingMethod = 'java.util.logging.Logger'
            _haveLogging = True
        except ImportError, err:
            print 'Neither logging nor java.util.logging.Logger is avalable!', err

################################################################################
class LogLevel:
    def __init__( self, levelName ):
        self.name = levelName
        self.__loggingMethodLevel = None

    def __repr__( self ):
        return "LogLevel('%s')" % self.name

    def __str__( self ):
        return self.name

    def setLoggingMethodLevel( self, loggingMethodLevel ):
        self.__loggingMethodLevel = loggingMethodLevel

    def getLoggingMethodLevel( self ):
        return self.__loggingMethodLevel

################################################################################
_levelNames = ('debug', 'info', 'warn', 'error', 'critical')
_logLevelsByName = dict()

for name in _levelNames:
    _logLevelsByName[name] = LogLevel( name )

def setLogLevelByName( name, level ):
    obj = _logLevelsByName[name]
    obj.setLoggingMethodLevel( level )

def getLogLevelByName( name ):
    level = _logLevelsByName[name]
    return level.getLoggingMethodLevel()

################################################################################
class LogBase:
    def __init__( self, loggerName ):
        self.name = loggerName
        self.user = userutil.getCurrentUser()

    def getLoggingLevel( self ):

        try:
            levelName = _levelByLogName[self.name]
            obj = _logLevelsByName[levelName]
            level = obj.getLoggingMethodLevel()
        except KeyError:
            level = _defaultLevel
        
        return level

    def debug( self, msg  ):
        self.logAtLevel( self.name, 'debug', msg )

    def info( self, msg ):
        self.logAtLevel( self.name, 'info', msg )

    def warn( self, msg ):
        self.logAtLevel( self.name, 'warn', msg )

    def error( self, msg ):
        self.logAtLevel( self.name, 'error', msg )

    def critical( self, msg ):
        self.logAtLevel( self.name, 'critical', msg )

    def logAtLevel( self, name, level, msg, msgargs=None ):
        pass

################################################################################
class LogWithPythonLogging( LogBase ):
    def __init__( self, name ):
        LogBase.__init__( self, name )
        setLogLevelByName ( 'debug', logging.DEBUG )
        setLogLevelByName( 'info', logging.INFO )
        setLogLevelByName( 'warn', logging.WARN )
        setLogLevelByName( 'error', logging.ERROR )
        setLogLevelByName( 'critical', logging.CRITICAL )
            
    def logAtLevel( self, name, levelName, msg, msgargs=None ):
        logger = logging.getLogger( name )
        loggingMethodLevel = getLogLevelByName( levelName )

        fmtargs = {'user': self.user}

        if msgargs:
            logger.log( loggingMethodLevel, msg, msargs, extra=fmtargs )
        else:
            logger.log( loggingMethodLevel, msg, extra=fmtargs )

################################################################################
class LogWithApacheCommonsLogging( LogBase ):
    def __init__( self, name ):
        LogBase.__init__( self, name )

    def logAtLevel( self, name, levelName, msg ):
        logger = LogFactory.getFactory().getInstance( name )
        if levelName == 'debug':
            logger.debug( msg );
        elif levelName == 'info':
            logger.info( msg )
        elif levelName == 'warn':
            logger.warn( msg )
        elif levelName == 'error':
            logger.error( msg )
        elif levelName == 'critical':
            logger.fatal( msg )
        else:
            raise Exception( 'Unknown log level [%s]' % levelName   )

################################################################################
class LogWithJavaUtilLogging( LogBase ):
    def __init__( self, name ):
        LogBase.__init__( self, name )
        setLogLevelByName( 'debug', Level.FINE )
        setLogLevelByName( 'info', Level.INFO )
        setLogLevelByName( 'warn', Level.WARNING )
        setLogLevelByName( 'error', Level.SEVERE )
        setLogLevelByName( 'critical', Level.SEVERE )
        _defaultLevel = Level.INFO

    def logAtLevel( self, name, levelName, msg ):
        logger = Logger.getLogger( name )
        loggerLevel = getLogLevelByName( levelName )
        logger.setLevel( self.getLoggingLevel() )
        loggingMethodLevel = loggerLevel
        print str(loggingMethodLevel) + ':' + str(loggerLevel)
        print logger.getLevel()
        logger.log( loggingMethodLevel, msg )

################################################################################
__loggers = dict()

def getLogInstance( key ):
    result = None
    name = 'default'

    try:
        if isinstance( key, basestring):
            name = key
        elif hasattr( key, '__class__'):
            name = key.__class__.__name__
        elif hasattr( key, '__name__'):
            name = key.__name__
        else:
            print( "key: [%s] [%s]" % (key, str(type(key))) )

        result = __loggers[name]
    except KeyError, ke:
        if _haveLogging:
            if _loggingMethod == 'logging':
                result = LogWithPythonLogging( name )
            elif _loggingMethod == 'org.apache.commons.logging':
                result = LogWithApacheCommonsLogging( name );
            elif _loggingMethod == 'java.util.logging.Logger':
                result = LogWithJavaUtilLogging( name )
            else:
                raise Exception(
                    'Unknown logging method: [%s]' % _loggingMethod  )

            __loggers[name] = result
        else:
            raise Exception( 'No usable logging method found!' )

    return result

def debug( name, msg ):
    l = getLogInstance( name )
    l.debug( msg )

def info( name, msg ):
    l = getLogInstance( name )
    l.info( msg )

def warn( name, msg ):
    l = getLogInstance( name )
    l.warn( msg )

def error( name, msg ):
    l = getLogInstance( name )
    l.error( msg )

def critical( name, msg ):
    l = getLogInstance( name )
    l.critical( msg )

if __name__ == '__main__':
    l = getLogInstance( 'log' )
    l.debug( 'This is a Debug test' );
    l.info( 'This is an Info test' );
    l.warn( 'This is a Warn test' );
    l.error( 'This is an Error test' );
    l.critical( 'This is a Critical test' );

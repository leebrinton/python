import leebrinton.util.log as log
import sys
from properties import *

_haveMySQLdb = False
_havezxJDBC = False

try:
    import MySQLdb
    _haveMySQLdb = True
except ImportError:
    log.info(__name__, "MySQLdb is not available...")

    try:
        from com.ziclix.python.sql import zxJDBC
        _havezxJDBC = True
    except ImportError:
        log.info(__name__, "zxJDBC is not available...")

try:
    import sqlite3
except ImportError:
    log.error(__name__, "sqlite3 is not available!")


##############################################################################
class NoConnectionMethodAvailable(Exception):
    def __init__(self, value):
        Exception.__init__(self, value)


def closer(closable):
    if closable:
        closable.close()


def getLastInsertRowIdUsingCursor(con, cursor):
    result = None

    try:
        sql = "SELECT last_insert_rowid()"
        cursor.execute(sql)
        row = cursor.fetchone()
        result = row[0]
    except Exception, ex:
        msg = "Unable to get last insert rowid: " + str(ex)
        log.error(__name__, msg)
        raise ex

    return result


def getLastInsertRowId(con):
    result = None
    cursor = None

    try:
        try:
            cursor = con.cursor()
            result = getLastInsertRowIdUsingCursor(con, cursor)
        except Exception, ex:
            msg = "Unable to get last insert rowid: " + str(ex)
            log.error(__name__, msg)
            raise ex
    finally:
        closer(cursor)


def getDBServerVersionUsingCursor(con, cursor):
    result = None

    try:
        if isinstance(con, sqlite3.Connection):
            sql = 'SELECT sqlite_version()'
        else:
            sql = 'SELECT version()'
        cursor.execute(sql)
        row = cursor.fetchone()
        result = row[0]
    except Exception, ex:
        msg = "Unable to get DB Server version: " + str(ex)
        log.error(__name__, msg)
        raise ex

    return result


def getDBServerVersion(con):
    result = None
    cursor = None
    try:
        try:
            cursor = con.cursor()
            result = getDBServerVersionUsingCursor(con, cursor)
        except Exception, ex:
            msg = "Unable to get DB Server version: " + str(ex)
            log.error(__name__, msg)
            raise ex
    finally:
        closer(cursor)

    return result


##############################################################################
def connectToSQLiteDB(database=':memory:', isolation_level=None):
    return sqlite3.connect(database)


def connectToSQLiteWebpix(database='/usr/local/share/webpix/webpix.db',
                          isolation_level=None):
    if sys.platform == 'win32':
        database = 'c:/cygwin/usr/local/share/webpix/webpix.db'

    return connectToSQLiteDB(database, isolation_level)


##############################################################################
def connectToMySQLJDBC(hostname, database, username, password):
    url = 'jdbc:mysql://%s/%s' % (hostname, database)
    drivername = 'com.mysql.jdbc.Driver'

    return zxJDBC.connect(url, username, password, drivername)


def connectToMySQLUnixSocket(hostname, database,
                             username, password, socket):
    con = MySQLdb.connect(host=hostname,
                          db=database,
                          user=username,
                          passwd=password,
                          unix_socket=socket)

    return con


def connectToMySQLDB(hostname, database, username, password):
    if _havezxJDBC:
        return connectToMySQLJDBC(hostname,
                                  database,
                                  username,
                                  password)
    elif _haveMySQLdb:
        if hostname == 'localhost':
            return connectToMySQLUnixSocket(hostname,
                                            database,
                                            username,
                                            password,
                                            "/tmp/mysql.sock")
        else:
            return MySQLdb.connect(host=hostname,
                                   db=database,
                                   user=username,
                                   passwd=password)
    else:
        raise NoConnectionMethodAvailable(
            'No Database connection method found')


##############################################################################
class DBUtil:
    def __init__(self):
        self._propNames = ('DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD')
        self._haveEnvProperties = False
        self._haveConnectionProperties = False
        self.__props = Properties()

    def getConnectionPropertiesFromEnv(self):
        self.__props.setPropertiesFromEnv(self._propNames)
        self._haveEnvProperties = True

    def readProperties(self, filename):
        filehandle = None

        try:
            try:
                filehandle = open(filename)
                self.__props.load(filehandle)
            except Exception, err:
                msg = 'Error reading properties from file [%s] ' % filename
                log.error(self,  msg + repr(err))
        finally:
            closer(filehandle)

    def logImproperUsage(self):
        log.error(
            self.__class__.__name__,
            """********************************************************
               ************** IMPROPER USAGE OF DBUtils.connectToMySQL()
               ************** Either set the environment variables
               ************** DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
               ************** Or call readProperties() method first...
               ********************************************************""")

    def checkProperties(self):
        result = True
        checks = [self.__props.haveProperty("DB_HOST"),
                  self.__props.haveProperty("DB_NAME"),
                  self.__props.haveProperty("DB_USER"),
                  self.__props.haveProperty("DB_PASSWORD")]

        for check in checks:
            if not check:
                result = False
                break

        return result

    def ensureProperties(self):
        if not self._haveEnvProperties:
            self.getConnectionPropertiesFromEnv()

        self._haveConnectionProperties = self.checkProperties()

        if not self._haveConnectionProperties:
            self.logImproperUsage()

    def getConnectionParameters(self, default_host,
                                default_db, default_user, default_passwd):

        if not self._haveConnectionProperties:
            self.getConnectionPropertiesFromEnv()

        msg = 'DB properties:'

        for name in self._propNames:
            p = self.__props.getPropertyOrDefault(name, '')
            msg += ' [%s]' % p

        log.debug(self, msg)

        host = self.__props.getPropertyOrDefault("DB_HOST", default_host)
        database = self.__props.getPropertyOrDefault("DB_NAME", default_db)
        user = self.__props.getPropertyOrDefault("DB_USER", default_user)
        passwd = self.__props.getPropertyOrDefault("DB_PASSWORD",
                                                   default_passwd)

        return (host, database, user, passwd)

##############################################################################
    def connectToSQLiteDatabase(database=':memory:', isolation_level=None):
        log.info(__name__,
                 'Attempting connect to SQLite [%s:%s]' %
                 (database, repr(isolation_level)))

        return connectToSQLiteDB(database, isolation_level)

##############################################################################
    def connectToMySQL(self):
        self.ensureProperties()

        (host, database, user, passwd) = self.getConnectionParameters(
            None, None, None, None)

        return self.connectToMySQLDatabase(host, database, user, passwd)

    def connectToMySQLDatabase(self, hostname, database, username, password):
        log.info(self,
                 'Attempting connect to MySQL [%s:%s:%s:%s]' %
                 (hostname, database, username, password))

        try:
            return connectToMySQLDB(hostname, database, username, password)
        except NoConnectionMethodAvailable:
            log.error(self, 'Unknown Database connection method')
            raise

    def connectToMySQLWebpix(self):
        (host, database, user, passwd) = self.getConnectionParameters(
            'localhost', 'webpix', 'webpixuser', 'webpixuser')

        return self.connectToMySQLDatabase(host, database, user, passwd)

    def connectToMySQLSesco(self):
        (host, database, user, passwd) = self.getConnectionParameters(
            'aragorn', 'sescodev', 'sescouser', 'sescouser')

        return self.connectToMySQLDatabase(host, database, user, passwd)


##############################################################################
class RowProcessor:
    def toObject(row):
        pass

    def toObjectList(rows):
        pass

    def toDict(row):
        pass


###############################################################################
def testConnectToMySQLDatabase():
    con = None

    try:
        try:
            util = DBUtil()

            con = util.connectToMySQLDatabase("localhost",
                                              "webpix",
                                              "webpixuser",
                                              "webpixuser")
            version = getDBServerVersion(con)
            print 'Server Version: ', version
        except Exception, err:
            print 'Error: ', err
    finally:
        closer(con)


def testConnectToMySQLWebpix():
    con = None

#    try:
#        try:
    util = DBUtil()

    con = util.connectToMySQLWebpix()
    version = getDBServerVersion(con)
    print 'Server Version: ', version
#         except Exception, err:
#            print 'Error: ', err
#            raise err
#    finally:
    closer(con)


def testConnectToMySQLSesco():
    con = None

    try:
        try:
            util = DBUtil()

            con = util.connectToMySQLSesco()
            version = getDBServerVersion(con)
            print 'Server Version: ', version
        except Exception, err:
            print 'Error: ', err
    finally:
        closer(con)


def testConnectToMySQL():
    con = None

    try:
        try:
            util = DBUtil()
            path = fileutil.findFileInPYTHONPATH("webpix.properties")
            util.readProperties(path)

            con = util.connectToMySQL()
            version = getDBServerVersion(con)
            print 'Server Version: %s', version
        except Exception, err:
            print 'Error: ', err
    finally:
        closer(con)


def testConnectToSQLiteWebpix():
    con = None

    try:
        try:
            con = connectToSQLiteWebpix()
            version = getDBServerVersion(con)
            print 'Server Version: %s' % version
        except Exception, err:
            print 'Error: ', err
    finally:
        closer(con)


if __name__ == '__main__':
    if _haveMySQLdb or _havezxJDBC:
        # testConnectToMySQLDatabase()
        testConnectToMySQLWebpix()
        testConnectToMySQLSesco()
        testConnectToMySQL()

    testConnectToSQLiteWebpix()

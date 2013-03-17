import leebrinton.util.log as log
import time

SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
SECONDS_PER_HOUR = (MINUTES_PER_HOUR * SECONDS_PER_MINUTE)
SECONDS_PER_DAY = (HOURS_PER_DAY * SECONDS_PER_HOUR)

def minutesFromSeconds( seconds ):
    return (seconds / SECONDS_PER_MINUTE)

def hoursFromSeconds( seconds ):
    return (seconds / SECONDS_PER_HOUR)

def daysFromSeconds( seconds ):
    return (seconds / SECONDS_PER_DAY)

class Duration:
    
    def __init__( self ):
        self.days = 0
        self.hours = 0
        self.minutes = 0
        self.seconds = 0

def computeDuration( starttime ):
    now = time.time();
    diff = int(now - starttime)

    result = Duration()
    result.days = int(daysFromSeconds( diff ))
    diff -= int((result.days * SECONDS_PER_DAY))

    result.hours = int(hoursFromSeconds( diff ))
    diff -= int((result.hours * SECONDS_PER_HOUR))

    result.minutes = int(minutesFromSeconds( diff ))
    diff -= int((result.minutes * SECONDS_PER_MINUTE))

    result.seconds = int(diff);
    return result

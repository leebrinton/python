import os

def getCurrentUser():
    '''Get a user name from the environment (USER, or USERNAME or LOGNAME). 
    
    Returns: string
    '''

    try:
        user = os.environ['USER']
    except KeyError:
        try:
            user = os.environ['USERNAME']
        except KeyError:
            user = os.environ['LOGNAME']

    return user

if __name__ == '__main__':
    print( 'User: %s' % getCurrentUser() )

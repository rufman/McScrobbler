'''
Created on Jan 28, 2012

@author: stephane
'''
import pylast
import time

class Scrobbler(object):
    '''
    classdocs
    '''
    API_KEY = ''
    API_SECRET = ''
    NETWORK = ''

    def __init__(self, api_key, api_secret):
        '''
        Constructor
        '''
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        
    def connect(self, username, password):
        '''
        Connect to last.fm with given username and password.
        
        Returns a LASTFMNetwork object
        '''
        network = pylast.LastFMNetwork(api_key = self.API_KEY, 
                                       api_secret = self.API_SECRET, 
                                       username = username, 
                                       password_hash = pylast.md5(password))
        
        self.NETWORK = network
    
    def update_now_playing(self, track, artist, album):
        self.NETWORK.update_now_playing(artist, track, album)
        
    def scrobbler(self, track, artist, timestamp, album):
        self.NETWORK.scrobble(artist, track, timestamp, album)
    
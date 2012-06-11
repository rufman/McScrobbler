'''
Created on Jan 28, 2012

@author: stephane
'''
from pyechonest import config, song, util
try:
    import json
except ImportError:
    import simplejson as json
    
from pyMcScrobbler.config import ECHOPRINT_API
import sys
sys.path.insert(0, ECHOPRINT_API)
import fp
    
class Echoprint(object):
    '''
    classdocs
    '''
    ECHOPRINT_SERVER = '' # local echoprint server with additional fingerprints


    def __init__(self, api_key, codgen_bin):
        '''
        Constructor
        '''
        config.ECHO_NEST_API_KEY = api_key
        config.CODEGEN_BINARY_OVERRIDE = codgen_bin
        
    def find_song_metadata(self, filename):
        '''
        Find the songs metadata.
        First query the echonest server and then
        a local echoprint server is available
        '''
        json_res = util.codegen(filename, 5, 30)
        fingerprint = json_res[0]['code']
        
        try:
            result = self._query_echonest(fingerprint)
        except:
            pass
        if result == []:
            result = self._query_echoprint(fingerprint)
        
        return result
            
    ## helper functions
    
    def _query_echonest(self, fingerprint):
        result = song.identify(code=fingerprint)
        
        return result
    
    def _query_echoprint(self, fingerprint):
        decoded = fp.decode_code_string(fingerprint)
        result = fp.best_match_for_query(decoded)
        if result.TRID:
            metadata = result.metadata
        else:
            raise Exception("No match. This track may not be in the database yet.")
            
        return metadata
    
    def _query_server_for_songdata(self, server):
        pass
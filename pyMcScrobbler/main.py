'''
Created on Jan 25, 2012

@author: stephane
'''
from pyMcScrobbler.main.record import Record
from pyMcScrobbler.main.echoprint import Echoprint
from pyMcScrobbler.main.scrobbler import Scrobbler
from pyMcScrobbler import config
import Queue, time, wave, signal, sys

CURRENT_TRACK = ''
SAMPLE_FILENAME = 'mic_data.wav'    

def main():
    metadata = fingerprinting_sys.find_song_metadata(SAMPLE_FILENAME)
    global CURRENT_TRACK
    CURRENT_TRACK = metadata
    
    scrobbler_sys.update_now_playing(metadata['track'], metadata['artist'], metadata['release'])
    print "Now playing %s by %s %s seconds long" % (metadata['track'], metadata['artist'], metadata['length'])
    time.sleep((metadata['length']-30)/2)
    
    scrobbler_sys.scrobbler(metadata['track'], metadata['artist'], int(time.time()), metadata['release'])
    print "Scrobbled %s by %s" % (metadata['track'], metadata['artist'])
    time.sleep((metadata['length']-30)/2)
    """global CURRENT_TRACK
    if CURRENT_TRACK != metadata:
        if CURRENT_TRACK != '':
            scrobbler_sys.scrobbler(CURRENT_TRACK['track'], CURRENT_TRACK['artist'], time.time(), CURRENT_TRACK['release'])
            print "Scrobbled %s by %s" % (CURRENT_TRACK['track'], CURRENT_TRACK['artist'])
        scrobbler_sys.update_now_playing(metadata['track'], metadata['artist'], metadata['release'])
        print "Now playing %s by %s" % (metadata['track'], metadata['artist'])
    
    CURRENT_TRACK = metadata"""
    
if __name__ == '__main__':
    mic_recorder = Record(SAMPLE_FILENAME)
    fingerprinting_sys = Echoprint(config.ECHO_NEST_API_KEY, config.CODEGEN_BINARY_OVERRIDE)
    scrobbler_sys = Scrobbler(config.LASTFM_API_KEY, config.LASTFM_SECRET_KEY)
    scrobbler_sys.connect(config.LASTFM_USERNAME, config.LASTFM_PASSWORD)
    while True:
        try:
            mic_recorder.record_mic()
            main()
        except KeyboardInterrupt:
            scrobbler_sys.scrobbler(CURRENT_TRACK['track'], CURRENT_TRACK['artist'], time.time(), CURRENT_TRACK['release'])
            print "Scrobbled %s by %s" % (CURRENT_TRACK['track'], CURRENT_TRACK['artist'])
            print "Finisched Scrobblering"
            sys.exit(0)
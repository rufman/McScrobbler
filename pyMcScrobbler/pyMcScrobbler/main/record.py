'''
Created on Jan 25, 2012

@author: stephane
'''
import alsaaudio, wave

class Record(object):
    '''
    classdocs
    '''
    SAMPLE_FILENAME = ''

    def __init__(self, filename):
        '''
        Constructor
        '''
        self.SAMPLE_FILENAME = filename    
        
    def record_mic(self):
        mic = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NORMAL)
        # Open the device in nonblocking capture mode. The last argument could
        # just as well have been zero for blocking mode. Then we could have
        # left out the sleep call in the bottom of the loop
        
        
        # Set attributes: Mono, 8000 Hz, 16 bit little endian samples
        mic.setchannels(1)
        mic.setrate(11025)
        mic.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        
        # The period size controls the internal number of frames per period.
        # The significance of this parameter is documented in the ALSA api.
        # For our purposes, it is sufficient to know that reads from the device
        # will return this many frames. Each frame being 2 bytes long.
        # This means that the reads below will return either 320 bytes of data
        # or 0 bytes of data. The latter is possible because we are in nonblocking
        # mode.
        mic.setperiodsize(160)
        frames_for_30_sec = (11025/160)*30
        pcm_data = wave.open(self.SAMPLE_FILENAME, 'w')
        pcm_data.setparams((1, 2, 11025, 0, 'NONE', 'not compressed'))
        for i in range(frames_for_30_sec):
            # Read data from device
            l,data = mic.read()
            pcm_data.writeframes(data)
            
        pcm_data.close()
        print "Got 30 Second sample"
        
    """def record_mic_win(self):
        
        import pyaudio
        import sys

        chunk = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 11025
        RECORD_SECONDS = 35
        WAVE_OUTPUT_FILENAME = "mic_data.wav"
        
        p = pyaudio.PyAudio()
        
        stream = p.open(format = FORMAT,
                        channels = CHANNELS,
                        rate = RATE,
                        input = True,
                        frames_per_buffer = chunk)
        
        print "* recording"
        all = []
        for i in range(0, RATE / chunk * RECORD_SECONDS):
            data = stream.read(chunk)
            all.append(data)
        print "* done recording"
        
        stream.close()
        p.terminate()
        
        # write data to WAVE file
        data = ''.join(all)
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()"""
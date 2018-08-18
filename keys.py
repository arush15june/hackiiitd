import os
import random
import time
import threading
import pygame

MUSIC_PATH = 'music'

class KeyPlayer():
    KEYS = {
        'A': [
            # { 
            #     'file': 'A_1.mp3',
            #     'start': 2
            # },
            # { 
            #     'file': 'A_2.mp3',
            #     'start': 4
            # }
            { 
                'file': 'A_3.mp3',
                'start': 10
            }
        ],
        'B': [
            # { 
            #     'file': 'B_1.mp3',
            #     'start': 61
            # },
            # { 
            #     'file': 'B_2.mp3',
            #     'start': 214
            # }
            { 
                'file': 'B_3.mp3',
                'start': 15
            }
        ],
        'C': [
            # { 
            #     'file': 'C_1.mp3',
            #     'start': 3
            # }
            { 
                'file': 'C_2.mp3',
                'start': 53
            }
        ],
        'D': [
            # { 
            #     'file': 'D_1.mp3',
            #     'start': 16
            # },
            # { 
            #     'file': 'D_2.mp3',
            #     'start': 27
            # }
            { 
                'file': 'D_3.mp3',
                'start': 10
            }
        ],
        'E': [
            # { 
            #     'file': 'E_1.mp3',
            #     'start': 67
            # },
            # { 
            #     'file': 'E_2.mp3',
            #     'start': 5
            # }
            { 
                'file': 'E_3.mp3',
                'start': 42
            }
        ],
        'F': [
            # { 
            #     'file': 'F_1.mp3',
            #     'start': 0.0
            # }
            { 
                'file': 'F_2.mp3',
                'start': 60
            }
        ],
        'G': [
            # { 
            #     'file': 'G_1.mp3',
            #     'start': 0.0
            # },
            # { 
            #     'file': 'G_2.mp3',
            #     'start': 8
            # },
            # { 
            #     'file': 'G_3.mp3',
            #     'start': 27
            # }
            { 
                'file': 'G_4.mp3',
                'start': 10
            }
        ]
    }

    @staticmethod
    def music_path(filename):
        return os.path.join(MUSIC_PATH, filename)

    def __init__(self):
        self.KEY = ''
        pygame.mixer.init()
        
    def _loadAudioFile(self, file):
        pygame.mixer.music.load(file)

    def _playAudioFile(self, *args, **kwargs):
        pygame.mixer.music.play(*args, **kwargs)
        
    def playAudioFile(self, file, *args, **kwargs):
        self._loadAudioFile(file)
        self._playAudioFile(*args, **kwargs)
        
    def _stopAudioFile(self):
        pygame.mixer.music.stop()

    def stopAudio(self):
        self._stopAudioFile()    
        
    def setKey(self, key):
        self.KEY = key;

    def _getKeyAudio(self):
        choice = random.choice(self.KEYS[self.KEY])
        return self.music_path(choice['file']), choice['start']

    def playAudio(self):
        audio_filename, start_time = self._getKeyAudio()
        self.playAudioFile(audio_filename, start=start_time)

    def playForTime(self, seconds):
        start = time.time()
        
        self.playAudio()
        while time.time() - start < seconds:
            continue
        self.stopAudio()

class KeyPlayerThread(threading.Thread):
    
    def __init__(self, *args, **kwargs):
        super(KeyPlayerThread, self).__init__(*args, **kwargs)
        self.KEYPLAYER = KeyPlayer()
        self.seconds = 5
        self.is_playing = False

    def setKey(self, key):
        self.KEYPLAYER.setKey(key)

    def setSeconds(self, seconds):
        self.seconds = seconds

    def _playAudio(self):
        self.KsEYPLAYER.playAudio()

    def stopAudio(self):
        self.KEYPLAYER.stopAudio()

    def playForTime(self, seconds):
        self.KEYPLAYER.playForTime(seconds)
        
    def run(self):
        self.playForTime(self.seconds)
        
        

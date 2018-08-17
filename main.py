import time
import threading
import numpy as np
import pyaudio

class NoteExtracter():
    NOTE_MIN = 60       # C4
    NOTE_MAX = 69       # A4
    FSAMP = 22050       # Sampling frequency in Hz
    FRAME_SIZE = 2048   # How many samples per frame?
    FRAMES_PER_FFT = 32 # FFT takes average across how many frames?

    # Derived quantities from constants above. Note that as
    # SAMPLES_PER_FFT goes up, the frequency step size decreases (so
    # resolution increases); however, it will incur more delay to process
    # new sounds.

    SAMPLES_PER_FFT = FRAME_SIZE*FRAMES_PER_FFT
    FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT
    NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()
    window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))
    buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
    num_frames = 0
    
    def __init__(self):
        self.imin = max(0, int(np.floor(self.note_to_fftbin(self.NOTE_MIN-1))))
        self.imax = min(self.SAMPLES_PER_FFT, int(np.ceil(self.note_to_fftbin(self.NOTE_MAX+1))))
        self.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                channels=1,
                                rate=self.FSAMP,
                                input=True,
                                frames_per_buffer=self.FRAME_SIZE)
        self._CURRENT_NOTE = ''

    def _start_stream(self):
        self.stream.start_stream()

    def _set_note(self, note):
        self._CURRENT_NOTE = note

    def run_extracter(self):
        self._start_stream()
        
        while self.stream.is_active():
            # Shift the buffer down and new data in
            self.buf[:-self.FRAME_SIZE] = self.buf[self.FRAME_SIZE:]
            self.buf[-self.FRAME_SIZE:] = np.fromstring(self.stream.read(self.FRAME_SIZE), np.int16)

            # Run the FFT on the windowed buffer
            fft = np.fft.rfft(self.buf * self.window)

            # Get frequency of maximum response in range
            freq = (np.abs(fft[self.imin:self.imax]).argmax() + self.imin) * self.FREQ_STEP

            # Get note number and nearest note
            n = self.freq_to_number(freq)
            n0 = int(round(n))

            # Console output once we have a full buffer
            self.num_frames += 1

            if self.num_frames >= self.FRAMES_PER_FFT:
                note = self.note_name(n0)
                self._set_note(note)
                # print('freq: {:7.2f} Hz     note: {:>3s} {:+.2f}'.format(
                #         freq, self.note_name(n0), n-n0))
    
    @property
    def current_note(self):
        return self._CURRENT_NOTE
        
    @staticmethod
    def freq_to_number(f):
        return 69 + 12*np.log2(f/440.0)

    @staticmethod
    def number_to_freq(n):
        return 440 * 2.0**((n-69)/12.0)

    def note_name(self, n):
        return self.NOTE_NAMES[n % 12] + str(n/12 - 1)

    def note_to_fftbin(self, n):
        return self.number_to_freq(n)/self.FREQ_STEP

class NoteExtracterThread(threading.Thread):
    
    def __init__(self, *args, **kwargs):
        super(NoteExtracterThread, self).__init__(*args, **kwargs)
        self._notes = NoteExtracter() 
        
    @property
    def note(self):
        return self._notes.current_note

    @property
    def key(self):
        return list(self.note)[0] if self.note is not '' else ''

    def run(self):
        self._notes.run_extracter()
        
if __name__ == '__main__':
    notes = NoteExtracterThread()
    notes.start()

    while 1:
        print(notes.note, notes.key)
        time.sleep(0.5)
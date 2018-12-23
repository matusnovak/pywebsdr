import numpy
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
from flask_socketio import SocketIO, emit

def gcd(a, b):
    while b:
        a, b = b, a%b
    return a
    
def compute_dec_interp(a,b):
    a = int(a)
    b = int(b)
    g = gcd(a,b)
    dec = a/g
    interp = b/g
    return dec,interp

def limit_offset_range(a,b):
    f = abs(a)
    sign = (-1,1)[a >= 0]
    f = (f,b)[f > b]
    return f * sign

class WideResampler():
    def __init__(self, in_samplerate, out_samplerate):
        dec_wid, interp_wid = compute_dec_interp(in_samplerate, out_samplerate)
        self.block = filter.rational_resampler_ccc(
            decimation=dec_wid,
            interpolation=interp_wid,
            taps=None,
            fractional_bw=None,
        )

class WideFir():
    def __init__(self, samplerate):
        fir_taps = firdes.complex_band_pass(1, samplerate, -samplerate/2, samplerate/2,samplerate/2)
        self.block = filter.freq_xlating_fir_filter_ccc(1, (fir_taps), 0.0, samplerate)

class WideLowPass():
    def __init__(self, samplerate):
        wfm_bw = 40e3
        wfm_taps = firdes.low_pass(1, samplerate, wfm_bw, 4e3, firdes.WIN_HAMMING, 6.76)
        self.block = filter.fir_filter_ccf(1, wfm_taps)

class Squeech():
    def __init__(self):
        level = -130.0
        self.block = analog.pwr_squelch_cc(level, 1e-4, 0, True)

class AutomaticGain():
    def __init__(self):
        self.block = analog.agc2_cc(1e-1, 1e-2, 1.0, 1.0)
        self.block.set_max_gain(1)

class WideFM():
    def __init__(self, samplerate, audiorate):
        self.audio_dec_wid = samplerate / audiorate
        self.block = analog.wfm_rcv(
            quad_rate=samplerate,
            audio_decimation=self.audio_dec_wid,
        )

class Volume():
    def __init__(self):
        volume = 0.5
        self.block = blocks.multiply_const_vff((volume, ))

class AudioSink():
    def __init__(self, audiorate):
        self.block = audio.sink(audiorate, "", True)

class AudioSocket(gr.sync_block):
    def __init__(self, audiorate, worker):
        gr.sync_block.__init__(self, name="AudioSocket", in_sig=[numpy.float32], out_sig=None)
        self.audiorate = audiorate
        self.block = self
        self.worker = worker

    def work(self, input_items, output_items):
        self.worker.push(input_items[0].copy())
        return len(input_items[0])
        #total = 0
        #for i in range(len(input_items)):
        #    new_file.write(input_items[i].tobytes())
        #    #print 'input: ' + str(input_items[i].__class__)
        #    self.worker.push(input_items[i])
        #    #self.socket.emit(u'stream', input_items[i].tobytes())
        #    total += len(input_items[i])
        #self.worker.push(input_items[0])
        #return total

from gnuradio import gr
from pywebsdr.blocks import AudioSink, WideResampler, WideFir, WideLowPass, Squeech, AutomaticGain, WideFM, Volume, AudioSocket

class Radio(gr.top_block):
    def __init__(self, device, audiorate, worker):
        gr.top_block.__init__(self, type(self).__name__)
        self.device = device
        self.worker = worker
        self.audiorate = audiorate
        #self.output = AudioSink(audiorate)
        self.output = AudioSocket(audiorate, worker)
        self.set_mode('WFM')

    def set_mode(self, value):
        self.mode = value
        blocks = []
        if value == 'WFM':
            wfm_samplerate = int(240e3)
            self.resampler_block = WideResampler(self.device.samplerate, wfm_samplerate)
            self.fir_block = WideFir(wfm_samplerate)
            self.low_pass_block = WideLowPass(wfm_samplerate)
            self.squeech_block = Squeech()
            self.automatic_gain = AutomaticGain()
            self.fm_block = WideFM(wfm_samplerate, self.audiorate)
            self.volume_block = Volume()

            blocks = [
                self.device,
                self.resampler_block,
                self.fir_block,
                self.low_pass_block,
                self.squeech_block,
                self.automatic_gain,
                self.fm_block,
                self.volume_block,
                self.output
            ]

        if len(blocks) == 0:
            raise ValueError('Invalid mode name')

        for i in range(len(blocks) - 1):
            a = blocks[i]
            b = blocks[i + 1]
            self.connect((a.block, 0), (b.block, 0))

        #self.connect((self.device.source, 0), (self.rational_resampler_wid, 0))
        #self.connect((self.rational_resampler_wid, 0), (self.freq_xlating_fir_filter, 0))
        #self.connect((self.freq_xlating_fir_filter, 0), (self.low_pass_filter_wfm, 0))
        #self.connect((self.low_pass_filter_wfm, 0), (self.analog_pwr_squelch, 0))
        #self.connect((self.analog_pwr_squelch, 0), (self.analog_agc_cc, 0))
        #self.connect((self.analog_agc_cc, 0), (self.analog_wfm_rcv, 0))
        #self.connect((self.analog_wfm_rcv, 0), (self.blocks_multiply_const_volume, 0))
        #self.connect((self.blocks_multiply_const_volume, 0), (self.audio_sink, 0))

        #print('get_freq_range', self.device.source.get_freq_range().values)
        #print('get_center_freq', self.device.source.get_center_freq())
        #print('get_freq_corr', self.device.source.get_freq_corr())
        #print('get_gain_mode', self.device.source.get_gain_mode())
        #print('get_bandwidth', self.device.source.get_bandwidth())
        #print('get_sample_rate', self.device.source.get_sample_rate())
        #print('get_gain IF', self.device.source.get_gain('IF'))
        #print('get_gain MIX', self.device.source.get_gain('MIX'))
        #print('get_gain LNA', self.device.source.get_gain('LNA'))

    def start_loop(self):
        print 'Starting loop!'
        self.start()

    def stop_loop(self):
        print 'Stopping loop!'
        self.stop()
        self.wait()
        self.worker.stop()


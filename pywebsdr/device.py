import osmosdr

SOURCE = osmosdr.source('airspy')

DEVICE_DRIVERS = {
    'Airspy': 'airspy',
    'AirSpy':'airspy',
    'BladeRF':'bladerf',
    'FCD':'fcd',
    'HackRF':'hackrf',
    'LimeSDR':'soapy=0,driver=lime',
    'Miri':'miri',
    'OsmoSDR':'osmosdr',
    'PlutoSDR':'ip:pluto.local',      
    'RedPitaya':'redpitaya=127.0.0.1:1234',
    'RFSPACE':'sdr-iq',
    'RTL-SDR':'rtl',
    'RTL-SDR TCP':'rtl_tcp=127.0.0.1:1234',
    'SDRplay':'soapy=0,driver=sdrplay',
    'USRP':'uhd',
}

class Device(object):
    def __init__(self, name):
        if name not in DEVICE_DRIVERS:
            raise ValueError('Invalid device name: ' + name)
        self.driver_name = DEVICE_DRIVERS[name]
        self.source = SOURCE
        self.source.set_bandwidth(1)

    @property
    def gain(self):
        ret = {}
        for name in self.source.get_gain_names():
            ret[name] = self.source.get_gain(name)
        return ret

    @gain.setter
    def gain(self, gain):
        for name in self.source.get_gain_names():
            self.source.set_gain(gain[name], name, 0)

    @property
    def gain_mode(self):
        return self.source.get_gain_mode()

    @gain_mode.setter
    def gain_mode(self, value):
        return self.source.set_gain_mode(value)

    @property
    def gain_ranges(self):
        ret = {}
        for name in self.source.get_gain_names():
            values = self.source.get_gain_range(name).values()
            ret[name] = {
                'min': values[0],
                'max': values[len(values)-1],
            }
        return ret

    @property
    def antenna(self):
        return self.source.get_antenna()

    @antenna.setter
    def antenna(self, value):
        self.source.set_antenna(value)

    @property
    def antennas(self):
        return self.source.get_antennas()

    @property
    def bandwidth(self):
        return self.source.get_bandwidth()

    @bandwidth.setter
    def bandwidth(self, value):
        self.source.set_bandwidth(value)

    @property
    def bandwidth_range(self):
        return self.source.get_bandwidth_range().values()

    @property
    def samplerate(self):
        return self.source.get_sample_rate()

    @samplerate.setter
    def samplerate(self, value):
        self.source.set_sample_rate(value)

    @property
    def samplerate_range(self):
        return self.source.get_sample_rates().values()

    @property
    def frequency(self):
        return self.source.get_center_freq()

    @frequency.setter
    def frequency(self, value):
        self.source.set_center_freq(value)

    @property
    def frequency_range(self):
        freq = self.source.get_freq_range().values()
        return {'min': freq[0], 'max': freq[1]}
    
    @property
    def corr(self):
        self.source.get_freq_corr()

    @corr.setter
    def corr(self, value):
        self.source.set_freq_corr(value)

    @property
    def block(self):
        return self.source

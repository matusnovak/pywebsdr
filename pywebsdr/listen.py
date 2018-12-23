from flask import request, jsonify
import traceback
import time
from pywebsdr import app, socketio
from pywebsdr.radio import Radio
from pywebsdr.device import Device, DEVICE_DRIVERS
from pywebsdr.responses import badRequest, ok
from pywebsdr.worker import Worker

radio = None
device = None
worker = None

@app.route('/rest/device/start', methods=['POST'])
def start_listen():
    global radio, device
    body = request.json
    if 'device' not in body:
        return badRequest('device name is required')

    if radio is not None:
        radio.stop_loop()
    else:
        worker = Worker(socketio)

        device = Device(body['device'])
        device.frequency = 92700000.0
        device.samplerate = 10000000.0
        device.bandwidth = 10000000.0
        device.corridor = 0.0
        device.gain = {
            'IF': 15,
            'MIX': 1,
            'LNA': 15
        }

        radio = Radio(device, 48000, worker)
        radio.start_loop()

        socketio.start_background_task(target=worker.do_work)
    info = {
        'gain': radio.device.gain,
        'gain_ranges': radio.device.gain_ranges,
        'antenna': radio.device.antenna,
        'antennas': radio.device.antennas,
        'bandwidth': radio.device.bandwidth,
        'bandwidth_range': radio.device.bandwidth_range,
        'samplerate': radio.device.samplerate,
        'samplerate_range': radio.device.samplerate_range,
        'frequency': radio.device.frequency,
        'frequency_range': radio.device.frequency_range,
        'corridor': radio.device.corridor
    }
    
    return ok(info)

@app.route('/rest/device/stop', methods=['POST'])
def stop_listen():
    global radio, device
    if radio is not None:
        radio.stop_loop()
        radio = None
        device = None
    return ok({'message': 'Device stopped'})

@app.route('/rest/device/list', methods=['GET'])
def rest_get_devices():
    return ok(DEVICE_DRIVERS.keys())

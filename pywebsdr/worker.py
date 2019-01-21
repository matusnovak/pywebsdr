import eventlet
import numpy

class Worker(object):
    switch = False
    packets = []

    def __init__(self, socketio):
        self.socketio = socketio
        self.switch = True

    def push(self, pcm):
        self.packets.append(pcm)

    def do_work(self):
        while self.switch:
            if len(self.packets) > 0:
                conn = numpy.concatenate(self.packets)
                self.packets = []
                #print 'conn: ' + str(len(conn))
                self.socketio.emit(u'stream', {'pcm': conn.tobytes()}, namespace='/listen')
            eventlet.sleep(1)

    def stop(self):
        print 'Stopping worker'
        self.switch = False

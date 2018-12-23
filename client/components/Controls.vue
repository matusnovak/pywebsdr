<template>
  <b-card header="Controls" header-tag="header">
    <label>Please select a device</label>
    <b-form-select v-model="device" :options="devices" class="w-100 mb-3" />
    <b-button-group class="w-100">
      <b-button variant="primary" @click="onStart" :disabled="connected || busy">Start</b-button>
      <b-button variant="primary" @click="onStop" :disabled="!connected || busy">Stop</b-button>
    </b-button-group>
  </b-card>
</template>

<script>
import io from 'socket.io-client'
//import SoundBuffer from './SoundBuffer'
var startTime = 0

export default {
  data() {
    return {
      devices: [],
      device: '',
      busy: false,
      connected: false,
      socket: null,
      test: false,
      audioCtx: null,
      soundBuffer: null,
      pcms: []
    }
  },
  methods: {
    fetch() {
      this.busy = true
      this.$http.get('/rest/device/list').then(response => {
        this.devices = response.data
        this.device = this.devices[0]
      }).catch(() => {
        this.$emit('error', 'Failed to fetch devices')
      }).finally(() => {
        this.busy = false
      })
    },
    onStart() {
      this.busy = true
      this.$http.post('/rest/device/start', {device: this.device}).then(response => {
        this.socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + '/listen')
        this.socket.on('connect', () => {
          this.busy = false
          this.connected = true
          this.$emit('start', this.socket, this.device, response.data)
          this.audioCtx = new AudioContext();
          //this.soundBuffer = new SoundBuffer(this.audioCtx, 48000)
          startTime = 0
        })
        this.socket.on('disconnect', () => {
          this.socket = null
          this.connected = false
          while (this.pcms.length > 0){
            this.pcms.shift()
          }
          this.$emit('stop')
        })
        this.socket.on('stream', (data) => {
          const pcm = new Float32Array(data.pcm)
          this.pcms.push(pcm)

          if (this.pcms.length >= 2) {
            const src = this.pcms.shift()
          //console.log('received stream data:', pcm)

          //if (this.pcms.length > 10) {
            //console.log('running')

            //var total = 0
            //this.pcms.map(pcm => total += pcm.length)
            //console.log('total:', total)
            var audioBuffer = this.audioCtx.createBuffer(1, src.length, 48000)
            var nowBuffering = audioBuffer.getChannelData(0, 32, 48000)
            var d = 0
            //this.pcms.map(pcm => {
              for (var i = 0; i < src.length; i++) {
                nowBuffering[d++] = src[i]
              }
            //})

            //console.log('copied', d, 'samples')

            var source = this.audioCtx.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(this.audioCtx.destination);
            source.start(startTime)
            startTime += audioBuffer.duration
          }
          /*} else {
            this.pcms.push(pcm)
          }*/

          //this.soundBuffer.addChunk(pcm)
          
          /*var audioBuffer = this.audioCtx.createBuffer(1, pcm.byteLength / 4, 48000)
          var nowBuffering = audioBuffer.getChannelData(0, 32, 48000)
          for (var i = 0; i < pcm.length; i++) nowBuffering[i] = pcm[i]

          var source = this.audioCtx.createBufferSource()
          source.buffer = audioBuffer
          source.start(startTime)
          source.connect(this.audioCtx.destination)

          startTime += audioBuffer.duration*/

          /*if (!this.test) {
            this.test = true
            
            var audioCtx = new AudioContext();
            var myAudioBuffer = audioCtx.createBuffer(1, pcm.byteLength / 4, 48000);
            var nowBuffering = myAudioBuffer.getChannelData(0, 32, 48000);
            for (var i = 0; i < pcm.length; i++) {
                nowBuffering[i] = pcm[i];
            }

            var source = audioCtx.createBufferSource();
            source.buffer = myAudioBuffer;
            source.connect(audioCtx.destination);
            source.start()
          }*/
        })
      }).catch(() => {
        this.$emit('error', 'Failed to start device')
      }).finally(() => {
        this.busy = false
      })
    },
    onStop() {
      this.busy = true
      this.$http.post('/rest/device/stop').then(() => {
        this.socket.disconnect()
      }).catch(() => {
        this.$emit('error', 'Failed to stop device')
      }).finally(() => {
        this.busy = false
      })
    }
  },
  mounted() {
		this.$nextTick(() => {
      this.fetch()
    })
  }
}
</script>

<template>
  <div class="radio">
    <alert v-if="alert" :variant="alertVariant" @dismissed="onAlertDismissed">{{alert}}</alert>

    <b-row>
      <b-col cols="3">
        <controls class="h-100" 
          @start="onStart" 
          @stop="onStop" 
          @error="onError"
        />
      </b-col>
      <b-col cols="3">
        <frequency class="h-100" 
          @error="onError" 
          :frequency="frequency" 
          :frequencyRange="frequencyRange" 
          :samplerate="samplerate" 
          :samplerateRange="samplerateRange"
          :disabled="!socket"
        />
      </b-col>
      <b-col cols="3">
        <gain class="h-100" 
          @error="onError"
          :gain="gain"
          :gainRange="gainRange"
          :disabled="!socket"
        />
      </b-col>
      <b-col cols="3">
        <modes class="h-100"
          @error="onError"
          :disabled="!socket"
        />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import Alert from './Alert'
import Controls from './Controls'
import Frequency from './Frequency'
import Gain from './Gain'
import Modes from './Modes'

export default {
  data() {
    return {
      namespace: '/listen',
      socket: null,
      alert: '',
      alertVariant: 'danger',
      frequency: 0,
      gain: {
        IF: 0,
        MIX: 0,
        LNA: 0
      },
      samplerate: 0,
      bandwidth: 0,
      frequencyRange: {
        min: 0, max: 0
      },
      samplerateRange: [],
      gainRange: {
        IF: {
          min: 0, max: 0
        },
        MIX: {
          min: 0, max: 0
        },
        LNA: {
          min: 0, max: 0
        }
      },
      bandwidthRange: {
        min: 0, max: 0
      }
    }
  },
  methods: {
    onAlertDismissed() {
      this.alert = ''
    },
    onStart(socket, device, data) {
      this.frequency = data.frequency
      this.gain = data.gain
      this.samplerate = data.samplerate
      this.bandwidth = data.bandwidth
      this.frequencyRange = data.frequency_range
      this.gainRange = data.gain_ranges
      this.samplerateRange = data.samplerate_range
      this.bandwidthRange = data.bandwidth_range
      this.socket = socket
    },
    onError(message) {
      this.alert = message
      this.alertVariant = 'danger'
    },
    onStop() {
      this.socket = null
    }
  },
  mounted() {
		this.$nextTick(() => {
      //this.connect()
    })
  },
  components: {
    Alert,
    Controls,
    Frequency,
    Gain,
    Modes
  }
}
</script>

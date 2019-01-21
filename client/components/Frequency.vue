<template>
  <b-card header="Frequency" header-tag="header">
    <b-form @submit="onSubmit">
      <b-form-group>
        <label>Sample Rate</label>
        <b-form-select v-model="samplerateValue" :options="samplerateRange" size="sm" :disabled="disabled"/>
      </b-form-group>
      <b-form-group>
        <label>Frequency in Mhz</label>
        <b-form-input v-model="freq" type="text" size="sm" :disabled="disabled"></b-form-input>
      </b-form-group>
    </b-form>
  </b-card>
</template>

<script>
export default {
  data() {
    return {
      frequencyValue: 0.0,
      samplerateValue: ''
    }
  },
  props: {
    frequency: {
      required: true
    },
    samplerate: {
      required: true
    },
    frequencyRange: {
      required: true
    },
    samplerateRange: {
      required: true
    },
    disabled: {
      required: false,
      default: false
    }
  },
  methods: {
    onSubmit() {
      if (this.frequencyValue > this.frequencyRange.max / 1000.0) this.freq = this.frequencyRange.max / 1000.0
      if (this.frequencyValue < this.frequencyRange.min / 1000.0) this.freq = this.frequencyRange.min / 1000.0

      this.$http.post('/rest/device/control', {frequency: this.frequencyValue * 1000.0}).catch(err => {
        this.$emit('error', err.message)
      })
    }
  },
  mounted() {
		this.$nextTick(() => {
    })
  },
  watch: {
    frequency() {
      this.frequencyValue = this.frequency / 1000.0
      if (this.frequencyValue < this.frequencyRange.min / 1000.0) this.frequencyValue = this.frequencyRange.min / 1000.0
      if (this.frequencyValue > this.frequencyRange.max / 1000.0) this.frequencyValue = this.frequencyRange.max / 1000.0
    },
    frequencyRange() {
      this.frequencyValue = this.frequency / 1000.0
      if (this.frequencyValue < this.frequencyRange.min / 1000.0) this.frequencyValue = this.frequencyRange.min / 1000.0
      if (this.frequencyValue > this.frequencyRange.max / 1000.0) this.frequencyValue = this.frequencyRange.max / 1000.0
    },
    samplerate() {
      this.samplerateValue = this.samplerate
    }
  },
  computed: {
    freq: {
      get() {
        return this.frequencyValue.toFixed(3)
      },
      set(value) {
        this.frequencyValue = parseFloat(value)
      }
    }
  }
}
</script>

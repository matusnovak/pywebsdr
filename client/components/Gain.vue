<template>
  <b-card header="Gain" header-tag="header">
    <b-form @submit="onSubmit">
      <b-row v-for="item in values" :key="item.name" class="mb-1">
        <b-col cols="3"><label>{{item.name}}:</label></b-col>
        <b-col cols="9"><b-form-input v-model="item.value" size="sm" type="number" @change="onSubmit" :disabled="disabled"></b-form-input></b-col>
      </b-row>
    </b-form>
  </b-card>
</template>

<script>
export default {
  data() {
    return {
      values: Object.keys(this.gainRange).map(key => {
        return {
          name: key,
          min: this.gainRange[key].min,
          value: 0,
          max: this.gainRange[key].max
        }
      })
    }
  },
  props: {
    gain: {
      required: true,
      type: Object
    },
    gainRange: {
      required: true,
      type: Object
    },
    disabled: {
      required: false,
      default: false
    }
  },
  methods: {
    onSubmit() {
      this.values = this.values.map(value => {
        if (value.value < value.min) value.value = value.min
        if (value.value > value.max) value.value = value.max
        return value
      })

      if (this.socket) {
        const gain = {}
        this.values.map(value => {
          gain[value.name] = parseInt(value.value)
        })
        //this.socket.emit('control', {'gain': gain})
      }
    }
  },
  mounted() {
		this.$nextTick(() => {
    })
  },
  watch: {
    gainRange() {
      this.values = this.values.map(value => {
        value.min = this.gainRange[value.name].min
        value.max = this.gainRange[value.name].max
        return value
      })
    },
    gain() {
      this.values = this.values.map(value => {
        value.value = this.gain[value.name]
        return value
      })
    }
  }
}
</script>

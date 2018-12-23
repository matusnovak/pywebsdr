<template>
  <b-card header="Modes" header-tag="header">
    <b-form @submit="onSubmit">
      <b-form-group>
        
      </b-form-group>
    </b-form>
  </b-card>
</template>

<script>
import io from 'socket.io-client'

export default {
  data() {
    return {
      frequency: this.min / 1000.0
    }
  },
  props: {
    disabled: {
      required: false,
      default: false
    }
  },
  methods: {
    onSubmit() {
    }
  },
  mounted() {
		this.$nextTick(() => {
    })
  }
}
</script>

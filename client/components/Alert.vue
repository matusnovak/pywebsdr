<template>
  <b-alert :variant="variant" show dismissible @dismissed="$emit('dismissed')">
    <slot></slot>
  </b-alert>
</template>

<script>
export default {
  props: {
    variant: {
      type: String,
      default: 'danger'
    }
  }
}
</script>

<template>
  <v-btn @click="$emit('click')" outline large :color="color" :disabled="this.$props.disable"><v-icon left>{{ icon }}</v-icon>{{ title }}</v-btn>
</template>

<script>
export default {
  name: 'Standard_Button',

  props: {
    title: String,
    color: String,
    icon: String,
    disable: Boolean
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

<template>
  <v-container class="loading-screen">
    <v-progress-circular
      :size="180"
      :width="5"
      color="white"
      indeterminate
    ></v-progress-circular>
  </v-container>
</template>

<script>
  export default {
    name: 'LoadingScreen'
  }
</script>

<style scoped>
  .loading-screen {
    background-color: grey;
    opacity: 0.8;
    display: flex;
    align-items: center;
    justify-content: center;
    max-width: none;
  }
</style>

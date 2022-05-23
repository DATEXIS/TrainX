<template>
  <v-toolbar flat dark color="primary">
    <v-toolbar-title><router-link :to="{ name: 'landingpage' }" tag="span" :style="{ cursor: 'pointer' }">TrainX <span v-if="session">- {{ session.title }}</span></router-link></v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items v-if="routeIsSamples()">
      <!-- <Counter /> -->
      <v-btn slot="activator" flat @click="reOpenClosedSamples"><v-icon>settings_backup_restore</v-icon></v-btn>
    </v-toolbar-items>
</v-toolbar>
</template>

<script>
import Counter from '@/components/Counter.vue'

export default {
  name: 'Toolbar',

  components: {
    Counter
  },

  methods: {
    routeIsSamples () { return this.$route.name === 'samples' },
    reOpenClosedSamples () { this.$store.commit('samples/reOpenClosedSamples') }
  },

  computed: {
    session () { return this.$store.getters['sessions/session'] }
  }
}
</script>

<style scoped>
</style>

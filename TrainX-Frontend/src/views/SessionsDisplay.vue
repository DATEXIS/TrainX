<template>
  <v-container>
    <v-layout justify-center>
      <v-flex md8>
        <v-list two-line v-for="session in sessions" :key="session.sessionId">
          <v-list-tile @click="getSession(session.sessionId)">
            <v-list-tile-content>
              <v-list-tile-title>{{ session.title }}</v-list-tile-title>
              <v-list-tile-sub-title>{{ session.description }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  export default {
    name: 'SessionsDisplay',

    methods: {
      getSession (sessionId) {
        this.$store.dispatch('sessions/getSession', sessionId)
        this.$router.push({name: 'landingpage'})
      }
    },

    computed: {
      sessions () { return this.$store.getters['sessions/sessions'] }
    }
  }
</script>

<style scoped>
</style>

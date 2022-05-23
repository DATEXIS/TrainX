<template>
  <v-app>
    <LoadingScreen v-if="loading"/>
    <div v-if="!loading">
      <Toolbar/>
      <v-content>
        <router-view :key="$route.fullPath"></router-view>
      </v-content>
    </div>
  </v-app>
</template>

<script>
  import Toolbar from '@/components/Toolbar.vue'
  import LoadingScreen from '@/components/LoadingScreen.vue'

  export default {
    name: 'App',

    components: {
      Toolbar,
      LoadingScreen
    },

    computed: {
      loading () { return this.$store.getters['loading/loading'] }
    }
  }
</script>

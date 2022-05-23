<template>
  <v-container>
    <v-layout justify-center pb-3>
      <v-flex md10>
        <Pagination/>
      </v-flex>
    </v-layout>

    <v-layout justify-center pb-3>
      <v-flex md10>
        <Card
          v-for="sample in samples"
          v-bind:key="sample.uid"
          v-bind:sample="sample">
        </Card>
      </v-flex>
    </v-layout>

    <v-layout justify-center pb-3>
      <v-flex md10>
        <Pagination/>
      </v-flex>
    </v-layout>
    <v-layout justify-center>
      <v-flex md10 class="button-grid">
        <StandardButton class="button-grid__button--stretched" color="primary" title="Upload Samples" icon="vertical_align_top" @click="uploadSamples"/>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import moment from 'moment'
  import Card from '@/components/cards/Card.vue'
  import Pagination from '@/components/Pagination.vue'
  import StandardButton from '@/components/StandardButton.vue'

  export default {
    name: 'CardsDisplay',

    components: {
      StandardButton,
      Card,
      Pagination
    },

    methods: {
      arrayIsEmpty (array) { return array.length === 0 },

      uploadSamples () {
        const start = this.$store.getters['samples/requestSamplesTimestamp']
        const end = moment()
        const duration = end.diff(start, 'milliseconds')

        const payload = { documents: this.samples, session_id: this.sessionId, sample_time: duration }
        this.$store.commit('samples/setRequestSamplesTimestamp', null)
        this.$store.dispatch('samples/postSamples', payload)
        this.$router.push({ name: 'landingpage' })
      }
    },

    computed: {
      samples () { return this.$store.getters['samples/samples'] },
      sessionId () { return this.$store.getters['sessions/sessionId'] },
      offset () { return this.$store.getters['pagination/offset'] },
      amount () { return this.$store.getters['pagination/amount'] }
    },

    watch: {
      offset (value) { this.$store.dispatch('samples/getSamples', { session_id: this.sessionId, offset: this.offset, amount: this.amount }) }
    }
  }
</script>

<style scoped>
  .button-grid {
    display: grid;
  }
  .button-grid__button--stretched  {
    margin-right: 0;
    margin-left: 0;
  }
</style>

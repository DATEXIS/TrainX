<template>
  <div>
    <div class="horizontal-divider my-2"></div>
    <Relation v-for="(relation, index) in this.sample.getRelations()" :key="index" :relation="relation" @addArgument="addArgument" @selectArgument="selectArgument" />
    <v-btn fab small color="primary" v-on:click="addRelation"><v-icon small>add</v-icon></v-btn>
  </div>
</template>

<script>
import Relation from '@/components/cards/Relation.vue'

export default {
  name: 'AddRelations',

  components: { Relation },

  props: { sample: Object },

  computed: {
    samples () { return this.$store.getters['samples/samples'] }
  },

  methods: {
    addRelation () {
      let payload = { event: 'addRelation' }
      this.$emit('addRelation', payload)
    },

    addArgument (payload) {
      this.$emit('addArgument', payload)
    },

    selectArgument (payload) {
      this.$emit('selectArgument', payload)
    }
  }
}
</script>

<style scoped lang="scss">
.horizontal-divider {
   border-top: 1.5px solid rgba(0,0,0,0.25);
   margin-left: -15px;
}
</style>

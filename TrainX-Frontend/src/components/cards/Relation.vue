<template>
  <div>{{ relation.isActive}}
    <v-btn fab small color="primary" outline @click="addArgument"><v-icon small>add</v-icon></v-btn>
    <span
      @mouseover="addActiveToAllArguments"
      @mouseleave="removeActiveFromAllArguments"
    >{{ relation.predicate }}</span>(<span v-for="(argument, index) in relation.relationArguments" :key="index">
        <span
          v-if="argument.type !== 'DELETED'"
          @mouseover="addACTIVE(argument)"
          @mouseleave="removeACTIVE(argument)"
          @click="selectArgument(argument, $event)"
          v-bind:class="{ activeArgument: argument.isActive }"
        >{{ argument.text }}</span><span v-if="index < relation.relationArguments.length-1">, </span></span>)
  </div>
</template>

<script>
export default {
  name: 'Relation',

  props: { relation: Object },

  methods: {
    selectArgument (argument, event) {
      let payload = { event: event, relation: this.relation, argument: argument }
      this.$emit('selectArgument', payload)
    },

    addArgument () {
      let payload = { relation: this.relation }
      this.$emit('addArgument', payload)
    },

    addActiveToAllArguments () {
      for (let argument of this.relation.relationArguments) {
        this.addACTIVE(argument)
      }
    },

    removeActiveFromAllArguments () {
      for (let argument of this.relation.relationArguments) {
        this.removeACTIVE(argument)
      }
    },

    addACTIVE (argument) {
      argument.source += ' ACTIVE'
    },

    removeACTIVE (argument) {
      argument.source = argument.source.replace(' ACTIVE', '')
    }
  }
}
</script>

<style scoped lang="scss">
  .activeArgument {
    color: #2196F3;
    font-weight: bold;
  }
  .active-argument span { // to make the comma black
    color: black;
  }
</style>

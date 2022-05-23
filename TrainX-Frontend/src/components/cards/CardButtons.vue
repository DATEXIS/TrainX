<template>
  <div class="vertical-divider">
    <v-tooltip><v-btn slot="activator" block flat v-on:click='markAsFinished'><v-icon>check</v-icon></v-btn><span>mark as finished</span></v-tooltip>
    <v-tooltip><v-btn slot="activator" block flat v-on:click='removeAnnotationsOfSample'><v-icon>close</v-icon></v-btn><span>remove all annotations</span></v-tooltip>
  </div>
</template>

<script>
export default {
  name: 'CardButtons',

  props: {
    sample: Object
  },

  methods: {
    markAsFinished () {
      this.sample.annotations.forEach(annotation => annotation.confidence = 1.0)
      this.sample.finished = true
    },

    removeAnnotationsOfSample () {
      for (let annotation of this.sample.annotations) this.markAnnotationAsDeleted(annotation)
    },

    markAnnotationAsDeleted (annotation) {
      annotation.type = 'DELETED'
      annotation.source = 'USER'
    }
  }
}
</script>

<style scoped lang="scss">
.vertical-divider {
   border-left: 1.5px solid rgba(0,0,0,0.25);
}
</style>

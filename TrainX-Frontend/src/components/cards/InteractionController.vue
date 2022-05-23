<template>
  <div>
    <MarkText v-bind:sample="sample" @markText="markText" />
    <AddRelations v-if="taskIsAddRelations" v-bind:sample="sample" @addRelation="addRelation" @addArgument="addPlaceholderArgument" @selectArgument="selectArgument" />
  </div>
</template>

<script>
import { Annotation } from '@/models/annotation'
import { Relation } from '@/models/relation'
import MarkText from '@/components/cards/MarkText.vue'
import AddRelations from '@/components/cards/AddRelations.vue'
import * as mark from '@/text-interactions/mark-text'

export default {
  name: 'InteractionController',

  components: {
    MarkText,
    AddRelations
  },

  props: { sample: Object },

  computed: { taskIsAddRelations () { return this.$store.state.task === 'addRelations' } },

  methods: {
    markText (payload) {
      if (this.userMarkedText(payload.selection)) this.createAnnotation(payload)
      else {
        const selectedAnnotation = mark.getAnnotationIfUserClickedOnAnnotation(payload.selection, this.sample)
        if (selectedAnnotation) {
          if (selectedAnnotation.classs === 'relationArgument') {
            if (!selectedAnnotation.isActive) {
              payload.argument = selectedAnnotation
              this.selectArgument(payload)
            } else mark.markAnnotationAsDeleted(selectedAnnotation)
          }      
        }
      }
    },

    createAnnotation (payload) {
      let newAnnotation = mark.markAnnotation(payload.selection, this.sample, payload.event)
      const {activeArgument, activeRelation} = this.getActiveArgumentAndRelation()
      if (activeArgument) this.addRelationArgument(newAnnotation, activeArgument, activeRelation)
      else this.addAnnotation(newAnnotation)
    },

    userMarkedText (selection) {
      return selection.length > 0
    },

    addRelationArgument (newAnnotation, activeArgument, activeRelation) {
      newAnnotation.classs = 'relationArgument'

      if (this.activeArgumentIsPlaceholder(activeArgument)) {
        const index = activeRelation.relationArguments.indexOf(activeArgument)
        if (index > -1) activeRelation.relationArguments.splice(index, 1)
      } else {
        activeArgument.isActive = false
        activeArgument.type = 'DELETED'
      }
      newAnnotation.isActive = true
      activeRelation.relationArguments.push(newAnnotation)
    },

    addAnnotation (newAnnotation) {
      newAnnotation.classs = 'NamedEntityAnnotation'      
      // newAnnotation.classs = 'MentionAnnotation'
      this.sample.annotations.push(newAnnotation)
    },

    activeArgument () {
      for (let relation of this.sample.getRelations()) for (let argument of relation.relationArguments) if (argument.isActive) return argument
      return null
    },

    getActiveArgumentAndRelation () {
      for (let relation of this.sample.getRelations()) for (let argument of relation.relationArguments) if (argument.isActive) return {'activeArgument': argument, 'activeRelation': relation}
      return {'argument': false, 'relation': false}
    },

    addRelation (payload) {
      let length = null
      let documentRef = null
      let uid = null
      let text = null
      let begin = null
      let classs = 'relationAnnotation'
      let type = null
      let source = null
      let confidence = null
      let isActive = false
      let predicate = 'DEV-NEW-Relation'
      let relationArguments = []

      let relation = new Relation(length, documentRef, uid, text, begin, classs, type, source, confidence, isActive, predicate, relationArguments)

      payload.relation = relation
      this.addPlaceholderArgument(payload)

      this.sample.annotations.push(relation)
    },

    activeArgumentIsPlaceholder (activeArgument) {
      return activeArgument.classs === 'PLACEHOLDER'
    },

    addPlaceholderArgument (payload) {
      for (let argument of payload.relation.relationArguments) {
        if (argument.isPlaceholder) {
          if (!argument.isActive) {
            payload.argument = argument
            this.selectArgument(payload)
          }
          return
        }
      }

      // todo neue methode anbieten die eine standard relation annotation oder mention annotation erstellt.
      let length = null
      let documentRef = null
      let uid = null
      let text = 'ARGUMENT'
      let begin = null
      let classs = 'PLACEHOLDER'
      let type = null
      let source = 'USER'
      let confidence = null
      let isActive = false
      let refId = ''
      let candidates = []
      let relationArgument = new Annotation(length, documentRef, uid, text, begin, classs, type, source, confidence, isActive, refId, candidates)
      relationArgument.isPlaceholder = true

      payload.relation.relationArguments.push(relationArgument)
      payload.argument = relationArgument
      this.selectArgument(payload)
    },

    selectArgument (payload) {
      const argumentWasActive = payload.argument.isActive
      this.setActiveArgumentsFalse()
      this.setActiveRelationsFalse()

      if (!argumentWasActive) {
        payload.argument.isActive = true
      }
    },

    setActiveArgumentsFalse () {
      for (let relation of this.sample.getRelations()) for (let argument of relation.relationArguments) argument.isActive = false
    },

    setActiveRelationsFalse () {
      for (let relation of this.sample.getRelations()) relation.isActive = false
    }
  }
}
</script>

<style scoped lang="scss">
</style>

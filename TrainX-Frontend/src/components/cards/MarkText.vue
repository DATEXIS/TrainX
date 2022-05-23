<template>
  <div class="position-wrapper" v-on:click="userSelectsText($event)">
    <annotation-highlight id="sample-text" :text="sample.text" :annotations="sample.annotations" :highlightComponent="AnnotationHelper"></annotation-highlight>
  </div>
</template>

<script>
import TextHighlight from 'vue-text-highlight'
import AnnotationHelper from '@/components/cards/AnnotationHelper.vue'
import { AnnotationHighlight } from 'vue-annotation-highlight'

export default {
  name: 'MarkText',

  components: {
    TextHighlight,
    AnnotationHighlight,
    AnnotationHelper
  },

  props: {
    sample: Object
  },

  data() {
    return {
      AnnotationHelper,
      AnnotationHighlight
    }
  },

  methods: {
    getSelection () {
      if (typeof window.getSelection !== 'undefined') {
        let selection = window.getSelection()
        if (selection.rangeCount > 0) {
          let range = selection.getRangeAt(0)
          let preCaretRange = range.cloneRange()

          preCaretRange.selectNodeContents(document.getElementById('sample-text'))
          preCaretRange.setEnd(range.startContainer, range.startOffset)
          let start = preCaretRange.toString().length

          preCaretRange.setEnd(range.endContainer, range.endOffset)
          let end = preCaretRange.toString().length

          let selectedText = this.sample.text.substring(start, end)

          return { begin: start, length: end - start, text: selectedText }
        }
      }
    },

    selectionMatchesAnnotation(selection) {
      for (let annotation of this.sample.annotations) {
        if (selection.begin == annotation.begin && selection.length == annotation.length) {
          return true
        }        
      }      
      return false
    },

    userSelectsText (event) {
      let payload = { event: event, selection: this.getSelection() }
      if (!this.selectionMatchesAnnotation(payload.selection)) {
        this.$emit('markText', payload)
      }      
    }
  }
}
</script>

<style scoped lang="scss">
pre {
  white-space: pre-wrap; /* Since CSS 2.1 */
  white-space: -moz-pre-wrap; /* Mozilla, since 1999 */
  white-space: -pre-wrap; /* Opera 4-6 */
  white-space: -o-pre-wrap; /* Opera 7 */
  word-wrap: break-word; /* Internet Explorer 5.5+ */

  font-family: roboto, sans-serif;
  font-size: 12pt;
}

.card-text {
  padding-top: 0px;
}

.unselectable {
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently supported by Chrome and Opera */
}

.stacked {
  position: absolute;
}

.position-wrapper {
  position: relative;
}

.transparent {
  opacity: 0.8;
}
</style>

<template>
  <div class="white-background shadow margin-between-cards flex-container" v-show="!sample.finished">
    <div class="content-container">
      <CardTitle :title="sample.title" />
      <InteractionController :sample="sample" />
      <!-- <ShowcaseSampleProperties v-bind:sample="sample" /> -->
    </div>
    <CardButtons class="buttons-container" v-bind:sample="sample" />
  </div>
</template>

<script>
import CardTitle from '@/components/cards/CardTitle.vue'
import CardButtons from '@/components/cards/CardButtons.vue'
import InteractionController from '@/components/cards/InteractionController.vue'
import ShowcaseSampleProperties from '@/components/cards/ShowcaseSampleProperties.vue'

export default {
  name: 'Card',

  components: {
    CardTitle,
    CardButtons,
    InteractionController,
    ShowcaseSampleProperties
  },

  props: { sample: Object }
}
</script>

<style scoped lang="scss">
  .white-background {
    background-color: #FFFFFF;
  }

  .shadow {
    box-shadow: 0 3px 5px -1px rgba(0,0,0,.2),0 5px 8px 0 rgba(0,0,0,.14),0 1px 14px 0 rgba(0,0,0,.12)
  }

  .flex-container {
    display: flex;
    flex-direction: row;
  }

  .content-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-left: 15px;
    margin-top: 15px;
    margin-bottom: 15px;
  }

  .buttons-container {
    min-width: 90px;
  }
</style>

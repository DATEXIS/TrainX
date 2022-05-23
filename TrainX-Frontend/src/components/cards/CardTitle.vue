<template>
  <div class="card-title">{{title}}</div>
</template>

<script>
export default {
  name: 'CardTitle',

  props: {
    title: String
  }
}
</script>

<style scoped lang="scss">
  .card-title {
    font-size: 12pt;
    font-weight: bold;
    padding-bottom: 0px;
  }
</style>

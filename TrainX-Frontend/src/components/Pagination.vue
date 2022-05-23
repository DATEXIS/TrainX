<template>
  <div class="elevation-5 margin-between-cards pagination-grid">
    <div class="pagination-grid__left">
      Samples
    </div>
    <div class="pagination-grid__right">
      <v-btn fab small flat class="button" v-on:click="decreasePageNumber" :disabled="isFirstPage"><v-icon>chevron_left</v-icon></v-btn>
      <div class="pageNumber">{{page}}</div>
      <v-btn fab small flat class="button" v-on:click="increasePageNumber"><v-icon>chevron_right</v-icon></v-btn>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Pagination',

  methods: {
    decreasePageNumber () {
      this.$store.commit('pagination/setOffset', this.offset - this.amount)
    },

    increasePageNumber () {
      this.$store.commit('pagination/setOffset', this.offset + this.amount)
    }
  },

  computed: {
    amount () { return this.$store.getters['pagination/amount'] },
    offset () { return this.$store.getters['pagination/offset'] },
    page () { return (this.offset / this.amount) + 1 },
    isFirstPage () { return this.page === 1 }
  }
}
</script>

<style scoped lang="scss">
  .pageNumber {
    font-size: 12pt;
  }

  .pagination-grid {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .pagination-grid__left {
    margin-left: 1rem;
  }

  .pagination-grid__right {
    display: flex;
    align-items: center;
  }

  .button {
    height: 30px;
    width: 30px;
  }

  .icon {
    font-size: 20px;
  }
</style>

<template>
  <div class="digits">{{ duration.hours() | two_digits }}:{{ duration.minutes() | two_digits }}:{{ duration.seconds() | two_digits }}</div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'Countdown',

  data () {
    return {
      now: moment()
    }
  },

  created () {
    setInterval(this.updateNow, 1000) // 1000 ms = 1 s
  },

  methods: {
    updateNow () { this.now = moment() }
  },

  computed: {
    duration () {
      const start = this.$store.getters['samples/requestSamplesTimestamp']
      const end = this.now
      const difference = end.diff(start)
      const duration = moment.duration(difference)
      return duration
    }
  },

  filters: {
    two_digits: value => {
      if (value.toString().length <= 1) return '0' + value.toString()
      return value.toString()
    }
  }
}
</script>

<style scoped>
  .digits {
    font-size: 16px;
    margin-top: 20px;
  }
</style>

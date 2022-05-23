<template>
  <v-alert :value="this.$props.showAlert" :type="getType()" outline>{{ this.$props.statusText }}</v-alert>
</template>

<script>
export default {
  name: "Feedback",

  props: {
    showAlert: Boolean,
    statusText: String,
  },
	
	methods: {
		getType () {
      if (this.$props.statusText.includes("FINISHED")) {
        return "success"
      } else {
        return "info" 
      }    
		}
	}
};
</script>

<style scoped>
</style>
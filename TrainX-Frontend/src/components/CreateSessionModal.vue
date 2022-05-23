<template>
  <div class="modal-backdrop" @click="closeWhenClickedOnBackdrop">
    <div class="modal">
      <div class="modal-content">
        <h1>Create a new Session</h1>
        <form @submit.prevent="submit" class="input-grid">
          <v-text-field required color="primary" label="title" single-line outline v-model="title"></v-text-field>
          <v-textarea color="primary" label="description" outline v-model="description"></v-textarea>
          <v-btn color="primary" outline block type="submit" class="text-capitalize" large :disabled="title ? false : true">
            create session
          </v-btn>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
  import StandardButton from '@/components/StandardButton.vue'

  export default {
    name: 'CreateSessionModal',

    components: {StandardButton},
    data () {
      return {
        title: null,
        description: ''
      }
    },

    methods: {
      closeWhenClickedOnBackdrop (event) {
        if (event && event.target.className === 'modal-backdrop') this.$emit('closeModal')
      },

      submit () {
        const payload = {sessionTitle: this.title, sessionDescription: this.description}
        this.$store.dispatch('sessions/createSession', payload)
        this.$emit('closeModal')
      }
    }
  }
</script>

<style scoped>
  h1 {
    margin-bottom: 20px;
  }

  .modal-backdrop {
    position: fixed;
    z-index: 1; /* Sit on top */
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgba(0, 0, 0, 0.3);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal {
    background: #FFFFFF;
    box-shadow: 2px 2px 20px 1px;
    overflow-x: auto;
    display: flex;
    flex-direction: column;
  }

  .modal-content {
    /* position: relative; */
    padding: 30px 30px;
    width: 100%;
    margin-top: auto;
    /* margin-left: 15%; */
    /* margin-right: auto; */
  }
</style>

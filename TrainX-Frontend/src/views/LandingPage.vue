<template>
  <v-container>
    <Feedback :showAlert="userRequestedStatus" :statusText="statusText" />
    <v-layout justify-center mt-4>
      <v-flex md8>
        <h1>TrainX</h1>
        <hr/>
      </v-flex>
    </v-layout>

    <CreateSessionModal v-if='showCreateSessionModal' @closeModal='closeCreateSessionModal()'/>

    <v-layout justify-center mt-4>
      <v-flex md8>
        <div class="button-grid">
          <StandardButton class="button-grid__button--left" v-if="!showInputForSessionName" color="primary" title="New Session" icon="add_circle_outline" @click="createSession"/>
          <StandardButton color="primary" title="Old Session" icon="update" @click="getSessions"/>

          <StandardButton :disable='showUploadDatasetButton' class="button-grid__button--stretched" v-if="!selectedFile" color="primary" title="Upload Dataset" icon="cloud_upload" @click="selectFile" />
          <input v-if="selectedFile" class="hide-input button-grid__button--left" type="file" id="file" ref="file" placeholder="select dataset" @change="selectFile">
          <label v-if="selectedFile" for="file" class="input-grid__box input-grid__label">{{ filename }}</label>
          <v-btn v-if="selectedFile" class="input-grid__button" color="primary" outline large @click="uploadDataset"><v-icon>cloud_upload</v-icon></v-btn>

          <StandardButton class="button-grid__button--left" :disable='!activeSession' color="primary" title="Get Samples" icon="vertical_align_bottom" @click="getSamples"/>
          <StandardButton :disable='showUploadSamplesButton' color="primary" title="Upload Samples" icon="vertical_align_top" @click="uploadSamples"/>

          <StandardButton class="button-grid__button--left" :disable='!activeSession' color="primary" title="Get Status" icon="play_circle_outline" @click="getStatusForUser"/>
          <StandardButton :disable='!activeSession' color="primary" title="Start Training" icon="play_circle_outline" @click="startTraining"/>          

          <StandardButton class="button-grid__button--stretched" :disable='!activeSession' color="primary" title="Get Last Model" icon="cloud_download" @click="getModel"/>

          <StandardButton class="button-grid__button--stretched" color="primary" title="User Guide" icon="format_list_numbered" @click="openUserGuide"/>
        </div>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import moment from 'moment'
  import StandardButton from '@/components/StandardButton.vue'
  import CreateSessionModal from '@/components/CreateSessionModal.vue'
  import Feedback from '@/components/Feedback.vue'

  export default {
    name: 'LandingPage',

    components: {
      StandardButton,
      CreateSessionModal,
      Feedback
    },

    data () {
      return {
        showInputForSessionName: false,
        selectedFile: false,
        sessionTitle: '',
        file: '',
        showCreateSessionModal: false,
        userRequestedStatus: false,      
        statusText: '',  
      }
    },

    methods: {
      async getSessions () {
        await this.$store.dispatch('sessions/getSessions')
        this.$router.push({name: 'sessions'})
      },

      async getSamples () {
        if (this.samples.length === 0) {
          await this.$store.dispatch('samples/getSamples', { session_id: this.sessionId, offset: this.offset, amount: this.amount })
          const timestamp = moment()
          this.$store.commit('samples/setRequestSamplesTimestamp', timestamp)
        }
        this.$router.push({ name: 'samples' })
      },

      uploadSamples () {
        const start = this.$store.getters['samples/requestSamplesTimestamp']
        const end = moment()
        const duration = end.diff(start, 'milliseconds')

        const payload = { documents: this.samples, session_id: this.sessionId, sample_time: duration }
        this.$store.commit('samples/setRequestSamplesTimestamp', null)
        this.$store.dispatch('samples/postSamples', payload)
        //    this.$router.push({ name: 'upload' })
      },

      uploadDataset () {
        let formData = new FormData()
        formData.append('dataset', this.file)
        const payload = {dataset: formData, session_id: this.sessionId}
        this.$store.dispatch('datasets/postDataset', payload)
        this.selectedFile = false
      },

      selectFile () {
        if (!this.selectedFile) this.selectedFile = true
        else this.file = this.$refs.file.files[0]
      },

      getStatus () { this.$store.dispatch('sessions/getStatus', this.sessionId) },

      async getStatusForUser () { 
        await this.$store.dispatch('sessions/getStatusForUser', this.sessionId)        
        this.statusText = this.$store.getters['sessions/apiFeedback'].text
        this.userRequestedStatus = true
        setTimeout(() => {
          this.userRequestedStatus = false
        }, 5000);
      },

      createSession () { this.showCreateSessionModal = true },

      startTraining () { this.$store.dispatch('jobs/startTraining', this.sessionId) },

      closeCreateSessionModal () { this.showCreateSessionModal = false },

      openUserGuide () { this.$router.push({name: 'UserGuide'}) },

      getModel () { this.$router.push({name: 'Model'}) },
    },

    computed: {
      session () { return this.$store.getters['sessions/session'] },
      activeSession () { return this.session !== null },
      showUploadDatasetButton () { return !(this.activeSession && this.session.jobs.length === 0) },
      showUploadSamplesButton () { return !(this.activeSession && this.samples.length > 0) },
      status () { return this.$store.getters.status },
      samples () { return this.$store.getters['samples/samples'] },
      sessionId () { return this.$store.getters['sessions/sessionId'] },
      filename () {
        if (this.file !== '') return this.file.name
        else return 'SELECT FILE'
      },
      offset () { return this.$store.getters['pagination/offset'] },
      amount () { return this.$store.getters['pagination/amount'] },      
    },

    watch: {
      async session () { await this.getStatus() }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .button-grid {
    display: grid;
    grid-template-columns: 3fr 1fr 4fr;
  }

  .button-grid__button--left {
    grid-column: 1 / 3;
  }

  .button-grid__button--stretched {
    grid-column: 1 / 4;
  }

  .input-grid__box {
    border: 2px solid #2196f3;
    color: #2196f3 !important;
    text-align: center;
    grid-column: 1 / 3;
    margin-top: 6px;
    margin-bottom: 6px;
    margin-left: 8px;
    margin-right: 8px;
  }

  .input-grid__input {
    font-size: 15px;
    font-weight: 500;
  }

  .input-grid__button {
    grid-column: 3 / 4;
  }

  .input-grid__label {
    cursor: pointer; /* "hand" cursor */
    font-size: 15px;
    font-weight: 500;
    padding-top: 9px;
  }

  .hide-input {
    width: 0.1px;
    height: 0.1px;
    opacity: 0;
    overflow: hidden;
    position: absolute;
    z-index: -1;
  }
</style>

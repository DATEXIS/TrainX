import Vue from 'vue'
import * as backend from '@/api/backend'
import { ApiFeedback } from '@/models/apiFeedback'

const jobs_container = {
  module: {
    namespaced: true,

		state: {
      apiFeedback: {},
    },

    getters: {},

    mutations: {
      setApiFeedback (state, apiFeedback) { state.apiFeedback = apiFeedback },
    },

    actions: {
      async startTraining (context, sessionId) {
        const response = await jobs_container.api.startTraining(sessionId)
        context.commit('setApiFeedback', response)
      },
    }
  },

  api: {
    apiFeedback: function (response) {
			return jobs_container.parser.instantiateApiFeedback(response)
    },

    startTraining: async function (sessionId) {
      const response = await backend.post(`session/${sessionId}/startJob`)
      return jobs_container.api.apiFeedback(response)
    }
  },

  parser: {
    instantiateApiFeedback: function (response) {
			return new ApiFeedback(response.method, response.url, response.status)
    },
  }
}

export default jobs_container
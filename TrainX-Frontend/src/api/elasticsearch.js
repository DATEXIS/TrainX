import Vue from 'vue'
import * as backend from '@/api/backend'
import { ApiFeedback } from '@/models/apiFeedback'

const elasticsearch_container = {
  module: {
    namespaced: true,

		state: {
      elasticResults: null,

      apiFeedback: {},
    },

    getters: {
      elasticResults (state) { return state.elasticResults },
    },

    mutations: {
      setElasticResults (state, results) { state.elasticResults = results },

      setApiFeedback (state, apiFeedback) { state.apiFeedback = apiFeedback },
    },

    actions: {
      async getElasticResults (context, query) {
        const response = await elasticsearch_container.api.getElasticResults(query)
        context.commit('setElasticResults', response.results)
      }
    }
  },

  api: {
    statusIs2XX: function (status) {
      return status > 199 && status < 300
    },

    apiFeedback: function (response) {
			return elasticsearch_container.parser.instantiateApiFeedback(response)
    },

    getElasticResults: async function (annotation) {
      let { text, refId, language } = annotation
      const response = await backend.getElastic(`/?query=${text}&language=${language}&limit=10/`)
      let results = []
      if (elasticsearch_container.api.statusIs2XX(response.status)) results = elasticsearch_container.parser.instantiateElasticResults(response, language)
      if (refId) {
        let hasMatchingCuiToRefId = results.some(result => result.cui === refId)
        if (!hasMatchingCuiToRefId) {
          const exactElasticResult = await elasticsearch_container.api.getExactElasticResult(annotation)
          results.push(exactElasticResult)
        }
      }
      return {'results': results, 'apiFeedback': elasticsearch_container.api.apiFeedback(response)}
    },

    getExactElasticResult: async function (annotation) {
      let { refId, language } = annotation
      const refIdReponse = await backend.getElastic(`/cui/?cui=${refId}`)
      if (elasticsearch_container.api.statusIs2XX(refIdReponse.status)) return elasticsearch_container.parser.instantiateElasticResults(refIdReponse, language)[0]
    }
  },

  parser: {
    instantiateApiFeedback: function (response) {
			return new ApiFeedback(response.method, response.url, response.status)
    },

    instantiateElasticResults: function (response, language) {
      const results = []
      for (let result of response.data) {
        results.push({
          'cui': result.cui,
          'names': result.names[language].all,
          'semantic_type': result.semantic_type.name
        })
      }
      return results
    }
  }
}

export default elasticsearch_container
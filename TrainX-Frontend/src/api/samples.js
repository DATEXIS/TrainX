import Vue from 'vue'
import * as backend from '@/api/backend'
import { Sample } from '@/models/sample'
import { Annotation } from '@/models/annotation'
import { ApiFeedback } from '@/models/apiFeedback'

const samples_container = {
  module: {
		namespaced: true,

		state: {
      samples: [],
      requestSamplesTimestamp: null,
      refId: '',

      apiFeedback: {},
    },

		getters: {
      samples (state) { return state.samples },
      requestSamplesTimestamp (state) { return state.requestSamplesTimestamp },
      refId (state) { return state.refId },
    },

		mutations: {
      setSamples (state, samples) { state.samples = samples },
      setRequestSamplesTimestamp (state, timestamp) { state.requestSamplesTimestamp = timestamp },
      reOpenClosedSamples (state) { for (let sample of state.samples) sample.finished = false },
      setRefId (state, ref) { state.samples.map(sample => {
        for (let index in sample.annotations) {
          if (sample.annotations[index] == ref.annotation) {
            sample.annotations[index].refId = ref.refId
            return
          }
        }
      })},
      deleteAnnotation (state, annotation) { state.samples.map(sample => {
        for (let index in sample.annotations) {
          if (sample.annotations[index] == annotation) {
            sample.annotations.splice(index, 1)
            return
          }
        }
      })},

      setApiFeedback (state, apiFeedback) { state.apiFeedback = apiFeedback },     
    },

		actions: {
      async getSamples (context, payload) {
        context.commit('loading/setLoading', true, { root: true })
        const response = await samples_container.api.getSamples(payload)
        context.commit('loading/setLoading', false, { root: true })
        context.commit('setSamples', response.samples)
        context.commit('setApiFeedback', response.apiFeedback)
      },

      async postSamples (context, payload) {
        context.commit('loading/setLoading', true, { root: true })
        const response = await samples_container.api.postSamples(payload)
        context.commit('loading/setLoading', false, { root: true })
        context.commit('setSamples', [])
        context.commit('setApiFeedback', response.apiFeedback)
      },
    },
	},

	api: {
    statusIs2XX: function (status) {
			return status > 199 && status < 300
		},

		apiFeedback: function (response) {
			return samples_container.parser.instantiateApiFeedback(response)
    },

    getSamples: async function (payload) {
      const response = await backend.get(`session/${payload.session_id}/samples?offset=${payload.offset}&amount=${payload.amount}`)
      let samples = []
      if (samples_container.api.statusIs2XX(response.status)) samples = samples_container.parser.instantiateSamples(response)
      return {'samples': samples, 'apiFeedback': samples_container.api.apiFeedback(response)}
    },

    postSamples: async function (payload) {
      const prepareSample = samples_container.parser.prepareSamplesToSendToBackend(payload.documents)
      var payload2 = { documents: prepareSample, sample_time: payload.sample_time }
      const response = await backend.post(`session/${payload.session_id}/uploadSamples`, payload2)
      return samples_container.api.apiFeedback(response)
    }
  },

	parser: {
    instantiateApiFeedback: function (response) {
			return new ApiFeedback(response.method, response.url, response.status)
    },

    instantiateSample: function (sample) {
      const classs = sample.class
      const begin = sample.begin
      const length = sample.length
      const text = sample.text
      const annotations = sample.annotations ? samples_container.parser.instantiateAnnotations(sample.annotations) : []
      const uid = sample.uid ? sample.uid : null
      const documentRef = classs === 'Document' ? uid : sample.refUid
      const type = sample.type ? sample.type : null
      const id = sample.id ? sample.id : null
      const language = sample.language
      const tokens = null
      const empty = null
      const sentences = null
      const source = sample.source ? sample.source : null
      const finished = false
      const highlightedText = null
      const title = sample.title ? sample.titel : null

      return new Sample(length, documentRef, uid, text, begin, classs, tokens, empty, type, annotations, language, sentences, source, id, finished, highlightedText, title)
    },

    instantiateSamples: function (response) {
      const samples = []
      for (let sample of response.data) samples.push(samples_container.parser.instantiateSample(sample))
      return samples
    },

    instantiateAnnotations: function (response) {
      let annotations = []
      for (let annotation of response) {
        let classs = annotation.class
        let begin = annotation.begin
        let text = annotation.text
        let source = annotation.source
        let confidence = annotation.confidence
        let type = annotation.type ? annotation.type : null
        let length = annotation.length
        let uid = annotation.uid ? annotation.uid : null 
        let documentRef = null
        let isActive = false
        let refId = annotation.refId ? annotation.refId : null
        let candidates = annotation.candidates ? annotation.candidates : null
        annotations.push(new Annotation(length, documentRef, uid, text, begin, classs, type, source, confidence, isActive, refId, candidates))
      }
      return annotations
    },

    prepareSamplesForPOST: function (samples) {
      let preparedSamples = []

      for (let sample of samples) {
        let preparedSample = {}
        for (let key in sample) {
          let keyWithoutUnderscore = key.replace('_', '')
          let value = keyWithoutUnderscore === 'annotations' ? samples_container.parser.prepareAnnotationsForPOST(sample.annotations) : sample[keyWithoutUnderscore]
          preparedSample[keyWithoutUnderscore] = value // add property with value to preparedSample
        }
        preparedSamples.push(preparedSample)
      }
      return preparedSamples
    },

    prepareAnnotationsForPOST: function (annotations) {
      let preparedAnnotations = []

      for (let annotation of annotations) {
        let preparedannotation = {}
        for (let key in annotation) {
          let keyWithoutUnderscore = key.replace('_', '')
          let value = annotation[keyWithoutUnderscore]      // to invoke the getter
          preparedannotation[keyWithoutUnderscore] = value  // add property with value to preparedannotation
        }
        preparedAnnotations.push(preparedannotation)
      }

      return preparedAnnotations
    },

    prepareSamplesToSendToBackend:  function (samples) {
      const cleanedSamples = []
      for (let sample of samples) cleanedSamples.push(samples_container.parser.removeFrontendAttributesFromSamples(sample))
      return cleanedSamples
    },

    removeFrontendAttributesFromSamples: function (sample) {
      const linterFriendlySample = {
        class: sample.class = 'Document',
        begin: sample.begin,
        length: sample.length,
        text: sample.text,
        annotations: samples_container.parser.prepareAnnotationsToSendToBackend(sample.annotations),
        uid: sample.uid,
        documentRef: sample.documentRef,
        title: sample.title,
        type: sample.type,
        id: sample.id,
        language: sample.language,
        tokens: sample.tokens,
        empty: sample.empty,
        sentences: sample.sentences,
        source: sample.source
      }

      return linterFriendlySample // es-lint: "return statement should not contain assignment"
    },

    prepareAnnotationsToSendToBackend: function (annotations) {
      const cleanedAnnotations = []
      for (let annotation of annotations) cleanedAnnotations.push(samples_container.parser.removeFrontendAttributesFromAnnotations(annotation))
      return cleanedAnnotations
    },

    removeFrontendAttributesFromAnnotations: function (annotation) {
      const linterFriendlyAnnotation = {
        source: annotation.source,
        text: annotation.text,
        begin: annotation.begin,
        class: annotation.classs,
        type: annotation.type,
        confidence: annotation.confidence,
        length: annotation.length,
        uid: null,
        refId: annotation.refId,
        documentRef: null,
        isActive: false
      }

      return linterFriendlyAnnotation // es-lint: "return statement should not contain assignment"
    }
  }
}

export default samples_container
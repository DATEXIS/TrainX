import Vue from 'vue'
import * as backend from '@/api/backend'
import { Session } from '@/models/session'
import { ApiFeedback } from '@/models/apiFeedback'

const sessions_container = {
	module: {
		namespaced: true,

		state: {
			session: null,
			sessions: [],
			status: '',

			apiFeedback: {},
		},

		getters: {
			session (state) { return state.session },
			sessionId (state) { return state.session.sessionId },
			sessions (state) { return state.sessions },
			apiFeedback (state) { return state.apiFeedback },
		},

		mutations: {
			setSession (state, session) { state.session = session },
			setSessions (state, sessions) { state.sessions = sessions },
			setStatus (state, status) { state.status = status },

			setSamples (state, samples) { state.samples = samples },	
			setApiFeedback (state, apiFeedback) { state.apiFeedback = apiFeedback },			
		},

		actions: {
			async getSessions (context) {
				const response = await sessions_container.api.getSessions()
				context.commit('setSessions', response.sessions)
				context.commit('setApiFeedback', response.apiFeedback)
			},

			async getSession (context, sessionId) {
				const session = await sessions_container.api.getSession(sessionId)
				context.commit('setSession', session)
				context.commit('setSamples', [])
			},

			async getStatus (context, sessionId) {
        const response = await sessions_container.api.getStatus(sessionId)
        context.commit('setStatus', response.status)
      },

      async getStatusForUser (context, sessionId) {
        const response = await sessions_container.api.getStatus(sessionId)
		response.apiFeedback.text = `Backend returned Status: ${response.status} `		
		context.commit('setApiFeedback', response.apiFeedback)
      },

			async createSession (context, payload) {
				const response = await sessions_container.api.createSession(payload)
				context.commit('setSession', response.session)
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
			return sessions_container.parser.instantiateApiFeedback(response)
		},

		getSession: async function (sessionId) {
			const response = await backend.get(`session/${sessionId}`)
			return sessions_container.parser.instantiateSession(response)
		},

		getSessions: async function () {
			const response = await backend.get('sessions')
			let sessions = []
			if (sessions_container.api.statusIs2XX(response.status)) sessions = sessions_container.parser.instantiateSessions(response)
			return {'sessions': sessions, 'apiFeedback': sessions_container.api.apiFeedback(response)}
		},

		getStatus: async function (sessionId) {
			const response = await backend.get(`session/${sessionId}/status`)
			return {'status': response.data[0], 'apiFeedback': sessions_container.api.apiFeedback(response)}
		},

		createSession: async function (payload) {
			payload = { title: payload.sessionTitle, description: payload.sessionDescription }
			const response = await backend.post('session', payload)
			let newSession
			if (sessions_container.api.statusIs2XX(response.status)) newSession = sessions_container.parser.instantiateSession(response)
			return {'session': newSession, 'apiFeedback': sessions_container.api.apiFeedback(response)}
		}
	},

	parser: {
		instantiateApiFeedback: function (response) {
			return new ApiFeedback(response.method, response.url, response.status)
		},

		instantiateSession: function (response) {
			const session = response.data[0]			
			const sessionId = session.session_id
			const jobs = session.jobs
			const title = session.title
			const description = session.description
			return new Session(sessionId, jobs, title, description)
		},

		instantiateSessions: function (response) {
			const sessions = []	
			Object.entries(response.data[0]).forEach(([uid, session]) => {	
				const sessionId = parseInt(uid)
				const jobs = []
				const title = session.title
				const description = session.description	
				sessions.push(new Session(sessionId, jobs, title, description))				
			})
			return sessions
		},		
	}
}

export default sessions_container
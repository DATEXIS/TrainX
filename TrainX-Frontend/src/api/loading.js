import Vue from 'vue'

const loading_container = {
  module: {
		namespaced: true,

		state: {
      loading: false,
    },

    getters: {
      loading (state) { return state.loading },
    },

		mutations: {
      setLoading (state, loading) { state.loading = loading },
    },
  }
}

export default loading_container
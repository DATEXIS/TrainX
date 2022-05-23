import Vue from 'vue'

const pagination_container = {
  module: {
		namespaced: true,

		state: {
      offset: 0,
      amount: 10,
    },

    getters: {
      offset (state) { return state.offset },
      amount (state) { return state.amount },
    },

    mutations: {
      setOffset (state, offset) { state.offset = offset },
      amount (state) { return state.amount },
    },

    actions: {}
  },
}

export default pagination_container
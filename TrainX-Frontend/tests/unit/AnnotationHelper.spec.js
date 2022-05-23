import { mount } from '@vue/test-utils'
import { sample, elasticResults } from './props'
import Vue from 'vue'
import Vuetify from 'vuetify'
import AnnotationHelper from '../../src/components/cards/AnnotationHelper'

Vue.use(Vuetify)

describe('AnnotationHelper.vue', () => {	
	const commit = jest.fn()
	const wrapper = mount(AnnotationHelper, {
		propsData: { annotation: sample.annotations[0] },
		slots: { default: `${sample.annotations[0].text}` },
		mocks: { $store: {
			getters: {
				elasticResults,
				samples: [sample],
				userQuery: ''
			},
			dispatch: () => null,
			commit
		}}
	})
	
	it('opens tooltip on hover event', async () => {
		wrapper.find('.tooltip').trigger('mouseover')		
		await wrapper.vm.$nextTick()
		
		expect(wrapper.vm.hover).toBe(true)
		expect(wrapper.html().includes('<div class="tooltiptext">')).toBe(true)
		expect(wrapper.html().includes('<div class="list-container">')).toBe(true)	

		wrapper.find('.tooltip').trigger('mouseleave')
		await wrapper.vm.$nextTick()

		expect(wrapper.html().includes('<div class="list-container">')).toBe(false)	
	})

	it('lists elastic search results', async () => {
		wrapper.find('.tooltip').trigger('mouseover')
		const resultIsListElement = result => {
			let expressions = [
				`<li .+?>.*?${result.names[0]}.*?<\/li>`,
				`<li .+?>.*?${result.cui}.*?<\/li>`,
				`<li .+?>.*?${result.semantic_type}.*?<\/li>`
			]
			return expressions.every(exp => new RegExp(exp, 'gs').test(wrapper.html()))
		}
		await wrapper.vm.$nextTick()

		expect(elasticResults.every(resultIsListElement)).toBe(true)		
	})

	it('changes annotation type to "USER" and className when selecting list item', async () => {		
		expect(wrapper.vm.annotation.source).not.toEqual('USER')
		expect(wrapper.find('mark').classes()).not.toContain('userAnnotation')	

		wrapper.find('.tooltip').trigger('mouseover')
		await wrapper.vm.$nextTick()
		wrapper.find('li').trigger('click')
		await wrapper.vm.$nextTick()
		
		expect(wrapper.vm.annotation.source).toEqual('USER')	
		expect(wrapper.find('mark').classes()).toContain('userAnnotation')
	})

	it('updates refId when selecting list item', async () => {		
		wrapper.find('.tooltip').trigger('mouseover')
		await wrapper.vm.$nextTick()
		wrapper.find('li').trigger('click')

		expect(commit).toBeCalledWith('setRefId', {'refId': elasticResults[0].cui, 'annotation': sample.annotations[0]})
	})

	it('calls removeAnnotation function on delete-button click', async () => {
		const mockedRemoveAnnotation = jest.fn()
		wrapper.vm.removeAnnotation = mockedRemoveAnnotation
		
		wrapper.find('.tooltip').trigger('mouseover')
		await wrapper.vm.$nextTick()
		wrapper.find('.delete-button').trigger('click')

		expect(mockedRemoveAnnotation).toBeCalled()
	})
})

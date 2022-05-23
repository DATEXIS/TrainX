import { mount } from '@vue/test-utils'
import { sample } from './props'
import MarkText from '../../src/components/cards/MarkText'

describe('MarkText.vue', () => {
  const wrapper = mount(MarkText, {
    propsData: { sample }
  })

  it('displays sample text', () => {
    expect(wrapper.text()).toBe(sample.text)
  })

  it('surrounds annotations with marker tags', () => {  
    const annotationMatchesHTMLMarkTag = annotation => {
      let expr = `<mark .+?${annotation.text}.+?<\/mark>`
      let re = new RegExp(expr, 'gs')
      return re.test(wrapper.html())
    }
    
    expect(sample.annotations.every(annotationMatchesHTMLMarkTag)).toBe(true)
  })
})

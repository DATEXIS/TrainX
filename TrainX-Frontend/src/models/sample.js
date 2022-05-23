import { Span } from '@/models/span'

export class Sample extends Span {
  constructor (length, documentRef, uid, text, begin, classs, type, tokens, empty, annotations, language, sentences, source, id, finished, highlightedText, title) {
    super(length, documentRef, uid, text, begin, classs, type)
    this._tokens = tokens
    this._empty = empty
    this._annotations = annotations
    this._language = language
    this._sentences = sentences
    this._source = source
    this._id = id
    this._finished = finished
    this._highlightedText = highlightedText
    this._title = title
  }

  get tokens () { return this._tokens }
  get empty () { return this._empty }
  get annotations () { return this._annotations }
  get language () { return this._language }
  get sentences () { return this._sentences }
  get source () { return this._source }
  get id () { return this._id }
  get finished () { return this._finished }
  get highlightedText () { return this._highlightedText }
  get title () { return this._title }

  set tokens (tokens) { this._tokens = tokens }
  set empty (empty) { this._empty = empty }
  set annotations (annotations) { this._annotations = annotations }
  set language (language) { this._language = language }
  set sentences (sentences) { this._sentences = sentences }
  set source (source) { this._source = source }
  set id (id) { this._id = id }
  set finished (finished) { this._finished = finished }
  set highlightedText (highlightedText) { this._highlightedText = highlightedText }
  set title (title) { this._highlightedText = title }

  getRelations () {
    return this._annotations.filter(annotation => annotation.classs === 'relationAnnotation')
  }

  getAnnotations () {
    const annotations = this._annotations.filter(annotation => annotation.classs !== 'relationAnnotation')
    const relations = this._annotations.filter(annotation => annotation.classs === 'relationAnnotation')
    for (let relation of relations) annotations.push(...relation.relationArguments)
    return annotations
  }
}
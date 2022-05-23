export class Span {
  constructor (length, documentRef, uid, text, begin, classs, type) {
    this._length = length
    this._documentRef = documentRef
    this._uid = uid
    this._text = text
    this._begin = begin
    this._classs = classs
    this._type = type
  }

  get length () { return this._length }
  get documentRef () { return this._documentRef }
  get uid () { return this._uid }
  get text () { return this._text }
  get begin () { return this._begin }
  get classs () { return this._classs }
  get type () { return this._type }

  set length (length) { this._length = length }
  set documentRef (documentRef) { this._documentRef = documentRef }
  set uid (uid) { this._uid = uid }
  set text (text) { this._text = text }
  set begin (begin) { this._begin = begin }
  set classs (classs) { this._classs = classs }
  set type (type) { this._type = type }

  toString () {
    let str = ''

    for (let key in this) {
      let keyWithoutUnderscore = key.replace('_', '')
      let value = this[keyWithoutUnderscore] // to invoke the getter
      str += '- ' + keyWithoutUnderscore + ': ' + value + '\n'
    }

    return str
  }

  toJSON () {
    let object = {}

    for (let key in this) {
      let keyWithoutUnderscore = key.replace('_', '')
      let value = this[keyWithoutUnderscore] // to invoke the getter
      object[keyWithoutUnderscore] = value
    }

    return object
  }
}
import { Span } from '@/models/span'

export class Annotation extends Span {
  constructor (length, documentRef, uid, text, begin, classs, type, source, confidence, isActive, refId, candidates) {
    super(length, documentRef, uid, text, begin, classs, type)
    this._source = source
    this._confidence = confidence
    this._isActive = isActive
    this._refId = refId
    this._candidates = candidates
  }

  get source () { return this._source }
  get confidence () { return this._confidence }
  get isActive () { return this._isActive }
  get refId () { return this._refId }
  get candidates () { return this._candidates }

  set source (source) { this._source = source }
  set confidence (confidence) { this._confidence = confidence }
  set isActive (isActive) { this._isActive = isActive }
  set refId (refId) { this._refId = refId }
  set candidates (candidates) { this._candidates = candidates }
}
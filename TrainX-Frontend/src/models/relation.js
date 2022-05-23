import { Annotation } from '@/models/annotation'

export class Relation extends Annotation {
    constructor (length, documentRef, uid, text, begin, classs, type, source, confidence, isActive, predicate, relationArguments) {
      super(length, documentRef, uid, text, begin, classs, type, source, confidence, isActive)
      this._predicate = predicate
      this._relationArguments = relationArguments
    }
  
    get predicate () { return this._predicate }
    get relationArguments () { return this._relationArguments }
  
    set predicate (predicate) { this._predicate = predicate }
    set relationArguments (relationArguments) { this._relationArguments = relationArguments }
  }
import { Annotation } from '@/models/annotation'

export function markAnnotation (selection, sample, event) {
  let newAnnotation = constructAnnotationFromSelection(selection, sample, event)
  mergeOverlappingAnnotations(newAnnotation, sample)
  return newAnnotation
}

function constructAnnotationFromSelection (selection, sample, event) {
  let offset = sample.begin

  let isActive = false
  let length = selection.length
  let documentRef = null
  let uid = null
  let text = selection.text
  let begin = selection.begin
  let classs = 'annotation'
  let source = 'USER'
  let confidence = null
  let typee

  // eslint-disable-next-line
  ({text, begin, length} = trimWhitespace(text, begin, length))
  // eslint-disable-next-line
  if (!event.altKey) ({text, begin, length} = selectCompleteToken(sample.text, begin, length))

  begin += offset

  return new Annotation(length, documentRef, uid, text, begin, classs, typee, source, confidence, isActive)
}

function trimWhitespace (selectiontext, begin, length) {
  if (selectiontext.startsWith(' ')) {
    selectiontext = selectiontext.trimStart()
    begin += 1
    length -= 1
  }

  if (selectiontext.endsWith(' ')) {
    selectiontext = selectiontext.trimEnd()
    length -= 1
  }

  let text = selectiontext
  return {text, begin, length}
}

function selectCompleteToken (sampletext, begin, length) {
  let sampletextLength = sampletext.length

  // right side
  let charPosition = begin + length
  while (isLetter(sampletext.charAt(charPosition)) && charPosition < sampletextLength) charPosition++
  length = charPosition - begin

  // left side
  charPosition = begin
  while (isLetter(sampletext.charAt(charPosition)) && charPosition >= 0) charPosition--
  charPosition++
  length += begin - charPosition
  begin = charPosition

  let text = sampletext.slice(begin, begin + length)

  return {text, begin, length}
}

function isLetter (char) {
  let regexWhitespaceOrPunctuationMark = /[\s.?!,:;]/
  return !regexWhitespaceOrPunctuationMark.test(char)
}

function mergeOverlappingAnnotations (newAnnotation, sample) {
  let notDeletedAnnotations = sample.getAnnotations().filter(annotation => annotation.type !== 'DELETED')
  for (let oldAnnotation of notDeletedAnnotations) {
    let oldBegin = oldAnnotation.begin
    let oldEnd = oldAnnotation.begin + oldAnnotation.length

    let newBegin = newAnnotation.begin
    let newEnd = newAnnotation.begin + newAnnotation.length

    if (isOverlappingFromLeft(oldBegin, oldEnd, newBegin, newEnd)) {
      newAnnotation.length = oldEnd - newBegin
      newAnnotation.text = getAnnotationTextFromSample(newAnnotation.begin, newAnnotation.length, sample)
      markAnnotationAsDeleted(oldAnnotation)
    } else if (isOverlappingFromRight(oldBegin, oldEnd, newBegin, newEnd)) {
      newAnnotation.begin = oldBegin
      newAnnotation.length = newEnd - oldBegin
      newAnnotation.text = getAnnotationTextFromSample(newAnnotation.begin, newAnnotation.length, sample)
      markAnnotationAsDeleted(oldAnnotation)
    } else if (isOverlappingFromLeftAndRight(oldBegin, oldEnd, newBegin, newEnd)) {
      markAnnotationAsDeleted(oldAnnotation)
    } else if (isInsideOfAnnotation(oldBegin, oldEnd, newBegin, newEnd)) {
      markAnnotationAsDeleted(oldAnnotation)
    }
  }
}

function getAnnotationTextFromSample (annotationBegin, annotationLength, sample) {
  let offset = sample.begin
  let begin = annotationBegin - offset
  let end = annotationBegin + annotationLength - offset
  return sample.text.substring(begin, end)
}

function isOverlappingFromLeft (oldBegin, oldEnd, newBegin, newEnd) {
  return newBegin < oldBegin && newEnd >= oldBegin && newEnd <= oldEnd
}

function isOverlappingFromRight (oldBegin, oldEnd, newBegin, newEnd) {
  return oldEnd < newEnd && newBegin <= oldEnd && newBegin >= oldBegin
}

function isOverlappingFromLeftAndRight (oldBegin, oldEnd, newBegin, newEnd) {
  return newBegin < oldBegin && oldEnd < newEnd
}

function isInsideOfAnnotation (oldBegin, oldEnd, newBegin, newEnd) {
  return oldBegin < newBegin && newEnd < oldEnd
}

export function getAnnotationIfUserClickedOnAnnotation (selection, sample) {
  for (let annotation of sample.getAnnotations()) {
    if (selectionIsWithinAnnotation(selection, annotation, sample)) return annotation
  }
  return false
}

function selectionIsWithinAnnotation (selection, annotation, sample) {
  let offset = sample.begin
  let selectedPosition = selection.begin + offset
  let annotationBegin = annotation.begin
  let annotationEnd = annotation.begin + annotation.length
  return selectedPosition >= annotationBegin && selectedPosition < annotationEnd
}

export function markAnnotationAsDeleted (annotation) {
  annotation.type = 'DELETED'
  annotation.source = 'USER'
}

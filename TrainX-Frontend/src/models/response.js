export class Response {
  constructor (url, method, status, data) {
    this._url = url
    this._method = method
    this._status = status
    if (Array.isArray(data)) this._data = data
    else this._data = [data]
  }

  get url () { return this._url }
  get method () { return this._method }
  get status () { return this._status }
  get data () { return this._data }

  set url (url) { this._url = url }
  set method (method) { this._method = method }
  set status (status) { this._status = status }
  set data (data) { this._data = data }
}

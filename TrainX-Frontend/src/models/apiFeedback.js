export class ApiFeedback {
	constructor(method, url, status, text) {
		this._method = method
		this._url = url
		this._status = status
		this._value = true
		this._type = this.statusIs2XX(this._status) ? 'success' : 'error'
		this._text = text ? text : this.getText(this._type, this._method, this._url)
	}

	get method() { return this._method }
	get url() { return this._url }
	get status() { return this._status }
	get value() { return this._value }
	get type() { return this._type }
	get text() { return this._text }

	set method(method) { this._method = method }
	set url(url) { this._url = url }
	set status(status) { this._status = status }
	set value(value) {
		setTimeout(() => {
			value = false
		}, 7000)
		this._value = value
	}
	set type(type) { this._type = type }
	set text(text) { this._text = text }

	statusIs2XX(status) { return status > 199 && status < 300 }

	getResource(url) { 		
		return url
		// return new URL(url).pathname.split('/').slice(2).join('/') 
	}

	getText(type, method, url) {
		const requestString = `${method} ${this.getResource(url)}`
		if (type === 'success') return `${requestString} was successful.`
		else if (type === 'error') return `${requestString}  failed.`
	}
}
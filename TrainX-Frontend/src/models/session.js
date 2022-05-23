export class Session {
	constructor(sessionId, jobs, title, description) {
		this._sessionId = sessionId
		this._jobs = jobs
		this._title = title
		this._description = description
	}

	get sessionId() { return this._sessionId }
	get jobs() { return this._jobs }
	get title() { return this._title }
	get description() { return this._description }

	set sessionId(sessionId) { this._sessionId = sessionId }
	set jobs(jobs) { this._jobs = jobs }
	set title(title) { this._title = title }
	set description(description) { this._description = description }
}
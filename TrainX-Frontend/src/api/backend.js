import axios from 'axios'
import { Response } from '@/models/response'

const baseUrl = setBaseURLWithDefaultOrEnvValue()
const elasticsearchUrl = setElasticsearchUrlWithDefaultOrEnvValue()
const elasticsearchUsername = setElasticsearchUsernameWithEnvValue()
const elasticsearchPassword = setElasticsearchPasswordWithEnvValue()

function canReadFromEnv (prop) {
	return !!process.env[prop]
}

export function setBaseURLWithDefaultOrEnvValue () {
	const defaultUrl = 'http://localhost:5000/trainerv2'
	return canReadFromEnv('VUE_APP_BASE_URL') ? process.env['VUE_APP_BASE_URL'] : defaultUrl
}

function setElasticsearchUrlWithDefaultOrEnvValue () {
	const defaultUrl = 'http://localhost:3000/'
	return canReadFromEnv('VUE_APP_ELASTICSEARCH_URL') ? process.env['VUE_APP_ELASTICSEARCH_URL'] : defaultUrl
}

function setElasticsearchUsernameWithEnvValue () {
	return process.env['VUE_APP_ELASTICSEARCH_USERNAME']
}

function setElasticsearchPasswordWithEnvValue () {
	return process.env['VUE_APP_ELASTICSEARCH_PASSWORD']
}

axios.defaults.baseURL = baseUrl
axios.defaults.headers.post['Content-Type'] = 'application/json;charset=UTF-8'
axios.defaults.headers['Accept'] = 'application/json'

export async function post (collection, payload) {
	try {
		const response = await axios.post(collection, payload)
		return new Response(response.config.url, response.config.method, response.status, response.data)
	} catch (error) {
		return handleError(error, 'post')
	}
}

export async function get (collection) {
	try {
		const response = await axios.get(collection)
		return new Response(response.config.url, response.config.method, response.status, response.data)
	} catch (error) {
		return handleError(error, 'get')
	}
}

// Setup authorization for elastic search service
const token = Buffer.from(`${elasticsearchUsername}:${elasticsearchPassword}`, 'utf8').toString('base64')
const config = {
	baseURL: elasticsearchUrl,
  	headers: { 'Content-Type': 'application/json', 'Authorization': `Basic ${token}` }
}
const axiosElastic = axios.create(config)

export async function getElastic (collection) {
	try {
		const response = await axiosElastic.get(collection)
		return new Response(response.config.url, response.config.method, response.status, response.data)
	} catch (error) {
		return handleError(error, 'get')
	}
}

function handleError (error, httpMethod) {
  if (error.response) {
    // The request was made and the server responded with a
    // status code that falls out of the range of 2xx
    return new Response(error.response.config.url, httpMethod, error.response.status, error.response.data)
  } else if (error.request) {
    // The request was made but no response was received, `error.request`
    // is an instance of XMLHttpRequest in the browser and an instance
    // of http.ClientRequest in Node.js
    return new Response(error.request.responseURL, httpMethod, error.request.status, null)
  }
}
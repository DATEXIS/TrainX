import moment from 'moment'

export default {
  install (Vue, options) {
    Vue.mixin({
      methods: {
        log (message) { log(message) },
        logButton (button) { logButton(button) }
      }
    })
  }
}

function logToConsole (level, message) {
  const timestamp = moment().format('YYYY-MM-DDTHH:mm:ss')
  console.info(`${level}: ${getCaller(4)} ${message}`)
  // console.info(`${timestamp} :${level}: ${getCaller(4)}: ${message}`)
}

function log (message) {
  logToConsole('INFO', message)
}

function logButton (button) {
  logToConsole('INFO', `User clicked button: ${button}`)
}

function getCaller (stacknumber) {
  // tweak stacknumber to get the correct caller
  const stackTrace = (new Error()).stack
  const caller = stackTrace.split("\n")[stacknumber]
  const regex = /src\/\w+\/\w+\.\w+/i
  let callerName = caller.match(regex)[0].replace(/src/, '@')
  return callerName
}

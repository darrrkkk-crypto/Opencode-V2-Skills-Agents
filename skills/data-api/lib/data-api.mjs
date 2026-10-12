import { readFile } from 'node:fs/promises'
import { homedir } from 'node:os'
import { join } from 'node:path'

// Read on every request: running batch scripts observe a reconnect/token refresh.
async function runtime() {
  let config
  try {
    if (process.env.MANUS_CONFIG_HOME) {
      config = JSON.parse(await readFile(join(process.env.MANUS_CONFIG_HOME, 'data-api/runtime.json'), 'utf8'))
      if (!config.revision || !process.env.MANUS_SESSION_ID || config.sessionId !== process.env.MANUS_SESSION_ID) {
        throw new Error('Invalid session')
      }
    } else {
      config = {
        apiBaseUrl: process.env.RUNTIME_API_HOST || 'https://api.manus.im',
        token: (await readFile(join(homedir(), '.secrets/sandbox_api_token'), 'utf8')).trim(),
      }
    }
    const url = new URL(config.apiBaseUrl)
    if (!['https:', 'http:'].includes(url.protocol) || url.username || url.password || !config.token) {
      throw new Error('Invalid runtime')
    }
    return config
  } catch {
    throw new Error(
      'Data API runtime is not ready. Retry after reconnecting Manus; do not supply credentials manually.',
    )
  }
}

function object(value, label) {
  if (value === undefined || value === null) return null
  if (typeof value !== 'object' || Array.isArray(value)) throw new Error(`${label} must be a JSON object`)
  return value
}

function stringMap(value, label) {
  const entries = object(value, label)
  if (entries === null) return null
  return Object.fromEntries(Object.entries(entries).map(([key, item]) => {
    if (!['string', 'boolean', 'number'].includes(typeof item) || (typeof item === 'number' && !Number.isFinite(item)))
      throw new Error(`${label}.${key} must be a string, boolean or finite number`)
    return [key, String(item)]
  }))
}

export class ApiClient {
  async #request(method, payload) {
    const { apiBaseUrl, token } = await runtime()
    let response
    try {
      response = await fetch(`${apiBaseUrl.replace(/\/$/, '')}/apiproxy.v1.ApiProxyService/${method}`, {
        method: 'POST',
        headers: { 'content-type': 'application/json', 'x-sandbox-token': token },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(120_000),
        redirect: 'error',
      })
    } catch {
      // Never print transport errors: URLs/headers may contain session credentials.
      throw new Error('Data API request failed or timed out')
    }
    let data
    try {
      data = await response.json()
    } catch {
      throw new Error('Data API returned an invalid response')
    }
    if (!response.ok) {
      const message =
        typeof data?.message === 'string'
          ? data.message.split(token).join('[redacted]').slice(0, 500)
          : 'Request failed'
      throw new Error(`Data API ${response.status}: ${message}`)
    }
    return data
  }

  async discoverApi(source, query, limit = 3) {
    if (!source || !query || !Number.isInteger(limit) || limit < 1)
      throw new Error('source, query and a positive integer limit are required')
    return this.#request('DiscoverApi', { source, query, limit })
  }

  async callApi(apiName, { body, query, pathParams, multipartFormData } = {}) {
    if (typeof apiName !== 'string' || !apiName.trim()) throw new Error('A discovered API name is required')
    const data = await this.#request('CallApi', {
      apiId: apiName,
      body: object(body, 'body'),
      query: stringMap(query, 'query'),
      path_params: stringMap(pathParams, 'pathParams'),
      multipart_form_data: stringMap(multipartFormData, 'multipartFormData'),
    })
    if (typeof data?.jsonData === 'string') {
      try {
        return JSON.parse(data.jsonData)
      } catch {
        throw new Error('Data API returned invalid jsonData')
      }
    }
    return data
  }
}

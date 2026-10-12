// Built-in LLM client for Manus computers (Sandbox, local computer, Cloud Computer).
// Run scripts that import it with `manus-node`; only Node built-in modules are used.
import { readFile } from 'node:fs/promises'
import { homedir } from 'node:os'
import { join } from 'node:path'

// Proxy-level failures arrive as HTTP 200 with {"error": "<message>"}; only these are transient.
const TRANSIENT_PROXY_ERRORS = new Set([
  'Rate limit exceeded',
  'Internal server error',
  'Failed to check credits',
  'Failed to create proxy request',
  'Failed to connect to LLM service',
  'Failed to read response',
])
// These affect every request in the session, so batch drivers stop instead of repeating them.
const FATAL_PROXY_ERRORS = /^(Authorization header is required|External tokens are not supported|Invalid or expired sandbox token|User is blocked|Session not found|Insufficient credits|Unsupported model|Service is temporarily unavailable)/

export class LlmError extends Error {
  constructor(message, { status = 0, retryable = false, fatal = false } = {}) {
    super(message)
    this.name = 'LlmError'
    this.status = status
    this.retryable = retryable
    this.fatal = fatal
  }
}

// Read on every request so long batches observe a reconnect or token refresh.
// On a local computer MANUS_CONFIG_HOME is set and the Manus-delivered session runtime is the
// only accepted source: OPENAI_* variables there may be the user's own provider credentials.
async function runtime() {
  try {
    let apiBaseUrl
    let token
    if (process.env.MANUS_CONFIG_HOME) {
      const config = JSON.parse(await readFile(join(process.env.MANUS_CONFIG_HOME, 'data-api/runtime.json'), 'utf8'))
      if (!config.revision || !process.env.MANUS_SESSION_ID || config.sessionId !== process.env.MANUS_SESSION_ID) {
        throw new Error('Invalid session')
      }
      ;({ apiBaseUrl, token } = config)
    } else {
      apiBaseUrl = process.env.RUNTIME_API_HOST || 'https://api.manus.im'
      token = (await readFile(join(homedir(), '.secrets/sandbox_api_token'), 'utf8')).trim()
    }
    const url = new URL(apiBaseUrl)
    if (!['https:', 'http:'].includes(url.protocol) || url.username || url.password || !token) {
      throw new Error('Invalid runtime')
    }
    return { baseUrl: `${apiBaseUrl.replace(/\/$/, '')}/api/llm-proxy/v1`, token }
  } catch {
    throw new LlmError(
      'Built-in LLM runtime is not ready. Run the script with manus-node and retry after reconnecting Manus; do not supply credentials manually.',
      { fatal: true },
    )
  }
}

function errorText(error) {
  if (typeof error === 'string') return error
  if (typeof error?.message === 'string') return error.message
  return JSON.stringify(error)
}

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))

export class LlmClient {
  #timeoutMs
  #maxRetries

  /** @param {{ timeoutMs?: number, maxRetries?: number }} [options] */
  constructor({ timeoutMs = 300_000, maxRetries = 3 } = {}) {
    this.#timeoutMs = timeoutMs
    this.#maxRetries = maxRetries
  }

  async #once(method, path, body, timeoutMs) {
    const { baseUrl, token } = await runtime()
    const redact = text => String(text).split(token).join('[redacted]').slice(0, 1000)
    let response
    try {
      response = await fetch(`${baseUrl}${path}`, {
        method,
        headers: { authorization: `Bearer ${token}`, 'content-type': 'application/json' },
        body: body === undefined ? undefined : JSON.stringify(body),
        signal: AbortSignal.timeout(timeoutMs),
        redirect: 'error',
      })
    } catch (error) {
      // Never print transport errors: URLs/headers may contain session credentials.
      const timedOut = error?.name === 'TimeoutError'
      throw new LlmError(timedOut ? 'LLM request timed out' : 'LLM request failed', { retryable: true })
    }
    let data
    try {
      data = await response.json()
    } catch {
      throw new LlmError(`LLM proxy returned an invalid response (HTTP ${response.status})`, {
        status: response.status,
        retryable: response.status === 429 || response.status >= 500,
      })
    }
    if (data?.error || !response.ok) {
      const message = data?.error ? errorText(data.error) : `HTTP ${response.status}`
      const detail = typeof data?.details?.message === 'string' ? ` (${data.details.message})` : ''
      const proxyLevel = response.ok && typeof data?.error === 'string'
      throw new LlmError(redact(`LLM ${response.ok ? 'proxy' : response.status}: ${message}${detail}`), {
        status: response.status,
        retryable: proxyLevel
          ? TRANSIENT_PROXY_ERRORS.has(data.error)
          : [408, 409, 429].includes(response.status) || response.status >= 500,
        fatal: proxyLevel && FATAL_PROXY_ERRORS.test(data.error),
      })
    }
    return data
  }

  async #request(method, path, body, { timeoutMs = this.#timeoutMs, maxRetries = this.#maxRetries } = {}) {
    for (let attempt = 0; ; attempt++) {
      try {
        return await this.#once(method, path, body, timeoutMs)
      } catch (error) {
        if (!(error instanceof LlmError) || !error.retryable || attempt >= maxRetries) throw error
        await sleep(Math.min(2 ** attempt, 20) * 1000 * (0.75 + Math.random() / 2))
      }
    }
  }

  /** Live catalog: model IDs, pricing and capabilities. */
  async models() {
    const data = await this.#request('GET', '/models')
    return Array.isArray(data?.data) ? data.data : []
  }

  /**
   * OpenAI Chat Completions request body, sent as-is (provider-specific keys such as
   * `reasoning`, `thinking` or `reasoning_effort` go at the top level).
   * @param {Record<string, unknown>} request
   * @param {{ timeoutMs?: number, maxRetries?: number }} [options]
   */
  async chat(request, options) {
    if (typeof request?.model !== 'string' || !request.model || !Array.isArray(request.messages)) {
      throw new LlmError('chat() requires a model ID from the live catalog and a messages array', { fatal: true })
    }
    if (request.stream) throw new LlmError('Streaming is not supported by the built-in LLM proxy', { fatal: true })
    return this.#request('POST', '/chat/completions', request, options)
  }
}

/** Text of the first choice, or null (for example when the output budget was exhausted). */
export function messageText(response) {
  const content = response?.choices?.[0]?.message?.content
  return typeof content === 'string' ? content : null
}

/** Runs `fn(item, index)` with at most `limit` in flight and returns results in input order. */
export async function mapLimit(items, limit, fn) {
  const results = new Array(items.length)
  let next = 0
  const workers = Array.from({ length: Math.max(1, Math.min(limit, items.length)) }, async () => {
    while (next < items.length) {
      const index = next++
      results[index] = await fn(items[index], index)
    }
  })
  await Promise.all(workers)
  return results
}

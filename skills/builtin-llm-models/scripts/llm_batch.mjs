// Concurrent, retrying batch LLM driver for the Manus built-in proxy.
// Runs with `manus-node` on the Sandbox, a local computer or a Cloud Computer.
//
// Reads inputs (one per line, or a JSON array), sends each to a chosen model with a prompt
// template, and writes results to JSONL in input order:
//   {"index", "input", "output", "error", "usage"?}
//
// Examples (replace <skill-dir> with the absolute directory containing SKILL.md):
//   manus-node "<skill-dir>/scripts/llm_batch.mjs" --input items.txt --out out.jsonl \
//     --system "You are concise." --template "Summarize in one sentence:\n{input}"
//   manus-node "<skill-dir>/scripts/llm_batch.mjs" --input items.txt --out out.jsonl \
//     --model gpt-5-mini --schema schema.json --template "Extract fields from:\n{input}"
import { readFile, rename, writeFile } from 'node:fs/promises'
import { parseArgs } from 'node:util'
import { LlmClient, mapLimit, messageText } from '../lib/llm.mjs'

const EFFORTS = ['minimal', 'low', 'medium', 'high']

function loadInputs(raw) {
  const trimmed = raw.trim()
  if (trimmed.startsWith('[')) {
    try {
      const items = JSON.parse(trimmed)
      if (Array.isArray(items)) return items.map(item => (typeof item === 'string' ? item : JSON.stringify(item)))
    } catch {
      // Not a JSON array: treat as plain lines.
    }
  }
  return raw.split(/\r?\n/).filter(line => line.trim())
}

// Family-specific thinking/reasoning and output-budget shape (see SKILL.md "Max-Token Trap").
function familyOptions(model, thinkingBudget, reasoningEffort) {
  const family = model.toLowerCase()
  const options = {}
  if (family.startsWith('gemini')) {
    // Gemini reasons by default; max_completion_tokens yields content: null, so use max_tokens.
    options.max_tokens = 16384
    if (reasoningEffort) options.reasoning_effort = reasoningEffort
  } else if (reasoningEffort) {
    options.reasoning = { effort: reasoningEffort }
  } else if (thinkingBudget > 0 && family.startsWith('gpt')) {
    options.reasoning = { effort: thinkingBudget <= 1024 ? 'low' : thinkingBudget <= 4096 ? 'medium' : 'high' }
  } else if (thinkingBudget > 0 && family.startsWith('claude')) {
    // Claude requires max_tokens strictly greater than budget_tokens.
    options.thinking = { type: 'enabled', budget_tokens: thinkingBudget }
    options.max_tokens = thinkingBudget + 4096
  }
  return options
}

function integer(value, name, min) {
  const number = Number(value)
  if (!Number.isInteger(number) || number < min) throw new Error(`--${name} must be an integer >= ${min}`)
  return number
}

try {
  const { values: args } = parseArgs({
    options: {
      input: { type: 'string' },
      out: { type: 'string' },
      model: { type: 'string', default: 'gpt-5-mini' },
      template: { type: 'string', default: '{input}' },
      system: { type: 'string', default: '' },
      schema: { type: 'string', default: '' },
      workers: { type: 'string', default: '8' },
      'thinking-budget': { type: 'string', default: '0' },
      'reasoning-effort': { type: 'string', default: '' },
      'max-retries': { type: 'string', default: '3' },
      'timeout-seconds': { type: 'string', default: '300' },
      help: { type: 'boolean', short: 'h' },
    },
  })
  if (args.help) {
    console.log(`Usage: manus-node llm_batch.mjs --input FILE --out FILE.jsonl [options]
  --model ID              Model ID from the live catalog (default gpt-5-mini)
  --template TEXT         Prompt template; {input} is replaced (default "{input}")
  --system TEXT           Optional system prompt
  --schema FILE           JSON schema for strict structured output
  --workers N             Concurrent requests, 4-10 recommended (default 8)
  --thinking-budget N     Claude thinking budget; mapped to effort for GPT; ignored for Gemini
  --reasoning-effort E    minimal | low | medium | high (GPT/Gemini)
  --max-retries N         Retries for transient failures (default 3)
  --timeout-seconds N     Per-request timeout (default 300)`)
    process.exit(0)
  }
  if (!args.input || !args.out) throw new Error('--input and --out are required (see --help)')
  if (args['reasoning-effort'] && !EFFORTS.includes(args['reasoning-effort'])) {
    throw new Error(`--reasoning-effort must be one of: ${EFFORTS.join(', ')}`)
  }
  const workers = integer(args.workers, 'workers', 1)
  const thinkingBudget = integer(args['thinking-budget'], 'thinking-budget', 0)
  const client = new LlmClient({
    maxRetries: integer(args['max-retries'], 'max-retries', 0),
    timeoutMs: integer(args['timeout-seconds'], 'timeout-seconds', 1) * 1000,
  })

  const request = { model: args.model, ...familyOptions(args.model, thinkingBudget, args['reasoning-effort']) }
  if (args.schema) {
    const schema = JSON.parse(await readFile(args.schema, 'utf8'))
    request.response_format = { type: 'json_schema', json_schema: { name: 'output', strict: true, schema } }
  }

  const inputs = loadInputs(await readFile(args.input, 'utf8'))
  if (!inputs.length) throw new Error('No inputs found.')

  let done = 0
  let fatal = null
  const results = await mapLimit(inputs, workers, async (text, index) => {
    const result = { index, input: text, output: null, error: null }
    if (fatal) {
      result.error = `Skipped after fatal error: ${fatal}`
    } else {
      const messages = args.system ? [{ role: 'system', content: args.system }] : []
      // split/join avoids String.replace "$" patterns in user text.
      messages.push({ role: 'user', content: args.template.split('{input}').join(text) })
      try {
        const response = await client.chat({ ...request, messages })
        result.output = messageText(response)
        if (result.output === null) {
          result.error = `No text content (finish_reason: ${response?.choices?.[0]?.finish_reason ?? 'unknown'})`
        }
        if (response?.usage) {
          result.usage = {
            prompt_tokens: response.usage.prompt_tokens,
            completion_tokens: response.usage.completion_tokens,
          }
        }
      } catch (error) {
        result.error = error.message
        if (error.fatal) fatal ??= error.message
      }
    }
    done++
    if (done % 10 === 0 || done === inputs.length) console.error(`  ${done}/${inputs.length} done`)
    return result
  })

  const temporary = `${args.out}.tmp-${process.pid}`
  await writeFile(temporary, results.map(result => JSON.stringify(result)).join('\n') + '\n', 'utf8')
  await rename(temporary, args.out)

  const errors = results.filter(result => result.error).length
  console.error(`Wrote ${results.length} results to ${args.out} (${errors} errors).`)
  if (fatal) console.error(`Stopped early: ${fatal}`)
  else if (errors) console.error('Re-run the failed items, optionally on a stronger model.')
  if (errors === results.length) process.exitCode = 1
} catch (error) {
  console.error(error instanceof SyntaxError ? `Invalid JSON: ${error.message}` : error.message)
  process.exitCode = 1
}

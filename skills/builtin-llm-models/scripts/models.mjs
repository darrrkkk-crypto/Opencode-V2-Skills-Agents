// Prints the live built-in model catalog (IDs, pricing, capabilities) as JSON.
import { LlmClient } from '../lib/llm.mjs'

try {
  console.log(JSON.stringify(await new LlmClient().models(), null, 2))
} catch (error) {
  console.error(error.message)
  process.exitCode = 1
}

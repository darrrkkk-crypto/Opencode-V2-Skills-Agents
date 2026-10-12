import { parseArgs } from 'node:util'
import { ApiClient } from '../lib/data-api.mjs'

try {
  const { values } = parseArgs({
    options: Object.fromEntries(
      ['api', 'query-json', 'body-json', 'path-params-json', 'multipart-form-data-json'].map(key => [
        key,
        { type: 'string' },
      ]),
    ),
  })
  const json = key => (values[key] === undefined ? undefined : JSON.parse(values[key]))
  const result = await new ApiClient().callApi(values.api, {
    query: json('query-json'),
    body: json('body-json'),
    pathParams: json('path-params-json'),
    multipartFormData: json('multipart-form-data-json'),
  })
  console.log(JSON.stringify(result, null, 2))
  if (result?.error) process.exitCode = 1
} catch (error) {
  console.error(error instanceof SyntaxError ? 'Arguments must contain valid JSON objects' : error.message)
  process.exitCode = 1
}

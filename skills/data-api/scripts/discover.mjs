import { parseArgs } from 'node:util'
import { ApiClient } from '../lib/data-api.mjs'

const SOURCES = {
  'x-twitter': 'X/Twitter',
  linkedin: 'LinkedIn',
  youtube: 'YouTube',
  'social-media': 'Social Media',
  'financial-market': 'Financial Market',
  'earnings-research': 'Quartr',
  crunchbase: 'Crunchbase',
  'world-bank': 'World Bank',
  'google-trends': 'Google Trends',
  'app-store': 'App Store',
  similarweb: 'Similarweb',
  'domain-check': 'Domainr',
  '3d-model': 'Tripo3D',
}
try {
  const { values } = parseArgs({
    options: {
      source: { type: 'string' },
      query: { type: 'string' },
      limit: { type: 'string', default: '3' },
    },
  })
  if (!Object.hasOwn(SOURCES, values.source)) throw new Error('Choose a source from the Skill source table')
  const { apis = [] } = await new ApiClient().discoverApi(values.source, values.query, Number(values.limit))
  console.log(JSON.stringify({ apis }, null, 2))
  const resources = apis.map(api => ({
    id: api.apiName || api.shortId,
    title: api.name || api.apiName,
    provider: api.provider || SOURCES[values.source],
  }))
  if (resources.length) console.log('MANUS_RESOURCE_EVENT=' + JSON.stringify({ type: 'data_api', resources }))
} catch (error) {
  console.error(error.message)
  process.exitCode = 1
}

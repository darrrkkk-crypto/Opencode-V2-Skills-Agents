# Google Maps proxy

The platform proxies Google Maps requests using platform credentials. Its project API base and keys are supplied at runtime as described in [service API](service-api.md#runtime-credentials-and-scope).

## Calling convention

`$MANUS_API_URL/v1/maps/proxy/<google-maps-path>` mirrors the Google Maps path. Authentication uses Google's `key=` query parameter: browser requests use `MANUS_API_BROWSER_KEY`; server requests use `MANUS_API_KEY`. Array-valued query parameters use `|` separators.

## Browser surface

The Maps JavaScript API is available at `/v1/maps/proxy/maps/api/js?key=<MANUS_API_BROWSER_KEY>&libraries=<libraries>`. Its browser namespace is `google.maps.*`. This is the Google browser API surface, not a requirement to use a particular application framework.

## Web Service APIs

Paths below append to `$MANUS_API_URL/v1/maps/proxy`. Responses retain Google's native shapes. Proxying a path does not constitute a guarantee that every upstream feature, request, or model of usage is available without limits.

| API | Path | Input (query) | Output to read |
| --- | --- | --- | --- |
| Geocoding | `/maps/api/geocode/json` | `address` or `latlng` (`"37.42,-122.08"`) | `results[0].geometry.location`, `formatted_address` |
| Directions | `/maps/api/directions/json` | `origin`, `destination`, `mode?`, `waypoints?`, `alternatives?` | `routes[0].legs[0]` distance/duration/steps |
| Distance Matrix | `/maps/api/distancematrix/json` | `origins`, `destinations` (`\|`-separated), `mode?`, `units?` | `rows[i].elements[j]` |
| Place text search | `/maps/api/place/textsearch/json` | `query`, `location?`, `radius?`, `type?` | `results[].name/rating/geometry/place_id` |
| Nearby search | `/maps/api/place/nearbysearch/json` | `location`, `radius`, `type?`, `keyword?` | `results[]` |
| Place details | `/maps/api/place/details/json` | `place_id`, `fields?` (`"name,rating,website"`) | `result` |
| Place autocomplete | `/maps/api/place/autocomplete/json` | `input`, `location?`, `radius?` | `predictions[].description/place_id` |
| Elevation | `/maps/api/elevation/json` | `locations` or `path` + `samples` | `results[].elevation` (meters) |
| Time zone | `/maps/api/timezone/json` | `location`, `timestamp` (unix seconds) | `timeZoneId`, `timeZoneName` |
| Roads | `/v1/snapToRoads`, `/v1/nearestRoads`, `/v1/speedLimits` | `path` / `points` (`"lat,lng\|lat,lng"`) | snapped points / speed limits |
| Static maps | `/maps/api/staticmap` | `center`, `zoom`, `size`, `markers?`, `maptype?` | an **image**, not JSON — use the URL directly in `<img src>` |

`mode` is `driving | walking | bicycling | transit`; `maptype` is
`roadmap | satellite | terrain | hybrid`.

## Integration choices

Use the platform Maps credentials instead of asking the user for a separate Google Maps key. Do not switch to a third-party map library as a substitute for the supplied proxy. For interactive maps, the default is Google's browser JavaScript API loaded through this proxy.

Use server-side Web Service calls when browser SDK use does not fit the work: persistence of results, bulk processing, caching, scheduled jobs or keeping business logic on the server. This default does not assert unlimited support for every upstream feature; check the actual API result and supported surface.

For a static site, substitute the public API base and browser key into the bundle at build time. For a container application, render or serve those public values from the runtime environment; do not assume the private server key or even every public variable is supplied to every container build placement. Preserve server-key/browser-key separation.

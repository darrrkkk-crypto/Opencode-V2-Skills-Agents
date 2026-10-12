# PWA manifest ownership

The `pwa` domain chooses who owns the published site's Web App Manifest. It does not create a
service worker, modify application code, or affect the dev preview. Declare it with
`PUT <config-plane>/config/pwa` ([the config plane guide](configuration.md)). A saved change
reaches the already-published site within about 60 seconds; no republish is needed.

## Modes

```jsonc
{
  "pwa": {
    "manifestMode": "platform_default"
  }
}
```

`manifestMode` is required whenever the `pwa` domain is present and accepts exactly:

- `platform_default` — the default. For a production project with a logo, the platform serves the
  generated manifest from `/__manus/pwa/manifest.webmanifest`. On the canonical hostname it also
  injects that manifest link only when the page does not already declare one; an
  application-provided `<link rel="manifest">` always wins. The generated manifest uses the
  project title and logo, opens at `/`, and requests standalone display. It does not include or
  generate a service worker.
- `application_owned` — the platform neither injects a manifest link nor serves its generated
  manifest. The application owns the link, manifest contents, icons, update behavior, and any
  service worker. Choose this mode when the product implements its own PWA contract; do not choose
  it merely to customize unrelated page metadata.

The whole `pwa` domain is optional. Its absence is exactly `platform_default`, preserving existing
published sites. To clear an explicit selection and return to that default, replace the domain with
an empty fragment: `PUT <config-plane>/config/pwa` with body `{}`.

Automatic link injection applies only to the canonical production hostname and only when the
project has a logo. Preview and alias hostnames do not receive the injected link. This selection
does not change authentication, route tables, caching, or the application's own ordinary manifest
paths such as `/manifest.webmanifest`.

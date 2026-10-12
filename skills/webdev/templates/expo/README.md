# Expo Mobile template README

Managed Mobile is the fixed Cloud Expo Router / React Native / TypeScript / NativeWind starter
with Express/tRPC and Drizzle. Plain-local Mobile, chosen through Work Locally before switching
or initializing, is outside these fixed-starter restrictions.

## Product inputs and runtime

Use `applicationKind: mobile_app`. Mobile accepts no `features`, framework, template, scaffold,
platform or port choices; managed server and database are enabled. Revision 1 installs:

```json
{"runtime":{"port":8081,"endpoints":[{"name":"api","port":3000}]},"preview":{"device":{"connect":"exps://{host:primary}","openWith":{"name":"Expo Go","ios":"https://apps.apple.com/app/id982107779","android":"https://play.google.com/store/apps/details?id=host.exp.exponent"}}}}
```

These Mobile values are fixed even though the generic Runtime schema supports other values.
Mobile's canonical repository must remain Manus-managed; native builds do not accept
a GitHub-canonical repository.

Init materializes the frozen starter and installs its lockfile, but does not start Metro/API
or establish the user table required by the starter's OAuth/API paths.

The platform supplies current addresses in `EXPO_PACKAGER_PROXY_URL`, `EXPO_WEB_PREVIEW_URL`,
`EXPO_APP_QR_URL`, `REACT_NATIVE_PACKAGER_HOSTNAME`, and `EXPO_PUBLIC_API_BASE_URL`.
Device Preview uses the current Metro endpoint, not a permanent Cloud hostname; do not hardcode,
persist or request these addresses from the user. The starter's environment loader exposes
public OAuth/application values; server API/signing credentials stay out of native and Web bundles.

## Metro/API startup and recovery

Run `pnpm db:push` as a finite command before the starter's first OAuth/API traffic and require
success. It synchronizes the starter schema. After attach or Sandbox replacement, repeat it
only for changed migrations or a required schema not yet established.

Check both listeners and start only the missing processes with `service=true`:

| Missing listener | Command |
| --- | --- |
| Both Metro 8081 and API 3000 | `pnpm dev` |
| Metro 8081 only | `pnpm dev:metro` |
| API 3000 only | `pnpm dev:server` |

Recheck both ports; Mobile Preview requires both listeners. `CI=1` or `CI=true` disables
Metro watch/reloads in this bundled Expo CLI. Do not set or inherit it on a resident Mobile
command; CI mode is for finite check/test/database commands.

After attach, replacement or a later turn, closed ports do not imply missing dependencies.
Use finite `pnpm install --prefer-offline` only if `node_modules` is missing or a finite check
reports missing packages, then restore the missing listeners.

## Expo Go authorization

Web Preview works before Expo authorization. Dashboard Connect Expo reuses or saves the attached
Session's Expo build credential and sends a token-free preparation request. For that request,
call `webdev.config` with `method: GET`, `path: env` and require `runtime_sync: applied`;
this refreshes private environment values even when the config revision is unchanged.
Never retrieve or print the credential. Token entry belongs to the Dashboard form, not chat
or source files; the phone must sign into Expo Go with the same Expo account.

Restart only Metro with the refreshed shell environment on its declared port; preserve the API
process and verify both listeners. Existing Metro does not inherit the new environment.
On sync failure, report it rather than claiming readiness. Dashboard shows the QR after
environment synchronization; that does not prove Metro restarted or a phone connected.

## Starter-specific implementation

The fixed tree is `app/`, `components/`, `hooks/`, `lib/`, `server/`, and `drizzle/`.
Preserve `appSlug`, scheme and generated iOS/Android identifiers in `app.config.ts`.
The supplied OAuth, database, storage and service adapters belong to this starter, not a
universal Web SDK.

- Use React Native components and NativeWind; isolate Web DOM code behind a platform boundary.
- The installed adapter calls `remapProps(Pressable, { className: false })`: style `Pressable`
  containers with `style`/`StyleSheet`; child `Text` still accepts NativeWind classes.
- React Native Web's `Alert.alert` is a no-op in this starter. For destructive confirmation,
  retain native confirmation on native and use a controlled modal or platform-gated
  `window.confirm` on Web so callbacks work on both.
- Plan screens and tap-by-tap flows for portrait, one-handed use.

## Native branding assets

New Mobile projects require a distinct square launcher icon without baked-in rounded corners
before the first checkpoint containing application work. This is a delivery requirement, not
a claim that the checkpoint API rejects a missing icon; no particular provider or paid tool
is required. Carry the same identity through the configured files:

```text
assets/images/icon.png
assets/images/splash-icon.png
assets/images/favicon.png
assets/images/android-icon-foreground.png
assets/images/android-icon-background.png
assets/images/android-icon-monochrome.png
```

Update their branding references in `app.config.ts` while preserving application identifiers.
Register that icon through the main Skill's project-logo metadata contract before checkpointing.
Metadata sync does not replace native bundle files or waive icon delivery; bundled files and
managed URLs have separate lifecycles under [Storage](../../references/storage.md).

## Native verification and build handoff

Expo Web, Expo Go and native release artifacts are different execution surfaces. A Web screenshot
does not verify camera, notifications, haptics, deep links or native storage; use deterministic
unit coverage or an actual device check for requested native-only features, and state gaps.
A raw Metro 404 does not establish that a managed asset is absent; use Dashboard/public Preview
without changing its stored path merely because Metro cannot serve it.

Dashboard builds Android APK/AAB or iOS/TestFlight from accepted source/configuration. Do not
run Android/iOS release builds inside Sandbox or Expo/EAS builds in the resident dev process.
Keep source, configuration, relevant checks and the accepted checkpoint ready for the Dashboard
action; claim a release artifact only after its actual build result.

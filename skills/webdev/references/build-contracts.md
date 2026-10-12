# Build and runtime contracts

Use this reference for the detailed contract or recovery needed by the current operation.
Read the section for the contract being configured:

- [Static build](#static-build)
- [Container build](#container-build)

## Static build

This is the complete `build` contract for static output. A project without an application
server can publish these files without a container, framework, or bundler. A server project
can also declare this contract for the static part of a hybrid publication.

<a id="static-declaration"></a>
### Declaration

`PUT <config-plane>/config/build` takes the complete `build` domain fragment. A valid no-build
example is:

```json
{"build":{"command":"true","outputDirectory":"public"}}
```

This example publishes the committed `public/` directory, which must contain `index.html`.
It does not imply any application scaffold or package manager.

| Field | Accepted value |
| --- | --- |
| `build.command` | Trimmed, non-empty string, at most 1000 characters at declaration; inline credential literals are rejected |
| `build.outputDirectory` | Canonical repository-relative subdirectory, 1–256 characters from `A-Za-z0-9._/-` |

An output path cannot be absolute, `.` or `..`, contain either as a segment, contain empty
segments (`//`), or end with `/`. Output symlinks must resolve inside the repository. The
publish pipeline also rejects NUL in the command and enforces its limit in bytes, so a
non-ASCII command can pass declaration length validation yet fail publication.

The config tool/HTTP transport and common response envelope, when unknown, are in
[configuration](configuration.md). No other capability is required merely to write `build`.

<a id="static-execution-and-build-environment"></a>
### Execution and build environment

The platform clones the selected checkpoint and runs, at the repository root:

```text
sh -eu -c "<build.command>"
```

There is no preceding dependency installation or package-manager detection. Only checkpoint
contents are available; additional files or installed dependencies from a development working
copy are not build inputs. The whole static activity has one documented five-minute budget
covering clone, command execution, and upload.

Static and hybrid host builds receive the resolved publish environment as process environment
variables. This includes the platform values and declared values supplied for that publication.
The static output has no server process or runtime environment of its own. Build-time access
to a value does not make that value browser-public.

The static host build does not provide a browser. A development Sandbox's installed tools and
network access do not guarantee the same capabilities in that hosted build environment.

<a id="static-output-and-result-boundary"></a>
### Output and result boundary

The platform uploads `build.outputDirectory` to object storage. Publication requires its root
`index.html`. It does not generate a missing application body or provide a prerendered crawler
snapshot. A hosted result covers clone, execution, the hosted time limit, and upload; a local
command is a different execution surface.

Custom path declarations belong to [routes](routing-and-responses.md#published-routes) only when the project uses them.
Platform HTTP transformations, cache headers, and republish behavior belong to
[published response handling](routing-and-responses.md#platform-http-behavior) when those response facts matter.

<a id="static-preparing-a-deployable-static-checkpoint"></a>
### Preparing a deployable static checkpoint

Make `build.command` self-contained. If the build has dependencies, include an explicit install
that matches the committed lockfile before the build; do not rely on a warm development copy.
Pin the chosen package-manager/toolchain version and commit the manifest, lockfile, and reviewed
installation/lifecycle policy. The hosted install must use that same policy. Never disable
required install scripts merely to silence a failure.

Declare the build contract once it matches the application's real output; do not wait for a
Publish request to leave the project publishable. For a no-build site, keep and verify the
committed `index.html` under the declared output subdirectory. Review the actual command,
script names, lockfile, install-policy files, and output-path configuration before checkpointing.
Do not claim a hosted output exists merely because the development server works.

Hosted Publish is the authoritative integration build; ordinary local
production or clean-checkout rehearsals are not default publication prerequisites.

For a browser-only application, use public/browser-safe APIs and never embed private runtime
credentials. If the selected feature actually needs server-held credentials, shared private
server data, Manus account login, a webhook, a server-side payment flow, or scheduled server
work, explain the server requirement rather than delivering a non-working frontend substitute.
Do not treat an existing external payment link as a request to enable platform payments.
Explain a one-way server/database enablement before making that change, preserving the user's
explicit staging requirements. Capability-specific contracts own the implementation details.

<a id="static-publish-failure-and-focused-reproduction"></a>
### Publish failure and focused reproduction

Start from the concrete returned failure and verify that cause against the project. Fix the
specific cause and run the affected checks. Missing or unhelpful detail is not permission to
guess a cause or rebuild everything locally.

Only when a nonstandard toolchain or concrete failure requires a clean-checkout comparison,
materialize `git archive HEAD` into a fresh empty scratch directory. Run the exact declared
`sh -eu -c "<build.command>"` there and confirm the declared output and its root `index.html`.
That comparison must not depend on uncommitted files or installed directories from the working
copy. Keep its result separate from hosted publication: hosted network/tools, time limits, and
upload are still different.

If discoverability is required, apply the [HTML/SEO workflow](../seo/SKILL.md) rather than
assuming a rendered browser page proves indexable HTML. When publication includes custom static
routes, apply the [route validation workflow](routing-and-responses.md#published-routes) for those actual routes.

## Container build

A server deployment requires `features.server: true` and a `deploy` declaration. The project
Dockerfile is the image build/run contract for any supported server language. The platform
binds its path, port, and health endpoint; it does not choose an application stack or generate
a project Dockerfile.

The project Dockerfile owns installation, compilation and the production entrypoint. Include the required build
steps and serve the resulting production assets; Publish does not add missing compilation
steps or replace development JS/CSS references for you. Skipping an extra sandbox build
does not remove these responsibilities.

<a id="container-runtime-properties-that-affect-the-application"></a>
### Runtime properties that affect the application

A deployed instance and its writable filesystem are ephemeral. Restart, replacement, and idle
reclamation can remove process memory and runtime-written files. Multiple instances can serve
concurrently without sharing those in-process or filesystem writes. A resident hosting mode
is not a persistence guarantee.

A new live `version_id` and successful `publish_status` do not mean all instances of the prior
version have already stopped. Deployment versions can overlap; the result exposes no fixed
cutover duration. The instance's residency and resource settings belong to [hosting](hosting.md)
when those capabilities are involved.

<a id="container-declaration"></a>
### Declaration

`PUT <config-plane>/config/deploy` takes a complete domain fragment, for example:

```json
{"deploy":{"healthPath":"/_app/health"}}
```

| Field | Accepted value and effect |
| --- | --- |
| `deploy.dockerfilePath` | Optional; defaults to root `Dockerfile`; canonical repository-relative path, 1–256 characters from `A-Za-z0-9._/-` |
| `deploy.healthPath` | Required path beginning with `/`, 1–256 characters from `A-Za-z0-9._/-`; no `..` segment or NUL; application success is an unauthenticated 2xx–3xx response |

The Dockerfile path rejects absolute paths, `.`/`..` segments, repeated separators, and a
trailing separator. On separate domain writes, stored `features.server` must already be true
or the `deploy` write fails with `needs_server_true`. A whole-document write is validated as
one final document, so it can contain both changes atomically. General transport is in
[configuration](configuration.md) if needed.

The application starts using its Dockerfile `ENTRYPOINT` and `CMD`. Keep startup logic in that file.

<a id="container-image-build-inputs-and-cache"></a>
### Image build inputs and cache

The context is the cloned checkpoint. The platform writes `.dockerignore`, excluding
`node_modules`, `.git`, `.env` and `.env.*`, with `.env.example` retained; a project-authored
file is overwritten. A Sandbox's installations are not additional image inputs. Server-side frontend
assets are built in the image unless the project separately declares `build` for hybrid static
output; the [static build contract](build-contracts.md#static-build) applies only to that separate output.

Layer caching across publishes is best-effort. The
optional top-level `buildCache` boolean controls container image caching; it is enabled by
default, and `false` asks for a fresh image build on the next publish. It is not part of `build`
and has no per-domain endpoint. It is valid only with `deploy`; otherwise validation returns
`build_cache_needs_container`. It changes neither a static host build nor development caches.

Documented image-build placements have per-attempt budgets of six or eight minutes. A
budget interruption can be retried up to three attempts in total; an ordinary failed build is
not retried by that mechanism.

<a id="container-build-time-and-runtime-environment"></a>
### Build-time and runtime environment

The platform supplies the publication environment. Private runtime credentials, including
`MANUS_API_KEY`, `MANUS_JWT_SECRET`, `DATABASE_URL` and private custom keys, are not guaranteed
during image compilation. Read them at runtime. A `MANUS_` prefix does not make a variable
public, and build-time availability does not permit exposing a value to the browser.
For public frontend configuration, use the selected Service API contract; when build-time
availability is uncertain, supply browser-safe values from the running application.

Static and hybrid host-build environment follows the [static build contract](#static-build).

<a id="container-startup-and-health-observations"></a>
### Startup and health observations

Container/hybrid publication configures HTTP readiness using the required `deploy.healthPath`.
The application must serve an unauthenticated success response at that path. Public gateway
responses and application responses can differ; a passing readiness check does not validate
other application routes. Use returned failure details for startup timeouts rather than
assuming a fixed provider-specific probe schedule.

Publish outcomes can arrive as attached context on a later Agent turn. They are not a complete
image-build log, and runtime console logs require a service that has started. The corresponding
platform log surface belongs to [diagnostics](diagnostics.md) when logs are actually needed.

HTTP rewriting and cache behavior are defined in [published response handling](routing-and-responses.md#platform-http-behavior) when
those response properties matter.

<a id="container-application-and-startup-preparation"></a>
### Application and startup preparation

For a new server project, record the matching `deploy` contract and committed Dockerfile once
the server is listening; do not leave its publication contract until a user presses Publish.

Preview does not exercise code enabled only by the production entrypoint or environment.
For a production-only failure, inspect differences in entrypoint, route registration, required
environment names, final dependencies and assets. Give these facts to the validation agent when
it reviews that path; use existing evidence and check only the concrete uncertainty.
The [platform environment contract](service-api.md#platform-owned-compatibility-names) owns
publication-only compatibility aliases that can change which application branch executes.

Keep durable state outside process memory and the ephemeral container filesystem. Use durable
database/object storage for data that must survive restarts or multiple instances; durable
scheduled triggers use the [scheduled-work contract](scheduled-work.md), not in-process timers.
For background work whose correctness depends on code/schema version, put the relevant version
or compatibility condition on the job, or make obsolete consumers reject incompatible jobs.
Do not treat publication as an instantaneous cutoff of the previous consumer.

Model work beyond the request limit as background execution with a result/status lookup rather
than one long HTTP request. Keep boot work short or bind the listener before heavy preparation;
a startup migration must not consume the health budget before the service can answer.

Choose an application-owned health path unlikely to collide with platform probe paths and
return an unauthenticated success response. If a public path returns a platform response,
diagnose the route before adding a duplicate application handler.

<a id="container-image-inputs-and-entrypoint"></a>
### Image inputs and entrypoint

Dockerfile `COPY` sources must be committed and reach the image stage that uses them. The
entrypoint/startup script must start the process that binds the published port.

For each stage that installs dependencies, carry the same pinned toolchain/package-manager,
matching lockfile, workspace manifests, and reviewed installation/lifecycle permissions used by
the project. Place them in the stage before its install. Never replace that checked-in policy
with a blanket skip of required scripts. Preserve binary/runtime compatibility across image
stages, including architecture and libc compatibility.

Supply frontend configuration from the running server using public values when portable
build-time availability is not established. Do not hardcode protected values into the image
source or client output. Build-time availability does not waive protected-value handling.

Do not install a container engine or make an ordinary
local image/production build or clean-checkout rehearsal a prerequisite for Publish.

<a id="container-failure-handling"></a>
### Failure handling

Use the actual returned error first and check it against the relevant image input or startup
path. Fix that cause and verify only the affected behavior. If the detail is missing, choose
the smallest inspection or reproduction that answers the open question; do not guess a cause
or default to a full rebuild. Use heavier local reproduction only for a nonstandard toolchain
or a concrete failure that specifically needs it. Runtime console logs are useful only after a
service has started; they are not a substitute for missing image-build output.

If the new version is accepted but old background behavior remains visible, compare the
reported version and overlapping-instance behavior before calling the deployment absent or
blaming an intermittent fault. Keep observed build, startup, and public-response evidence
separate in the handoff.

Keep Dockerfile `EXPOSE` consistent with the application listener and honor `PORT` when supplied; use 3000 by default. Do not declare `deploy.port` or copy Preview's `runtime.port` into production settings.

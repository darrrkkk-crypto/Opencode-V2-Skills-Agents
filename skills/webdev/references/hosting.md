# Published resources and hosting

This page owns container resource sizes and the published deployment's residency declaration.
They do not configure development Preview processes. The provider, region, and scaling
placement are platform decisions, not selectable fields on this surface.

## `resources`

`PUT <config-plane>/config/resources` takes `{"resources": {"cpu": N, "memoryMb": N}}`.
Both fields are required when the domain is present. A `deploy` contract must exist; otherwise
validation returns `resources_needs_deploy`. The only accepted pairs are:

| vCPU (`cpu`) | MiB (`memoryMb`) |
| --- | --- |
| 0.25 | 512 |
| 0.5 | 1024 |
| 1 | 2048 |
| 2 | 4096 |
| 4 | 8192 |
| 8 | 16384 |

The pair is exact, not rounded to the nearest tier (`resources_tier_invalid`). Omission keeps
the platform default size. A stored tier takes effect on the **next publish**; a tier change
that requires a platform move causes a cold redeploy.

The 8 vCPU / 16384 MiB tier requires membership **at publish, not save**. Its declaration can
be stored by a non-member, while every subsequent publish is refused `requires_membership`
until membership or the declared tier changes. A rejected publish does not roll the stored
resource declaration back.

## `hosting` schema

`PUT <config-plane>/config/hosting` takes the complete hosting domain, for example
`{"hosting": {"mode": "on_demand", "idleMinutes": 120}}`. It replaces, rather than merges,
that domain. General replacement/response behavior is in
[configuration](configuration.md) when needed.


| Field | Contract |
| --- | --- |
| `mode` | Required when `hosting` is declared: `on_demand` or `always_on`. An empty domain is invalid. |
| `idleMinutes` | Optional integer 30–4320; valid only with `on_demand`. Omission leaves the environment's platform-selected window, not a fixed documented number. |

`on_demand` permits idle sleep; a later request wakes the deployment and can pay a cold-start
delay. `always_on` requests a resident deployment and requires owner membership. An idle window
above 1440 minutes also requires membership. A failed membership check at hosting save returns
`403 requires_membership` and stores nothing; the Dashboard hosting settings expose the owner
upgrade path. This differs from the resource-tier publish rejection above.

The domain cannot implicitly switch back from `always_on` by omitting `mode`; the declaration
must explicitly say `on_demand`. The schema codes are `hosting_empty`, `required` at
`hosting.mode`, and `hosting_idle_minutes_conflicts_always_on`.

Save hosting separately from `pwa` and `features`; combined live writes are rejected before
any platform change. A `409 revision_conflict` with `reason_code: hosting_apply_unknown`
means the platform setting may already have changed while the config revision did not commit.
Read `GET config` and `GET infra/overview` before choosing a correction; do not blindly replay
the PUT. The service preserves this outcome and rechecks platform state on a later attempt.

## Choosing a hosting mode

**Reserved** is the product name for `always_on`; **Autoscale** is the product name for
`on_demand`.

For Reserved, make the requested `PUT config/hosting` with `{"hosting":{"mode":"always_on"}}`
after the normal `GET config` preparation. When entering Reserved, the service opens its product-owned
confirmation Widget with `409 confirmation_required`, `reason_code: hosting_confirmation_required`, an
operation `action_url`, and an agent pause. Do not ask for a duplicate chat confirmation, invent
another card, or bypass the Widget with another direct write. Stop and wait for the card result.
After `hosting_mode_confirmed`, the original operation is already applied: read `GET config`, then
`GET infra/overview`; do not repeat the PUT. Report the saved declaration and observed deployment
reality separately—the confirmation does not prove that deployment has completed. After
`hosting_mode_cancelled`, do not reopen the card unless the user asks. After
`hosting_mode_failed`, read current config and infra state before explaining the failure; never
blindly replay the original write.

For Autoscale, explain verbally before the write that idle traffic can let an `on_demand`
deployment sleep and that a later request can experience a cold start. Obtain the user's explicit
agreement, then issue the direct `PUT config/hosting` for `{"hosting":{"mode":"on_demand"}}`
(including an intended valid `idleMinutes` when applicable). **Autoscale never uses a confirmation
Widget**: do not create, request, or wait for one. A normal successful response is the durable
write receipt; continue with the ordinary deployment-observation workflow below.

## Declaration, deployment, and current observations

A changed `hosting` domain starts a rolling redeploy for an already-published project; the old
version serves until the new one is ready. An unpublished project stores the declaration for
its first publish. A stored declaration alone does not establish that a redeploy succeeded.
The residency mode reaches a deployment when it is created, not by an already-running
container rereading configuration.

The owner's Dashboard hosting switch does not update the config document. Only a save that
actually changes the hosting domain projects that declaration; an unrelated config save does
not overwrite the owner's Dashboard choice with a stale hosting section.

`GET <config-plane>/infra/overview` exposes `atoms.hosting`:

| Field / value | Meaning |
| --- | --- |
| `declaredMode` | Requested mode in stored configuration. |
| `effectiveMode` | Live deployment's residency mode: `always_on`, `on_demand`, or `null`. |
| `reality: match` | Declared and effective modes agree. |
| `reality: always_on_pending_publish` | Declared always-on; observed deployment is on-demand. |
| `reality: on_demand_pending_publish` | Declared on-demand; observed deployment is always-on. |
| `reality: reality_unknown` | No effective-mode comparison is available. |
| `reality: not_declared` | No mode was declared. |

`effectiveMode: null` is unknown, not an on-demand default. It can occur before a successful
publish, during redeploy, or when deployment-state lookup fails. `effectiveMode: always_on`
reports the deployment's residency configuration, not instantaneous container liveness or
process survival. Neither mode is a guarantee for in-memory data; container persistence is
defined in [container publishing](build-contracts.md#container-build).

`idleMinutes` is enforced only on elastic placements. A non-elastic placement accepts the
declaration without applying an idle window; later placement changes can use the stored
value. Delivery of that setting is also environment-dependent, and the save receipt has no
field confirming the effective idle window. A returned stored number is the requested window,
not a measurement of sleep timing.

## Traffic and observability

Idle reclamation emits no dedicated shutdown log. A later waking request can create startup
output, but logs or a residency label do not establish whether the container is running now.
Any request to the published domain, including Dashboard reachability probes, affects idle
timing. Repeated probing can keep an on-demand deployment awake; an observation request is
not passive with respect to the state being observed.

Application boot identity and startup logs can distinguish process changes when the application
exposes that information. A process change alone does not uniquely identify idle reclamation;
deployments and other restarts can also replace the process.
The platform's available log fields and lifecycle coverage are in [diagnostics](diagnostics.md#production-logs).

## Selecting and applying the hosting policy

Read this contract before changing `resources` or `hosting`. Start from `GET config`, preserve the fields that are not changing, and use one domain write for the intended change. Do not declare container resources without a deploy contract. Omit a resource override when the platform's default size is appropriate; if overriding it, select one of the exact supported CPU/memory pairs rather than rounding an arbitrary request.

If the top resource tier was saved but publication is refused for membership, do not retry unrelated publishes: the stored tier still blocks them. Either use the owner's upgrade path or write a supported lower tier consistent with the requested capacity, then publish under that revised contract. Do not bypass the membership check or silently claim the rejected tier is active.

A hosting membership rejection is different: the rejected hosting write stored nothing. Stop repeating that write and report the required plan upgrade and the blocked setting. Direct the owner to Dashboard hosting settings, where the platform provides the upgrade path; ordinary on-demand hosting remains available. Do not work around an always-on or long-idle-window rejection with traffic generation.

Keep durable application state outside the process regardless of residency mode. Do not design a warm cache, in-process queue consumer or in-memory rate counter as the only durable record. Always-on reduces idle wakes; it does not guarantee process survival.

Do not assume an omitted `idleMinutes` means 720 minutes or any fixed environment default. A 30-minute window has been observed; treat that as a possible short idle window, not proof of the current setting. When exact sleep timing matters, measure the actual deployment and measure again after a placement or relevant hosting change. Do not use the saved idle number alone as the acceptance result.

## Accepting the deployed result

After the applicable deployment completes, read `GET infra/overview` and compare `atoms.hosting.declaredMode`, `effectiveMode`, and `reality`. Report a stored declaration separately from its observed deployed effect:

- `match`: the mode reached the observed deployment; do not resave the same mode to fix a cold start. Investigate the actual process behavior instead.
- `always_on_pending_publish`: the observed deployment is still on-demand. Complete the required publication through the applicable mode's publish path; rereading or resaving an unchanged declaration does not change a running deployment.
- `on_demand_pending_publish`: publish the intended on-demand contract when that change is required.
- `reality_unknown` or `effectiveMode: null`: report the observation as unknown and inspect the deployment outcome; never count it as agreement, on-demand, or proof that the process is alive.
- `not_declared`: there is no declared mode to verify; do not invent a residency claim.

A changed hosting save already starts a rolling redeploy on a published project. Do not issue repeated saves, a settlement loop, or another publish merely because that operation has not finished yet. Use its actual deployment outcome before choosing a recovery action. An unpublished project needs its first publish. Resource-tier changes instead take effect at the next publish.

Follow [Git checkpoints](git-checkpoints.md) for the Cloud/Local publication boundary; that contract also defines the user's automatic publishing authorization.

## Measuring idle behavior without keeping it awake

When sleep or a cold-start regression is the behavior under investigation, use a deliberate observation sequence rather than a polling loop:

1. Expose a cheap application endpoint with a process-start timestamp and a random boot ID created once per process. Record the current pair and deployed version.
2. Close the infra panel and stop or account for monitoring jobs, reachability checks, crawlers and other requests to every published domain. A quiet measurement is not quiet if a different domain or the Dashboard still generates traffic. Do not stop unrelated user work without the task's authorization; if it cannot be quieted, report that measurement limitation.
3. Leave a genuinely quiet interval appropriate to the timing being tested, then make one deliberate endpoint request. Read the console/startup logs around that request and compare the boot pair. The same pair identifies the same process; a changed pair plus a startup at the waking request is evidence to correlate with an idle wake.
4. Exclude intervening publication, restart or other process replacement before attributing a changed pair to idle reclamation. If those causes cannot be separated, report the ambiguity rather than claiming a measured sleep threshold.
5. Remember that this request restarts the idle clock. Do not repeatedly probe while waiting for the clock to expire; begin any subsequent measurement from its own last observed traffic.

The earlier infra-panel observation was a 3-second probe cadence that stopped after ten minutes without operator activity. Do not depend on that historical stop interval to create a quiet test: close or pause the prober and verify that it is not generating requests. Do not measure normal idle behavior while the panel is actively keeping the application warm.

Never build a keep-alive pinger to evade on-demand sleep. It can turn an idle-sleep deployment into a continuously billed one. If the product cannot tolerate cold starts, use the supported always-on choice and the owner's membership path, then verify its actual deployment state as above. Keep measurement and long-running traffic generation separate.

# On-Demand Architecture Assessment

Read this reference only when routing requires an architectural choice: an independent automation product, multiple users, custom interfaces or integrations, material scale or latency requirements, or runtime and durability constraints. Do not turn a straightforward personal automation into an architecture questionnaire.

## 1. Identify the deciding constraints

Reuse established requirements. Ask only for missing information that could change the mechanism, permissions, execution context, cost, or delivery behavior.

| Dimension | Determine | Routing consequence |
| --- | --- | --- |
| Ownership | One personal task, an existing application feature, or an independent product? | Prefer native Manus automation for a straightforward task; preserve application ownership for its backend work. |
| Detection | An unconditional time, incoming event, supported field predicate, cross-event correlation, or semantic judgment? | Discover native events and filters first. Do not assume deterministic filters support semantic classification or event-order correlation. |
| Execution | Deterministic operations, a bounded model call, or open-ended Agent work? | Separate condition detection from the work performed on a match. Invoke Manus where Agent capabilities are useful, not for every inexpensive check. |
| Frequency and scale | Resources monitored, detection cadence, matching-event volume, and acceptable delay? | Account for polling, batching, execution cost, and resource limits. Do not equate a detection tick with an Agent run. |
| Interface | Native controls, a custom dashboard, multi-user access, or a specialized approval workflow? | Use an application when its interface or ownership requirements justify one; adjustable thresholds alone do not. |
| Data and authorization | Required APIs, accounts, resources, and allowed side effects? | Verify access in the selected runtime. Do not assume interactive connector credentials transfer into a script or host. |
| Runtime and durability | Special packages, system tools, continuous processes, durable state, or particular network resources? | Consult available deployment guidance and verify current capabilities. Do not rely on historical platform limits or assume an always-on service requires a separate VM. |
| Delivery | Result destination, context continuity, and destination permissions? | Check delivery requirements before selecting a mechanism or host. Preserve the requested execution context. |

If one route clearly meets the requirements, choose it and proceed. If alternatives involve a material unresolved tradeoff, explain that tradeoff and ask only for the decision that determines the route.

## 2. Choose the execution model

| Model | Prefer for | Responsibility |
| --- | --- | --- |
| Deterministic code | Fetching, comparisons, transformations, and rule-based application actions | Own integration, state, deployment, and failure handling in the application. |
| Scoped model call | Classification, extraction, translation, or generation with bounded inputs and outputs | Verify model access, quality, cost, and failure behavior in the selected runtime. |
| Manus execution | Research, cross-tool work, open-ended analysis, or actions requiring Agent judgment | Use the selected automation mechanism to invoke the Agent with adequate context and permissions. |
| Hybrid | Inexpensive detection followed by selective Agent work, or application logic with bounded AI steps | Define detection, execution, state, and authorization responsibilities explicitly. |

Do not exclude Manus merely because part of a task is deterministic. A low-frequency personal task may reasonably prioritize simple setup. Conversely, do not route a purely programmatic application through Manus solely because it runs periodically or reacts to events.

For scoped AI steps, verify the selected runtime's actual model access and pricing. Explain material setup, cost, and quality tradeoffs before embedding a model. Do not assume that every host exposes the same models or credentials.

## 3. Apply the selected pattern

### Native Manus automation

Use ScheduleTask for ordinary time-based instructions unless the user explicitly selects another supported mechanism. For event- or condition-based Manus work, read `triggers` and use its current discovery flow to choose an event with supported filters or, when appropriate, a scheduled script. Define the work to perform separately from the condition that causes it.

Preserve the selected product's execution-context and lifecycle rules. Include the required inputs, output, destination, and failure behavior in the saved instruction. Supply sufficient context for a new-session target; do not rely on "do the same thing as before." Once an execution arrives at its selected target, perform the work there rather than creating another task to implement the target setting again.

If a ScheduleTask run executes a saved sandbox script, treat it as an Agent invocation, not an independent script scheduler. Verify file and state availability across runs. A resumed sandbox may preserve files, while reset, replacement, or expiry can invalidate that assumption. Use this pattern only when the work can tolerate a missed or delayed run caused by unavailable sandbox files or state. Otherwise, follow `persistent-computing` when available and select a scheduler or host that meets the required durability and timing guarantees.

### Application scheduling and event handlers

Use the application's scheduler or event handlers for its own backend work. Preserve existing WebDev ownership and follow current WebDev guidance for implementation. Add an interface for a user requirement, not merely because automation has configurable parameters.

Keep deterministic application work in code and add scoped model calls where justified. Evaluate hosting, dependencies, state, and service lifetime through available deployment tools and guidance. Read `persistent-computing` if it is enrolled and relevant; otherwise inspect the available runtime without inventing a Skill path or assuming deployment support.

Verify source and destination integrations in that runtime. Use supported authorization paths; do not assume connectors are universally available or unavailable outside Agent execution. Explain material new setup or maintenance requirements before committing to a different architecture.

### Custom host, with Manus API only when needed

Choose a custom host when the native mechanisms or suitable managed application environment cannot meet the requirements, or when the user explicitly requests an independent integration. Do not introduce one merely because an event should invoke Manus.

Let the host own event receipt or scheduled detection, bounded state, deduplication, and retries. Read `persistent-computing` for host selection and deployment when available; otherwise verify the selected host's capabilities through its available deployment tools and guidance. Read `manus-api` only if the design needs to invoke Manus through its API. Use documented completion or callback mechanisms where available, rather than an Agent-side polling loop.

Keep finite current-task scripts and jobs in the current task when no unattended service is required. Persisting a file does not keep its process online; use the selected scheduler or host for future execution.

## 4. Verify the architecture and hand off

| Concern | Required check |
| --- | --- |
| Cost | Separate detection, Agent execution, hosting, external API, and model charges. Do not equate "no Agent invocation" with "free." |
| Permissions | Ensure the user has authorized the intended unattended effects and their scope, including posting, emailing, purchasing, deleting, or modifying important external data. Do not automate effects outside that authorization. Reuse existing authorization within its scope; do not introduce extra gates for routine authorized work or bypass confirmations required by the selected tools. Never broaden accounts or export protected credentials to make a route work. |
| State and retries | Define initial baseline, cursors, duplicates, partial failures, and bounded retries where relevant. Do not advance checkpoints after incomplete reads or promise exactly-once delivery without a supporting guarantee. |
| Reliability | Match state durability, resource limits, and service lifetime to the required behavior. Treat unsupported latency or dependencies as design constraints. |
| Validation and observability | Distinguish configured, source-ready, matched, and delivered states. Use supported status and completion paths; do not substitute repeated Agent polling for a monitoring system. |

Return to the owning Skill or tools once the route is settled. Implement and verify the selected mechanism without repeatedly reopening resolved choices.

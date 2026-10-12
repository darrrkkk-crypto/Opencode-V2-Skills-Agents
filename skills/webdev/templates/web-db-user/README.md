# web-db-user template README

The default new Cloud Web starter is React/Express/tRPC/Drizzle. `webdev.init_project` accepts
`template: "web-db-user"` or `"flexible"`; use flexible for another stack or an existing Local
worktree. Local may explicitly select web-db-user for a new empty authorized Git worktree.
Template defaults remain editable within the same Resource; changing stacks does not require
another initialization.

## Prepared code and resources

Init copies the complete starter and installs its pinned dependencies for every resource choice.
With database selected, it also applies the checked-in users-table migration; otherwise it
neither fetches a database connection nor runs migrations. It does not start the dev process.

| Selected resources | Development command | Initial publish configuration |
| --- | --- | --- |
| Neither | `pnpm dev:static` | `pnpm build:static` after pinned installation; upload `dist/public` |
| Server only | `pnpm dev` | `Dockerfile` and `/api/health`; no managed database |
| Server and database | `pnpm dev` | Same Dockerfile plus database environment and completed base migration |

The static dev HTTP process is not a hosted Server resource. Unused backend/helper files remain
in the tree. The supplied persisted-user login requires both Server and database; public pages
need neither. Init performs no Stripe setup. Application roles live in the application's
database; the current visitor does not identify the site owner.

Port 3000, `Dockerfile`, and `/api/health` are editable initial defaults, not values to reapply
on attach or restart. For Local development, pass the Session port through the process environment;
do not commit it into project files.

## Supplied application structure

| Area | Supplied code |
| --- | --- |
| Frontend | React, Tailwind, routes in `client/src/App.tsx`, reusable components in `client/src/components/` |
| Backend | Express entry `server/_core/index.ts`, tRPC router `server/routers.ts`, request context and protected procedures under `server/_core/` |
| Database | Drizzle MySQL schema `drizzle/schema.ts`, queries in `server/db.ts`, migrations under `drizzle/` |
| Authentication | OAuth routes and SDK under `server/_core/`, client `useAuth` and `startLogin`; no simulated Preview login |
| Storage/services | `server/storage.ts` and optional `_core` helpers for LLM, images, voice, maps, notifications and scheduled work |
| Browser configuration | `/api/platform/config.js`: dynamic Express response, or static-build file served by Vite during static development; only named public values are exposed |
| Deployment | `Dockerfile` builds `dist/index.js` and `dist/public/`; `node dist/index.js` honors `PORT` |

Database-backed features connect schema, `server/db.ts`, tRPC procedures and UI. Add HTTP
handlers for platform callbacks or other HTTP requirements; tRPC does not prohibit them.
The supplied components do not require a dashboard layout.

## Other commands and pinned tooling

- `pnpm check`: types; `pnpm test`: application tests.
- `pnpm build` / `pnpm start`: build / serve production assets. Hosted Publish is the ordinary
  integration build; no per-task local Docker rehearsal is required.
- `pnpm db:migrate`: apply checked-in migrations. `pnpm db:push`: generate and apply new
  migrations after intentional schema edits, following the selected Database guide.
- pnpm is pinned to 10.18.0; reviewed dependency build permissions live in `pnpm-workspace.yaml`.

## Adding resources later

Declare both feature keys explicitly. Adding Server to untouched default static configuration
replaces the default static build declaration with the standard Dockerfile declaration.
Custom build/deploy settings stay as written; explicit static routes retain their static build.
Resource changes neither copy/overwrite application files nor restart the dev process.

Adding database provisions its connection through the existing environment mechanism, but does
not establish the application's schema. Inspect current schema/migrations and use `pnpm db:migrate`
for checked-in migrations, or the Database guide's schema-change workflow after business changes.
Init's base-migration receipt applies only to a database selected during init.

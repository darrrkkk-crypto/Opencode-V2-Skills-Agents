# Shopify

Read this page before choosing a stack or initializing a new Shopify storefront, and before enabling Shopify or writing storefront/Admin API code in an existing project.

## Enable the integration

1. Initialize or attach the WebDev project first. Shopify and Stripe are mutually exclusive per project.
2. Call `webdev.config` with `POST integrations/shopify/enable` and no body.
3. The response contains an `action_url` and pauses the agent. Stop and let the owner choose **Create a new store** or **Connect an existing store** in the card. Do not invent a store domain or bypass the card with a raw config write.
4. Resume only after the platform reports that Shopify is configured. Read `GET config` if the current state is unclear. The integration manages `SHOPIFY_STORE_DOMAIN` and `SHOPIFY_STOREFRONT_ACCESS_TOKEN`; never ask the user to enter or replace them.

The Storefront token is for storefront runtime use. Never put an Admin token in source code, project config, environment files, logs, chat, or tool arguments. The platform never returns an Admin token to you.

## Choose a server-rendered storefront first

For a new Shopify web storefront, build a server-rendered JavaScript application with a server-side cart unless the user explicitly requires a different architecture. Choose the SSR-capable stack before scaffolding, declare the required server capability through [features](features.md), and keep the published application server-backed. Do not build a client-only/static storefront first and then use that self-created incompatibility to skip Shopify's first-party primitives.

Before implementing the cart, read Shopify's [Cart overview](https://shopify.dev/docs/storefronts/headless/hydrogen/cart) and follow the [current Hydrogen API documentation](https://shopify.dev/docs/api/hydrogen) for the installed version. Use the official cart context/handler, forms, and cart-ID persistence where supported. Follow version-specific setup guidance; do not blindly copy older Remix setup examples into a newer Hydrogen project.

Once the server-rendered project is scaffolded, use Shopify's first-party preview SDK and Agent Skills:

```bash
npx @shopify/hydrogen@preview setup
```

Read the skills that setup installs before implementing storefront behavior. Prefer its Storefront client, cart, product, collection, money, analytics/consent, Shop Pay, redirects, predictive search, and customer-account primitives over hand-written equivalents. The preview requires a server-rendered JavaScript storefront, Node.js/npm, and Storefront API access.

In Manus, read these project skills from `.agents/skills/`. Shopify's setup also generates `.claude/skills/` for Claude Code compatibility; that is not a Manus skill directory. In a new Manus project, remove only the duplicate Hydrogen skill directories that this setup just generated under `.claude/skills/`, after verifying their counterparts exist under `.agents/skills/`. Preserve any pre-existing or user-maintained Claude configuration and skills.

For an existing project, preserve its framework and package manager. Use the same first-party workflow when compatible; if the existing architecture or an explicit user constraint prevents it, use the official [Storefront Cart API](https://shopify.dev/docs/storefronts/headless/building-with-the-storefront-api/cart) instead. Do not migrate an existing application merely to adopt Hydrogen without the user's agreement. This fallback is not the default for a new Shopify storefront.

Treat the preview as developer-preview software: inspect the generated diff, pin the installed package version in the lockfile, retain only behavior required by this project, and run the project's normal typecheck/tests. Do not copy an entire Hydrogen template over an existing app.

### Verify the embedded Preview cart

Manus Preview embeds the storefront cross-site. A cart cookie using `SameSite=Lax` can pass local or curl checks while failing to persist between requests in that iframe. Configure the server-side cart session for the public HTTPS Preview (`HttpOnly; Secure; SameSite=None; Path=/`), with partitioned cookies where supported when third-party cookies are blocked. Keep plain-HTTP local development working separately; do not infer the public request scheme solely from the app server's internal HTTP connection. Keep the framework's origin/CSRF protections when enabling cross-site cookies.

Test through the actual embedded Preview in a browser: add an item, change its quantity, reload, remove it, and follow the checkout handoff. Also check a standalone storefront visit; a partitioned Preview cart is not automatically shared with the standalone site's cookie jar. Curl cookie jars and checking `Set-Cookie` headers do not validate browser iframe policy. If the browser blocks persistence, report that limitation rather than declaring checkout verified.

For Hydrogen, load the installed version's required browser runtime (`ShopifyScripts` / Standard Actions) and verify cart actions after hydration. A working Storefront GraphQL call alone does not validate the product form or cart drawer.

## Development-store Admin work

`webdev.shopify` is listed only while this Resource uses an unclaimed development store. Use it for products, collections, inventory, files, themes, metaobjects, and other Admin GraphQL work needed to build the store. The development store intentionally uses the Vibe Code app's available Admin scopes; do not add a second client-side scope model.

For Admin work, call `webdev.shopify` with `action: "graphql"`, a complete `query`, optional `variables`, and optional `operationName`. Inspect both top-level `errors` and mutation payload `userErrors`; HTTP success does not imply GraphQL success. Keep input arrays at or below 250 items, keep each operation under Shopify's 1,000-point query-cost limit, inspect `extensions.cost.throttleStatus`, and retry throttling only with bounded backoff. Query the minimal fields needed.

After the owner claims the store, the Admin tool is removed and all pre-claim Admin credentials are invalidated by the platform. Do not retry it or ask for the old key. Tell the owner to open the side Widget panel, go to **Settings → Integrations → Shopify**, and choose **Add to Connectors**. Once the store is authorized in Connectors, select its account through the workflow below before using the Shopify Connector MCP tools.

### Demo products and images

When seeding a new store, if the user has not specified products, create **exactly 2 demo products**. If the user specified products, use that catalog instead of adding unsolicited demo products. Do not create extra products merely to populate filters, categories, or related-product sections. Reuse existing products on retries, and do not seed an existing connected store without the user's request.

**Every demo product must include an image attached to the Shopify product**, not just a frontend placeholder. Follow this sequence:

1. Reuse an appropriate user-provided product image, or generate one with the registered built-in image-generation tool, following its current model-selection contract. If generation is asynchronous, continue unrelated UI work until its completion result; a reserved URL is not ready for Shopify ingestion.
2. Obtain an absolute HTTP(S) image URL that Shopify can fetch without a Manus login. For a managed asset instead of a local file, use [storage](storage.md) to obtain an externally fetchable URL; do not assume a local file exists or pass a relative `/manus-storage/...` path to Shopify.
   For a local image, run `manus-upload-file <image-path>` **without `--webdev`** and use the returned public CDN URL. The `--webdev` result is an app-relative storage path, not a Shopify media source.
3. Through the currently authorized Shopify Admin tool, use [productCreate with media](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productCreate): pass `media` entries containing `originalSource`, `mediaContentType: "IMAGE"`, and descriptive `alt` text. Inspect GraphQL `errors` and mutation `userErrors`; do not make raw Admin HTTP calls.
4. Shopify processes media asynchronously. Continue UI work, then check media processing and confirm the image is returned by the Storefront API before declaring the demo catalog complete. If processing fails or remains pending, fix or report the image on the existing product rather than creating another product or silently delivering an image-less demo.

## Existing Connector store

Connecting an existing store does not expose Admin credentials to the WebDev Addon. Use Storefront configuration for the app and use the Shopify Connector MCP tools for Admin actions. Never fall back to a globally selected Shopify account when the Resource has a bound account.

Before using the Shopify Connector MCP tools, run `manus-config config load` and match the selected store to the loaded Shopify accounts. For a `shopify_configured` notification with `mode=connect`, use its `connectorUid` and `accountUid` to identify the selection; the notification does not switch accounts or grant authorization. For a claimed store without that payload, identify the account matching the project's store domain; ask the owner if the match is unclear. Use `manus-config config save` to set `activeAccountUid` to the matching account and complete any authorization required by the normal Connector flow. Continue only after the save succeeds; if permission or account selection is blocked, ask the owner instead of using the previous or default account. This configures the session's active Connector account, not WebDev project configuration.

## Claiming a new store

When the user asks to claim or take ownership of their store, call `webdev.shopify({"action":"get_claim_link"})`. Building, testing, delivering, or publishing a storefront is not a request to claim it; do not call this action automatically at those milestones. It uses the current website binding and accepts no other arguments. A `claimable` result displays a **Claim store** widget so the owner can finish setup and accept payments. Do not duplicate the card or wait for the owner to claim; finish your reply normally. Use the returned `claimUrl` only as a fallback if widgets are unavailable. Never invent a link, open it yourself, or claim the store for the owner. If already claimed, expired, or unavailable, explain the returned state rather than reusing an old link.

Claim is still available in **Settings → Integrations → Shopify**. After claim, direct the owner to **Add to Connectors**; continuing to use the development-store Admin tool is a bug. Keep the Storefront domain/config intact unless the owner connects a different store.

## Security and verification

- Do not make raw Shopify Admin HTTP calls; use `webdev.shopify` pre-claim or the Shopify Connector MCP post-claim/existing-store.
- Never print access tokens. Storefront values are injected by managed config and must not be copied into committed `.env` files.
- Inspect mutation `userErrors`; an HTTP success alone does not establish a successful Admin mutation.

# Owner notifications

This is a one-way operational notification to the Manus project owner. It uses the [shared runtime API contract](service-api.md#calling-the-platform-api-surface).

## Calling convention

`POST $MANUS_API_URL/webdevtoken.v1.WebDevService/SendNotification` (Connect RPC).

| JSON field | Contract |
| --- | --- |
| `title` | Plain text, at most 1200 characters |
| `content` | Plain text, at most 20000 characters |

## Delivery semantics

A successful 2xx response means the service accepted the notification. It is not evidence that the owner read it. Error responses do not establish acceptance.

## Boundary

The recipient is the project owner. This endpoint has no customer-recipient addressing contract and is not a customer email, order-confirmation, reminder, or campaign channel. An independently chosen provider can use [protected secret configuration](secrets.md); that does not make this endpoint a customer-email service.

## Application handling

Validate title/content lengths in the application before calling the service and reject oversized input rather than relying on an upstream validation error. Keep the owner's alert informative and compact.

A notification failure should degrade gracefully rather than crash the triggering form submission or workflow. Read the real failure reason; choose whether that event needs a durable Dashboard record or an already-configured alternate channel. Retry only when the error is transient. Do not classify every non-2xx as temporary, and do not route customer email through this owner-only channel.

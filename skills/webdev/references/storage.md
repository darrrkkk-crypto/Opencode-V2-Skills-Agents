# Assets and file storage

The platform provides durable object storage backed by presigned S3 uploads. Runtime API authentication is needed only for an upload/API call and is defined in [service API](service-api.md). A returned stable asset address can be used without reading that API contract.

## Runtime contract

| Request | Response and transfer |
| --- | --- |
| `GET $MANUS_API_URL/v1/storage/presign/put?path=<key>` | `{ "url": "…" }`; the returned URL accepts HTTP `PUT` of the object bytes and content type |
| `GET $MANUS_API_URL/v1/storage/presign/get?path=<key>` | `{ "url": "…" }`; a signed CDN download URL, valid for one hour |

Both calls use the runtime Bearer credential. `path` is required and must be ASCII. Missing/invalid authorization returns 401; an empty or non-ASCII path returns 400. Failures use an `error` string instead of `url`. This endpoint pair is registered when the platform's presign service is configured.

The signed download URL supplies an absolute, externally fetchable address for APIs such as [LLM multimodal input](llm.md#message-shapes). The relative `/manus-storage/<key>` address used inside a website is not itself such an input URL, and merely prefixing a private Preview origin does not establish that a model provider can fetch it. The temporary download URL does not replace the stable address retained in application data. Issuing a download URL does not prove that the object's bytes are already ready.

The runtime API has no listing or deletion operation. Storage holds bytes, not an application's file index or ownership records. Hiding an application record does not erase the stored object.

Project operators have separate config-plane list, presign, and delete operations requiring an owner-issued key with storage scopes. Runtime credentials do not grant that operator surface.

## Stable asset addresses

`/manus-storage/<key>` is a platform-owned stable project asset address, not a local file or
browser `blob:` URL. Stable Cloud Preview intercepts this reserved path before the application
listener; published sites also resolve it through the platform. The application does not need
its own storage proxy. A direct development-port request bypasses the stable Preview route and
cannot validate it. If an object
works after publication but Preview returns 502, inspect the platform's Preview storage
resolver; preserve the stable path instead of reuploading the object or substituting a temporary URL.

## Static publishes

A static deployment has no server process for authenticated runtime uploads. It can reference existing stable storage addresses. Assets included in the declared build output are a separate delivery mechanism.

## Generated image assets

An asynchronous Agent image-generation result returned as `/manus-storage/...` is the authoritative managed asset. That asynchronous result does not create a local file at the requested project path; the returned URL does not imply a corresponding repository file. It needs no download or second upload.

The runtime [ImageService](images.md) has a different output contract: its returned URL or base64 bytes are not a durable application asset. A stored object and its stable address exist only after those bytes have been transferred to project storage. A runtime result and an already-managed Agent asset are not interchangeable.

## Application storage practice

For user uploads, receive the request on a trusted server and validate the requesting user's authorization and upload size before obtaining an upload URL or accepting the bytes. Keep the server API key out of browser code. Add a random suffix to object keys that must not collide.

After upload, persist the object key and the application's ownership/product metadata in the database. Build file browsing, authorization, export and soft-delete behavior against that application index. Store and render the stable `/manus-storage/<key>` address. A soft-delete can hide an application record; do not promise physical removal through a runtime API that cannot perform it.

Keep large media out of Git; use durable object addresses. Small icons, manifests, robots and sitemap files may stay in the repository. Do not substitute local filesystem paths for browser assets.

For a runtime ImageService result that must become a durable application asset: decode `b64Json` or fetch its returned URL, upload the bytes under an application key, then persist the key/stable URL in the database and reference it from the application. This transfer procedure does not apply to an Agent result already returned as a managed `/manus-storage/...` asset.

Do not expose credentials or temporary signed URLs in the development agent's chat, reports, or logs. An application implementing the user's requested multimodal feature may send the signed download URL to the designated model service as that request's input. Keep that transfer scoped to the feature; do not replace it with a private Preview origin or relative path that the service cannot fetch. Temporary download addresses do not replace stable addresses in application records.

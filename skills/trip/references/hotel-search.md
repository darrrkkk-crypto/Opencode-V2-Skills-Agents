# `search_hotels` reference

The tool calls Trip.com's `POST /api/v1/products/hotels/query` (v2 contract). It sends the destination and stay, plus filters, sort and page only when supplied. The JSON Schema in `tools/list` lists every accepted value; this reference covers the semantics the schema cannot express.

## Destination and stay

| Argument | Required | Meaning |
|---|---:|---|
| `destinationType` | yes | `CITY` (whole city), `HOTEL` (a named hotel) or `POI` (near a place). |
| `cityName` | yes | The city containing the destination; results stay within it. |
| `countryName` | one of the two | Country or region of `cityName`, any language (e.g. `Japan`, `中国`, `Hong Kong`). |
| `countryCode` | one of the two | ISO two-letter code (e.g. `JP`, `CN`, `HK`) when no country name is passed; use `UK`, not `GB`. |
| `name` | `HOTEL`: yes; `POI`: recommended | The hotel name, or the place name that labels distance texts. Omit for `CITY`. |
| `latitude`, `longitude` | `POI` only | WGS84 decimal degrees of the place to stay near. |
| `checkIn`, `checkOut` | no | `YYYY-MM-DD`. Always pass both, using the user's local tomorrow and the following day when unspecified; the server-side fallback uses the server clock. |
| `roomCount` | no | 1 through 10; defaults to 1. |
| `adults` | no | 1 through 20; defaults to 2 and cannot be below `roomCount`. |
| `childAges` | no | Age of every child, 0 through 17; at most 20 children. |

Preserve the most specific resolvable place entity and derive its containing city separately. Never supply IDs or a title.

## Filters

All filters are optional; an omitted filter is not sent.

| Argument | Notes |
|---|---|
| `minPrice`, `maxPrice` | Non-negative; either bound may be used; minimum cannot exceed maximum. |
| `priceDisplay` | `NIGHTLY_BEFORE_TAX`, `NIGHTLY_WITH_TAX` or `STAY_TOTAL_WITH_TAX`; sets both the price filter and the shown price. Omitted, the tool uses the tax-inclusive stay total, or tax-inclusive per night when a budget is set. Pass `STAY_TOTAL_WITH_TAX` for a whole-stay budget and `NIGHTLY_BEFORE_TAX` only when the user asks for pre-tax prices. |
| `starLevels`, `superDiamond`, `hotelTypes` | Property class and type. |
| `paymentTypes` | `PAY_AT_HOTEL`, `PAY_ONLINE`, `FLASH_STAY`, `GIFT_CARD`. A pay-at-hotel filter does not establish whether a guarantee or deposit is required. |
| `hotelFacilities` | Every selected facility is required. |
| `roomFacilities`, `roomFeatures` | Room-level requirements, e.g. `NON_SMOKING`, `BATHTUB`, `SUITE`, `BALCONY`. |
| `bedroomCount` | `STUDIO_OR_ONE`, `TWO` or `THREE_OR_MORE`. Bed, bathroom and homestay-bedroom counts cannot be filtered. |
| `bedTypes` | `TWIN_BEDS` is a bed type, not a room count. |
| `meals` | Does not establish how many breakfasts a specific room rate includes. |
| `ratingThreshold` | `AT_LEAST_3` … `AT_LEAST_4_7`, `FIVE`. |
| `roomAreaMinSqm` | Positive square-metre value. |
| `openedOrRenovatedWithin` | `WITHIN_6_MONTHS`, `WITHIN_1_YEAR`, `WITHIN_2_YEARS`; opened **or** renovated within the period. |
| `distanceKm` | `0.5`, `1`, `2`, `4`, `8` or `10`; maximum distance from the coordinates; `POI` only. |
| `bookingPolicies` | `BOOKABLE`, `INSTANT_CONFIRMATION`, `FREE_CANCELLATION`, `EXCLUDE_HOURLY_ROOMS`. Free cancellation does not establish a deadline. |

Array filters do not share a universal AND/OR rule. Do not emulate unsupported combinations or silently remove conflicts. Brand is not supported.

The age filter is a combined **opened OR renovated** condition. If the user requires either one alone, explain the limitation and ask whether the combined condition is acceptable before applying it; do not silently broaden or drop their criterion.

## Sort and page

| Argument | Meaning |
|---|---|
| `sortBy` | `RECOMMENDED`, `PRICE`, `DISTANCE`, `POSITIVE_REVIEW`, `REVIEW_COUNT`, `INTELLIGENT`, `WALK_DRIVE_DISTANCE` or `STAR`. |
| `sortOrder` | Only for `PRICE` (`ASC` = cheapest first, the default, or `DESC`). Distance sorts (which need a `POI` destination) are always nearest first and the others best first. |
| `pageIndex` | Page number starting at 1; omit for the first page. |
| `pageSize` | 1 through 20; defaults to 5. Keep the same size when fetching more pages. |

Omit both sort arguments when the user did not request an order.

## Result mapping

| Trip API source | Deal field |
|---|---|
| `name.display`, then `name.local` or `name.english` | `title` |
| `actions.targetLink` | `deeplink`, preferring online, then H5, then app |
| `star.value`, `star.type` | `star`, `star_type` |
| `rating.score`, `rating.fullScore`, `rating.level`, `rating.reviewCount` | `rating`, `rating_scale`, `rating_label`, `review_count` |
| `location.address`, `location.cityName`, `location.relativePosition.text` | `address`, `destination_city`, `relative_position` |
| `availability.status`, `availability.scarcityText` | `availability_status`, `availability_text` |
| `price.currency`, `price.displayPrice`, `price.originalPrice` | `price.currency`, `price.display_price`, `price.original_price` |
| Positive difference of the same hotel's original and display price | `price.savings_amount` |
| First readable `labels` entry with `kind: PROMOTION` | `promotion_label` |
| numeric `discount` ratio | `discount.ratio`, plus `discount.percent = ratio * 100` |

Hotel order is preserved. Hotels without a discount or original price remain in the result. The API's `originalPrice: 0` sentinel is omitted. Observed `star.type` values include `STAR`, `DIAMOND` and provider-specific `DOT`; do not reinterpret `DOT` as stars or diamonds.

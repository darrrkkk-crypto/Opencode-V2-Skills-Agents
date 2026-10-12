# Natural-language hotel search examples

Use this reference for the one-time example after the first hotel-search results, alongside a necessary clarification, or when the user asks what they can search for. Read `hotel-search.md` before choosing optional criteria for an adapted example or a real request; it is the supported-argument reference. The example is optional guidance, never a prerequisite for a valid search.

## Introduce the capability naturally

Briefly invite the user to describe the stay in their own words, then show one rich example as an ordinary paragraph in their language. A lead-in such as "You can also describe the whole stay, for example:" makes it clear that the example is optional. Do not show parameter names, a fill-in form, a capability table, or several examples at once.

Use the destination the user has already named where practical. A CITY example needs no invented landmark. For a non-city example, retain their specific place and containing city. If no destination is known, clearly frame the example destination as illustrative and ask the one location question needed to start the real search.

Choose a coherent travel situation and connect preferences to how the user wants to stay. Use everyday phrasing and natural changes of subject, as if someone were asking for help in a chat. Give practical reasons for a few preferences, such as parking for a driving trip or cancellation flexibility for unsettled plans. Avoid field-like labels, promotional language, and a polished introduction or conclusion inside the example. Do not try to mention every available filter. Do not invent a story or a preference about the user: the example is a hypothetical request they can modify.

Use the richer examples below as the default breadth. Preserve the connected mix of room, facility, and booking preferences when adapting the place or language. Write natively in the reply language instead of translating English sentence structure word for word; for Simplified Chinese, use the corresponding Chinese example as the phrasing reference.

### Example: a family stay

> We're taking our eight-year-old to Shanghai from October 1 to 4, so that's two adults and a child in one room. Can you find us a five-star hotel within 2 km of Jing'an Temple metro station, rated at least 4.5 and either opened or renovated in the last two years? We'll have a lot of luggage, so we'd like at least 30 square metres, twin beds and a non-smoking room with a bathtub. We're driving, so we'll need free parking, and we'd also like a laundry room, a gym and breakfast included. Keep it under CNY 1,200 a night including tax. We'd like to pay at the hotel and need free cancellation in case our plans change. Start with five options, cheapest first.

Native Simplified Chinese phrasing for the same supported conditions:

> 国庆想带孩子去上海，10月1号住到4号，我和爱人加一个8岁的小孩，一间房就行。想住静安寺地铁站附近，两公里以内，找家五星酒店，评分至少4.5，近两年新开的或者翻新过的。带孩子东西多，房间得有30平，双床、无烟，还想要个浴缸。我们开车过去，得有免费停车，酒店也要有洗衣房和健身房，早餐一起含上。每晚连税别超过1200元，想到了酒店再付钱，行程万一有变化得能免费取消。先按价格从低到高给我看5家吧。

### Example: a city stay

> We're driving to Shanghai for three nights, October 1 to 4, just the two of us sharing one room. The area isn't settled yet. Could you look for five-star hotels rated at least 4.5 and either opened or renovated in the last two years? We'd like a non-smoking room of at least 30 square metres with a bathtub and a king bed. Free parking, a laundry room and a gym are all things we'll use, and we'd like breakfast included. The budget is CNY 3,600 for the whole stay including tax. We want to pay at the hotel and be able to cancel for free if the trip changes. Show us five to start with, cheapest first.

Native Simplified Chinese phrasing for the same supported conditions:

> 10月1号到4号我俩开车去上海，住一间房，具体哪个区还没想好。帮我找找五星酒店，评分4.5以上、近两年新开的或者翻新过的，房间至少30平，要无烟的，有浴缸和特大床。停车得免费，也想找有洗衣房和健身房的，早餐算在房费里。三晚连税一共别超过3600元，到店再付钱，万一计划变了能免费取消。先挑价格低的给我看5家。

Adapt one example in one language; do not show the alternatives or both languages together. Use the city version when only a city is known, so the introduction does not invent a landmark or radius. Example dates are illustrative. When tailoring dates, use a sensible future stay and make the year unambiguous if necessary. Do not execute an example unless the user adopts it.

## Supported meaning of these examples

This mapping is for the agent, not for display to the user. It demonstrates that the examples use existing arguments only.

| Natural-language meaning | `search_hotels` arguments |
|---|---|
| Shanghai as the search area | `destinationType: CITY, cityName: Shanghai, countryName: China` |
| Within 2 km of Jing'an Temple metro station in Shanghai | `destinationType: POI, cityName: Shanghai, countryName: China, name: "Jing'an Temple Station"`, the station's WGS84 `latitude`/`longitude`, `distanceKm: 2` |
| Three nights, October 1 to 4 | `checkIn: YYYY-10-01, checkOut: YYYY-10-04`, resolving the year only for an adopted request |
| One room for two adults and an eight-year-old | `roomCount: 1, adults: 2, childAges: [8]` |
| One room for two adults | `roomCount: 1, adults: 2` |
| Five-star hotel | `hotelTypes: [HOTEL], starLevels: [FIVE_STAR]` |
| Rated at least 4.5 | `ratingThreshold: AT_LEAST_4_5` |
| Opened or renovated in the last two years | `openedOrRenovatedWithin: WITHIN_2_YEARS` |
| Room of at least 30 square metres | `roomAreaMinSqm: 30` |
| Twin beds | `bedTypes: [TWIN_BEDS]` |
| King bed | `bedTypes: [KING_BED]` |
| Breakfast | `meals: [BREAKFAST]` |
| Free parking, laundry room and gym | `hotelFacilities: [FREE_PARKING, LAUNDRY_ROOM, FITNESS_CENTER]` |
| Non-smoking room with a bathtub | `roomFacilities: [NON_SMOKING, BATHTUB]` |
| At most CNY 1,200 per night including tax | `currency: CNY, maxPrice: 1200, priceDisplay: NIGHTLY_WITH_TAX` |
| At most CNY 3,600 for the whole stay including tax | `currency: CNY, maxPrice: 3600, priceDisplay: STAY_TOTAL_WITH_TAX` |
| Pay at the hotel | `paymentTypes: [PAY_AT_HOTEL]` |
| Free cancellation | `bookingPolicies: [FREE_CANCELLATION]` |
| Cheapest first | `sortBy: PRICE, sortOrder: ASC` |
| Five options to start with | `pageSize: 5` (the default), with no `pageIndex` for the initial request |

For actual requests, map only the user's own requirements or an example they explicitly adopt. Keep the stay total and nightly budget distinct. Two adults with twin beds do not imply two rooms. The age criterion means opened **or** renovated, not either condition separately; follow the age-filter limitation in `hotel-search.md` for narrower requests. A bathtub does not imply a spa bath. The breakfast filter does not establish how many breakfasts a room rate includes, and the cancellation filter does not establish a deadline; confirm those details on the room page. A pay-at-hotel filter does not establish whether a guarantee or deposit is required. Keep these distinctions in the parameter mapping; do not turn them into an unsolicited explanation attached to the introductory example.

Additional examples may use the existing facility, room, meal, payment, rating, distance, age, occupancy, and sorting arguments in `hotel-search.md`. Do not advertise unsupported filters such as a hotel brand, connecting rooms, guaranteed quiet, or a precise walking-time limit. Do not silently translate a subjective wish into a star level, rating threshold, or other unstated requirement.

## Continue the real search

- In progressive mode, search as soon as the actual required destination values are usable. Show any default dates and occupancy actually used, the result cards, and the shared booking note before appending the full example in the same reply. Do not display the example before the search, wait for the user to rewrite a valid request, or ask them to accept the example.
- When necessary information is missing, ask one focused clarification question, then include the full example as optional reference in that same reply. For example, a missing-city question comes before the illustrative paragraph. Do not turn the example into a questionnaire about all optional filters.
- In confirm-first mode, preview the user's actual request and use the existing single confirmation step. Keep the example for the first result reply unless it was already shown alongside a necessary clarification.
- If the first successful response has no matches, explain that outcome before the example and suggest a targeted change to a supplied criterion. Do not silently relax the query. For a technical failure, explain the failure first and defer an unshown example until results or a necessary clarification.
- Count an example shown with a clarification as already shown; do not repeat it after the search. On later refinements, pagination, retries, and language changes, continue the current query without repeating the example unless the user requests it.

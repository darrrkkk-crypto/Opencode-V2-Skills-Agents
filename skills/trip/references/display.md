# Compact deal cards

Use these presentation rules with the product template in `SKILL.md`. Template placeholders are display fragments, not additional result fields. Render the cards as normal response content, not inside a code fence.

## Layout and emphasis

- Use one compact card per deal, normally two to four logical lines, with one blank line between cards. Long titles and addresses may wrap naturally; preserve them rather than truncating them to meet a line count.
- Unless the product template specifies separate lines, group the current price, reference price, offer, and savings on one logical line immediately after the product title or carrier. Follow the template's emphasis; by default, bold the current price, offer, savings, and title when present, keeping reference prices and supporting facts in normal weight.
- Keep the detail link on the line specified by the product template, normally the price line. If the product has no displayed price, keep a standalone detail link as the last line.
- Use the complete returned `deeplink` verbatim, including `allianceid`, `sid`, and all other query parameters. Do not rebuild, shorten, or strip parameters from the URL.
- Follow the product's field set and order. Omit empty optional fragments, their icons, and adjacent separators. Do not add a table, image, box border, horizontal rule, nested list, or a repeated heading for each card.
- Preserve the returned result order and returned titles. Do not select only discounted results or sort again to make an offer appear stronger.

## Offers and savings

Resolve `{discount_summary}` using the product-specific rule in `SKILL.md`:

- Prefer a returned discount. Otherwise use an explicitly supported promotion label, preserving its text and any eligibility conditions. Display it as a promotion, not a numerical discount. Never invent promotional wording or use internal codes, recent-order messages, cabin classes, or amenities as offers.
- If neither is present, omit the offer, icon, and adjacent separator without a missing-discount label, placeholder, or explanation. Keep the product and price.
- `{savings_summary}` uses only the returned positive `price.savings_amount` for hotels or `savings_amount` for other products, in that deal's currency. Express it as saving that amount against the displayed reference price. Omit it when absent; do not calculate savings or discounts yourself, multiply by nights, rooms, or passengers, or add separate promotions together.
- Label the comparison price as a displayed reference/struck-through price, not a historical, usual, market-wide, or guaranteed booking price. Never claim "best", "lowest", or "exclusive" beyond the evidence or inflate a small discount into a major offer.
- Translate labels and supporting prose into the user's language. Preserve returned discount and promotion text; hotel percentage discounts are formatted from the numeric value as described in the hotel section of `SKILL.md`.

## One useful selection sentence

Before the cards, add at most one short sentence highlighting up to two useful choices from this response, grounded in returned prices, explicit discounts, ratings/review counts, or location. Keep the cards and their order intact. Skip the sentence for a single result, no meaningful distinction, or a user requesting cards only.

Scope comparisons to these returned options, never the whole destination or market. Compare prices only within the same currency, price basis, and relevant stay or itinerary conditions; a lower price is not proof of better overall value. Compare numerical discounts only when their meanings are unambiguous; promotion labels do not establish discount strength. Use only supported product facts and bookable results, respect the user's priorities, and do not imply unreturned room amenities or rate terms from query filters alone. Do not make extra searches to produce this sentence.

## Desktop and TUI

Use the same information hierarchy in both environments. Adapt formatting to the known output channel, not to a guessed application name.

- In chat or Markdown, including a TUI that renders Markdown, use the template's `**emphasis**`, `~~reference price~~`, and clickable `[{view_details_label}]({deeplink})`. Preserve the lines within a card with Markdown hard breaks (two trailing spaces); use one blank line between cards. Do not output a plain-text link label without its destination. Do not wrap a Markdown link inside backticks. If strikethrough is unsupported, remove its markers and retain the reference-price label.
- In a known plain-text terminal, remove Markdown emphasis and strikethrough markers, retain the reference-price label, and use `Offer:` / `Price:` in place of icons if Unicode is unsupported. Print the details label followed by the full URL. Let long lines wrap, or break at a fragment boundary before the link; do not align columns with spaces.
- Use an OSC 8 hyperlink only when the output channel is explicitly known to support it. Do not infer OSC 8 support only from `TERM` or `TERM_PROGRAM`. No terminal escape sequences or forced colors belong in chat output.
- If channel capabilities are unknown, use the Markdown version. Compactness must never hide the destination URL or remove factual fields required by the product template.

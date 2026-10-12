# manus-pptx XML Syntax Reference
Complete syntax reference for pptx-mode Slides decks. Read this file BEFORE writing `design.xml` or any `<slide_id>.xml`. Every `.xml` write/edit is checked by the Slides file-edit hook, and `slides/present` re-validates every file before delivery. **This document is self-contained**: every tag, attribute, value syntax, and validation rule you need is here — no other document required. Tags/attributes not written here do not exist; do not invent them.

A pptx deck consists of:

- `design.xml` — ONE deck-level design file defining the canvas size and the deck's shared color/font variables. Write it FIRST, before any slide.
- `<slide_id>.xml` — one file per registered slide, directly in the project directory (no subdirectories). One slide = one `<slide>`, composed of 6 element types: `<text>` `<shape>` `<image>` `<icon>` `<table>` `<chart>`. The `slide_id` must match an id registered in the `slides/init_slides` outline.

## Authoring procedure
- Write `<project_dir>/design.xml` FIRST, then each registered `<project_dir>/<id>.xml` with the native file `write` tool — one call with one complete XML document per page; use the `edit` tool for targeted follow-up fixes. NEVER write these files via shell commands or Python/Node scripts, and never emit several pages from one call: such writes bypass the file-edit hook, so the deck never registers that content — a page never written through the file tools stays `edit_pending` and blocks `slides/present`. All files go directly in the project directory — no subdirectories.
- `design` is a reserved slide id; it names the deck-level design file and cannot be used as a slide in the outline.
- Each `.xml` write/edit is validated. Validation failures do not block the write but MUST be fixed before `slides/present`, which re-validates every file before delivery. Some rules in this document are only checked at render/export time — treat every rule here as binding whether or not the hook flags it.

## Global rules (apply to every file)
- Write raw XML markup. Output the document directly; do NOT wrap it in Markdown code fences and do NOT entity-encode the whole document.
- **Escaping — read carefully.** ONLY escape literal `<` `>` `&` that appear as VISIBLE TEXT inside `<text>` content (e.g. write the words "5 < 10" as `5 &lt; 10`). NEVER escape the markup tags themselves — the document structure MUST be raw `<`/`>`.
  - Correct: `<text ...><p>5 &lt; 10</p></text>`
  - WRONG (do not do this): `&lt;text&gt;&lt;p&gt;5 &lt; 10&lt;/p&gt;&lt;/text&gt;`
- The canvas is fixed at **1280x720 px**. Unit is px, numbers carry no unit suffix (`x="120"`), decimals allowed; origin is top-left, `rotation` is clockwise degrees. For every element `x + width <= 1280` and `y + height <= 720` (line-type shapes with negative width/height are the one exception — see `<shape>`).
- **Separators**: arrays (lists of same-kind items) use commas `columns="2,5,3"`; compound values (components with different meanings) use spaces `padding="10 14"`.
- **No global fallback, fail-fast**: missing required fields or unresolvable variable names are validation errors, never silently degraded. Required list: one `<background>` child per slide, `font` for `text`/`table`/`chart`, `height` for `table`, `fill` for area-type shapes, a color for every chart series, `name` for `icon`, `src` for `image`, `type` for `shape`/`chart`.
- **Writing order = stacking order**: later elements sit on top of earlier ones.
- **`id` short and preferably semantic**: purpose/content understandable at a glance (e.g. `cover-title`, `revenue-chart`), for locating during incremental edits and for `<a slide>` jumps; don't use meaningless `e1` or random strings.
- When a parameter is meaningless to its host (e.g. `fill` on a line, `y-axis` on a pie), it is ignored if written.
- Attribute values are always quoted (`attr="value"`). Attributes are written kebab-case (e.g. `line-height`, `corner-radius`, `data-labels`).
- Image `src` MUST be an absolute local path (e.g. `/home/user/project/assets/photo.png` or `C:/Users/me/project/assets/photo.png`) or an HTTP(S) URL. Relative paths are not supported.
- Do NOT use python-pptx, OpenXML SDK, or any other library to create or edit `.pptx` files, and do NOT write the `.xml` files through shell or scripts. The XML files ARE the deck, authored ONLY with the native file `write`/`edit` tools.

## Color and fill values
**Color** is one of two: a hex literal `#1A2B3C` (optionally 8-digit with alpha `#1A2B3C80` for semi-transparency), or a variable name defined in `<design>` such as `brand` (leading `#` means literal, otherwise looked up in the variable table; variables carry no alpha, so for semi-transparency write an 8-digit hex directly). Prefer variables for deck consistency.

**Fill** has three forms (used for slide background, text box background, shape fill; table accepts solid color only). Solid color is written directly as a `fill` attribute on shape/text/table; the slide background is a `<background>` child element (see the `<slide>` section):

```xml
<shape fill="#1A2B3C" .../>  <!-- 1. Solid: written directly as an attribute -->
<background color="brand"/>  <!-- Solid form of slide background (type defaults to solid) -->
<background type="gradient" direction="135">  <!-- 2. Gradient: direction angle, 0=left-to-right clockwise, default 0; at least 2 stops; linear only, no radial -->
  <stop offset="0%" color="#0F2027"/>
  <stop offset="100%" color="#2C5364"/>
</background>
<background type="image" src="/abs/path/bg.jpg" fit="cover" overlay="#000000" overlay-opacity="0.4"/>  <!-- 3. Image: fit also supports contain/stretch/tile; always add an overlay to darken when placing text over an image -->
<background type="image" src="/abs/path/bg.jpg" fit="cover">  <!-- 3b. Gradient overlay: <overlay> child, same syntax as gradient, stops use 8-digit hex with alpha (clear at top -> darker at bottom); attribute and child are two forms of the same thing, child wins -->
  <overlay direction="90">
    <stop offset="0%" color="#0F172A10"/>
    <stop offset="100%" color="#0F172AF0"/>
  </overlay>
</background>
```

## Common parameters (inherited by all 6 elements)
```
id?         unique element identifier (for locating during incremental edits)
x y         top-left position, px (default 0)
width height  size, px (default 0 — always set them explicitly; table's height is required, as the authoritative total height)
rotation    rotation angle, default 0 (table/chart unsupported, ignored if written)
opacity     0~1, default 1, overall opacity (fill/stroke/text change together; not yet effective on chart)
```
`shadow` applies to text/shape/image/icon: `shadow="true"` gives the default shadow (4px straight below, blur 12, black 35%), fine-tunable via `shadow-x / shadow-y / shadow-blur / shadow-color / shadow-opacity`.

## `<design>` — deck-level design file (design.xml)
Exactly one `<design>` root element. Its children are only `<size>`, `<color>`, and `<font>` — all EMPTY elements (self-closing `<size .../>` or immediately closed `<size ...></size>`; child content is never allowed). No text content is allowed inside `<design>`.

```xml
<design>
  <size width="1280" height="720"/>
  <color name="brand" value="#1A5276"/>
  <color name="accent" value="#E67E22"/>
  <color name="ink" value="#1B1B1B"/>
  <color name="paper" value="#FFFFFF"/>
  <font name="heading" family="Montserrat" size="32"/>
  <font name="body" family="Inter" size="18"/>
</design>
```

Rules:

- `<size width height>` — exactly one, both attributes required, positive px numbers. This deck's canvas is fixed at **1280x720**; the hook enforces/injects this authoritative size, so always write `width="1280" height="720"`.
- `<color name value>` — at least one. `value` is `#RRGGBB` only (variables carry no alpha; where you need semi-transparency, write an 8-digit hex literal at the point of use).
- `<font name family size>` — at least one. Font-family + font-size binding, both required; `family` must be a font listed in Google Fonts (e.g. Noto Sans SC / Inter), a SINGLE font name — no comma fallback list. `size` is the default px size, positive number.
- Variable `name`s: lowercase letter first, then lowercase letters, digits, hyphens (e.g. `brand`, `bg-dark`). `none`, `true`, and `false` are reserved words and cannot be used as names. Duplicate definitions are illegal; variables cannot reference variables.
- `<color>` and `<font>` are two independent namespaces; names must be unique within each.
- Reference by bare name: `fill="brand"`, `font="heading"`. Font variables carry their own size; an explicit sibling `size` overrides it. Literal fonts (`font="Inter"`; any uppercase/CJK character makes it a literal) set only the font-family, and must likewise be a single Google Fonts name.
- Numbers are plain decimal literals (`18`, `18.5`); scientific/hex notation and stray whitespace are rejected.
- Optional root attributes `lang` (BCP 47 language tag) and `dir` (`ltr|rtl`): write `<design lang="ar" dir="rtl">` for Arabic decks only — `dir="rtl"` requires an Arabic `lang`. Omit both for all other decks. `lang` doubles as the document language for exports (proofing/typography); direction overrides below carry it locally.

## `<slide>` — page container
```
id?             page identifier (also the target of <a slide="..."> intra-deck jumps)
<background>!   a child tag written as a sibling of text and other elements (NOT a slide attribute), required exactly once per slide; write it first by convention (position is free — it always renders as the bottom-most layer and never participates in content stacking); a white background must also be explicit: <background color="#FFFFFF"/>
content elements 0..n    text/shape/image/icon/table/chart, writing order is stacking order (later on top)
```
No other tags and no bare text are allowed directly inside `<slide>`.

```xml
<slide id="cover">
  <background color="paper"/>
  <shape type="rect" x="0" y="0" width="1280" height="120" fill="brand"/>
  <text x="60" y="30" width="900" height="60" font="heading" size="40" color="paper">Quarterly Review</text>
  <text x="60" y="160" width="560" height="480" font="body">
    <p><strong>Revenue</strong> grew 18% year over year.</p>
    <ul>
      <li>APAC up <span color="accent">32%</span></li>
      <li>EMEA up 11%</li>
    </ul>
  </text>
  <image x="680" y="160" width="540" height="480" src="/home/user/deck/assets/chart.png" fit="cover"/>
</slide>
```

## `<text>` — text (titles, body, lists all use it)
Container attributes:

```
font!    font variable or literal (variable carries its own size)
size     px; overrides the variable size when written explicitly; defaults to 18 for a literal font when unset
color    default #000000        align    left|center|right|justify, default follows dir (ltr→left, rtl→right)
line-height  multiplier, default 1.2   anchor   top|middle|bottom vertical alignment, default top
padding  1/2/4 px values (CSS order), default 0
autofit  none|shrink, default none (shrink recommended for long text boxes: auto-reduces font size when content overflows)
wrap     true|false, default true (false = no wrapping, single-line overflow)
writing-mode  horizontal|vertical, default horizontal (vertical = East Asian vertical layout, see below)
fill     box background (solid color, or one <fill> child for gradient/image box fills)   shadow
```
Content is one of two forms, NEVER mixed: **clean text** (may contain inline tags, treated as a single paragraph) or **all block-level tags**; mixing them is illegal.

- Block-level: `<p>`, `<ul>` (`bullet` allows a custom single-character symbol, default •, inherited from parent when a child omits it), `<ol>` (numbering 1. 2. 3. only), `<li>`; nest `<ul>/<ol>` inside `<li>` for multi-level lists (at most one nested list per `<li>`), up to 5 levels.
- Inline: `<strong>`(bold) `<em>`(italic) `<u>` `<s>` `<sup>`(superscript) `<sub>`(subscript) `<span>`(pure attribute holder) `<a>`(hyperlink), all can carry `font/size/color/highlight` (highlight = text background highlight color), and can nest within each other (max depth 20). **`<b>` and `<i>` are not supported**, only the semantic forms; `<sup>/<sub>` are for `H<sub>2</sub>O`, `x<sup>2</sup>`, etc.
- `<a>` hyperlink: `href` (external URL) and `slide` (target page id) are **mutually exclusive, exactly one required**; referencing a nonexistent slide id is an error; **no automatic underline/link color** (for the traditional look, nest `<u>` or add `color` yourself); an `<a>` may not nest another `<a>`, and may not contain block-level tags.
- Vertical `writing-mode="vertical"`: characters upright, top-to-bottom within a column, columns right-to-left (Chinese/Japanese covers/poetry). `align`/`anchor` value names are unchanged, but their axes rotate 90° with the text (align controls vertical position within a column, anchor controls overall horizontal position, top = toward the right-most first column). Rotating Latin text 90° is not vertical layout — use `rotation`.
- `font/size/color/align/line-height` can be written on the container/`<p>`/`<li>`/inline and override level by level (field-level merge).
- `<p>`/`<li>` also have `space-before`/`space-after` (default 0).

### Reading direction & language (RTL / mixed decks)
- `dir` (`ltr|rtl`) is accepted on `<text>`, `<table>`, `<p>` and `<li>`, plus inline `<span dir>` — nowhere else. Nearest declaration wins: `<design dir>` → element → block → span. Write it when a whole box/paragraph/item reads opposite to the deck, e.g. an English card in an Arabic deck (`<text dir="ltr">`) or one Arabic paragraph in an English box (`<p dir="rtl">`). `dir` flips the writing direction, the DEFAULT alignment, and (on `<table>`) the visual column order; an explicit `align` is always physical (`align="right"` = right edge regardless of `dir`).
- Bare foreign WORDS (a brand name, an English term in an Arabic sentence) need no markup — the bidi algorithm places them. But a weak-direction SEQUENCE of Latin letters / ASCII digits whose internal order must not change — phone (`+966 11 234 5678`), version, date, score, formula, value+unit — or any Latin phrase carrying paired brackets or neutral separators (`(` `)`, `/`, `·`) — MUST be ONE `<span dir="ltr">` island inside an RTL paragraph (mirror with `<span dir="rtl">` in LTR), brackets and separators INSIDE the span (`<span dir="ltr">(SQL / NoSQL)</span>`); splitting one phrase into adjacent islands reorders them and mirrors the brackets. An island holds ONLY weak or opposite-script content: never wrap RTL-letter text in `<span dir="ltr">`, nor Latin-letter text in `<span dir="rtl">`.
- `lang` (BCP 47): on `<text>`/`<table>`/`<p>`/`<li>` only, and only when direction cannot imply the language (an Arabic quote in an LTR deck: `<text dir="rtl" lang="ar">`; a French passage in an Arabic deck: `<p dir="ltr" lang="fr">`); otherwise omit — a `dir` override already switches the local language context. Do NOT echo the same fact in two languages on one line; lead with one language, parenthesize or line-break the other.
- **Not available**: `<br>` (use multiple `<p>`), `<h1>~<h6>` (a heading is just large-size text), `letter-spacing`, columns, first-line indent.
- Set `wrap="false"` on any `<text>` expected to render as a single line; unexpected line breaks are common once font size exceeds 44px.

```xml
<text x="80" y="200" width="560" height="300" font="body" line-height="1.4">
  <p font="heading" size="24">Q3 Highlights</p>
  <ul bullet="✓">
    <li>Revenue up <strong color="brand">45%</strong></li>
    <li>See the <a href="https://example.com/report"><u>annual report</u></a></li>
  </ul>
  <p><a slide="chapter-1" color="brand">01 Market Review →</a></p>
</text>
```

## `<shape>` — geometric shapes (cards, color blocks, dividers, connectors, flowchart shapes)
```
type!    rect ellipse line elbow curve arrow chevron diamond triangle parallelogram trapezoid pentagon hexagon star —— the 14 common ones; all 187 OOXML preset names may be used by their original name (e.g. cloud)
fill     required for area types (solid color, one <fill> child, or "none" — a transparent background must be explicitly "none"); ignored for line types
stroke   stroke color; stroke-width default 1. Line types have a stroke by default (#000000/1px), area types have none by default
stroke-dash    solid|dash|dot, default solid, applies to all types (dashed dividers / helper boxes)
corner-radius  effective on rect only, px
arrow-start / arrow-end   none|arrow, effective on line types (line/elbow/curve) only
head-ratio     0~1, default 0.5, effective on arrow/chevron only: head depth ratio, use a small value (e.g. 0.3) for flat/long arrows
shadow
```
Line types (`line`/`elbow`/`curve`) share two-endpoint positioning: drawn from `(x,y)` to `(x+width, y+height)`; horizontal line `height="0"`, vertical line `width="0"`, width/height may be negative to express leftward/upward. `line` is straight, `elbow` is an L-shaped bend, `curve` is an S-shaped curve (bend point not adjustable; for a special bend, stitch multiple `line`s). Connector endpoints align by coordinate and do not snap to shapes.

**Shapes hold no text** — for text on a shape, overlay a `<text>` at the same coordinates (`align="center" anchor="middle"`).

```xml
<!-- Card + text on the card -->
<shape type="rect" x="80" y="160" width="340" height="200" corner-radius="12" fill="#FFFFFF" shadow="true"/>
<text x="80" y="160" width="340" height="200" font="body" align="center" anchor="middle">Text overlaid at same coordinates</text>

<!-- Decorative line / flow arrow / L-shaped connector / dashed helper box -->
<shape type="line" x="80" y="130" width="120" height="0" stroke="brand" stroke-width="3"/>
<shape type="elbow" x="420" y="220" width="200" height="160" arrow-end="arrow"/>
<shape type="rect" x="700" y="120" width="300" height="180" fill="none" stroke="#999999" stroke-dash="dot"/>
```

## `<image>` — image
```
src!     absolute local path (POSIX or Windows drive-absolute) or HTTP(S) URL (a relative path like ./assets/x.png is a validation error — it is never uploaded and renders broken)
fit      cover(default, crop to fill) | contain(fully shown with letterboxing) | stretch(stretched/distorted)
mask     shape mask, same values as shape's type (ellipse=round avatar), default rect
corner-radius  effective only when mask="rect"
crop-left/top/right/bottom  RATIO cropped inward from each edge, 0~1, default 0; unset means no crop
stroke / stroke-width / stroke-dash  stroke, reuses shape syntax (no border by default, strokes along the mask shape)
flip-h / flip-v  mirror flip, default false (use for subject facing direction; rotation cannot replace it)
shadow / opacity (lower opacity to use as a background texture)
```
`crop-*` is mainly produced by the editor writing back a crop; you cannot see pixels, so unless an exact ratio is known, leave cropping to `fit="cover"`.

```xml
<image src="/home/user/deck/assets/team/cto.jpg" x="120" y="200" width="160" height="160" mask="ellipse"/>
<image src="/home/user/deck/assets/product.png" x="400" y="180" width="480" height="300" fit="contain" corner-radius="16" shadow="true"/>
<image src="/home/user/deck/assets/cover.jpg" x="400" y="180" width="480" height="300" stroke="brand" stroke-width="4"/>
```

## `<icon>` — icon (built-in vector icons, visual anchors for feature lists / advantages / flows)
```
name!    Lucide icon name, kebab-case (e.g. circle-check / mail / trending-up / rocket). Vocabulary = the full Lucide set (1600+); a name not found is a validation error
color    single-color tint, default #000000; prefer referencing a <design> variable to follow the theme color, and remember to lighten it on dark-background pages
all others are common parameters + shadow, no private parameters
```
- Icons are always square in ratio: when `width ≠ height` they scale by the smaller side and center, without stretching; the normal way is to make the two equal.
- Use sparingly: prefer small (24~48px) and single-color; large sizes (64px+) only as decoration with reduced opacity; not every paragraph needs an icon.
- Common name reference: `check circle-check x arrow-right chevron-right trending-up chart-column chart-pie target user users briefcase handshake mail phone send globe map-pin calendar clock settings zap rocket lightbulb sparkles award star shield-check lock search file-text clipboard-list database cloud dollar-sign wallet package truck cpu`

```xml
<icon name="rocket" x="120" y="200" width="40" height="40" color="brand"/>
<icon name="trending-up" x="1040" y="480" width="180" height="180" color="#7DD3E0" opacity="0.15"/>  <!-- large decorative icon on a dark page -->
```

## `<table>` — table
```
columns   column-width weight array, normalized to table width ("2,5,3" or px values both work), defaults to equal width
height!   total table height, px, required (authoritative total height; row heights are distributed within it; elements below are laid out absolutely against it)
rows      row-height array, mixing numbers/auto ("56,auto,auto"), defaults to all auto; length must = the number of logical rows (count of <tr>); auto = evenly split the space left after subtracting fixed rows from height (NOT content-based autofit) — match content amount to the allotted row height when generating; no auto row and sum of fixed rows ≠ height → error
font!  size  color  align  line-height   cascade to all cells, overridable per tr/td
padding   default cell inner padding        anchor  default middle (note: differs from text's top)
align     unset = cells center horizontally, rtl→right (note: differs from text's dir-following start edge)
fill / header-fill    background, solid only. header-fill = header (the first H logical rows, see below); priority td > tr > header > table level
border-h / border-v / border-outer / header-border    row lines / column lines / outer frame / header bottom line; value is a compound "[width] [style] color", component order is fixed, the first two are omittable (e.g. "brand", "2 brand", "dash #E0E0E0", "1 dot #CCC"); style is solid|dash|dot only; width 0 = explicitly no line (overrides lower-priority lines); default is no lines
border-top / border-right / border-bottom / border-left    single outer-frame edges, override the corresponding edge of border-outer
```
Child tags: `<tr>` (may carry fill + the five cascade items applied to the whole row), `<td>` (may additionally carry anchor/padding/wrap/colspan/rowspan + cell-level borders: `border` for all four sides and `border-top/right/bottom/left` for single sides, same compound value; priority cell single side > cell border > table level — a cell-side value fully replaces the table-level line on that side, incl. width 0 to explicitly remove it; content follows text's content model: clean inline OR all block tags).

**Merged cells**: `colspan`/`rowspan` follow HTML semantics (default 1); **cells covered by a merge are not written**. Iron rule: each logical row is covered by **exactly N columns** — mental check: sum of this row's td colspans + cells intruding into this row from rowspans above = N; with no merges it reduces to "exactly N td per row". A merged cell's styles (fill/anchor/padding/cascade items) all go on the starting td and apply to the whole region; header depth H = the max rowspan among the first row's td (H=1 with no merge), header-fill covers the first H rows, header-border is drawn at the bottom edge of row H.

```xml
<table x="80" y="160" width="1120" height="280" columns="3,2,2,2" rows="40,40,auto,auto" font="body" padding="10 14" header-fill="brand" header-border="2 brand" border-h="1 dash #E0E0E0">
  <!-- Two-row grouped header: H=2 -->
  <tr color="#FFFFFF"><td rowspan="2">Product Line</td><td colspan="2">First Half</td><td rowspan="2">Q3</td></tr>
  <tr color="#FFFFFF"><td>Q1</td><td>Q2</td></tr>   <!-- 2×1 + intrusion 2 = 4 = N ✓ -->
  <tr><td>Cloud Services</td><td>120M</td><td>150M</td><td>210M</td></tr>
  <tr fill="#FFF2CC"><td><strong>Total</strong></td><td>120M</td><td>150M</td><td>210M</td></tr>
</table>
```

## `<chart>` — chart
```
type!     bar column line area pie donut scatter (these 7 only, no combo —— see combination charts); semantically = the default rendering of each series
font!     font shared by axis ticks / legend / data labels / axis titles; text-size overrides the variable size (12 when a literal font is unset); text-color default #666666 (remember to lighten on dark-background pages)
categories  category-text array (omit for scatter; category names may not contain commas)
color       color array: assigned to each series in order; for pie/donut assigned to each slice (length must be ≥ category count)
legend      none(default)|top|bottom|left|right
data-labels default false; when true, non-scatter series use label-expr when present (otherwise Cartesian charts show raw values and pie/donut show their computed shares); scatter uses labels when present, otherwise raw coordinates
x-axis / y-axis  axis toggles, default true (ignored by pie/donut)   y-min / y-max  value-axis range, default auto
y-format    number(default)|percent|thousands  value-axis tick number format
x-title / y-title   axis title strings (y-title rotates 90° along the axis; the chart title is still laid out with an adjacent text)
gridlines   none|h|v|hv, default follows the value-axis direction and its toggle (column/line/area=h, bar=v, scatter=hv); when written explicitly it decouples from the axis toggle (minimalist look with ticks but no lines: gridlines="none")
stack       none(default)|normal|percent  stacking, bar/column/area only; percent = percentage stacking (each bar stretched to 100%, value axis auto 0%~100%, y-min/max/format ignored)
smooth      smoothed curve, line only
y2-min / y2-max / y2-format / y2-title   secondary-axis set of four, same semantics as the primary y series; ignored if no series is on secondary
gap-width   bar gap as a percentage of bar width, 0~500, default 150, larger = thinner bars (bar/column only; the only lever for bar thickness, increase e.g. to 300 when categories are few and the chart is wide)
fill-opacity  area fill opacity, 0~1, default 1 (area only; lower e.g. to 0.6 when layers overlap)
line-width  line thickness, px, default 2 (line/area only)   line-dash  solid|dash|dot, default solid (line/area only)
marker      data-point marker toggle, default false (line/area only; scatter always has markers)
marker-size marker size, px, 2~72, default 5 (effective on line/area when marker is on; always effective for scatter)
gridline-color  primary-axis gridline color, default light gray (Cartesian types; must be lightened explicitly on dark pages)
hole-size   donut inner-radius ratio, 0~1, default 0.55 (donut only)
```
y-series parameters refer to the **value axis** (a bar's value axis is horizontal); x-series refer to the category axis.

Child tag `<series name? values color? label-expr? labels? type? axis?>` (always an empty element):

- `values` numeric array, length must = category count; accepts pure numbers only (not `"45%"`, `"120M"`)
- `label-expr` non-scatter data-label template, evaluated independently for every current value whenever data changes. Use `{value}` or `{value:format}`; safe arithmetic with numeric constants is allowed inside the placeholder (`+ - * /`, normal multiplication/division precedence). Supported formats are `.0f`~`.6f`, `,.0f`~`,.6f`, and `.0%`~`.6%`. Literal prefixes/suffixes stay outside the placeholder: `{value:.0%}` turns `0.78` into `78%`, `${value:,.0f}` turns `12400` into `$12,400`, and `¥{value / 10000:.0f}万` turns `34000000` into `¥3400万`
- `labels` display-text array: use it only on scatter to name individual points; its length must equal the parallel `x`/`y` arrays and its text may not contain commas. On non-scatter charts use `label-expr` instead
- `color` single value, overrides the chart-level assignment; every series/slice must resolve a color from one of the two color levels
- Pie/donut have **exactly one series**. Scatter is the exception: a series uses parallel `x`/`y` arrays (equal length)
- **Combination chart**: `type="column|line|area"` overrides this series' rendering (only when the chart-level type is also one of these three, otherwise a validation error); `axis="primary|secondary"` (default primary) attaches to the left/right axis, any series on secondary makes a right-side secondary axis appear (e.g. "revenue bars + growth-rate line"). type and axis are independent; gridlines only follow the primary axis

**No** chart-title parameter (lay it out with an adjacent `<text>`). Chart values must reflect real data from your research — never invent numbers.

```xml
<!-- Multi-series column chart -->
<chart type="column" x="80" y="160" width="560" height="360" font="body" categories="Q1,Q2,Q3" color="brand,#A5A5A5" legend="bottom">
  <series name="Cloud Services"   values="1.2,1.5,2.1"/>
  <series name="Enterprise Software" values="0.8,0.9,1.0"/>
</chart>

<!-- Pie chart: the label expression is recalculated from each current value -->
<chart type="pie" x="720" y="160" width="400" height="360" font="body" categories="East,South,North" color="brand,#5B9BD5,#A5A5A5" data-labels="true">
  <series values="0.45,0.30,0.25" label-expr="{value:.0%}"/>
</chart>

<!-- Scatter uses explicit point labels; it has x/y rather than values -->
<chart type="scatter" x="720" y="160" width="400" height="360" font="body" color="brand" data-labels="true">
  <series x="12,18,25" y="0.34,0.51,0.22" labels="Alpha,Beta,Gamma"/>
</chart>

<!-- Combination chart: revenue bars (left axis, thousands) + growth-rate line (right axis, percent) -->
<chart type="column" x="80" y="160" width="1120" height="400" font="body" categories="2024,2025,2026" color="brand,#E8A33D" legend="bottom" y-format="thousands" y-title="Revenue (K)" y2-format="percent" y2-title="Growth Rate">
  <series name="Revenue"     values="8200,12400,18100"/>
  <series name="Growth Rate" values="0.33,0.51,0.46" type="line" axis="secondary"/>
</chart>

<!-- Percentage stacking: composition over time -->
<chart type="column" x="80" y="160" width="560" height="360" font="body" categories="2024,2025,2026" color="brand,#5B9BD5,#A5A5A5" stack="percent" legend="bottom">
  <series name="Own Brand" values="120,180,260"/>
  <series name="Reseller"  values="200,190,180"/>
  <series name="Other"     values="80,70,60"/>
</chart>
```

## Validation red lines (self-check for the most common errors)
The file-edit hook catches many of these; the rest surface at render/export. Check ALL of them yourself before presenting:

1. `slide` missing its `<background>` child; `text/table/chart` missing `font`; `table` missing `height`; area-type shape missing `fill`; `icon`'s `name` not found in Lucide.
2. Referencing a variable name that does not exist in `<design>` (spell-check!).
3. Table grid not exactly filled: some row's colspan sum + rowspan intrusion count ≠ column count (with no merge, "td count ≠ column count"); `rows` array length ≠ logical row count; colspan/rowspan out of bounds or merged regions overlapping; no auto row and sum of fixed row heights ≠ height.
4. A chart series gets no color; a pie/donut with multiple series; non-scatter `values` length ≠ category count; scatter `x`/`y`/`labels` lengths differ; malformed `label-expr` or `label-expr` on scatter; a series `type` outside column/line/area, or a series has `type` while the chart-level type is not one of those three.
5. Bare text mixed with block-level tags inside `<text>`; list nesting deeper than 5 levels; an `<a>` with both or neither of `href`/`slide`, a `slide` referencing a nonexistent page id, or an `<a>` nested inside an `<a>`.
6. Arrays separated with spaces (should be commas); compound values separated with commas (should be spaces); commas inside category names / series labels; commas inside a font `family`/`font` (fallback lists unsupported, write a single Google Fonts name).
7. `dir`/`lang` misplaced: on `<ul>`/`<ol>` (put them on `<li>` items or the parent `<text>`), on `<tr>`/`<td>` (use the `<table>` attribute or `<p dir>`/`<p lang>` inside the cell), `dir` on inline tags other than `<span>` (wrap the segment in `<span dir>` instead), `lang` on any inline tag (no inline form — use the parent block), or `dir="auto"` (only `ltr`/`rtl` exist).

## Layout and consistency checklist (validated visually, enforced by you)
- Every element lies fully inside the 1280x720 canvas; elements do not overlap unless the overlap is a deliberate design choice (e.g. text over a background shape).
- Distribute body content evenly: after fixed page elements (title, footer, slide number), actual content height should be close to the body area height — avoid content crammed at the top with a large empty bottom. If content is genuinely sparse, center it vertically with equal top/bottom whitespace.
- Maintain grid alignment; in left/right layouts keep both columns' grids aligned with consistent heights, in top/bottom layouts keep equal left/right whitespace.
- Keep fixed page elements (header, footer, slide number) IDENTICAL across slides — same font, same coordinates.
- Estimate text box sizes: oversized content overflows, undersized content leaves holes. Prefer sizing text to fill its box.
- Balance visuals and text; use cards sparingly (only when needed for legibility).
- Use the `design.xml` variables consistently across all slides for a coherent deck.

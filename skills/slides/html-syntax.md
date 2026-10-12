# Self-contained HTML slide rules
Reference for HTML-mode Slides decks. Read this file BEFORE writing any `<id>.html`. Each slide is one standalone, self-contained HTML file that the Studio renders directly: apart from the approved CDN libraries listed below, anything external or relative may render blank.

## Structure
- Each slide is a **complete standalone HTML document** — never a bare markup fragment. A fragment (or utility classes without their framework loaded) renders as unstyled text. Follow this skeleton:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <!-- CDN includes ONLY on slides that use them — see the approved list below -->
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .slide-container { width: 1280px; min-height: 720px; background: #FFFFFF; display: flex; flex-direction: column; }
    /* all other styles go here */
  </style>
</head>
<body>
  <div class="slide-container">
    <!-- slide content -->
  </div>
</body>
</html>
```

- One slide per `<id>.html` file, self-contained at **1280x720**. Default to native CSS inlined in the `<style>` tag.
- Write each page with the native file `write` tool: one call carrying the complete document per page; use the `edit` tool for later targeted fixes. NEVER produce slide HTML via shell commands or Python/Node scripts, and never emit several pages from one call — such writes bypass the Slides file-edit hook, so the deck never registers that content (a page never written through the file tools stays `edit_pending`).
- Wrap the slide content in a single `<div class="slide-container">` with `width: 1280px; min-height: 720px; box-sizing: border-box`. Do NOT put CSS on `body`, and do NOT add padding to `.slide-container`.
- The slide `id` (from the outline) is lowercase letters/digits/underscore and is used verbatim as the `<id>.html` filename.

## Approved CDN libraries (the ONLY allowed external references)
- Chart.js: `<script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1"></script>`
- D3.js: `<script src="https://d3js.org/d3.v7.min.js"></script>`
- Font Awesome icons: `<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">`
- Google Fonts stylesheets (`fonts.googleapis.com`) for the font families named in the design brief.
- Tailwind CSS: `<script src="https://cdn.tailwindcss.com"></script>` — REQUIRED on any slide that uses Tailwind classes; utility classes carry no styling without it. Native CSS remains the default choice.

Include a library only on slides that use it. Everything else — scripts, styles, fonts, assets — must be inline or a local absolute path.

## Not allowed
- No external references beyond the approved CDN list, no inline SVG, `<deck-stage>`, `@keyframes`, animations, transitions, hover-only behavior, or placeholders.

## Layout and overflow discipline
The canvas is fixed and rendered height is measured after every write/edit. The two failure modes are overflow and a top-heavy page (content crammed at the top, large empty bottom) — guard both:
- Inner containers use `min-height` instead of fixed `height` so overflow stays visible and measurable; never use `overflow: hidden` to mask it.
- Use only `padding-top` for vertical spacing — no `padding-bottom` anywhere.
- Give images, charts, and major layout regions explicit pixel dimensions; never size images with percentages or bare flex.
- Do not use `position: absolute` for main content containers.
- Fill the canvas vertically: make `.slide-container` a flex column and give the content zone below the title `flex: 1`, distributing its children with `justify-content: space-between`/`space-evenly` or stretched grid rows so actual content reaches toward the bottom edge.
- If content is genuinely sparse, scale up type and spacing or center the content block vertically with equal top and bottom whitespace — never leave it sitting at the top of an empty page.
- Align containers to a grid; use grid layouts to fill the page horizontally and distribute elements evenly instead of leaving trailing whitespace. In left/right layouts both columns end at the same height; in top/bottom layouts keep left/right whitespace equal.
- Keep every element — including decorative shapes, logos, and text — fully inside the container.

## Images
Use images deliberately: they should raise the deck's visual quality, not fill space.
- **Structural pages** (cover, section dividers, closing): a well-chosen full-bleed image (`object-fit: cover`) is the recommended device — pick one that matches the deck's subject and palette.
- **Content pages**: use images sparingly — either as the page's central subject or as one supporting visual that complements the content. Most content pages need no image at all; never add one as decoration.
- Only reference images that actually exist locally in the sandbox (searched or generated earlier in the session), by absolute path. NEVER write a non-existent or remote image URL into a slide.
- Give every non-background image explicit pixel dimensions and `object-fit: contain`.
- Use high-quality, watermark-free images; never reuse the same image on two pages.
- Do not embed diagram images rendered from Mermaid, D2, or plotting scripts — they lower deck quality. Build diagrams with HTML/CSS, charts with Chart.js/D3, and photos/illustrations from real image files.

## Data presentation
- Default to a cleanly styled HTML table when the audience needs exact values, multi-dimension comparisons, or several series — a table is often the better choice, not the fallback.
- Reach for a chart only when the *shape* of the data carries the message: trend, distribution, proportion, ranking.
- Chart rules: Chart.js v3 syntax only (no v2 idioms like `horizontalBar`); ALWAYS disable animation (`options: { animation: false }`) so screenshots and exports capture the finished chart; ALWAYS wrap each `<canvas>` in a parent div with an explicit pixel height, e.g. `<div style="height: 300px;"><canvas id="chart1"></canvas></div>`; at most one chart or image per column and never stack charts/images vertically; no radar charts; derive series colors from the deck palette. Use Chart.js for standard charts and D3.js only for custom visualizations Chart.js cannot express.
- D3 scripts must be idempotent: render into a dedicated container and clear it first (e.g. `d3.select('#viz').selectAll('*').remove()`) — the Studio editor saves the rendered DOM back into the file, so a non-idempotent script draws the chart twice on the next render.
- Chart only real data collected in this session and cite the source in small text near the chart or table. Never fabricate numbers.

## Design
- Treat each page as a presentation slide rather than a website: avoid navigation UI, rounded-corner card components, border-accent boxes, and decorative shadows. Minimize card-style containers — they fragment the page — and never use cards on data-visualization pages.
- Keep a clear hierarchy, align to a grid, and use at most four main content points per slide.
- Keep the `.slide-container` background identical across all content pages (cover and closing may differ); maintain one consistent color system and recurring visual motifs across the deck, using at most 2-3 palette colors per slide with accents reserved for emphasis.
- If the deck uses fixed page elements (header, footer, page number), keep them IDENTICAL across slides — same position, same size, same font.
- Vary the composition of adjacent content slides when appropriate. Keep the title slide concise and visually distinctive — bold typography, geometric shapes, or an asymmetric split work well.
- When the user gives an explicit style request, follow it throughout the deck.
- Before writing each slide's HTML, think through the design approach, continuity with the rest of the deck, layout structure, key content, and canvas-fit checks; then write the complete document.
- Use real, verifiable information. Never fabricate data, citations, or authoritative claims.

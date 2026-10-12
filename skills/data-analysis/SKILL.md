---
name: data-analysis
description: "Analyze structured data or create visualizations from data. Use when the task requires processing data, performing analysis, or creating insightful visualizations or spreadsheets."
compatibility: opencode
metadata:
  source-bundle: all_skills.zip
  adaptation: opencode-v2
  opencode/slash: "true"
---

# Data Analysis

## When to Use

- When the task requires processing data, performing analysis, and creating insightful visualizations or spreadsheets
- When the deliverable includes charts, plots, diagrams, or other data visualizations
- When the task requires locating authoritative datasets or statistical information

## Data Analysis Best Practices

- When a dedicated data skill (e.g., `financial-market-data`, `world-bank-data`, `similarweb-data`) covers the needed source, prefer it over general web search
- DO NOT use simulated datasets or randomly generated data for analysis; when real datasets cannot be found, MUST request user assistance
- Use the `read` tool to verify data visualizations for layout, content, and text rendering issues
- For data visualization tasks, choose between programming approaches (Python or utilities) or AI-based image generation tools depending on the scenario
- For diagrams, flowcharts, and infographics with limited information that can be conveyed through detailed prompts, prioritize using AI image generation tools (`generate_image` in the `manus-tools` MCP server)
- For data-driven visualizations requiring large datasets or precise numerical values/proportions, prioritize programming approaches like Python (matplotlib/seaborn) or use the `manus-render-diagram` utility (D2 for architecture/complex diagrams, Mermaid otherwise)
- If user explicitly requests visually appealing visualizations, prioritize AI image generation tools; if user emphasizes professionalism and accuracy, prioritize programming approaches
- MUST set appropriate fonts for non-Latin character sets like CJK to ensure correct rendering in visualizations, e.g., using Noto Sans
- Set different font family based on the language of the text, e.g., "Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Sans CJK KR"
- When using matplotlib with custom fonts, apply the style first and then set the custom font in rcParams, or the style will override your font and break character rendering

## Delivering Results

- In addition to final result files, also deliver key supporting files such as images, raw data, or visualizations

## OpenCode V2 portability notes

This skill was adapted from instructions that mention another platform or its integrations. Before following platform-specific steps, inspect the current OpenCode V2 configuration and the tools actually available in this session. Do not assume that named external tools, MCP servers, APIs, credentials, hosted sandboxes, or platform-specific commands exist in OpenCode. Use an equivalent only when it is actually configured and documented; otherwise state the missing dependency and ask before installing, connecting, or substituting a different service. Preserve the original workflow as reference, but do not claim an external action succeeded unless it was executed and verified.

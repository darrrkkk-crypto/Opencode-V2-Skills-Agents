# OpenCode V2 Skills Collection

This repository contains the skills from the supplied `all_skills.zip`, adapted for OpenCode V2 and arranged for GitHub distribution.

## What was adapted

- Converted the frontmatter of each skill to the portable Agent Skills fields accepted by OpenCode V2: `name`, `description`, optional `license`, `compatibility`, and string-valued `metadata`.
- Normalized skill IDs to lowercase kebab-case and aligned each `name` with its containing directory.
- Preserved each skill's body, references, scripts, templates, and other bundled resources.
- Removed two byte-identical nested duplicate skill files (`webdev/worklocally` and `webdev/seo`) so they do not shadow the canonical skills.
- Added a portability warning to skills that explicitly mention Manus or Claude Code-specific platforms/integrations. These integrations are not automatically recreated by this conversion.
- Added a validation report and install script.

## Important compatibility boundary

This is a format and packaging adaptation, not a claim that every original workflow is fully executable in OpenCode. Skills that depend on Manus-only APIs/tools, hosted sandboxes, external MCP servers, credentials, or platform-specific commands still need their dependencies configured or their workflows rewritten against available OpenCode tools. The skill text identifies what to check; do not treat external actions as completed without verification.

## Install globally in OpenCode V2

From the extracted repository root:

```bash
bash install.sh
```

The installer copies each skill directory into `~/.config/opencode/skills/`, creates a timestamped backup for any destination it replaces, and does not change your OpenCode server/process configuration. It does not install MCP servers or connect external accounts.

To install manually, copy individual directories from `skills/` into `~/.config/opencode/skills/`.

## Install for a single project

Copy the desired skill directories into your project at `.opencode/skills/`:

```bash
mkdir -p .opencode/skills
cp -a skills/humanizer .opencode/skills/
```

Replace `humanizer` with the skill ID you want. Commit project-local skills if you want to share them with collaborators.

## OpenCode V2 discovery rules

OpenCode discovers skills from `.opencode/skills/<id>/SKILL.md` and `~/.config/opencode/skills/<id>/SKILL.md`, among other compatibility paths. The directory-derived ID should be lowercase kebab-case, unique, and stable. Official documentation: https://dev.opencode.ai/v2/docs/skills/

## Validation

Run:

```bash
python3 scripts/validate_skills.py
```

The validator checks skill directory IDs, required frontmatter, description length, duplicate IDs, and required `SKILL.md` files. This is static validation, not a runtime test of all workflows.


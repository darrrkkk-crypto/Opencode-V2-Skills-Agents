#!/usr/bin/env python3
from pathlib import Path
import re, sys, yaml
root=Path(__file__).resolve().parents[1]/"skills"
errors=[]; rows=[]
name_re=re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
for p in sorted(root.glob("*/SKILL.md")):
    skill_id=p.parent.name
    text=p.read_text(encoding="utf-8")
    m=re.match(r"\A---\s*\n(.*?)\n---\s*\n",text,re.S)
    if not m:
        errors.append(f"{p}: missing YAML frontmatter")
        continue
    try: fm=yaml.safe_load(m.group(1)) or {}
    except Exception as e:
        errors.append(f"{p}: invalid YAML frontmatter: {e}"); continue
    name=fm.get("name"); desc=fm.get("description")
    if not isinstance(name,str) or not name: errors.append(f"{p}: missing name")
    elif not name_re.fullmatch(name) or len(name)>64: errors.append(f"{p}: invalid name {name!r}")
    if name != skill_id: errors.append(f"{p}: name {name!r} does not match directory {skill_id!r}")
    if not isinstance(desc,str) or not desc.strip(): errors.append(f"{p}: missing description")
    elif len(desc)>1024: errors.append(f"{p}: description exceeds 1024 characters")
    if not p.is_file(): errors.append(f"{p}: missing SKILL.md")
    rows.append(skill_id)
if len(rows)!=len(set(rows)): errors.append("duplicate skill IDs")
print(f"Skills checked: {len(rows)}")
if errors:
    print("FAIL")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print("PASS: all skill IDs and frontmatter satisfy the package's static checks")

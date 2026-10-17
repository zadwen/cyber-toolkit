"""Generate the human-readable catalog from catalog.json."""
import json
from pathlib import Path
root = Path(__file__).resolve().parent
catalog = json.loads((root / 'catalog.json').read_text())
lines = ['# Tool catalog', '', f"{len(catalog['tools'])} curated APT/pipx entries, plus {len(catalog['ai_packages'])} AI environment packages and the optional Kali complete metapackage.", '', '| Tool ID | Group | Installer | Purpose |', '|---|---|---|---|']
for tool in catalog['tools']:
    manager = tool['manager'] + (' (Kali only)' if tool.get('kali_only') else '')
    lines.append(f"| `{tool['id']}` | {tool['group']} | {manager} | [{tool['description']}]({tool['source']}) |")
lines += ['', 'AI environment: ' + ', '.join('`'+p+'`' for p in catalog['ai_packages']) + '.', '', 'Optional CPU packages: `torch`, `torchvision`, `torchaudio`.', '', 'Package availability is checked on the target system before installation.', '']
(root / 'CATALOG.md').write_text('\n'.join(lines))

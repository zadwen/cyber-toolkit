#!/usr/bin/env bash
set -euo pipefail
command -v python3 >/dev/null || { echo 'Install Python 3 first.' >&2; exit 1; }
exec python3 "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/install.py" "$@"

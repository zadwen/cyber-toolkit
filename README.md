# Cyber Toolkit

One Linux installer for cybersecurity students, CTF players, defenders and AI students. Choose a profile, preview the tool list, then install the packages you want.

This is a curated catalog, not a claim to include every cybersecurity tool ever made. Kali users can optionally choose the official `kali-linux-everything` metapackage for the broadest Kali toolset.

## Get started

Requires Python 3 and an APT-based Linux distribution: Ubuntu, Debian, Zorin OS or Kali. Run as your normal user, not root. Installation requests sudo for APT; Python applications remain in user-owned isolated environments.

```bash
git clone https://github.com/zadwen/cyber-toolkit.git
cd cyber-toolkit
./install.sh --install
```

The interactive menu asks which type of student or practitioner you are. Choose one or several numbers, inspect the plan, and confirm installation. To preview the menu without installing, run `./install.sh`.

## Profiles

| ID | Designed for | Included areas |
|---|---|---|
| `cyber-student` | Cybersecurity beginners | Networking, web labs, metadata and forensics |
| `ctf` | CTF players | Web, pwn, crypto, steganography, forensics, reverse engineering |
| `pentest` | Authorized assessment labs | Networking, web, passwords, wireless and Kali-specific tools |
| `blue-team` | SOC / defensive security students | Traffic analysis, host auditing, memory and file analysis |
| `forensics` | Digital investigators | Disk, file, metadata and memory analysis |
| `reverse` | Reverse engineering / pwn students | GDB, ELF inspection, binary utilities, pwntools and ROP tools |
| `ai-student` | AI / data science students | JupyterLab, NumPy, pandas, SciPy, Matplotlib, scikit-learn and developer tools |
| `developer` | Secure software development | Compilers, linting, static analysis and audit tools |
| `all` | Complete curated catalog | All the above, with optional CPU PyTorch |
| `kali-everything` | Dedicated Kali workstation / VM | Official Kali complete toolset; Kali Linux only |

See [CATALOG.md](CATALOG.md) for every catalog entry. Availability varies by distribution and repository configuration; unavailable packages are explicitly reported.

## Examples

```bash
# Preview only: no package installation or settings changes
./install.sh --profile ctf

# List all roles, or inspect tools in a role
./install.sh --list
./install.sh --profile blue-team --list-tools

# Install a profile; confirm the plan interactively
./install.sh --profile cyber-student --install

# Combine roles
./install.sh --profile ctf,ai-student --install

# Exclude named tools (IDs are in CATALOG.md)
./install.sh --profile ctf --exclude sagemath,wireshark --install

# Install available packages when some are absent on this distribution
./install.sh --profile ctf --install --allow-missing

# AI environment with CPU-only PyTorch
./install.sh --profile ai-student --torch cpu --install

# Dedicated Kali machine only; very large installation
./install.sh --profile kali-everything --install

# Noninteractive installation after reviewing the selection
./install.sh --profile forensics --install --yes --allow-missing
```

`--dry-run` always overrides `--install`. Omitting `--install` always previews. On noninteractive input, supply `--profile`; actual unattended installation also needs `--yes` and working sudo authorization.

## Installation behavior

- Uses packages from the machine's existing APT repositories and Python applications from PyPI through pipx. It does not add Kali repositories to Ubuntu or Zorin, execute downloaded shell scripts, or change GPU drivers, firewall rules, startup apps or kernel settings.
- Refreshes APT metadata, checks package candidates, then installs available packages with `--no-install-recommends` and `--no-remove`.
- Missing APT packages stop installation before selected packages are installed unless `--allow-missing` was supplied. Kali-only catalog entries are omitted and listed on other distributions.
- APT packages follow the configured distribution versions. Python dependencies follow their current package releases; this is not a reproducibly version-locked environment.
- System packages such as auditd, Suricata or iperf3 may install/start services according to the distribution's packaging defaults. Exclude those tools if you do not want them.
- Repeating installation does not force upgrades of pipx tools. Manage updates with APT and `pipx upgrade TOOL`. AI pip installation follows normal pip behavior in its existing environment.
- APT operations are not transactional with Python installs. Failures do not roll back successful earlier operations. Every actual run writes a JSON result with installed, unavailable, omitted and failed items under `~/.local/state/cyber-toolkit/` (respects `XDG_STATE_HOME`). A required failure exits nonzero; intentionally allowed missing packages produce a clearly marked partial report.

Large profiles can require substantial storage. Review APT's size estimate when it runs; the installer prints current free space but does not predict the download size. Wordlists, game images, training datasets, AI models and GPU drivers are not bundled.

## AI environment

The installer creates `~/.local/share/cyber-toolkit/venvs/ai` (respects `XDG_DATA_HOME`). Activate it with:

```bash
source ~/.local/share/cyber-toolkit/venvs/ai/bin/activate
jupyter lab
```

`--torch cpu` uses PyTorch's official CPU package index. GPU acceleration requires choosing a compatible build for your GPU and driver using the [official PyTorch selector](https://pytorch.org/get-started/locally/); CUDA is not installed automatically.

Python CLI applications installed with pipx are normally in `~/.local/bin`. Add that directory to your PATH if it is not already present. No system Python packages are overwritten with sudo pip.

## Tool coverage and limits

Examples include Nmap, Wireshark, tcpdump, sqlmap, ffuf, Gobuster, Hashcat, John, GDB, binutils, pwntools, ROPGadget, SageMath, steghide, Binwalk, ExifTool, YARA, Volatility 3, Semgrep, Bandit and pip-audit. Kali-only entries include Ghidra, Burp Suite, ZAP, Metasploit, SecLists and others.

This project installs tools; it does not run scans, attacks, training jobs, packet captures or vulnerable lab services for you. Use security tools on systems and labs you own or are authorized to assess. Commercial editions and third-party licenses remain separate.

## Contributing and validation

Edit `build_catalog.py`, regenerate the JSON, and add profile coverage tests where appropriate:

```bash
python3 build_catalog.py
python3 scripts_catalog_docs.py
bash -n install.sh
python3 -m unittest discover -s tests -v
./install.sh --profile ctf --dry-run
```

Tests use temporary directories and mocked package operations; they do not install tools. CI tests Python 3.10 and 3.12. Initial validation includes catalog checks, profile selection, preview behavior, Kali restrictions, missing packages, partial failures, reporting and AI installation plans. Actual installation of every catalog tool across all supported distributions has not been performed.

## Sources

- [Kali metapackages](https://www.kali.org/docs/general-use/metapackages/)
- [Kali tool directory](https://www.kali.org/tools/all-tools/)
- [pipx documentation](https://pipx.pypa.io/stable/)
- [PyTorch installation selector](https://pytorch.org/get-started/locally/)

Installer code is MIT licensed. Installed tools retain their own licenses.

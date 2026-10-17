# Tool catalog

109 curated APT/pipx entries, plus 10 AI environment packages and the optional Kali complete metapackage.

| Tool ID | Group | Installer | Purpose |
|---|---|---|---|
| `git` | base | apt | [Version control](https://packages.debian.org/) |
| `curl` | base | apt | [HTTP client](https://packages.debian.org/) |
| `wget` | base | apt | [File downloader](https://packages.debian.org/) |
| `jq` | base | apt | [JSON processor](https://packages.debian.org/) |
| `ripgrep` | base | apt | [Fast text search](https://packages.debian.org/) |
| `tmux` | base | apt | [Terminal multiplexer](https://packages.debian.org/) |
| `unzip` | base | apt | [ZIP extraction](https://packages.debian.org/) |
| `p7zip-full` | base | apt | [Archive utilities](https://packages.debian.org/) |
| `file` | base | apt | [File identification](https://packages.debian.org/) |
| `python3-venv` | base | apt | [Python virtual environments](https://packages.debian.org/) |
| `python3-pip` | base | apt | [Python package manager](https://packages.debian.org/) |
| `pipx` | base | apt | [Isolated Python applications](https://packages.debian.org/) |
| `build-essential` | base | apt | [C/C++ compiler and build tools](https://packages.debian.org/) |
| `pkg-config` | base | apt | [Build dependency discovery](https://packages.debian.org/) |
| `libssl-dev` | base | apt | [TLS development headers](https://packages.debian.org/) |
| `libffi-dev` | base | apt | [FFI development headers](https://packages.debian.org/) |
| `python3-dev` | base | apt | [Python development headers](https://packages.debian.org/) |
| `nmap` | network | apt | [Network discovery and port scanning](https://packages.debian.org/) |
| `tcpdump` | network | apt | [Packet capture](https://packages.debian.org/) |
| `tshark` | network | apt | [Command-line packet analysis](https://packages.debian.org/) |
| `wireshark` | network | apt | [Graphical packet analysis](https://packages.debian.org/) |
| `netcat-openbsd` | network | apt | [TCP/UDP client](https://packages.debian.org/) |
| `socat` | network | apt | [Network relay](https://packages.debian.org/) |
| `dnsutils` | network | apt | [DNS lookup utilities](https://packages.debian.org/) |
| `whois` | network | apt | [Domain registration lookup](https://packages.debian.org/) |
| `traceroute` | network | apt | [Network route diagnostics](https://packages.debian.org/) |
| `iproute2` | network | apt | [IP and routing tools](https://packages.debian.org/) |
| `mtr-tiny` | network | apt | [Route quality diagnostics](https://packages.debian.org/) |
| `iperf3` | network | apt | [Network throughput testing](https://packages.debian.org/) |
| `openssl` | network | apt | [TLS and cryptography](https://packages.debian.org/) |
| `openvpn` | network | apt | [Lab VPN client](https://packages.debian.org/) |
| `sqlmap` | web | apt | [SQL injection testing](https://packages.debian.org/) |
| `nikto` | web | apt | [Web server assessment](https://packages.debian.org/) |
| `gobuster` | web | apt | [Web content discovery](https://packages.debian.org/) |
| `ffuf` | web | apt | [Web fuzzing](https://packages.debian.org/) |
| `whatweb` | web | apt | [Web technology identification](https://packages.debian.org/) |
| `dirb` | web | apt | [Web directory discovery](https://packages.debian.org/) |
| `wafw00f` | web | apt | [WAF identification](https://packages.debian.org/) |
| `hashcat` | passwords | apt | [Offline password recovery](https://packages.debian.org/) |
| `john` | passwords | apt | [Password recovery](https://packages.debian.org/) |
| `hydra` | passwords | apt | [Authentication testing](https://packages.debian.org/) |
| `crunch` | passwords | apt | [Wordlist generation](https://packages.debian.org/) |
| `cewl` | passwords | apt | [Lab wordlist generation](https://packages.debian.org/) |
| `aircrack-ng` | wireless | apt | [Wireless auditing suite](https://packages.debian.org/) |
| `iw` | wireless | apt | [Wireless device diagnostics](https://packages.debian.org/) |
| `sleuthkit` | forensics | apt | [Filesystem forensics](https://packages.debian.org/) |
| `testdisk` | forensics | apt | [Partition and file recovery](https://packages.debian.org/) |
| `foremost` | forensics | apt | [File carving](https://packages.debian.org/) |
| `binwalk` | forensics | apt | [Firmware and embedded file analysis](https://packages.debian.org/) |
| `libimage-exiftool-perl` | forensics | apt | [File metadata inspection](https://packages.debian.org/) |
| `exif` | forensics | apt | [EXIF inspection](https://packages.debian.org/) |
| `pngcheck` | forensics | apt | [PNG validation](https://packages.debian.org/) |
| `jpeginfo` | forensics | apt | [JPEG inspection](https://packages.debian.org/) |
| `yara` | forensics | apt | [Pattern matching](https://packages.debian.org/) |
| `sqlite3` | forensics | apt | [SQLite inspection](https://packages.debian.org/) |
| `hexedit` | forensics | apt | [Hex editor](https://packages.debian.org/) |
| `xxd` | forensics | apt | [Hex dumps](https://packages.debian.org/) |
| `steghide` | ctf | apt | [Steganography](https://packages.debian.org/) |
| `outguess` | ctf | apt | [Steganography analysis](https://packages.debian.org/) |
| `zbar-tools` | ctf | apt | [Barcode/QR decoding](https://packages.debian.org/) |
| `qrencode` | ctf | apt | [QR generation](https://packages.debian.org/) |
| `sagemath` | ctf | apt | [Symbolic mathematics](https://packages.debian.org/) |
| `fcrackzip` | ctf | apt | [ZIP password recovery](https://packages.debian.org/) |
| `gdb` | reverse | apt | [Native debugger](https://packages.debian.org/) |
| `gdb-multiarch` | reverse | apt | [Cross-architecture debugger](https://packages.debian.org/) |
| `binutils` | reverse | apt | [Binary inspection](https://packages.debian.org/) |
| `strace` | reverse | apt | [System-call tracing](https://packages.debian.org/) |
| `ltrace` | reverse | apt | [Library-call tracing](https://packages.debian.org/) |
| `patchelf` | reverse | apt | [ELF modification](https://packages.debian.org/) |
| `nasm` | reverse | apt | [Assembler](https://packages.debian.org/) |
| `valgrind` | reverse | apt | [Memory debugging](https://packages.debian.org/) |
| `checksec` | reverse | apt | [Binary protection checks](https://packages.debian.org/) |
| `radare2` | reverse | apt | [Reverse engineering framework](https://packages.debian.org/) |
| `lynis` | blue | apt | [Host configuration audit](https://packages.debian.org/) |
| `clamav` | blue | apt | [File malware scanning](https://packages.debian.org/) |
| `auditd` | blue | apt | [Linux audit tools](https://packages.debian.org/) |
| `suricata` | blue | apt | [Network IDS engine](https://packages.debian.org/) |
| `zeek` | blue | apt | [Network security monitoring](https://packages.debian.org/) |
| `rkhunter` | blue | apt | [Host integrity checks](https://packages.debian.org/) |
| `shellcheck` | developer | apt | [Shell linting](https://packages.debian.org/) |
| `cmake` | developer | apt | [Build generator](https://packages.debian.org/) |
| `ninja-build` | developer | apt | [Build executor](https://packages.debian.org/) |
| `sqlitebrowser` | developer | apt | [SQLite GUI](https://packages.debian.org/) |
| `git-lfs` | developer | apt | [Large file support](https://packages.debian.org/) |
| `seclists` | kali | apt (Kali only) | [Security testing wordlists](https://www.kali.org/tools/) |
| `ghidra` | kali | apt (Kali only) | [Reverse engineering GUI](https://www.kali.org/tools/) |
| `burpsuite` | kali | apt (Kali only) | [Web application testing proxy](https://www.kali.org/tools/) |
| `zaproxy` | kali | apt (Kali only) | [Web security scanner](https://www.kali.org/tools/) |
| `metasploit-framework` | kali | apt (Kali only) | [Security assessment framework](https://www.kali.org/tools/) |
| `responder` | kali | apt (Kali only) | [Lab name-resolution testing](https://www.kali.org/tools/) |
| `netexec` | kali | apt (Kali only) | [Network assessment toolkit](https://www.kali.org/tools/) |
| `bloodhound` | kali | apt (Kali only) | [Directory relationship analysis](https://www.kali.org/tools/) |
| `feroxbuster` | kali | apt (Kali only) | [Recursive content discovery](https://www.kali.org/tools/) |
| `nuclei` | kali | apt (Kali only) | [Template-based security checks](https://www.kali.org/tools/) |
| `subfinder` | kali | apt (Kali only) | [Subdomain discovery](https://www.kali.org/tools/) |
| `amass` | kali | apt (Kali only) | [Attack surface discovery](https://www.kali.org/tools/) |
| `rustscan` | kali | apt (Kali only) | [Port scanning](https://www.kali.org/tools/) |
| `chisel` | kali | apt (Kali only) | [Lab tunneling utility](https://www.kali.org/tools/) |
| `pwntools` | ctf | pipx | [CTF binary exploitation toolkit](https://pypi.org/project/pwntools/) |
| `ropgadget` | ctf | pipx | [ROP gadget analysis](https://pypi.org/project/ROPGadget/) |
| `ropper` | ctf | pipx | [Binary gadget analysis](https://pypi.org/project/ropper/) |
| `mitmproxy` | web | pipx | [Interactive HTTP debugging proxy](https://pypi.org/project/mitmproxy/) |
| `httpie` | web | pipx | [Human-friendly HTTP client](https://pypi.org/project/httpie/) |
| `volatility3` | forensics | pipx | [Memory forensics](https://pypi.org/project/volatility3/) |
| `semgrep` | blue | pipx | [Static analysis](https://pypi.org/project/semgrep/) |
| `bandit` | blue | pipx | [Python security checks](https://pypi.org/project/bandit/) |
| `pip-audit` | blue | pipx | [Python dependency audit](https://pypi.org/project/pip-audit/) |
| `ruff` | developer | pipx | [Python linting and formatting](https://pypi.org/project/ruff/) |
| `pre-commit` | developer | pipx | [Repository checks](https://pypi.org/project/pre-commit/) |

AI environment: `jupyterlab`, `numpy`, `pandas`, `scipy`, `matplotlib`, `seaborn`, `scikit-learn`, `sympy`, `ipykernel`, `requests`.

Optional CPU packages: `torch`, `torchvision`, `torchaudio`.

Package availability is checked on the target system before installation.

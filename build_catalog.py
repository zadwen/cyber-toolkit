"""Generate the reviewed catalog. Edit this file and run it to extend the catalog."""
import json
from pathlib import Path

GROUPS = {
'base': [('git','Version control'),('curl','HTTP client'),('wget','File downloader'),('jq','JSON processor'),('ripgrep','Fast text search'),('tmux','Terminal multiplexer'),('unzip','ZIP extraction'),('p7zip-full','Archive utilities'),('file','File identification'),('python3-venv','Python virtual environments'),('python3-pip','Python package manager'),('pipx','Isolated Python applications'),('build-essential','C/C++ compiler and build tools'),('pkg-config','Build dependency discovery'),('libssl-dev','TLS development headers'),('libffi-dev','FFI development headers'),('python3-dev','Python development headers')],
'network': [('nmap','Network discovery and port scanning'),('tcpdump','Packet capture'),('tshark','Command-line packet analysis'),('wireshark','Graphical packet analysis'),('netcat-openbsd','TCP/UDP client'),('socat','Network relay'),('dnsutils','DNS lookup utilities'),('whois','Domain registration lookup'),('traceroute','Network route diagnostics'),('iproute2','IP and routing tools'),('mtr-tiny','Route quality diagnostics'),('iperf3','Network throughput testing'),('openssl','TLS and cryptography'),('openvpn','Lab VPN client')],
'web': [('sqlmap','SQL injection testing'),('nikto','Web server assessment'),('gobuster','Web content discovery'),('ffuf','Web fuzzing'),('whatweb','Web technology identification'),('dirb','Web directory discovery'),('wafw00f','WAF identification')],
'passwords': [('hashcat','Offline password recovery'),('john','Password recovery'),('hydra','Authentication testing'),('crunch','Wordlist generation'),('cewl','Lab wordlist generation')],
'wireless': [('aircrack-ng','Wireless auditing suite'),('iw','Wireless device diagnostics')],
'forensics': [('sleuthkit','Filesystem forensics'),('testdisk','Partition and file recovery'),('foremost','File carving'),('binwalk','Firmware and embedded file analysis'),('libimage-exiftool-perl','File metadata inspection'),('exif','EXIF inspection'),('pngcheck','PNG validation'),('jpeginfo','JPEG inspection'),('yara','Pattern matching'),('sqlite3','SQLite inspection'),('hexedit','Hex editor'),('xxd','Hex dumps')],
'ctf': [('steghide','Steganography'),('outguess','Steganography analysis'),('zbar-tools','Barcode/QR decoding'),('qrencode','QR generation'),('sagemath','Symbolic mathematics'),('fcrackzip','ZIP password recovery')],
'reverse': [('gdb','Native debugger'),('gdb-multiarch','Cross-architecture debugger'),('binutils','Binary inspection'),('strace','System-call tracing'),('ltrace','Library-call tracing'),('patchelf','ELF modification'),('nasm','Assembler'),('valgrind','Memory debugging'),('checksec','Binary protection checks'),('radare2','Reverse engineering framework')],
'blue': [('lynis','Host configuration audit'),('clamav','File malware scanning'),('auditd','Linux audit tools'),('suricata','Network IDS engine'),('zeek','Network security monitoring'),('rkhunter','Host integrity checks')],
'developer': [('shellcheck','Shell linting'),('cmake','Build generator'),('ninja-build','Build executor'),('sqlitebrowser','SQLite GUI'),('git-lfs','Large file support')],
'kali': [('seclists','Security testing wordlists'),('ghidra','Reverse engineering GUI'),('burpsuite','Web application testing proxy'),('zaproxy','Web security scanner'),('metasploit-framework','Security assessment framework'),('responder','Lab name-resolution testing'),('netexec','Network assessment toolkit'),('bloodhound','Directory relationship analysis'),('feroxbuster','Recursive content discovery'),('nuclei','Template-based security checks'),('subfinder','Subdomain discovery'),('amass','Attack surface discovery'),('rustscan','Port scanning'),('chisel','Lab tunneling utility')],
}
PIPX = {
'ctf': [('pwntools','CTF binary exploitation toolkit'),('ROPGadget','ROP gadget analysis'),('ropper','Binary gadget analysis')],
'web': [('mitmproxy','Interactive HTTP debugging proxy'),('httpie','Human-friendly HTTP client')],
'forensics': [('volatility3','Memory forensics')],
'blue': [('semgrep','Static analysis'),('bandit','Python security checks'),('pip-audit','Python dependency audit')],
'developer': [('ruff','Python linting and formatting'),('pre-commit','Repository checks')],
}
PROFILES = {
'cyber-student': {'label':'Cybersecurity student','groups':['base','network','web','forensics'], 'note':'Foundations, networking, web labs and file analysis.'},
'ctf': {'label':'CTF player','groups':['base','network','web','passwords','forensics','ctf','reverse'],'note':'Web, pwn, crypto, reverse engineering, steganography and forensics.'},
'pentest': {'label':'Penetration testing lab','groups':['base','network','web','passwords','wireless','kali'],'note':'Authorized assessment tools; Kali-only entries are identified on other distributions.'},
'blue-team': {'label':'Blue team / SOC student','groups':['base','network','forensics','blue'],'note':'Traffic analysis, host auditing, file analysis and static analysis. Some distro packages may start services.'},
'forensics': {'label':'Digital forensics student','groups':['base','network','forensics'],'note':'Disk, file, metadata and memory investigation.'},
'reverse': {'label':'Reverse engineering / pwn','groups':['base','reverse','ctf'],'note':'Debuggers, ELF tools, mathematics and binary exploitation utilities.'},
'ai-student': {'label':'AI / data science student','groups':['base','developer'],'note':'Adds an isolated environment with JupyterLab, NumPy, pandas, SciPy, Matplotlib and scikit-learn; optional CPU PyTorch.'},
'developer': {'label':'Secure software developer','groups':['base','developer','blue'],'note':'Build and audit tools; use --exclude to omit host monitoring packages.'},
'all': {'label':'All curated tools','groups':list(GROUPS),'note':'Large installation. This is the complete catalog, not every security tool in existence.'},
'kali-everything': {'label':'Kali complete distribution toolset','groups':['base'],'note':'Kali Linux only: official kali-linux-everything metapackage; very large.'},
}
tools=[]
for group,entries in GROUPS.items():
 for package,description in entries:
  tools.append({'id':package,'manager':'apt','package':package,'group':group,'description':description,'kali_only':group=='kali','source':'https://www.kali.org/tools/' if group=='kali' else 'https://packages.debian.org/'})
for group,entries in PIPX.items():
 for package,description in entries:
  tools.append({'id':package.lower(),'manager':'pipx','package':package,'group':group,'description':description,'source':'https://pypi.org/project/'+package+'/'})
ai=['jupyterlab','numpy','pandas','scipy','matplotlib','seaborn','scikit-learn','sympy','ipykernel','requests']
data={'schema_version':1,'profiles':PROFILES,'tools':tools,'ai_packages':ai}
Path(__file__).with_name('catalog.json').write_text(json.dumps(data,indent=2)+'\n')

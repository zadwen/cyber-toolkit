#!/usr/bin/env python3
"""Profile-based Linux learning toolkit installer. Preview is the default."""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def load_catalog():
    data = json.loads((ROOT / 'catalog.json').read_text())
    ids = set()
    for tool in data['tools']:
        if tool['id'] in ids or tool['manager'] not in ('apt', 'pipx'):
            raise ValueError('Duplicate tool or unsupported package manager')
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9+_.-]*', tool['package']):
            raise ValueError('Invalid package name: ' + tool['package'])
        ids.add(tool['id'])
    return data


def distro():
    result = {}
    try:
        for line in Path('/etc/os-release').read_text().splitlines():
            if '=' in line:
                key, value = line.split('=', 1)
                result[key] = value.strip('"')
    except OSError:
        pass
    return result


def select_tools(data, profiles, exclude=()):
    groups = set()
    for profile in profiles:
        if profile not in data['profiles']:
            raise ValueError('Unknown profile: ' + profile)
        groups.update(data['profiles'][profile]['groups'])
    unknown = set(exclude) - {t['id'] for t in data['tools']}
    if unknown:
        raise ValueError('Unknown exclusions: ' + ', '.join(sorted(unknown)))
    return sorted((t for t in data['tools'] if t['group'] in groups and t['id'] not in exclude), key=lambda t: t['id'])


def candidate_exists(package):
    proc = subprocess.run(['apt-cache', 'policy', package], capture_output=True, text=True, check=False, env={**os.environ, 'LC_ALL': 'C'})
    return proc.returncode == 0 and bool(re.search(r'Candidate:\s+(?!\(none\))\S+', proc.stdout))


def run(command, dry=False):
    print('+ ' + shlex.join(map(str, command)), flush=True)
    if not dry:
        subprocess.run(list(map(str, command)), check=True)


def choose(data):
    names = list(data['profiles'])
    print('\nChoose your learning profile (multiple numbers separated by commas):\n')
    for index, name in enumerate(names, 1):
        item = data['profiles'][name]
        print(f"  {index:2}. {item['label']} [{name}]\n      {item['note']}")
    raw = input('\nSelection: ')
    numbers = [int(x.strip()) for x in raw.split(',')]
    if not numbers or any(n < 1 or n > len(names) for n in numbers):
        raise ValueError('Select a number from the menu')
    return list(dict.fromkeys(names[n - 1] for n in numbers))


def accept_missing(packages, allowed=False):
    if not packages:
        return True
    print('Unavailable on this system: ' + ', '.join(packages))
    if allowed:
        return True
    if sys.stdin.isatty():
        return input('Skip these packages and install the available tools? [y/N] ').strip().lower() in ('y', 'yes')
    return False


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', action='append', default=[], help='Profile ID; repeat or separate with commas')
    parser.add_argument('--list', action='store_true', help='List profiles')
    parser.add_argument('--list-tools', action='store_true', help='List selected tools and exit')
    parser.add_argument('--install', action='store_true', help='Execute the displayed installation plan')
    parser.add_argument('--dry-run', action='store_true', help='Preview only; never installs')
    parser.add_argument('--yes', action='store_true', help='Accept the installation plan without prompting')
    parser.add_argument('--exclude', action='append', default=[], help='Tool IDs to exclude, comma-separated')
    parser.add_argument('--allow-missing', action='store_true', help='Allow unavailable distro packages; recorded in report')
    parser.add_argument('--torch', choices=['none', 'cpu'], default='none', help='Optional PyTorch in AI environment; CUDA is configured separately')
    parser.add_argument('--report', type=Path, help='Installation report path (written only during installation)')
    args = parser.parse_args(argv)
    data = load_catalog()
    if args.list:
        for name, profile in data['profiles'].items():
            print(f"{name:18} {profile['label']} — {profile['note']}")
        return 0
    profiles = [p.strip() for value in args.profile for p in value.split(',') if p.strip()]
    if not profiles:
        if not sys.stdin.isatty():
            parser.error('Specify --profile in noninteractive mode; use --list for choices')
        profiles = choose(data)
    exclusions = [p.strip() for value in args.exclude for p in value.split(',') if p.strip()]
    tools = select_tools(data, profiles, exclusions)
    ai = 'ai-student' in profiles or 'all' in profiles
    if args.torch != 'none' and not ai:
        raise ValueError('--torch requires ai-student or all')
    info = distro()
    is_kali = info.get('ID') == 'kali'
    if 'kali-everything' in profiles and not is_kali:
        raise ValueError('kali-everything requires Kali Linux. Kali repositories will not be added to another distribution.')
    if args.list_tools:
        for tool in tools:
            print(f"{tool['id']:24} {tool['manager']:5} {tool['description']}" + (' [Kali only]' if tool.get('kali_only') else ''))
        if ai:
            print('AI venv: ' + ', '.join(data['ai_packages']))
        return 0
    if not shutil.which('apt-get') or not shutil.which('apt-cache'):
        raise ValueError('Supported systems: Debian, Ubuntu, Zorin and Kali with APT')
    apt_tools = [t['package'] for t in tools if t['manager'] == 'apt' and (is_kali or not t.get('kali_only'))]
    pipx_tools = [t['package'] for t in tools if t['manager'] == 'pipx']
    skipped = [t['id'] for t in tools if t.get('kali_only') and not is_kali]
    if 'kali-everything' in profiles:
        apt_tools.append('kali-linux-everything')
    dry = not args.install or args.dry_run
    # Dependencies remain available even if the user excludes their catalog entries.
    if pipx_tools or ai:
        apt_tools += ['python3-venv', 'python3-pip']
    if pipx_tools:
        apt_tools.append('pipx')
    apt_tools = sorted(set(apt_tools))
    state = Path(os.environ.get('XDG_STATE_HOME', str(Path.home() / '.local/state'))) / 'cyber-toolkit'
    env_dir = Path(os.environ.get('XDG_DATA_HOME', str(Path.home() / '.local/share'))) / 'cyber-toolkit/venvs/ai'
    print('Profiles: ' + ', '.join(profiles))
    print('System: ' + info.get('PRETTY_NAME', 'unknown Linux'))
    print(f'Free home space: {shutil.disk_usage(Path.home()).free / 1024**3:.1f} GiB')
    print('APT packages: ' + ' '.join(apt_tools))
    print('pipx applications: ' + (' '.join(pipx_tools) or '(none)'))
    if skipped:
        print('Kali-only tools omitted: ' + ', '.join(skipped))
    if ai:
        print('AI environment: ' + str(env_dir))
        print('AI packages: ' + ', '.join(data['ai_packages']))
    print('\nPackage versions are resolved by your configured APT repositories and PyPI at installation time.')
    if dry:
        print('\nPREVIEW ONLY. Use --install to install. No files or settings changed.')
        return 0
    if os.geteuid() == 0:
        raise ValueError('Run as your normal user; the installer requests sudo for APT only')
    if not shutil.which('sudo'):
        raise ValueError('sudo is required for system packages')
    if not args.yes:
        if not sys.stdin.isatty():
            raise ValueError('Use --yes with --install in noninteractive mode')
        if input('\nInstall this selection? [y/N] ').strip().lower() not in ('y', 'yes'):
            print('Cancelled.')
            return 0
    state.mkdir(parents=True, exist_ok=True)
    report_path = args.report or state / ('install-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f') + '.json')
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = {'profiles': profiles, 'system': info, 'started': datetime.datetime.now().isoformat(), 'installed': [], 'unavailable': [], 'omitted_kali_only': skipped, 'failed': [], 'status': 'running'}
    def save():
        report_path.write_text(json.dumps(report, indent=2) + '\n')
    save()
    try:
        run(['sudo', 'apt-get', 'update'])
        available = [p for p in apt_tools if candidate_exists(p)]
        report['unavailable'] = sorted(set(apt_tools) - set(available))
        save()
        if not accept_missing(report['unavailable'], args.allow_missing):
            raise ValueError('Unavailable APT packages: ' + ', '.join(report['unavailable']) + '. No selected packages installed. Use --allow-missing to continue without them.')
        if available:
            # --no-remove prevents resolving dependencies by removing installed software.
            run(['sudo', 'env', 'DEBIAN_FRONTEND=noninteractive', 'apt-get', 'install', '--no-install-recommends', '--no-remove', '-y'] + available)
            report['installed'] += ['apt:' + p for p in available]
            save()
        pipx_bin = shutil.which('pipx') or '/usr/bin/pipx'
        for package in pipx_tools:
            try:
                run([pipx_bin, 'install', package])
                report['installed'].append('pipx:' + package)
            except subprocess.CalledProcessError:
                report['failed'].append('pipx:' + package)
            save()
        if ai:
            run([sys.executable, '-m', 'venv', str(env_dir)])
            run([env_dir / 'bin/python', '-m', 'pip', 'install'] + data['ai_packages'])
            if args.torch == 'cpu':
                run([env_dir / 'bin/python', '-m', 'pip', 'install', 'torch', 'torchvision', 'torchaudio', '--index-url', 'https://download.pytorch.org/whl/cpu'])
            report['installed'].append('venv:ai')
            report['ai_environment'] = str(env_dir)
        report['status'] = 'partial' if report['failed'] or report['unavailable'] else 'complete'
        print('\nReport: ' + str(report_path))
        if pipx_tools:
            print('Python CLI tools are normally in ~/.local/bin. Add that directory to PATH if needed.')
        if ai:
            print('Start Jupyter: ' + shlex.join([str(env_dir / 'bin/jupyter'), 'lab']))
        print('Install finished: ' + report['status'])
        return 1 if report['failed'] else 0
    except (subprocess.CalledProcessError, ValueError, OSError, KeyboardInterrupt) as error:
        report['status'] = 'failed'
        report['error'] = str(error)
        raise
    finally:
        report['finished'] = datetime.datetime.now().isoformat()
        save()
        print('Saved report: ' + str(report_path))


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print('\nInterrupted. Completed package operations are not rolled back.', file=sys.stderr)
        sys.exit(130)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print('Error: ' + str(error), file=sys.stderr)
        sys.exit(1)

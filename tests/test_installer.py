import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'install.py')
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.data = app.load_catalog()
        self.stdout = contextlib.redirect_stdout(io.StringIO())
        self.stdout.__enter__()

    def tearDown(self):
        self.stdout.__exit__(None, None, None)

    def test_catalog_unique_and_group_coverage(self):
        groups = {t['group'] for t in self.data['tools']}
        for profile in self.data['profiles'].values():
            self.assertTrue(set(profile['groups']) <= groups)
        self.assertGreaterEqual(len(self.data['tools']), 90)

    def test_profile_union_and_exclusions(self):
        single = app.select_tools(self.data, ['ctf'])
        merged = app.select_tools(self.data, ['ctf', 'cyber-student', 'ctf'], ['nmap'])
        self.assertNotIn('nmap', {t['id'] for t in merged})
        self.assertEqual(len(merged), len({t['id'] for t in merged}))
        self.assertTrue({t['id'] for t in single} - {'nmap'} <= {t['id'] for t in merged})

    def test_unknown_profile_and_exclusion_rejected(self):
        with self.assertRaises(ValueError):
            app.select_tools(self.data, ['typo'])
        with self.assertRaises(ValueError):
            app.select_tools(self.data, ['ctf'], ['typo'])

    def test_preview_never_runs_commands_or_writes_report(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(app, 'run') as run:
            report = Path(directory) / 'report.json'
            self.assertEqual(app.main(['--profile', 'ctf', '--report', str(report)]), 0)
            run.assert_not_called()
            self.assertFalse(report.exists())

    def test_dry_run_wins_over_install(self):
        with patch.object(app, 'run') as run:
            self.assertEqual(app.main(['--profile', 'ai-student', '--install', '--dry-run']), 0)
            run.assert_not_called()

    def test_kali_everything_rejected_on_ubuntu(self):
        with patch.object(app, 'distro', return_value={'ID': 'ubuntu'}):
            with self.assertRaisesRegex(ValueError, 'requires Kali'):
                app.main(['--profile', 'kali-everything'])

    def test_interactive_missing_packages_can_be_skipped(self):
        with patch.object(app.sys.stdin, 'isatty', return_value=True), patch('builtins.input', return_value='y'):
            self.assertTrue(app.accept_missing(['sagemath', 'zeek']))

    def test_interactive_missing_packages_decline_by_default(self):
        with patch.object(app.sys.stdin, 'isatty', return_value=True), patch('builtins.input', return_value=''):
            self.assertFalse(app.accept_missing(['zeek']))

    def test_noninteractive_missing_packages_need_explicit_flag(self):
        with patch.object(app.sys.stdin, 'isatty', return_value=False), patch('builtins.input') as prompt:
            self.assertFalse(app.accept_missing(['zeek']))
            self.assertTrue(app.accept_missing(['zeek'], allowed=True))
            prompt.assert_not_called()

    def test_cpu_torch_requires_ai(self):
        with self.assertRaises(ValueError):
            app.main(['--profile', 'ctf', '--torch', 'cpu'])

    def execute_install(self, directory, available=True, fail_pipx=False, allow_missing=False):
        report = Path(directory) / 'report.json'
        calls = []
        def fake_run(cmd, dry=False):
            calls.append([str(x) for x in cmd])
            if fail_pipx and 'pipx' in str(cmd[0]) and 'install' in cmd:
                raise subprocess.CalledProcessError(1, cmd)
        args = ['--profile', 'forensics', '--install', '--yes', '--report', str(report)]
        if allow_missing:
            args.append('--allow-missing')
        with patch.object(app.os, 'geteuid', return_value=1000), patch.object(app, 'run', side_effect=fake_run), patch.object(app, 'candidate_exists', return_value=available), patch.object(app.shutil, 'which', side_effect=lambda x: '/usr/bin/' + x), patch.dict(os.environ, {'XDG_STATE_HOME': directory}):
            status = app.main(args)
        return status, json.loads(report.read_text()), calls

    def test_successful_install_report_and_no_shell_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            status, report, calls = self.execute_install(directory)
            self.assertEqual(status, 0)
            self.assertEqual(report['status'], 'complete')
            self.assertIn('pipx:volatility3', report['installed'])
            self.assertTrue(any('--no-remove' in c for c in calls))
            self.assertFalse(any('bash' in c or 'sh' in c for c in calls))

    def test_pipx_failure_returns_failure_and_partial_report(self):
        with tempfile.TemporaryDirectory() as directory:
            status, report, _ = self.execute_install(directory, fail_pipx=True)
            self.assertEqual(status, 1)
            self.assertEqual(report['status'], 'partial')
            self.assertIn('pipx:volatility3', report['failed'])

    def test_missing_packages_fail_before_install_and_save_report(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                self.execute_install(directory, available=False)
            report = json.loads((Path(directory) / 'report.json').read_text())
            self.assertEqual(report['status'], 'failed')
            self.assertTrue(report['unavailable'])
            self.assertEqual(report['installed'], [])

    def test_allow_missing_explicitly_reports_partial(self):
        with tempfile.TemporaryDirectory() as directory:
            status, report, _ = self.execute_install(directory, available=False, allow_missing=True)
            self.assertEqual(status, 0)
            self.assertEqual(report['status'], 'partial')

    def test_ai_environment_and_cpu_torch_plan(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {'XDG_STATE_HOME': directory, 'XDG_DATA_HOME': directory}), patch.object(app.os, 'geteuid', return_value=1000), patch.object(app, 'candidate_exists', return_value=True), patch.object(app.shutil, 'which', return_value='/usr/bin/tool'), patch.object(app, 'run') as run:
            self.assertEqual(app.main(['--profile', 'ai-student', '--torch', 'cpu', '--install', '--yes']), 0)
            commands = [[str(x) for x in call.args[0]] for call in run.call_args_list]
            self.assertTrue(any('https://download.pytorch.org/whl/cpu' in c for c in commands))
            self.assertTrue(any('venv' in c for c in commands))


if __name__ == '__main__':
    unittest.main()

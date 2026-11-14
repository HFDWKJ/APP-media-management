"""Synthetic checks for UTC log routing and release-note compatibility."""
import ast
from datetime import datetime, timezone, timedelta
import importlib.util
import logging
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from core import reorganize_report, reorganize_marker
from utils import paths
from utils import logging as app_logging

class LogPathsTests(unittest.TestCase):
    def test_utc_receipts_do_not_overwrite_and_legacy_remains_readable(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            logs = root / '.log'
            logs.mkdir()
            source = root / 'source'
            source.mkdir()
            when = datetime(2026, 11, 14, 1, 30, tzinfo=timezone(timedelta(hours=-8)))
            with patch.object(reorganize_report, 'log_dir', return_value=logs):
                first = reorganize_report.write_reorganize_csv(source, [{'sequence_no': 1}], processed_at=when)
                before = first.read_bytes()
                second = reorganize_report.write_reorganize_csv(source, [{'sequence_no': 2}], processed_at=when)
                self.assertRegex(first.name, r'^2026111409-reorganize-[a-f0-9]{12}\.csv$')
                self.assertNotEqual(first, second)
                self.assertEqual(first.read_bytes(), before)
                self.assertTrue(reorganize_marker.has_reorganize_marker(source))
                self.assertIn('2026-11-14T09:30:00+00:00', before.decode('utf-8-sig'))
                self.assertEqual(reorganize_report.find_latest_reorganize_csv(source), second)
                first.unlink(); second.unlink()
                legacy = source / 'reorganize_20200101_010203.csv'
                legacy.write_text('original')
                self.assertEqual(reorganize_report.find_latest_reorganize_csv(source), legacy)
            with self.assertRaises(ValueError):
                reorganize_report.report_filename(datetime(2026, 11, 14))

    def test_source_portable_and_installed_log_roots(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(paths, 'application_root', return_value=root / 'app'), patch.object(paths, '_installed_config_dir', return_value=root / 'state'):
                for compiled, portable, expected in [(False, False, 'app'), (True, True, 'app'), (True, False, 'state')]:
                    with patch.object(paths, 'is_compiled', return_value=compiled), patch.object(paths, 'is_portable_mode', return_value=portable):
                        self.assertEqual(paths.log_dir(), root / expected / '.log')

    def test_runtime_log_keeps_timezone_and_appends(self):
        with tempfile.TemporaryDirectory() as temporary:
            logger = logging.getLogger()
            old_handlers, old_level = logger.handlers[:], logger.level
            try:
                with patch.object(app_logging, 'log_dir', return_value=Path(temporary)):
                    app_logging.setup_logging()
                    logger.info('synthetic first')
                    for handler in logger.handlers:
                        handler.flush()
                    app_logging.setup_logging()
                    logger.info('synthetic second')
                    for handler in logger.handlers:
                        handler.flush()
                    path, = Path(temporary).glob('*.log')
                    self.assertRegex(path.name, r'^[0-9]{10}-media-manager-runtime\.log$')
                    text = path.read_text()
                    self.assertIn('synthetic first', text)
                    self.assertIn('synthetic second', text)
                    self.assertRegex(text, r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
            finally:
                for handler in logger.handlers:
                    handler.close()
                logger.handlers = old_handlers
                logger.setLevel(old_level)

    def test_runtime_rolls_over_by_record_utc_hour(self):
        with tempfile.TemporaryDirectory() as temporary:
            handler = app_logging.HourlyUTCFileHandler(Path(temporary))
            try:
                for hour in (9, 10, 9):
                    record = logging.LogRecord("synthetic", logging.INFO, __file__, 1, f"hour {hour}", (), None)
                    record.created = datetime(2026, 11, 14, hour, tzinfo=timezone.utc).timestamp()
                    handler.handle(record)
                handler.flush()
                logs = sorted(Path(temporary).glob("*.log"))
                self.assertEqual([path.name[:10] for path in logs], ["2026111409", "2026111410"])
                self.assertEqual(logs[0].read_text().count("hour 9"), 2)
                self.assertEqual(logs[1].read_text().count("hour 10"), 1)
            finally:
                handler.close()

    def test_about_reads_dated_release_body(self):
        source = (ROOT / 'src/gui/about_dialog.py').read_text()
        tree = ast.parse(source)
        function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == '_load_changelog_text')
        namespace = {'_changelog_path': lambda: ROOT / 'CHANGELOG.md', 're': re}
        exec(compile(ast.Module(body=[function], type_ignores=[]), '<about loader>', 'exec'), namespace)
        content = namespace['_load_changelog_text']()
        self.assertIn('## 0.0.4', content)
        self.assertNotIn('Release History Index', content)

if __name__ == '__main__':
    unittest.main()

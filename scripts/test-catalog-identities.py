import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "validator", Path(__file__).with_name("validate-catalog-identities.py")
)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
ID = "qcat_00aabbcc-1234-4123-8123-abcdef123456"
ENTRY = {
    "catalogId": ID,
    "repository": "example/game",
    "folderName": "Example",
}


class Tests(unittest.TestCase):
    def check(self, entries):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "list.json"
            path.write_text(json.dumps({"apps": entries}))
            return validator.validate([path])

    def test_legacy(self):
        self.assertEqual(self.check([{"name": "Legacy"}]), 0)

    def test_valid(self):
        self.assertEqual(self.check([ENTRY]), 1)

    def test_reject_test_and_duplicate(self):
        for entries in [
            [{**ENTRY, "catalogId": ID.replace("qcat_", "qtest_")}],
            [ENTRY, ENTRY],
        ]:
            with self.subTest(entries=entries), self.assertRaises(ValueError):
                self.check(entries)


if __name__ == "__main__":
    unittest.main()

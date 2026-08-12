import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
TEST_TMP_ROOT = Path(__file__).resolve().parent / "tmp"
TEST_TMP_ROOT.mkdir(exist_ok=True)

from design_system import _resolved_child, persist_design_system, safe_path_slug


class PersistencePathTests(unittest.TestCase):
    def test_slug_is_one_safe_component(self):
        self.assertEqual(safe_path_slug("Área do Cliente"), "area-do-cliente")
        self.assertEqual(safe_path_slug("../.."), "default")
        self.assertNotIn("/", safe_path_slug("/tmp/example"))
        self.assertNotIn("\\", safe_path_slug(r"C:\\tmp\\example"))

    def test_resolved_child_rejects_escape(self):
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            parent = Path(tmp)
            with self.assertRaises(ValueError):
                _resolved_child(parent, "../outside")
            with self.assertRaises(ValueError):
                _resolved_child(parent, str(parent.parent / "outside"))

    def test_untrusted_names_stay_inside_output_directory(self):
        with tempfile.TemporaryDirectory(dir=TEST_TMP_ROOT) as tmp:
            output = Path(tmp).resolve()
            result = persist_design_system(
                {"project_name": r"C:\\tmp\\example"},
                page=r"..\\..\\override",
                output_dir=str(output),
            )

            expected_root = (output / "design-system").resolve()
            design_dir = Path(result["design_system_dir"]).resolve()
            design_dir.relative_to(expected_root)

            for created in result["created_files"]:
                created_path = Path(created).resolve()
                created_path.relative_to(design_dir)

            self.assertTrue((design_dir / "MASTER.md").is_file())
            self.assertTrue((design_dir / "pages" / "override.md").is_file())


if __name__ == "__main__":
    unittest.main()


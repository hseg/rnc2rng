import rnc2rng
import unittest
from urllib.parse import urlparse
from urllib.request import url2pathname
import importlib.resources as resources
from . import golden


class TestSuite(unittest.TestCase):
    def test_from_string(self):
        with (
            resources.open_text(golden, "features.rnc") as src,
            resources.open_text(golden, "features.rng") as expect_src,
        ):
            expected = expect_src.read().rstrip()
            actual = rnc2rng.dumps(rnc2rng.loads(src.read())).strip()
            self.assertEqual(expected, actual)

    def _is_golden(self, fn):
        root = rnc2rng.load(fn)
        ref = fn.replace(".rnc", ".rng")
        if ref.startswith("file:"):
            parse_result = urlparse(ref)
            ref = url2pathname(parse_result.path)
        with resources.open_text(golden, ref) as expect_src:
            expected = expect_src.read().rstrip()
            actual = rnc2rng.dumps(root).strip()
            self.assertEqual(expected, actual)

    def test_data_files_exist(self):
        self.assertNotEqual(list(resources.files(golden).iterdir()), [])

    def test_golden(self):
        for fn in filter(
            lambda f: f.suffix == ".rnc", resources.files(golden).iterdir()
        ):
            with self.subTest(fn=fn):
                self._is_golden(str(fn))

    # synthesize a test that reads its input from a URL
    def test_urlinput(self):
        with resources.path(golden, "include.rnc") as path:
            self._is_golden(path.absolute().as_uri())


if __name__ == "__main__":
    unittest.main()

import rnc2rng
import unittest
import sys
from urllib.parse import urljoin, urlparse
from urllib.request import pathname2url, url2pathname
import importlib.resources as resources
from . import golden


class TestSuite(unittest.TestCase):
    def test_from_string(self):
        src = resources.read_text(golden, 'features.rnc')
        expected = resources.read_text(golden, 'features.rng').rstrip()
        actual = rnc2rng.dumps(rnc2rng.loads(src)).strip()
        self.assertEqual(expected, actual)

    def _is_golden(self, fn):
        root = rnc2rng.load(fn)
        ref = fn.replace('.rnc', '.rng')
        if ref.startswith('file:'):
            parse_result = urlparse(ref)
            ref = url2pathname(parse_result.path)
        expected = resources.read_text(golden, ref).rstrip()
        actual = rnc2rng.dumps(root).strip()
        self.assertEqual(expected, actual)

    def test_golden(self):
        for fn in resources.files(golden).iterdir():
            if fn.suffix != 'rnc':
                continue
            with self.subTest(fn=fn):
                self._is_golden(fn)
        # synthesize a test that reads its input from a URL
        with resources.path(golden, 'include.rnc') as path:
            self._is_golden(path.absolute().as_uri())


if __name__ == '__main__':
    unittest.main()

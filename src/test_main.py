from main import *
import unittest

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        md = """
random paragraph

# heading

more random stuff
"""
        h1 = extract_title(md)
        self.assertEqual(h1, "heading")

    def test_no_heading(self):
        md = """
- this is not a heading

**and neither is this**

## and this is an h2
"""
        self.assertRaises(Exception, extract_title, md)
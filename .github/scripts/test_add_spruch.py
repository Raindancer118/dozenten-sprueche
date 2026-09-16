import os
import tempfile
import unittest

from add_spruch import add_spruch, escape, extract_spruch


FORM_BODY = "### Spruch\n\nWer nicht testet, der nicht gewinnt.\n"


class ExtractSpruchTest(unittest.TestCase):
    def test_reads_value_below_form_heading(self):
        self.assertEqual(extract_spruch(FORM_BODY), "Wer nicht testet, der nicht gewinnt.")

    def test_keeps_multiline_spruch_and_trims_whitespace(self):
        body = "### Spruch\r\n\r\n  Zeile eins\r\nZeile zwei  \r\n\r\n"
        self.assertEqual(extract_spruch(body), "Zeile eins\nZeile zwei")

    def test_stops_at_next_heading(self):
        body = "### Spruch\n\nDer Spruch\n\n### Anderes Feld\n\nIgnorieren"
        self.assertEqual(extract_spruch(body), "Der Spruch")

    def test_falls_back_to_whole_body_without_heading(self):
        self.assertEqual(extract_spruch("  Einfach so  "), "Einfach so")

    def test_empty_or_no_response_yields_none(self):
        self.assertIsNone(extract_spruch("### Spruch\n\n_No response_\n"))
        self.assertIsNone(extract_spruch(""))
        self.assertIsNone(extract_spruch(None))


class EscapeTest(unittest.TestCase):
    def test_neutralises_html_and_liquid(self):
        self.assertEqual(
            escape("<script>{{ site }}</script> & {% raw %}"),
            "&lt;script&gt;&#123;&#123; site &#125;&#125;&lt;/script&gt; &amp; &#123;% raw %&#125;",
        )

    def test_neutralises_markdown_links_and_images(self):
        result = escape("[klick](javascript:alert(1)) ![x](javascript:alert(2))")
        self.assertNotIn("[", result)
        self.assertNotIn("]", result)
        self.assertEqual(result, "&#91;klick&#93;(javascript:alert(1)) !&#91;x&#93;(javascript:alert(2))")

    def test_multiline_becomes_single_list_item(self):
        self.assertEqual(escape("a\n\nb"), "a<br>b")

    def test_leading_markdown_block_syntax_is_neutralised(self):
        self.assertEqual(escape("# Überschrift"), "&#35; Überschrift")


class AddSpruchTest(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".md")
        os.close(fd)

    def tearDown(self):
        os.remove(self.path)

    def write(self, content):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(content)

    def read(self):
        with open(self.path, encoding="utf-8") as f:
            return f.read()

    def test_appends_as_list_item(self):
        self.write("# Sprüche\n\n- Alt\n")
        self.assertTrue(add_spruch(self.path, "Neu"))
        self.assertEqual(self.read(), "# Sprüche\n\n- Alt\n- Neu\n")

    def test_adds_missing_trailing_newline(self):
        self.write("# Sprüche\n\n- Alt")
        add_spruch(self.path, "Neu")
        self.assertEqual(self.read(), "# Sprüche\n\n- Alt\n- Neu\n")

    def test_skips_duplicates_ignoring_case_and_whitespace(self):
        self.write("# Sprüche\n\n- Das  ist so\n")
        self.assertFalse(add_spruch(self.path, "das ist SO"))
        self.assertEqual(self.read(), "# Sprüche\n\n- Das  ist so\n")


if __name__ == "__main__":
    unittest.main()

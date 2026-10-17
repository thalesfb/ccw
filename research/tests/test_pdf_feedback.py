"""Offline tests with synthetic annotations; no advisor material is committed."""

import hashlib
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfWriter
from pypdf.annotations import Link, Text
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NumberObject, TextStringObject

from src.validation.pdf_feedback import extract_feedback, extract_transcript


class FeedbackExtractionTests(unittest.TestCase):
    def test_notes_preserve_page_coordinates_and_hash_without_inventing_excerpt(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.pdf"
            writer = PdfWriter()
            writer.add_blank_page(width=600, height=800)
            writer.add_blank_page(width=600, height=800)
            writer.add_annotation(1, Text(rect=(20, 30, 44, 54), text="Clarify this term"))
            writer.add_annotation(0, Link(rect=(0, 0, 10, 10), url="https://example.org"))
            writer.write(path)

            result = extract_feedback(path)

            self.assertEqual(result["source_sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(result["page_count"], 2)
            self.assertEqual(len(result["annotations"]), 1)
            note = result["annotations"][0]
            self.assertEqual(note["page"], 2)
            self.assertEqual(note["type"], "Text")
            self.assertEqual(note["contents"], "Clarify this term")
            self.assertEqual(note["rect"], [20.0, 30.0, 44.0, 54.0])
            self.assertIsNone(note["associated_excerpt"])
            self.assertEqual(note["association_status"], "not_anchored")
            self.assertEqual(result, extract_feedback(path))
            self.assertEqual(result["pages"][1]["text_integrity"], "no_extractable_text")

    def test_pdf_without_annotations_returns_empty_feedback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.pdf"
            writer = PdfWriter()
            writer.add_blank_page(width=600, height=800)
            writer.write(path)
            self.assertEqual(extract_feedback(path)["annotations"], [])

    def test_indirect_annotation_arrays_and_strings_are_resolved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "indirect.pdf"
            writer = PdfWriter()
            page = writer.add_blank_page(width=600, height=800)
            note = DictionaryObject({
                NameObject("/Subtype"): NameObject("/Text"),
                NameObject("/Contents"): writer._add_object(TextStringObject("Exact comment")),
                NameObject("/T"): writer._add_object(TextStringObject("Synthetic reviewer")),
                NameObject("/Rect"): writer._add_object(ArrayObject([NumberObject(v) for v in (1, 2, 3, 4)])),
            })
            page[NameObject("/Annots")] = writer._add_object(ArrayObject([writer._add_object(note)]))
            writer.write(path)
            result = extract_feedback(path)
            self.assertEqual(result["annotations"][0]["contents"], "Exact comment")
            self.assertEqual(result["annotations"][0]["author"], "Synthetic reviewer")
            self.assertEqual(result["annotations"][0]["rect"], [1.0, 2.0, 3.0, 4.0])

    def test_bom_crlf_and_multiline_segments_preserve_byte_hash_and_offsets(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transcript.txt"
            data = b"\xef\xbb\xbfFirst line\r\nsecond line\r\n\r\n  Final remark.  \r\n"
            path.write_bytes(data)
            result = extract_transcript(path)
            self.assertEqual(result["source_sha256"], hashlib.sha256(data).hexdigest())
            self.assertEqual(len(result["segments"]), 2)
            self.assertEqual(result["segments"][0]["text"], "First line\r\nsecond line")
            for segment in result["segments"]:
                self.assertEqual(result["original_text"][segment["char_start"]:segment["char_end"]], segment["text"])

    def test_transcript_preserves_original_and_exact_segment_offsets(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transcript.txt"
            text = "First remark.\n\nSecond remark with accents: revisão.\n"
            path.write_text(text, encoding="utf-8", newline="")
            result = extract_transcript(path)
            self.assertEqual(result["original_text"], text)
            self.assertEqual(len(result["segments"]), 2)
            for segment in result["segments"]:
                self.assertEqual(text[segment["char_start"]:segment["char_end"]], segment["text"])


if __name__ == "__main__":
    unittest.main()

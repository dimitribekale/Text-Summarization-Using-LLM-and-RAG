"""Test _clean_text() method."""
import pytest

class TestCleanText:
    """Tests for _clean_text() method."""

    def test_removes_references(self, file_processor):
        """References section is removed."""
        text = "Content.\n\nReferences\n[1] Item"
        cleaned = file_processor._clean_text(text)
        assert "References" not in cleaned
        assert "[1] Item" not in cleaned

    def test_removes_bibliography(self, file_processor):
        """Bibliography section is removed."""
        text = "Content.\n\nBibliography\nItem 1"
        cleaned = file_processor._clean_text(text)
        assert "Bibliography" not in cleaned
        assert "Item 1" not in cleaned

    def test_removes_appendix(self, file_processor):
        """Appendix section is removed."""
        text = "Content.\n\nAppendix A\nInfo"
        cleaned = file_processor._clean_text(text)
        assert "Appendix A" not in cleaned

    def test_preserve_content(self, file_processor):
        """Content before unwanted section is kept."""
        text = "Keep this.\n\nReferences\nRemove this"
        cleaned = file_processor._clean_text(text)
        assert "Keep this" in cleaned

    def test_wanted_sections(self, file_processor):
        """Works correctly when no unwanted sections exist."""
        text = "Just regular content."
        cleaned = file_processor._clean_text(text)
        assert cleaned == text.strip()
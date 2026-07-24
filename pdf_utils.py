"""
pdf_utils.py — extract plain text from an uploaded PDF book.

Requires: pip install pypdf
"""

from pypdf import PdfReader


def extract_text_from_pdf(file_obj) -> str:
    """
    file_obj: a file-like object (e.g. from st.file_uploader), opened in binary mode.
    Returns the concatenated text of every page, separated by blank lines so
    paragraph-based chunking downstream still works reasonably well.
    """
    reader = PdfReader(file_obj)
    pages_text = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            pages_text.append(text.strip())
    return "\n\n".join(pages_text)

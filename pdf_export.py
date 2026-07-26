"""
pdf_export.py — turn AI-generated study material (markdown-ish text from
Gemini) into downloadable, nicely styled PDFs using reportlab.
"""

import re
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

_styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "NexoraTitle", parent=_styles["Title"], textColor=colors.HexColor("#4834d4")
)
SUBTITLE_STYLE = ParagraphStyle(
    "NexoraSubtitle", parent=_styles["Normal"], textColor=colors.HexColor("#666666"), spaceAfter=14
)
H1_STYLE = ParagraphStyle(
    "NexoraH1", parent=_styles["Heading1"], textColor=colors.HexColor("#4834d4"),
    spaceBefore=14, spaceAfter=6,
)
H2_STYLE = ParagraphStyle(
    "NexoraH2", parent=_styles["Heading2"], textColor=colors.HexColor("#6C5CE7"),
    spaceBefore=10, spaceAfter=4,
)
BODY_STYLE = ParagraphStyle("NexoraBody", parent=_styles["Normal"], spaceAfter=6, leading=15)
BULLET_STYLE = ParagraphStyle(
    "NexoraBullet", parent=_styles["Normal"], leftIndent=14, spaceAfter=3, leading=14
)


def _inline_markdown_to_html(text: str) -> str:
    """Convert basic inline markdown (bold/italic) to reportlab's mini-HTML markup."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*(?!\*)", r"<i>\1</i>", text)
    return text


def _markdown_to_flowables(md_text: str):
    flowables = []
    for raw_line in md_text.split("\n"):
        stripped = raw_line.strip()

        if not stripped:
            flowables.append(Spacer(1, 6))
            continue

        if stripped.startswith("### "):
            flowables.append(Paragraph(_inline_markdown_to_html(stripped[4:]), H2_STYLE))
        elif stripped.startswith("## "):
            flowables.append(Paragraph(_inline_markdown_to_html(stripped[3:]), H1_STYLE))
        elif stripped.startswith("# "):
            flowables.append(Paragraph(_inline_markdown_to_html(stripped[2:]), H1_STYLE))
        elif re.match(r"^[-*]\s+", stripped):
            bullet_text = re.sub(r"^[-*]\s+", "", stripped)
            flowables.append(Paragraph("&bull;&nbsp; " + _inline_markdown_to_html(bullet_text), BULLET_STYLE))
        elif re.match(r"^\d+[.)]\s+", stripped):
            flowables.append(Paragraph(_inline_markdown_to_html(stripped), BULLET_STYLE))
        elif stripped.startswith("|") and stripped.endswith("|"):
            # Markdown table rows aren't rendered as real tables here — show as plain text
            # so nothing is silently dropped.
            flowables.append(Paragraph(_inline_markdown_to_html(stripped), BODY_STYLE))
        else:
            flowables.append(Paragraph(_inline_markdown_to_html(stripped), BODY_STYLE))

    return flowables


def _sanitize_filename(name: str) -> str:
    name = re.sub(r"[^\w\-. ]", "", name).strip().replace(" ", "_")
    return name or "document"


# Public alias — views/ code should use this rather than the underscored name.
sanitize_filename = _sanitize_filename


def build_pdf(title: str, subtitle: str, body_markdown: str) -> bytes:
    """Build a PDF from a title/subtitle plus markdown-ish body text. Returns raw PDF bytes."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
    )
    story = [Paragraph(_inline_markdown_to_html(title), TITLE_STYLE)]
    if subtitle:
        story.append(Paragraph(_inline_markdown_to_html(subtitle), SUBTITLE_STYLE))
    story.append(Spacer(1, 10))
    story.extend(_markdown_to_flowables(body_markdown))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def build_flashcards_pdf(title: str, cards: list[dict]) -> bytes:
    """Build a PDF listing each flashcard's question and answer. Returns raw PDF bytes."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
    )
    story = [Paragraph(_inline_markdown_to_html(title), TITLE_STYLE), Spacer(1, 12)]
    for idx, card in enumerate(cards, start=1):
        story.append(Paragraph(f"Card {idx}", H2_STYLE))
        story.append(Paragraph(f"<b>Q:</b> {_inline_markdown_to_html(card.get('question', ''))}", BODY_STYLE))
        story.append(Paragraph(f"<b>A:</b> {_inline_markdown_to_html(card.get('answer', ''))}", BODY_STYLE))
        story.append(Spacer(1, 10))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

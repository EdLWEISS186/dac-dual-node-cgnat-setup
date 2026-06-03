import argparse
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


BASE_DIR = Path(__file__).resolve().parent
CUSTOM_REPORT_DIR = BASE_DIR / "reports" / "generated" / "custom"

RANGE_OPTIONS = {"7d", "30d", "all"}


def normalize_text(value: str) -> str:
    replacements = {
        "—": "-",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "→": "->",
        "✅": "[OK]",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    return value


def strip_markdown_inline(value: str) -> str:
    value = normalize_text(value)
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"\*\*([^*]*)\*\*", r"\1", value)
    value = re.sub(r"\*([^*]*)\*", r"\1", value)
    return value.strip()


def md_file_for_range(selected_range: str) -> Path:
    return CUSTOM_REPORT_DIR / f"dac-enode-report-{selected_range}.md"


def pdf_file_for_range(selected_range: str) -> Path:
    return CUSTOM_REPORT_DIR / f"dac-enode-report-{selected_range}.pdf"


def is_table_separator(line: str) -> bool:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return False

    body = stripped.strip("|").strip()
    return bool(body) and all(set(cell.strip()) <= {"-", ":"} for cell in body.split("|"))


def parse_table(lines: list[str], start_index: int) -> tuple[list[list[str]], int]:
    rows = []
    index = start_index

    while index < len(lines):
        line = lines[index].strip()

        if not (line.startswith("|") and line.endswith("|")):
            break

        if not is_table_separator(line):
            cells = [strip_markdown_inline(cell.strip()) for cell in line.strip("|").split("|")]
            rows.append(cells)

        index += 1

    return rows, index


def make_paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    cleaned = strip_markdown_inline(text)
    return Paragraph(escape(cleaned), style)


def make_table(rows: list[list[str]], styles: dict) -> Table:
    if not rows:
        return Table([["N/A"]])

    max_cols = max(len(row) for row in rows)
    normalized = []

    for row in rows:
        padded = row + [""] * (max_cols - len(row))
        normalized.append([
            Paragraph(escape(strip_markdown_inline(cell)), styles["table_cell"])
            for cell in padded
        ])

    available_width = 10.0 * inch
    col_width = available_width / max_cols
    col_widths = [col_width] * max_cols

    table = Table(normalized, colWidths=col_widths, repeatRows=1)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
        ("TOPPADDING", (0, 0), (-1, 0), 7),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 1), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
    ]))

    return table


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(0.55 * inch, 0.35 * inch, "DAC Enode Intelligence Watcher - Optional PDF Export")
    canvas.drawRightString(10.45 * inch, 0.35 * inch, f"Page {doc.page}")
    canvas.restoreState()


def markdown_to_pdf(markdown_text: str, output_file: Path) -> None:
    sample = getSampleStyleSheet()

    styles = {
        "title": ParagraphStyle(
            "CustomTitle",
            parent=sample["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=14,
            alignment=TA_LEFT,
        ),
        "heading": ParagraphStyle(
            "CustomHeading",
            parent=sample["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#1E293B"),
            spaceBefore=12,
            spaceAfter=8,
        ),
        "body": ParagraphStyle(
            "CustomBody",
            parent=sample["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "CustomBullet",
            parent=sample["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            leftIndent=14,
            firstLineIndent=-8,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=4,
        ),
        "table_cell": ParagraphStyle(
            "CustomTableCell",
            parent=sample["BodyText"],
            fontName="Helvetica",
            fontSize=6.4,
            leading=8,
            textColor=colors.HexColor("#0F172A"),
        ),
    }

    doc = SimpleDocTemplate(
        str(output_file),
        pagesize=landscape(letter),
        rightMargin=0.45 * inch,
        leftMargin=0.45 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.55 * inch,
        title="DAC Enode Intelligence Watcher Report",
        author="JERUZZALEM",
    )

    lines = markdown_text.splitlines()
    story = []
    index = 0

    while index < len(lines):
        raw_line = lines[index]
        line = raw_line.strip()

        if not line:
            story.append(Spacer(1, 4))
            index += 1
            continue

        if line.startswith("|") and line.endswith("|"):
            rows, next_index = parse_table(lines, index)
            if rows:
                story.append(make_table(rows, styles))
                story.append(Spacer(1, 10))
            index = next_index
            continue

        if line.startswith("# "):
            story.append(make_paragraph(line[2:], styles["title"]))
            index += 1
            continue

        if line.startswith("## "):
            story.append(make_paragraph(line[3:], styles["heading"]))
            index += 1
            continue

        if line == "---":
            story.append(PageBreak())
            index += 1
            continue

        if line.startswith("- "):
            story.append(make_paragraph(f"- {line[2:]}", styles["bullet"]))
            index += 1
            continue

        story.append(make_paragraph(line, styles["body"]))
        index += 1

    output_file.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def generate_pdf(selected_range: str) -> Path:
    markdown_file = md_file_for_range(selected_range)
    output_file = pdf_file_for_range(selected_range)

    if not markdown_file.exists():
        raise FileNotFoundError(
            f"Markdown source not found: {markdown_file}. "
            "Run generate_custom_report.py first."
        )

    markdown_text = markdown_file.read_text(encoding="utf-8")
    markdown_to_pdf(markdown_text, output_file)

    return output_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate optional PDF reports from custom Markdown reports.")
    parser.add_argument(
        "--range",
        choices=sorted(RANGE_OPTIONS),
        default="all",
        help="Report range: 7d, 30d, or all.",
    )

    args = parser.parse_args()
    output_file = generate_pdf(args.range)

    print(f"[OK] PDF report generated: {output_file}")
    print(f"[OK] Range: {args.range}")


if __name__ == "__main__":
    main()

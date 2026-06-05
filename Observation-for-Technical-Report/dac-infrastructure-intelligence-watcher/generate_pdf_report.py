#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak


PROJECT = "DAC Infrastructure Intelligence Watcher"
VERSION = "v1.8.0"

BASE_DIR = Path(__file__).resolve().parent
CUSTOM_DIR = BASE_DIR / "reports" / "generated" / "custom"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def clean(value):
    if value is None or value == "":
        return "N/A"
    return str(value).replace("—", "-").replace("–", "-")


def count_text(counts):
    if not counts:
        return "N/A"
    return ", ".join(f"{key}: {value}" for key, value in counts.items())


def para(value, style):
    return Paragraph(clean(value), style)


def make_table(rows, widths=None, repeat_rows=1):
    table = Table(rows, colWidths=widths, repeatRows=repeat_rows)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#10233d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.3),
        ("LEADING", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#0f172a")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(14 * mm, 10 * mm, "Made by JERUZZALEM - DAC Infra Tester")
    canvas.drawRightString(196 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(payload, output_path):
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0f172a"),
        alignment=TA_LEFT,
        spaceAfter=10,
    )

    heading_style = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=7,
    )

    body_style = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.6,
        leading=11,
        textColor=colors.HexColor("#334155"),
        spaceAfter=5,
    )

    small_style = ParagraphStyle(
        "SmallCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=7.2,
        leading=8.5,
        textColor=colors.HexColor("#334155"),
    )

    story = []
    summary = payload.get("summary", {})
    timeline = payload.get("timeline", [])

    story.append(Paragraph("DAC Infrastructure Intelligence Watcher - Custom Range Report", title_style))
    story.append(Paragraph(f"Range: <b>{clean(payload.get('range'))}</b>", body_style))
    story.append(Paragraph(f"Report layer version: <b>{clean(payload.get('report_layer_version'))}</b>", body_style))
    story.append(Paragraph(f"Generated at UTC: <b>{clean(payload.get('generated_at_utc'))}</b>", body_style))
    story.append(Paragraph("This portrait PDF is generated from the structured custom range JSON summary.", body_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Range Summary", heading_style))
    rows = [
        ["Field", "Value"],
        ["Project", PROJECT],
        ["Snapshot count", clean(summary.get("snapshot_count"))],
        ["First snapshot", clean(summary.get("first_snapshot"))],
        ["Latest snapshot", clean(summary.get("latest_snapshot"))],
        ["First checked at UTC", clean(summary.get("first_checked_at_utc"))],
        ["Latest checked at UTC", clean(summary.get("latest_checked_at_utc"))],
        ["Overall status counts", count_text(summary.get("overall_status_counts"))],
    ]
    story.append(make_table([[para(c, small_style) for c in row] for row in rows], widths=[45 * mm, 137 * mm]))
    story.append(Spacer(1, 7))

    story.append(Paragraph("2. Endpoint Status Counts", heading_style))
    endpoint_rows = [["Endpoint", "Status counts"]]
    for key, counts in summary.get("endpoint_status_counts", {}).items():
        endpoint_rows.append([key, count_text(counts)])
    story.append(make_table([[para(c, small_style) for c in row] for row in endpoint_rows], widths=[55 * mm, 127 * mm]))
    story.append(Spacer(1, 7))

    story.append(Paragraph("3. Response-Time Summary", heading_style))
    response_rows = [["Endpoint", "Average", "Max", "Response class counts"]]
    for key, item in summary.get("response_time_summary", {}).items():
        response_rows.append([
            key,
            f"{clean(item.get('average_response_ms'))} ms",
            f"{clean(item.get('max_response_ms'))} ms",
            count_text(item.get("response_class_counts")),
        ])
    story.append(make_table([[para(c, small_style) for c in row] for row in response_rows], widths=[48 * mm, 28 * mm, 28 * mm, 78 * mm]))
    story.append(PageBreak())

    story.append(Paragraph("4. Snapshot Timeline - Availability", heading_style))
    availability_rows = [["#", "Checked at UTC", "Overall", "RPC", "Web", "API"]]
    for item in timeline:
        availability_rows.append([
            clean(item.get("index")),
            clean(item.get("checked_at_utc")),
            clean(item.get("overall_status")),
            clean(item.get("official_public_rpc_status")),
            clean(item.get("explorer_web_status")),
            clean(item.get("primary_explorer_api_status")),
        ])
    story.append(make_table([[para(c, small_style) for c in row] for row in availability_rows], widths=[10 * mm, 62 * mm, 34 * mm, 28 * mm, 24 * mm, 24 * mm]))

    story.append(Spacer(1, 8))
    story.append(Paragraph("5. Snapshot Timeline - Response Classes", heading_style))
    class_rows = [["#", "Checked at UTC", "RPC class", "Web class", "API class", "RPC block"]]
    for item in timeline:
        story_block = item.get("rpc_latest_block_decimal") or item.get("rpc_latest_block_hex")
        class_rows.append([
            clean(item.get("index")),
            clean(item.get("checked_at_utc")),
            clean(item.get("official_public_rpc_response_class")),
            clean(item.get("explorer_web_response_class")),
            clean(item.get("primary_explorer_api_response_class")),
            clean(story_block),
        ])
    story.append(make_table([[para(c, small_style) for c in row] for row in class_rows], widths=[10 * mm, 62 * mm, 30 * mm, 30 * mm, 30 * mm, 20 * mm]))

    story.append(PageBreak())
    story.append(Paragraph("6. Interpretation Guide", heading_style))
    for note in payload.get("interpretation_guide", []):
        story.append(Paragraph(f"- {clean(note)}", body_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph(f"Prepared by <b>{clean(payload.get('prepared_by'))}</b>.", body_style))

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=14 * mm,
        leftMargin=14 * mm,
        topMargin=14 * mm,
        bottomMargin=16 * mm,
        title=f"{PROJECT} - {payload.get('range')} PDF Report",
        author="JERUZZALEM - DAC Infra Tester",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    parser = argparse.ArgumentParser(description="Generate PDF from DAC infrastructure custom range JSON report.")
    parser.add_argument("--range", choices=["7d", "30d", "all"], required=True)
    args = parser.parse_args()

    json_path = CUSTOM_DIR / f"infrastructure-report-{args.range}.json"
    output_path = CUSTOM_DIR / f"infrastructure-report-{args.range}.pdf"

    if not json_path.exists():
        raise SystemExit(f"Missing JSON input: {json_path}")

    payload = load_json(json_path)
    payload["pdf_generated_at_utc"] = datetime.now(timezone.utc).isoformat()

    build_pdf(payload, output_path)

    print("[OK] Infrastructure PDF report generated.")
    print(f"[OK] Range: {args.range}")
    print(f"[OK] Input: {json_path}")
    print(f"[OK] Output: {output_path}")


if __name__ == "__main__":
    main()

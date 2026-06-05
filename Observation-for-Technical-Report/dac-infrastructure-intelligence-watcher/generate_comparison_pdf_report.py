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
VERSION = "v1.8.1"

BASE_DIR = Path(__file__).resolve().parent
COMPARISON_DIR = BASE_DIR / "reports" / "generated" / "comparison"


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


def window_summary_rows(label, window, comparison):
    summary = window.get("summary", {})

    rows = [
        ["Field", label],
        ["Snapshot count", clean(summary.get("snapshot_count"))],
        ["Observation index range", f"{clean(summary.get('first_index'))} -> {clean(summary.get('latest_index'))}"],
        ["First checked at UTC", clean(summary.get("first_checked_at_utc"))],
        ["Latest checked at UTC", clean(summary.get("latest_checked_at_utc"))],
        ["Overall status counts", count_text(summary.get("overall_status_counts"))],
    ]

    if label == "Window A":
        rows.append(["Availability score", clean(comparison.get("availability_score_a"))])
    else:
        rows.append(["Availability score", clean(comparison.get("availability_score_b"))])

    return rows


def endpoint_comparison_rows(payload):
    summary_a = payload.get("window_a", {}).get("summary", {})
    summary_b = payload.get("window_b", {}).get("summary", {})

    rows = [["Endpoint", "Window A status", "Window B status", "A avg", "B avg"]]

    for key in ["official_public_rpc", "explorer_web", "primary_explorer_api"]:
        a_status = summary_a.get("endpoint_status_counts", {}).get(key, {})
        b_status = summary_b.get("endpoint_status_counts", {}).get(key, {})
        a_response = summary_a.get("endpoint_response_summary", {}).get(key, {}).get("average_response_ms")
        b_response = summary_b.get("endpoint_response_summary", {}).get(key, {}).get("average_response_ms")

        rows.append([
            key,
            count_text(a_status),
            count_text(b_status),
            f"{clean(a_response)} ms",
            f"{clean(b_response)} ms",
        ])

    return rows


def response_class_rows(payload):
    summary_a = payload.get("window_a", {}).get("summary", {})
    summary_b = payload.get("window_b", {}).get("summary", {})

    rows = [["Endpoint", "Window A classes", "Window B classes", "A max", "B max"]]

    for key in ["official_public_rpc", "explorer_web", "primary_explorer_api"]:
        a_item = summary_a.get("endpoint_response_summary", {}).get(key, {})
        b_item = summary_b.get("endpoint_response_summary", {}).get(key, {})

        rows.append([
            key,
            count_text(a_item.get("response_class_counts")),
            count_text(b_item.get("response_class_counts")),
            f"{clean(a_item.get('max_response_ms'))} ms",
            f"{clean(b_item.get('max_response_ms'))} ms",
        ])

    return rows


def timeline_rows(timeline):
    rows = [["#", "Checked at UTC", "Overall", "RPC", "RPC class", "Web", "API"]]

    for item in timeline:
        rows.append([
            clean(item.get("index")),
            clean(item.get("checked_at_utc")),
            clean(item.get("overall_status")),
            clean(item.get("official_public_rpc_status")),
            clean(item.get("official_public_rpc_response_class")),
            clean(item.get("explorer_web_status")),
            clean(item.get("primary_explorer_api_status")),
        ])

    return rows


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
    comparison = payload.get("comparison", {})

    story.append(Paragraph("DAC Infrastructure Intelligence Watcher - Observation Window Comparison", title_style))
    story.append(Paragraph(f"Comparison scope: <b>{clean(payload.get('comparison_scope'))}</b>", body_style))
    story.append(Paragraph(f"Comparison layer version: <b>{clean(payload.get('comparison_layer_version'))}</b>", body_style))
    story.append(Paragraph(f"Generated at UTC: <b>{clean(payload.get('generated_at_utc'))}</b>", body_style))
    story.append(Paragraph("This portrait PDF compares Window A and Window B infrastructure observation segments.", body_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Window Summary", heading_style))
    a_rows = window_summary_rows("Window A", payload.get("window_a", {}), comparison)
    b_rows = window_summary_rows("Window B", payload.get("window_b", {}), comparison)

    story.append(make_table([[para(c, small_style) for c in row] for row in a_rows], widths=[48 * mm, 134 * mm]))
    story.append(Spacer(1, 6))
    story.append(make_table([[para(c, small_style) for c in row] for row in b_rows], widths=[48 * mm, 134 * mm]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. Endpoint Availability and Response Comparison", heading_style))
    story.append(make_table(
        [[para(c, small_style) for c in row] for row in endpoint_comparison_rows(payload)],
        widths=[43 * mm, 45 * mm, 45 * mm, 24 * mm, 24 * mm],
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3. Response Class Comparison", heading_style))
    story.append(make_table(
        [[para(c, small_style) for c in row] for row in response_class_rows(payload)],
        widths=[43 * mm, 47 * mm, 47 * mm, 22 * mm, 22 * mm],
    ))

    story.append(PageBreak())

    story.append(Paragraph("4. Interpretation", heading_style))
    for note in comparison.get("interpretation", []):
        story.append(Paragraph(f"- {clean(note)}", body_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("5. Window A Timeline", heading_style))
    story.append(make_table(
        [[para(c, small_style) for c in row] for row in timeline_rows(payload.get("window_a", {}).get("timeline", []))],
        widths=[10 * mm, 58 * mm, 30 * mm, 25 * mm, 25 * mm, 17 * mm, 17 * mm],
    ))

    story.append(PageBreak())

    story.append(Paragraph("6. Window B Timeline", heading_style))
    story.append(make_table(
        [[para(c, small_style) for c in row] for row in timeline_rows(payload.get("window_b", {}).get("timeline", []))],
        widths=[10 * mm, 58 * mm, 30 * mm, 25 * mm, 25 * mm, 17 * mm, 17 * mm],
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("7. Interpretation Guide", heading_style))
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
        title=f"{PROJECT} - {payload.get('comparison_scope')} Comparison PDF",
        author="JERUZZALEM - DAC Infra Tester",
    )

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    parser = argparse.ArgumentParser(description="Generate PDF from DAC infrastructure comparison JSON report.")
    parser.add_argument("--range", choices=["7d", "30d", "all"], required=True)
    args = parser.parse_args()

    json_path = COMPARISON_DIR / f"infrastructure-comparison-{args.range}.json"
    output_path = COMPARISON_DIR / f"infrastructure-comparison-{args.range}.pdf"

    if not json_path.exists():
        raise SystemExit(f"Missing JSON input: {json_path}")

    payload = load_json(json_path)
    payload["pdf_generated_at_utc"] = datetime.now(timezone.utc).isoformat()

    build_pdf(payload, output_path)

    print("[OK] Infrastructure comparison PDF generated.")
    print(f"[OK] Scope: {args.range}")
    print(f"[OK] Input: {json_path}")
    print(f"[OK] Output: {output_path}")


if __name__ == "__main__":
    main()

from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def parse_markdown_lines(lines, base_dir):
    styles = getSampleStyleSheet()
    normal = ParagraphStyle(
        "Normal",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        spaceAfter=8,
    )
    heading1 = ParagraphStyle(
        "Heading1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        spaceBefore=12,
        spaceAfter=6,
    )
    heading2 = ParagraphStyle(
        "Heading2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=6,
    )
    quote = ParagraphStyle(
        "Quote",
        parent=styles["BodyText"],
        fontName="Helvetica-Oblique",
        fontSize=11,
        leading=14,
        leftIndent=10,
        textColor=colors.HexColor("#333333"),
        spaceAfter=8,
    )
    story = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\n")
        if not line.strip():
            story.append(Spacer(1, 8))
            i += 1
            continue

        if line.startswith("# "):
            story.append(Paragraph(line[2:].strip(), heading1))
            i += 1
            continue
        if line.startswith("## "):
            story.append(Paragraph(line[3:].strip(), heading2))
            i += 1
            continue

        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                text = lines[i].strip()[2:].replace("`", "")
                items.append(ListItem(Paragraph(text, normal), leftIndent=10))
                i += 1
            story.append(ListFlowable(items, bulletType="bullet", start="bullet"))
            continue

        if line.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            if len(table_lines) >= 2:
                rows = [
                    [cell.strip() for cell in row.strip("|").split("|")]
                    for row in table_lines
                ]
                if len(rows) > 1:
                    # Skip separator row if present
                    if all(set(cell) <= set("-:") for cell in rows[1]):
                        rows = [rows[0]] + rows[2:]
                    tbl = Table(rows, repeatRows=1, hAlign="LEFT")
                    tbl.setStyle(
                        TableStyle(
                            [
                                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                                ("TOPPADDING", (0, 0), (-1, -1), 4),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                            ]
                        )
                    )
                    story.append(tbl)
                    story.append(Spacer(1, 12))
            continue

        if line.startswith("![") and "](" in line and line.endswith(")"):
            alt_text = line[line.find("![") + 2:line.find("](")].strip()
            start = line.find("](") + 2
            image_path = line[start:-1]
            image_file = base_dir / image_path
            if image_file.exists():
                pil_img = PILImage.open(image_file)
                max_width = 6.5 * inch
                max_height = 7.5 * inch
                width, height = pil_img.size
                ratio = min(max_width / width, max_height / height, 1)
                img_width = width * ratio
                img_height = height * ratio
                img = Image(str(image_file), width=img_width, height=img_height)
                img.hAlign = "CENTER"
                story.append(img)
            story.append(Paragraph(alt_text, ParagraphStyle("Caption", parent=normal, alignment=1, fontSize=10, textColor=colors.black)))
            story.append(Spacer(1, 10))
            i += 1
            continue

        if line.startswith("*") and line.endswith("*"):
            story.append(Paragraph(line.strip("*"), quote))
            i += 1
            continue

        # Replace markdown formatting tokens
        text = line.replace("`", "").replace("**", "").replace("*", "")
        text = text.replace("<br>", " ").replace("<br/>", " ").replace("<br />", " ")
        story.append(Paragraph(text, normal))
        i += 1
    return story


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    report_md = repo_root / "reports" / "final_report.md"
    pdf_out = repo_root / "reports" / "final_report.pdf"
    base_dir = report_md.parent

    lines = report_md.read_text(encoding="utf-8").splitlines()
    story = parse_markdown_lines(lines, base_dir)

    doc = SimpleDocTemplate(
        str(pdf_out),
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    doc.build(story)
    print(f"Generated PDF: {pdf_out}")


if __name__ == "__main__":
    main()

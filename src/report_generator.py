import os
from datetime import datetime

import pandas as pd
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from src.analysis import (
    build_priority_analysis,
    build_competitor_analysis,
    build_statistical_summary,
    build_research_source_analysis,
)


REPORTS_DIR = "reports"
CHARTS_DIR = "charts"


COLORS = {
    "dark_blue": "1F4E78",
    "blue": "2F75B5",
    "sky_blue": "00A2E8",
    "light_blue": "D9EAF7",
    "very_light_blue": "EAF3F8",
    "green": "00A65A",
    "dark_green": "0B6E0B",
    "light_green": "D9EAD3",
    "orange": "E69138",
    "light_orange": "FCE5CD",
    "red": "E31B23",
    "light_red": "F4CCCC",
    "yellow": "FFF2CC",
    "gray": "6C7A89",
    "light_gray": "D9E2F3",
    "white": "FFFFFF",
    "black": "000000",
}


def ensure_reports_dir():
    os.makedirs(REPORTS_DIR, exist_ok=True)


def create_border():
    return Border(
        left=Side(style="thin", color="B7C9D6"),
        right=Side(style="thin", color="B7C9D6"),
        top=Side(style="thin", color="B7C9D6"),
        bottom=Side(style="thin", color="B7C9D6"),
    )


def style_title(ws, title, subtitle, start_col=1, end_col=8):
    ws.merge_cells(start_row=1, start_column=start_col, end_row=1, end_column=end_col)
    ws.merge_cells(start_row=2, start_column=start_col, end_row=2, end_column=end_col)

    title_cell = ws.cell(row=1, column=start_col)
    subtitle_cell = ws.cell(row=2, column=start_col)

    title_cell.value = title
    subtitle_cell.value = subtitle

    title_cell.fill = PatternFill("solid", fgColor=COLORS["dark_blue"])
    title_cell.font = Font(color=COLORS["white"], bold=True, size=16)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    subtitle_cell.fill = PatternFill("solid", fgColor=COLORS["blue"])
    subtitle_cell.font = Font(color=COLORS["white"], bold=True, italic=True, size=10)
    subtitle_cell.alignment = Alignment(horizontal="center", vertical="center")

    ws.row_dimensions[1].height = 28
    ws.row_dimensions[2].height = 22


def style_headers(ws, header_row, start_col, end_col, fill_color=None):
    fill_color = fill_color or COLORS["dark_blue"]

    for col in range(start_col, end_col + 1):
        cell = ws.cell(row=header_row, column=col)
        cell.fill = PatternFill("solid", fgColor=fill_color)
        cell.font = Font(color=COLORS["white"], bold=True, size=10)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = create_border()


def style_body(ws, min_row, max_row, min_col, max_col, fill_alternate=True):
    for row in range(min_row, max_row + 1):
        fill = COLORS["very_light_blue"] if row % 2 == 0 else COLORS["white"]

        for col in range(min_col, max_col + 1):
            cell = ws.cell(row=row, column=col)

            if fill_alternate:
                cell.fill = PatternFill("solid", fgColor=fill)

            cell.border = create_border()
            cell.alignment = Alignment(vertical="top", wrap_text=True)


def auto_fit_columns(ws, min_width=10, max_width=32):
    for col_idx in range(1, ws.max_column + 1):
        col_letter = get_column_letter(col_idx)
        max_length = 0

        for row_idx in range(1, ws.max_row + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            value = cell.value

            if value is None:
                continue

            text = str(value)
            if len(text) > max_length:
                max_length = len(text)

        ws.column_dimensions[col_letter].width = min(
            max(max_length + 2, min_width),
            max_width,
        )


def write_dataframe(ws, df, start_row, start_col, header_color=None):
    if df is None or df.empty:
        ws.cell(start_row, start_col).value = "No data available"
        return start_row + 2

    for col_idx, column_name in enumerate(df.columns, start=start_col):
        ws.cell(row=start_row, column=col_idx).value = column_name

    style_headers(
        ws,
        header_row=start_row,
        start_col=start_col,
        end_col=start_col + len(df.columns) - 1,
        fill_color=header_color or COLORS["dark_blue"],
    )

    for row_idx, row in enumerate(df.itertuples(index=False), start=start_row + 1):
        for col_idx, value in enumerate(row, start=start_col):
            ws.cell(row=row_idx, column=col_idx).value = value

    end_row = start_row + len(df)
    end_col = start_col + len(df.columns) - 1

    style_body(ws, start_row + 1, end_row, start_col, end_col)
    auto_fit_columns(ws)

    return end_row + 3


def apply_priority_colors(ws):
    priority_colors = {
        "Critical": COLORS["red"],
        "High": COLORS["orange"],
        "Medium": COLORS["green"],
        "Low": COLORS["gray"],
    }

    for row in range(1, ws.max_row + 1):
        for col in range(1, ws.max_column + 1):
            value = ws.cell(row=row, column=col).value

            if value in priority_colors:
                cell = ws.cell(row=row, column=col)
                cell.fill = PatternFill("solid", fgColor=priority_colors[value])
                cell.font = Font(color=COLORS["white"], bold=True)
                cell.alignment = Alignment(horizontal="center", vertical="center")


def create_metadata_sheet(wb, generated_at_str, output_file_name):
    ws = wb.create_sheet("Report Metadata", 0)

    style_title(
        ws,
        "Technology Market Intelligence Report Metadata",
        "Report generation details and execution context",
        start_col=1,
        end_col=4,
    )

    rows = [
        ("Generated Date & Time", generated_at_str),
        ("Report File Name", output_file_name),
        ("Generated By", "Technology Research & Market Intelligence Analysis System"),
        ("Report Type", "Professional Excel Intelligence Report"),
    ]

    start_row = 4
    ws.cell(start_row, 1).value = "Field"
    ws.cell(start_row, 2).value = "Value"
    style_headers(ws, start_row, 1, 2)

    for index, (field, value) in enumerate(rows, start=start_row + 1):
        ws.cell(index, 1).value = field
        ws.cell(index, 2).value = value

    style_body(ws, start_row + 1, start_row + len(rows), 1, 2)
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 60


def create_executive_dashboard(
    wb,
    analysis_df,
    category_summary,
    top10_df,
    statistical_summary_df,
    generated_at_str,
    output_file_name,
):
    ws = wb.create_sheet("Executive Dashboard")

    style_title(
        ws,
        "Technology Market Intelligence — Executive Dashboard",
        f"Generated on: {generated_at_str}",
        start_col=1,
        end_col=8,
    )

    stats = statistical_summary_df.iloc[0].to_dict()

    kpis = [
        ("Total Technologies", stats.get("total_technologies", 0), COLORS["dark_blue"]),
        ("Avg Priority Score", stats.get("average_priority_score", 0), COLORS["blue"]),
        ("Avg Risk Score", stats.get("average_risk_score", 0), COLORS["red"]),
        ("Critical Priority", stats.get("critical_technologies", 0), COLORS["red"]),
        ("High Priority", stats.get("high_priority_technologies", 0), COLORS["orange"]),
        ("Medium Priority", stats.get("medium_priority_technologies", 0), COLORS["green"]),
        ("Low Priority", stats.get("low_priority_technologies", 0), COLORS["gray"]),
        ("Adoption Correlation", stats.get("adoption_priority_correlation", 0), COLORS["sky_blue"]),
    ]

    start_row = 4

    for index, (label, value, color) in enumerate(kpis, start=1):
        label_cell = ws.cell(row=start_row, column=index)
        label_cell.value = label
        label_cell.fill = PatternFill("solid", fgColor=color)
        label_cell.font = Font(color=COLORS["white"], bold=True, size=9)
        label_cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        label_cell.border = create_border()

        value_cell = ws.cell(row=start_row + 1, column=index)
        value_cell.value = value
        value_cell.fill = PatternFill("solid", fgColor=COLORS["light_blue"])
        value_cell.font = Font(color=color, bold=True, size=14)
        value_cell.alignment = Alignment(horizontal="center", vertical="center")
        value_cell.border = create_border()

        col_letter = get_column_letter(index)
        ws.column_dimensions[col_letter].width = 18

    ws.cell(row=7, column=1).value = "Category Performance Summary"
    ws.cell(row=7, column=1).font = Font(bold=True, color=COLORS["dark_blue"], size=12)

    dashboard_category = category_summary[
        [
            "category",
            "total_technologies",
            "average_priority_score",
            "average_risk_score",
            "average_product_impact",
            "average_adoption_potential",
        ]
    ].copy()

    dashboard_category.columns = [
        "Category",
        "Technologies",
        "Avg Priority",
        "Avg Risk",
        "Avg Impact",
        "Avg Adoption",
    ]

    next_row = write_dataframe(
        ws,
        dashboard_category.head(12),
        start_row=8,
        start_col=1,
    )

    ws.cell(row=next_row, column=1).value = "Top 10 Priority Technologies"
    ws.cell(row=next_row, column=1).font = Font(
        bold=True, color=COLORS["dark_blue"], size=12
    )

    dashboard_top = top10_df[
        [
            "technology_name",
            "category",
            "final_priority_score",
            "priority_level",
            "recommendation",
        ]
    ].copy()

    dashboard_top.columns = [
        "Technology Name",
        "Category",
        "Priority Score",
        "Level",
        "Recommendation",
    ]

    write_dataframe(
        ws,
        dashboard_top,
        start_row=next_row + 1,
        start_col=1,
        header_color=COLORS["sky_blue"],
    )

    ws["G4"] = "Latest Report File"
    ws["G4"].font = Font(bold=True, color=COLORS["dark_blue"])
    ws["G5"] = output_file_name
    ws["G5"].alignment = Alignment(wrap_text=True)

    ws.column_dimensions["E"].width = 70
    apply_priority_colors(ws)


def create_priority_report(wb, priority_report, generated_at_str):
    ws = wb.create_sheet("Priority Report")

    style_title(
        ws,
        "Technology Priority Report",
        f"Generated on: {generated_at_str}",
        start_col=1,
        end_col=15,
    )

    df = priority_report.copy()
    df.columns = [
        "Technology ID",
        "Technology Name",
        "Category",
        "Expected Release Date",
        "Product Impact Score",
        "Adoption Potential Score",
        "Market Readiness Score",
        "R&D Investment Score",
        "Risk Score",
        "Competitor Activity Score",
        "Research Reliability Score",
        "Patent Reference Count",
        "Final Priority Score",
        "Priority Level",
        "Recommendation",
    ]

    write_dataframe(ws, df, start_row=3, start_col=1)
    ws.column_dimensions["B"].width = 36
    ws.column_dimensions["O"].width = 80
    apply_priority_colors(ws)


def create_competitor_analysis_sheet(wb, competitor_summary_df, generated_at_str):
    ws = wb.create_sheet("Competitor Analysis")

    style_title(
        ws,
        "Competitor Activity Analysis",
        f"Generated on: {generated_at_str}",
        start_col=1,
        end_col=9,
    )

    df = competitor_summary_df.copy()
    df.columns = [
        "Competitor Name",
        "Total Tracked Technologies",
        "Average Market Activity Score",
        "Adopted Count",
        "Pilot Count",
        "Research Count",
        "Not Adopted Count",
        "High Investment Count",
        "Adoption Rate Percentage",
    ]

    write_dataframe(ws, df, start_row=3, start_col=1)


def create_research_sources_sheet(wb, sources_df, generated_at_str):
    ws = wb.create_sheet("Research Sources")

    style_title(
        ws,
        "Research Sources Intelligence",
        f"Generated on: {generated_at_str}",
        start_col=1,
        end_col=10,
    )

    df = sources_df.copy().head(100)
    df.columns = [
        "Source ID",
        "Technology ID",
        "Source Type",
        "Source Name",
        "Source URL",
        "Research Summary",
        "Reliability Score",
        "Technology Maturity Level",
        "Patent Office",
        "Filing Year",
    ]

    write_dataframe(ws, df, start_row=3, start_col=1)
    ws.column_dimensions["D"].width = 34
    ws.column_dimensions["E"].width = 34
    ws.column_dimensions["F"].width = 55


def create_statistical_summary_sheet(wb, statistical_summary_df, generated_at_str):
    ws = wb.create_sheet("Statistical Summary")

    style_title(
        ws,
        "Statistical Summary & Key Metrics",
        f"Generated on: {generated_at_str}",
        start_col=1,
        end_col=4,
    )

    stats = statistical_summary_df.iloc[0].to_dict()
    rows = list(stats.items())

    df = pd.DataFrame(rows, columns=["Metric", "Value"])
    write_dataframe(ws, df, start_row=3, start_col=1)
    ws.column_dimensions["A"].width = 36
    ws.column_dimensions["B"].width = 42


def create_visual_charts_sheet(wb, generated_at_str):
    ws = wb.create_sheet("Visual Charts")

    style_title(
        ws,
        "Python Visualization Gallery",
        f"Generated on: {generated_at_str}",
        start_col=1,
        end_col=10,
    )

    chart_files = [
        ("charts/top_technologies.png", "Top Technologies by Priority Score"),
        ("charts/category_trends.png", "Category-wise Technology Trends"),
        ("charts/competitor_activity.png", "Competitor Activity Comparison"),
        ("charts/risk_distribution.png", "Risk Distribution"),
        ("charts/research_source_distribution.png", "Research Source Distribution"),
        ("charts/patent_reference_count.png", "Patent Reference Count"),
        ("charts/release_timeline.png", "Release Timeline"),
        ("charts/risk_vs_priority.png", "Risk vs Priority Scatter Plot"),
        ("charts/patent_office_distribution.png", "Patent Office Distribution"),
        ("charts/literature_source_distribution.png", "Literature Source Distribution"),
    ]

    positions = [
        ("A4", "A3"),
        ("J4", "J3"),
        ("A27", "A26"),
        ("J27", "J26"),
        ("A50", "A49"),
        ("J50", "J49"),
        ("A73", "A72"),
        ("J73", "J72"),
        ("A96", "A95"),
        ("J96", "J95"),
    ]

    for (chart_path, chart_title), (image_cell, title_cell) in zip(chart_files, positions):
        ws[title_cell] = chart_title
        ws[title_cell].font = Font(bold=True, color=COLORS["dark_blue"], size=12)

        if os.path.exists(chart_path):
            img = Image(chart_path)
            img.width = 560
            img.height = 300
            ws.add_image(img, image_cell)
        else:
            ws[image_cell] = f"Chart file not found: {chart_path}"

    for col_idx in range(1, 20):
        ws.column_dimensions[get_column_letter(col_idx)].width = 13


def generate_excel_report():
    ensure_reports_dir()

    generated_at = datetime.now()
    generated_at_str = generated_at.strftime("%d-%m-%Y %I:%M:%S %p")
    timestamp = generated_at.strftime("%Y%m%d_%H%M%S")

    output_file_name = f"technology_market_intelligence_report_{timestamp}.xlsx"
    output_file = os.path.join(REPORTS_DIR, output_file_name)

    (
        analysis_df,
        technologies_df,
        competitors_df,
        activity_df,
        sources_df,
    ) = build_priority_analysis()

    _, competitor_summary_df = build_competitor_analysis(
        activity_df, competitors_df, technologies_df
    )

    statistical_summary_df = build_statistical_summary(analysis_df)

    # Agar function 7 values return kare ya 8, dono safe
    research_outputs = build_research_source_analysis(sources_df, technologies_df)

    priority_report = analysis_df[
        [
            "technology_id",
            "technology_name",
            "category",
            "expected_release_date",
            "product_impact_score",
            "adoption_potential_score",
            "market_readiness_score",
            "rd_investment_score",
            "risk_score",
            "competitor_activity_score",
            "research_reliability_score",
            "patent_reference_count",
            "final_priority_score",
            "priority_level",
            "recommendation",
        ]
    ].sort_values("final_priority_score", ascending=False)

    category_summary = (
        analysis_df.groupby("category")
        .agg(
            total_technologies=("technology_id", "count"),
            average_priority_score=("final_priority_score", "mean"),
            average_risk_score=("risk_score", "mean"),
            average_product_impact=("product_impact_score", "mean"),
            average_adoption_potential=("adoption_potential_score", "mean"),
        )
        .reset_index()
        .sort_values("average_priority_score", ascending=False)
    )

    for col in [
        "average_priority_score",
        "average_risk_score",
        "average_product_impact",
        "average_adoption_potential",
    ]:
        category_summary[col] = category_summary[col].round(2)

    wb = Workbook()
    default_sheet = wb.active
    wb.remove(default_sheet)

    create_metadata_sheet(wb, generated_at_str, output_file_name)
    create_executive_dashboard(
        wb,
        analysis_df,
        category_summary,
        priority_report.head(10),
        statistical_summary_df,
        generated_at_str,
        output_file_name,
    )
    create_priority_report(wb, priority_report, generated_at_str)
    create_competitor_analysis_sheet(wb, competitor_summary_df, generated_at_str)
    create_research_sources_sheet(wb, sources_df, generated_at_str)
    create_statistical_summary_sheet(wb, statistical_summary_df, generated_at_str)
    create_visual_charts_sheet(wb, generated_at_str)

    wb.save(output_file)

    print(f"Professional Excel report generated successfully: {output_file}")
    return output_file
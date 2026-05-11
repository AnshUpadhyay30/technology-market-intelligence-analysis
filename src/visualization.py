import os
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from src.analysis import build_priority_analysis, build_competitor_analysis


CHARTS_DIR = "charts"


def ensure_charts_dir():
    os.makedirs(CHARTS_DIR, exist_ok=True)


def generate_top_technologies_chart(analysis_df):
    top_df = analysis_df.sort_values("final_priority_score", ascending=False).head(10)

    plt.figure(figsize=(12, 7))
    plt.barh(top_df["technology_name"], top_df["final_priority_score"])
    plt.xlabel("Final Priority Score")
    plt.ylabel("Technology")
    plt.title("Top 10 Technologies by Priority Score")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/top_technologies.png")
    plt.close()


def generate_category_trends_chart(analysis_df):
    category_df = (
        analysis_df.groupby("category")["final_priority_score"]
        .mean()
        .reset_index()
        .sort_values("final_priority_score", ascending=False)
    )

    plt.figure(figsize=(11, 6))
    plt.bar(category_df["category"], category_df["final_priority_score"])
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Technology Category")
    plt.ylabel("Average Priority Score")
    plt.title("Category-wise Average Priority Score")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/category_trends.png")
    plt.close()


def generate_competitor_activity_chart(activity_df, competitors_df, technologies_df):
    _, competitor_summary_df = build_competitor_analysis(
        activity_df, competitors_df, technologies_df
    )

    competitor_summary_df = competitor_summary_df.sort_values(
        "average_market_activity_score", ascending=False
    )

    plt.figure(figsize=(10, 6))
    plt.bar(
        competitor_summary_df["competitor_name"],
        competitor_summary_df["average_market_activity_score"],
    )
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Competitor")
    plt.ylabel("Average Market Activity Score")
    plt.title("Competitor Activity Comparison")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/competitor_activity.png")
    plt.close()


def generate_risk_distribution_chart(analysis_df):
    risk_bins = {
        "Low Risk": (analysis_df["risk_score"] <= 3).sum(),
        "Medium Risk": (
            (analysis_df["risk_score"] >= 4) & (analysis_df["risk_score"] <= 6)
        ).sum(),
        "High Risk": (analysis_df["risk_score"] >= 7).sum(),
    }

    plt.figure(figsize=(8, 8))
    plt.pie(
        risk_bins.values(),
        labels=risk_bins.keys(),
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.title("Risk Level Distribution")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/risk_distribution.png")
    plt.close()


def generate_source_type_chart(sources_df):
    source_df = (
        sources_df.groupby("source_type")["source_id"]
        .count()
        .reset_index()
        .rename(columns={"source_id": "total_sources"})
        .sort_values("total_sources", ascending=False)
    )

    plt.figure(figsize=(11, 6))
    plt.bar(source_df["source_type"], source_df["total_sources"])
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Research Source Type")
    plt.ylabel("Total Sources")
    plt.title("Research Source Type Distribution")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/research_source_distribution.png")
    plt.close()


def generate_patent_reference_chart(sources_df, technologies_df):
    patent_df = sources_df[sources_df["source_type"] == "Patent Reference"]

    if patent_df.empty:
        return

    patent_summary = (
        patent_df.groupby("technology_id")["source_id"]
        .count()
        .reset_index()
        .rename(columns={"source_id": "patent_reference_count"})
        .merge(
            technologies_df[["technology_id", "technology_name"]],
            on="technology_id",
            how="left",
        )
        .sort_values("patent_reference_count", ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12, 7))
    plt.barh(
        patent_summary["technology_name"],
        patent_summary["patent_reference_count"],
    )
    plt.xlabel("Patent Reference Count")
    plt.ylabel("Technology")
    plt.title("Top Technologies by Patent Reference Count")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/patent_reference_count.png")
    plt.close()


def generate_release_timeline_chart(analysis_df):
    timeline_df = analysis_df.copy()
    timeline_df["expected_release_date"] = pd.to_datetime(
        timeline_df["expected_release_date"]
    )
    timeline_df["release_month"] = (
        timeline_df["expected_release_date"].dt.to_period("M").astype(str)
    )

    monthly_release_df = (
        timeline_df.groupby("release_month")["technology_id"]
        .count()
        .reset_index()
        .rename(columns={"technology_id": "technology_count"})
        .sort_values("release_month")
    )

    plt.figure(figsize=(12, 6))
    plt.plot(
        monthly_release_df["release_month"],
        monthly_release_df["technology_count"],
        marker="o",
    )
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Release Month")
    plt.ylabel("Number of Technologies")
    plt.title("Monthly Emerging Technology Release Timeline")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/release_timeline.png")
    plt.close()


def generate_risk_vs_priority_scatter(analysis_df):
    plt.figure(figsize=(10, 6))
    plt.scatter(
        analysis_df["risk_score"],
        analysis_df["final_priority_score"],
        alpha=0.7,
    )
    plt.xlabel("Risk Score")
    plt.ylabel("Final Priority Score")
    plt.title("Risk Score vs Priority Score")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/risk_vs_priority.png")
    plt.close()


def generate_patent_office_chart(sources_df):
    patent_df = sources_df[sources_df["source_type"] == "Patent Reference"]

    if patent_df.empty:
        return

    office_df = (
        patent_df.groupby("patent_office")["source_id"]
        .count()
        .reset_index()
        .rename(columns={"source_id": "total_patents"})
        .sort_values("total_patents", ascending=False)
    )

    plt.figure(figsize=(10, 6))
    plt.bar(office_df["patent_office"], office_df["total_patents"])
    plt.xlabel("Patent Office")
    plt.ylabel("Total Patent References")
    plt.title("Patent References by Patent Office")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/patent_office_distribution.png")
    plt.close()


def generate_literature_analysis_chart(sources_df):
    literature_df = sources_df[
        sources_df["source_type"].isin(["Academic Literature", "Industry White Paper"])
    ]

    if literature_df.empty:
        return

    literature_summary = (
        literature_df.groupby("source_type")["source_id"]
        .count()
        .reset_index()
        .rename(columns={"source_id": "total_literature"})
    )

    plt.figure(figsize=(8, 6))
    plt.bar(literature_summary["source_type"], literature_summary["total_literature"])
    plt.xlabel("Literature Source Type")
    plt.ylabel("Total Literature Sources")
    plt.title("Academic Literature and White Paper Distribution")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/literature_source_distribution.png")
    plt.close()


def generate_all_visualizations():
    ensure_charts_dir()

    (
        analysis_df,
        technologies_df,
        competitors_df,
        activity_df,
        sources_df,
    ) = build_priority_analysis()

    generate_top_technologies_chart(analysis_df)
    generate_category_trends_chart(analysis_df)
    generate_competitor_activity_chart(activity_df, competitors_df, technologies_df)
    generate_risk_distribution_chart(analysis_df)
    generate_source_type_chart(sources_df)
    generate_patent_reference_chart(sources_df, technologies_df)
    generate_release_timeline_chart(analysis_df)
    generate_risk_vs_priority_scatter(analysis_df)
    generate_patent_office_chart(sources_df)
    generate_literature_analysis_chart(sources_df)

    print("Python visualizations generated successfully in charts folder.")
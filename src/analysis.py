from datetime import datetime

import pandas as pd

from src.db_connection import get_connection


def get_release_urgency_score(expected_release_date):
    today = datetime.today().date()
    release_date = pd.to_datetime(expected_release_date).date()
    days_left = (release_date - today).days

    if days_left <= 30:
        return 10
    if days_left <= 60:
        return 8
    if days_left <= 90:
        return 6
    if days_left <= 180:
        return 5
    return 4


def get_priority_level(score):
    if score >= 38:
        return "Critical"
    if score >= 30:
        return "High"
    if score >= 22:
        return "Medium"
    return "Low"


def get_recommendation(row):
    if row["priority_level"] == "Critical":
        return (
            "Immediate R&D evaluation recommended due to strong competitor activity, "
            "high market readiness, product impact, and research signals."
        )

    if row["priority_level"] == "High":
        return (
            "Prioritize for roadmap planning, competitor benchmarking, and technology evaluation."
        )

    if row["priority_level"] == "Medium":
        return (
            "Monitor market adoption and evaluate based on product roadmap and maturity level."
        )

    return "Low priority; continue tracking for long-term technology relevance."


def fetch_data_from_mysql():
    connection = get_connection()

    technologies_df = pd.read_sql("SELECT * FROM technologies", connection)
    competitors_df = pd.read_sql("SELECT * FROM competitors", connection)
    activity_df = pd.read_sql("SELECT * FROM competitor_activity", connection)
    sources_df = pd.read_sql("SELECT * FROM research_sources", connection)

    connection.close()

    return technologies_df, competitors_df, activity_df, sources_df


def build_priority_analysis():
    technologies_df, competitors_df, activity_df, sources_df = fetch_data_from_mysql()

    competitor_score_df = (
        activity_df.groupby("technology_id")["market_activity_score"]
        .mean()
        .reset_index()
        .rename(columns={"market_activity_score": "competitor_activity_score"})
    )

    research_score_df = (
        sources_df.groupby("technology_id")["reliability_score"]
        .mean()
        .reset_index()
        .rename(columns={"reliability_score": "research_reliability_score"})
    )

    patent_count_df = (
        sources_df[sources_df["source_type"] == "Patent Reference"]
        .groupby("technology_id")["source_id"]
        .count()
        .reset_index()
        .rename(columns={"source_id": "patent_reference_count"})
    )

    literature_count_df = (
        sources_df[
            sources_df["source_type"].isin(
                ["Academic Literature", "Industry White Paper"]
            )
        ]
        .groupby("technology_id")["source_id"]
        .count()
        .reset_index()
        .rename(columns={"source_id": "literature_reference_count"})
    )

    analysis_df = (
        technologies_df.merge(competitor_score_df, on="technology_id", how="left")
        .merge(research_score_df, on="technology_id", how="left")
        .merge(patent_count_df, on="technology_id", how="left")
        .merge(literature_count_df, on="technology_id", how="left")
    )

    analysis_df["competitor_activity_score"] = analysis_df[
        "competitor_activity_score"
    ].fillna(0)
    analysis_df["research_reliability_score"] = analysis_df[
        "research_reliability_score"
    ].fillna(0)
    analysis_df["patent_reference_count"] = analysis_df[
        "patent_reference_count"
    ].fillna(0)
    analysis_df["literature_reference_count"] = analysis_df[
        "literature_reference_count"
    ].fillna(0)

    analysis_df["release_urgency_score"] = analysis_df["expected_release_date"].apply(
        get_release_urgency_score
    )

    analysis_df["final_priority_score"] = (
        analysis_df["competitor_activity_score"]
        + analysis_df["product_impact_score"]
        + analysis_df["adoption_potential_score"]
        + analysis_df["market_readiness_score"]
        + analysis_df["release_urgency_score"]
        + (analysis_df["research_reliability_score"] / 2)
        + (analysis_df["patent_reference_count"] * 0.4)
        + (analysis_df["literature_reference_count"] * 0.3)
        - analysis_df["risk_score"]
    ).round(2)

    analysis_df["priority_level"] = analysis_df["final_priority_score"].apply(
        get_priority_level
    )
    analysis_df["recommendation"] = analysis_df.apply(get_recommendation, axis=1)

    return analysis_df, technologies_df, competitors_df, activity_df, sources_df


def build_competitor_analysis(activity_df, competitors_df, technologies_df):
    merged_df = (
        activity_df.merge(competitors_df, on="competitor_id", how="left")
        .merge(
            technologies_df[["technology_id", "technology_name", "category"]],
            on="technology_id",
            how="left",
        )
    )

    competitor_summary = (
        merged_df.groupby("competitor_name")
        .agg(
            total_tracked_technologies=("technology_id", "count"),
            average_market_activity_score=("market_activity_score", "mean"),
            adopted_count=("adoption_status", lambda x: (x == "Adopted").sum()),
            pilot_count=("adoption_status", lambda x: (x == "Pilot").sum()),
            research_count=("adoption_status", lambda x: (x == "Research").sum()),
            not_adopted_count=("adoption_status", lambda x: (x == "Not Adopted").sum()),
            high_investment_count=("investment_level", lambda x: (x == "High").sum()),
        )
        .reset_index()
    )

    competitor_summary["average_market_activity_score"] = competitor_summary[
        "average_market_activity_score"
    ].round(2)

    competitor_summary["adoption_rate_percentage"] = (
        competitor_summary["adopted_count"]
        / competitor_summary["total_tracked_technologies"]
        * 100
    ).round(2)

    return merged_df, competitor_summary


def build_statistical_summary(analysis_df):
    correlation_value = analysis_df["adoption_potential_score"].corr(
        analysis_df["final_priority_score"]
    )

    summary = {
        "total_technologies": len(analysis_df),
        "average_priority_score": round(analysis_df["final_priority_score"].mean(), 2),
        "average_risk_score": round(analysis_df["risk_score"].mean(), 2),
        "average_market_readiness_score": round(
            analysis_df["market_readiness_score"].mean(), 2
        ),
        "average_adoption_potential_score": round(
            analysis_df["adoption_potential_score"].mean(), 2
        ),
        "critical_technologies": int(
            (analysis_df["priority_level"] == "Critical").sum()
        ),
        "high_priority_technologies": int(
            (analysis_df["priority_level"] == "High").sum()
        ),
        "medium_priority_technologies": int(
            (analysis_df["priority_level"] == "Medium").sum()
        ),
        "low_priority_technologies": int(
            (analysis_df["priority_level"] == "Low").sum()
        ),
        "highest_priority_technology": analysis_df.sort_values(
            "final_priority_score", ascending=False
        ).iloc[0]["technology_name"],
        "adoption_priority_correlation": round(correlation_value, 2),
    }

    return pd.DataFrame([summary])


def build_research_source_analysis(sources_df, technologies_df):
    merged_df = sources_df.merge(
        technologies_df[["technology_id", "technology_name", "category"]],
        on="technology_id",
        how="left",
    )

    source_type_summary = (
        merged_df.groupby("source_type")
        .agg(
            total_sources=("source_id", "count"),
            average_reliability_score=("reliability_score", "mean"),
        )
        .reset_index()
        .sort_values("total_sources", ascending=False)
    )
    source_type_summary["average_reliability_score"] = source_type_summary[
        "average_reliability_score"
    ].round(2)

    patent_df = merged_df[merged_df["source_type"] == "Patent Reference"].copy()

    patent_summary = (
        patent_df.groupby(["technology_id", "technology_name", "category"])
        .agg(
            patent_reference_count=("source_id", "count"),
            average_patent_reliability=("reliability_score", "mean"),
        )
        .reset_index()
        .sort_values("patent_reference_count", ascending=False)
    )

    if not patent_summary.empty:
        patent_summary["average_patent_reliability"] = patent_summary[
            "average_patent_reliability"
        ].round(2)

    maturity_summary = (
        merged_df.groupby("technology_maturity_level")
        .agg(
            total_sources=("source_id", "count"),
            average_reliability_score=("reliability_score", "mean"),
        )
        .reset_index()
        .sort_values("total_sources", ascending=False)
    )
    maturity_summary["average_reliability_score"] = maturity_summary[
        "average_reliability_score"
    ].round(2)

    patent_office_summary = (
        patent_df[patent_df["patent_office"].notna()]
        .groupby("patent_office")
        .agg(
            total_patents=("source_id", "count"),
            average_reliability=("reliability_score", "mean"),
        )
        .reset_index()
        .sort_values("total_patents", ascending=False)
    )

    if not patent_office_summary.empty:
        patent_office_summary["average_reliability"] = patent_office_summary[
            "average_reliability"
        ].round(2)

    literature_summary = (
        merged_df[
            merged_df["source_type"].isin(
                ["Academic Literature", "Industry White Paper"]
            )
        ]
        .groupby(["source_type", "category"])
        .agg(
            total_literature=("source_id", "count"),
            average_reliability=("reliability_score", "mean"),
        )
        .reset_index()
        .sort_values("total_literature", ascending=False)
    )

    if not literature_summary.empty:
        literature_summary["average_reliability"] = literature_summary[
            "average_reliability"
        ].round(2)

    patent_year_trend = (
        patent_df[patent_df["filing_year"].notna()]
        .groupby("filing_year")
        .agg(
            total_patents=("source_id", "count"),
            average_reliability=("reliability_score", "mean"),
        )
        .reset_index()
        .sort_values("filing_year")
    )

    if not patent_year_trend.empty:
        patent_year_trend["average_reliability"] = patent_year_trend[
            "average_reliability"
        ].round(2)

    category_patent_coverage = (
        patent_df.groupby("category")
        .agg(
            total_patents=("source_id", "count"),
            unique_technologies=("technology_id", "nunique"),
            average_reliability=("reliability_score", "mean"),
        )
        .reset_index()
        .sort_values("total_patents", ascending=False)
    )

    if not category_patent_coverage.empty:
        category_patent_coverage["average_reliability"] = category_patent_coverage[
            "average_reliability"
        ].round(2)

    technology_source_summary = (
        merged_df.groupby(["technology_id", "technology_name", "category"])
        .agg(
            total_research_sources=("source_id", "count"),
            average_reliability_score=("reliability_score", "mean"),
            patent_reference_count=(
                "source_type",
                lambda x: (x == "Patent Reference").sum(),
            ),
            literature_reference_count=(
                "source_type",
                lambda x: x.isin(["Academic Literature", "Industry White Paper"]).sum(),
            ),
        )
        .reset_index()
        .sort_values("total_research_sources", ascending=False)
    )

    technology_source_summary["average_reliability_score"] = (
        technology_source_summary["average_reliability_score"].round(2)
    )

    return (
        source_type_summary,
        patent_summary,
        maturity_summary,
        patent_office_summary,
        literature_summary,
        patent_year_trend,
        category_patent_coverage,
        technology_source_summary,
    )


def save_analysis_results_to_mysql(analysis_df):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM analysis_results")

        insert_query = """
            INSERT INTO analysis_results (
                technology_id,
                competitor_activity_score,
                release_urgency_score,
                research_reliability_score,
                patent_reference_count,
                final_priority_score,
                priority_level,
                recommendation
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        for _, row in analysis_df.iterrows():
            cursor.execute(
                insert_query,
                (
                    int(row["technology_id"]),
                    float(row["competitor_activity_score"]),
                    int(row["release_urgency_score"]),
                    float(row["research_reliability_score"]),
                    int(row["patent_reference_count"]),
                    float(row["final_priority_score"]),
                    row["priority_level"],
                    row["recommendation"],
                ),
            )

        connection.commit()
        print("Analysis results saved into MySQL successfully.")

    except Exception as error:
        connection.rollback()
        print(f"Failed to save analysis results: {error}")

    finally:
        cursor.close()
        connection.close()
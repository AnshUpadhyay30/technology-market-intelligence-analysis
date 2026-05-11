import pandas as pd

from src.db_connection import get_connection


def clear_tables(cursor):
    cursor.execute("DELETE FROM analysis_results")
    cursor.execute("DELETE FROM research_sources")
    cursor.execute("DELETE FROM competitor_activity")
    cursor.execute("DELETE FROM competitors")
    cursor.execute("DELETE FROM technologies")


def load_technologies(cursor):
    df = pd.read_csv("data/technologies.csv")

    query = """
        INSERT INTO technologies (
            technology_id,
            technology_name,
            category,
            expected_release_date,
            product_impact_score,
            adoption_potential_score,
            risk_score,
            market_readiness_score,
            rd_investment_score,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        cursor.execute(
            query,
            (
                int(row["technology_id"]),
                row["technology_name"],
                row["category"],
                row["expected_release_date"],
                int(row["product_impact_score"]),
                int(row["adoption_potential_score"]),
                int(row["risk_score"]),
                int(row["market_readiness_score"]),
                int(row["rd_investment_score"]),
                row["status"],
            ),
        )

    print("Technologies loaded successfully.")


def load_competitors(cursor):
    df = pd.read_csv("data/competitors.csv")

    query = """
        INSERT INTO competitors (
            competitor_id,
            competitor_name,
            country,
            industry_segment
        )
        VALUES (%s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        cursor.execute(
            query,
            (
                int(row["competitor_id"]),
                row["competitor_name"],
                row["country"],
                row["industry_segment"],
            ),
        )

    print("Competitors loaded successfully.")


def load_competitor_activity(cursor):
    df = pd.read_csv("data/competitor_activity.csv")

    query = """
        INSERT INTO competitor_activity (
            activity_id,
            competitor_id,
            technology_id,
            adoption_status,
            market_activity_score,
            launch_year,
            investment_level
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        cursor.execute(
            query,
            (
                int(row["activity_id"]),
                int(row["competitor_id"]),
                int(row["technology_id"]),
                row["adoption_status"],
                int(row["market_activity_score"]),
                int(row["launch_year"]),
                row["investment_level"],
            ),
        )

    print("Competitor activity loaded successfully.")


def clean_optional_value(value):
    if pd.isna(value):
        return None
    return value


def load_research_sources(cursor):
    df = pd.read_csv("data/research_sources.csv")

    query = """
        INSERT INTO research_sources (
            source_id,
            technology_id,
            source_type,
            source_name,
            source_url,
            research_summary,
            reliability_score,
            technology_maturity_level,
            patent_office,
            filing_year
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        filing_year = clean_optional_value(row["filing_year"])
        if filing_year is not None:
            filing_year = int(float(filing_year))

        cursor.execute(
            query,
            (
                int(row["source_id"]),
                int(row["technology_id"]),
                row["source_type"],
                row["source_name"],
                row["source_url"],
                row["research_summary"],
                int(row["reliability_score"]),
                row["technology_maturity_level"],
                clean_optional_value(row["patent_office"]),
                filing_year,
            ),
        )

    print("Research sources loaded successfully.")


def load_all_data():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        clear_tables(cursor)

        load_technologies(cursor)
        load_competitors(cursor)
        load_competitor_activity(cursor)
        load_research_sources(cursor)

        connection.commit()
        print("All CSV data loaded into MySQL successfully.")

    except Exception as error:
        connection.rollback()
        print(f"Data loading failed: {error}")

    finally:
        cursor.close()
        connection.close()
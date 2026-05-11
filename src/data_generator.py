import os
import random
from datetime import datetime, timedelta

import pandas as pd


DATA_DIR = "data"

TECH_CATEGORIES = [
    "AI",
    "IoT",
    "Smart Home",
    "Connectivity",
    "Energy Efficiency",
    "Security",
    "Display Technology",
    "Audio",
    "Home Appliance",
    "Automation",
    "Firmware",
    "Robotics",
    "Cloud Computing",
    "Edge Computing",
    "5G Integration",
    "Sustainability",
]

BASE_TECHNOLOGIES = [
    "AI Smart TV Recommendation",
    "Matter Smart Home Support",
    "Bluetooth 5.4",
    "Wi-Fi 7 Connectivity",
    "Energy Efficient Compressor",
    "AI Noise Cancellation",
    "Smart Diagnosis Feature",
    "Security Firmware Update",
    "Voice Assistant Integration",
    "Predictive Maintenance",
    "Mini LED Display Enhancement",
    "Smart Refrigerator Food Detection",
    "AI Washing Cycle Optimization",
    "Low Power IoT Sensor",
    "Edge AI Device Processing",
    "Smart Energy Monitoring",
    "Gesture Control Interface",
    "Cloud Connected Appliance",
    "Advanced OLED Panel",
    "Home Automation Gateway",
    "5G Enabled Smart Device",
    "AI-Powered HVAC Control",
    "Neural Processing Unit Integration",
    "Sustainable Energy Recovery",
    "Digital Twin Home Simulation",
    "Biometric Access Control",
    "Quantum Dot Display",
    "Self-Healing Firmware",
    "AR Appliance Interface",
    "AI-Based Fault Detection",
]

COMPETITORS = [
    ("LG", "South Korea", "Consumer Electronics"),
    ("Samsung", "South Korea", "Consumer Electronics"),
    ("Sony", "Japan", "Consumer Electronics"),
    ("Panasonic", "Japan", "Consumer Electronics"),
    ("Whirlpool", "USA", "Home Appliances"),
    ("Haier", "China", "Home Appliances"),
    ("Bosch", "Germany", "Home Appliances"),
    ("Xiaomi", "China", "Smart Devices"),
    ("Philips", "Netherlands", "Consumer Electronics"),
    ("Siemens", "Germany", "Home Appliances"),
    ("TCL", "China", "Consumer Electronics"),
    ("Hisense", "China", "Consumer Electronics"),
]

SOURCE_TYPES = [
    "Market Report",
    "Competitor Product Release",
    "Technical Article",
    "Patent Reference",
    "Vendor Documentation",
    "News Update",
    "Academic Literature",
    "Industry White Paper",
    "Standards Documentation",
]

MATURITY_LEVELS = ["Research", "Prototype", "Pilot", "Commercial", "Mature"]
ADOPTION_STATUS = ["Adopted", "Pilot", "Research", "Not Adopted"]

LITERATURE_TYPES = [
    "IEEE Research Paper",
    "ACM Conference Paper",
    "Journal Article",
    "Technical White Paper",
    "Industry Benchmark Study",
]

PATENT_OFFICES = ["USPTO", "EPO", "KIPO", "CNIPA", "JPO"]


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def generate_technologies(total_records=1000):
    rows = []
    today = datetime.today()

    for tech_id in range(1, total_records + 1):
        release_date = today + timedelta(days=random.randint(15, 730))

        rows.append(
            {
                "technology_id": tech_id,
                "technology_name": f"{random.choice(BASE_TECHNOLOGIES)} V{tech_id}",
                "category": random.choice(TECH_CATEGORIES),
                "expected_release_date": release_date.strftime("%Y-%m-%d"),
                "product_impact_score": random.randint(4, 10),
                "adoption_potential_score": random.randint(4, 10),
                "risk_score": random.randint(2, 9),
                "market_readiness_score": random.randint(1, 10),
                "rd_investment_score": random.randint(1, 10),
                "status": random.choice(["Upcoming", "Research", "Pilot", "Commercial"]),
            }
        )

    return pd.DataFrame(rows)


def generate_competitors():
    rows = []

    for competitor_id, competitor in enumerate(COMPETITORS, start=1):
        name, country, segment = competitor

        rows.append(
            {
                "competitor_id": competitor_id,
                "competitor_name": name,
                "country": country,
                "industry_segment": segment,
            }
        )

    return pd.DataFrame(rows)


def generate_competitor_activity(technologies_df, competitors_df):
    rows = []
    activity_id = 1

    for _, tech in technologies_df.iterrows():
        selected_competitors = competitors_df.sample(
            random.randint(4, len(competitors_df))
        )

        for _, competitor in selected_competitors.iterrows():
            rows.append(
                {
                    "activity_id": activity_id,
                    "competitor_id": int(competitor["competitor_id"]),
                    "technology_id": int(tech["technology_id"]),
                    "adoption_status": random.choice(ADOPTION_STATUS),
                    "market_activity_score": random.randint(3, 10),
                    "launch_year": random.choice([2024, 2025, 2026, 2027, 2028]),
                    "investment_level": random.choice(["Low", "Medium", "High"]),
                }
            )
            activity_id += 1

    return pd.DataFrame(rows)


def generate_research_sources(technologies_df):
    rows = []
    source_id = 1

    for _, tech in technologies_df.iterrows():
        number_of_sources = random.randint(4, 8)

        for _ in range(number_of_sources):
            source_type = random.choice(SOURCE_TYPES)
            patent_office = None
            filing_year = None

            if source_type == "Patent Reference":
                source_name = f"Patent Reference for {tech['technology_name']}"
                source_url = f"https://patents.example.com/{source_id}"
                summary = (
                    f"Patent reference related to {tech['technology_name']} "
                    "and possible technical implementation."
                )
                patent_office = random.choice(PATENT_OFFICES)
                filing_year = random.choice([2021, 2022, 2023, 2024])

            elif source_type == "Academic Literature":
                literature_type = random.choice(LITERATURE_TYPES)
                source_name = f"{literature_type}: {tech['technology_name']}"
                source_url = f"https://literature.example.com/paper/{source_id}"
                summary = (
                    f"Academic study analyzing technical feasibility, benchmarks, "
                    f"and research outcomes for {tech['technology_name']}."
                )
                filing_year = random.choice([2020, 2021, 2022, 2023, 2024])

            elif source_type == "Market Report":
                source_name = f"Market Report on {tech['technology_name']}"
                source_url = f"https://marketresearch.example.com/report/{source_id}"
                summary = (
                    f"Market research report covering adoption trends and "
                    f"commercial potential of {tech['technology_name']}."
                )

            elif source_type == "Technical Article":
                source_name = f"Technical Article for {tech['technology_name']}"
                source_url = f"https://techarticle.example.com/{source_id}"
                summary = (
                    f"Technical article explaining feasibility, challenges, "
                    f"and architecture of {tech['technology_name']}."
                )

            elif source_type == "Vendor Documentation":
                source_name = f"Vendor Documentation for {tech['technology_name']}"
                source_url = f"https://vendor.example.com/docs/{source_id}"
                summary = (
                    "Vendor documentation describing product integration "
                    "and technical specifications."
                )

            elif source_type == "Competitor Product Release":
                source_name = f"Competitor Release Note for {tech['technology_name']}"
                source_url = f"https://competitor.example.com/release/{source_id}"
                summary = "Competitor release information showing adoption and market activity."

            elif source_type == "Industry White Paper":
                source_name = f"White Paper: {tech['technology_name']} Industry Analysis"
                source_url = f"https://whitepaper.example.com/{source_id}"
                summary = (
                    f"Industry white paper covering strategic direction, use cases, "
                    f"and ROI analysis for {tech['technology_name']}."
                )

            elif source_type == "Standards Documentation":
                source_name = f"Standards Doc: {tech['technology_name']}"
                source_url = f"https://standards.example.com/{source_id}"
                summary = (
                    f"Standards body documentation defining compliance requirements "
                    f"and integration protocols for {tech['technology_name']}."
                )

            else:
                source_name = f"News Update for {tech['technology_name']}"
                source_url = f"https://news.example.com/update/{source_id}"
                summary = "News update related to market movement and technology adoption."

            rows.append(
                {
                    "source_id": source_id,
                    "technology_id": int(tech["technology_id"]),
                    "source_type": source_type,
                    "source_name": source_name,
                    "source_url": source_url,
                    "research_summary": summary,
                    "reliability_score": random.randint(5, 10),
                    "technology_maturity_level": random.choice(MATURITY_LEVELS),
                    "patent_office": patent_office,
                    "filing_year": filing_year,
                }
            )

            source_id += 1

    return pd.DataFrame(rows)


def generate_all_data():
    ensure_data_dir()

    technologies_df = generate_technologies(total_records=1000)
    competitors_df = generate_competitors()
    competitor_activity_df = generate_competitor_activity(technologies_df, competitors_df)
    research_sources_df = generate_research_sources(technologies_df)

    technologies_df.to_csv(f"{DATA_DIR}/technologies.csv", index=False)
    competitors_df.to_csv(f"{DATA_DIR}/competitors.csv", index=False)
    competitor_activity_df.to_csv(f"{DATA_DIR}/competitor_activity.csv", index=False)
    research_sources_df.to_csv(f"{DATA_DIR}/research_sources.csv", index=False)

    total_records = (
        len(technologies_df)
        + len(competitors_df)
        + len(competitor_activity_df)
        + len(research_sources_df)
    )

    print("Large sample datasets generated successfully.")
    print(f"Technologies: {len(technologies_df)}")
    print(f"Competitors: {len(competitors_df)}")
    print(f"Competitor activity records: {len(competitor_activity_df)}")
    print(f"Research source records: {len(research_sources_df)}")
    print(f"Total records generated: {total_records}")

    return technologies_df, competitors_df, competitor_activity_df, research_sources_df
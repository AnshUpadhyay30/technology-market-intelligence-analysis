DROP DATABASE IF EXISTS tech_market_intelligence_db;
CREATE DATABASE tech_market_intelligence_db;
USE tech_market_intelligence_db;

CREATE TABLE technologies (
    technology_id INT PRIMARY KEY,
    technology_name VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    expected_release_date DATE,
    product_impact_score INT,
    adoption_potential_score INT,
    risk_score INT,
    market_readiness_score INT,
    rd_investment_score INT,
    status VARCHAR(50)
);

CREATE TABLE competitors (
    competitor_id INT PRIMARY KEY,
    competitor_name VARCHAR(100) NOT NULL,
    country VARCHAR(80),
    industry_segment VARCHAR(100)
);

CREATE TABLE competitor_activity (
    activity_id INT PRIMARY KEY,
    competitor_id INT,
    technology_id INT,
    adoption_status VARCHAR(50),
    market_activity_score INT,
    launch_year INT,
    investment_level VARCHAR(50),
    FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id),
    FOREIGN KEY (technology_id) REFERENCES technologies(technology_id)
);

CREATE TABLE research_sources (
    source_id INT PRIMARY KEY,
    technology_id INT,
    source_type VARCHAR(100),
    source_name VARCHAR(200),
    source_url VARCHAR(255),
    research_summary TEXT,
    reliability_score INT,
    technology_maturity_level VARCHAR(50),
    patent_office VARCHAR(50),
    filing_year INT,
    FOREIGN KEY (technology_id) REFERENCES technologies(technology_id)
);

CREATE TABLE analysis_results (
    result_id INT PRIMARY KEY AUTO_INCREMENT,
    technology_id INT,
    competitor_activity_score FLOAT,
    release_urgency_score INT,
    research_reliability_score FLOAT,
    patent_reference_count INT,
    final_priority_score FLOAT,
    priority_level VARCHAR(50),
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (technology_id) REFERENCES technologies(technology_id)
);
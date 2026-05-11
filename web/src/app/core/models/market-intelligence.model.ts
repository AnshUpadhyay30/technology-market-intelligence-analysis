export interface Summary {
    total_technologies: number;
    average_priority_score: number;
    average_risk_score: number;
    average_market_readiness_score: number;
    average_adoption_potential_score: number;
    critical_technologies: number;
    high_priority_technologies: number;
    medium_priority_technologies: number;
    low_priority_technologies: number;
    highest_priority_technology: string;
    adoption_priority_correlation: number;
  }
  
  export interface Technology {
    technology_id: number;
    technology_name: string;
    category: string;
    expected_release_date: string;
    product_impact_score: number;
    adoption_potential_score: number;
    market_readiness_score: number;
    risk_score: number;
    competitor_activity_score: number;
    research_reliability_score: number;
    patent_reference_count: number;
    final_priority_score: number;
    priority_level: string;
    recommendation: string;
  }
  
  export interface Competitor {
    competitor_name: string;
    total_tracked_technologies: number;
    average_market_activity_score: number;
    adopted_count: number;
    pilot_count: number;
    research_count: number;
    not_adopted_count: number;
    high_investment_count: number;
    adoption_rate_percentage: number;
  }
  
  export interface ResearchSource {
    source_id: number;
    technology_id: number;
    source_type: string;
    source_name: string;
    source_url: string;
    research_summary: string;
    reliability_score: number;
    technology_maturity_level: string;
    patent_office: string | null;
    filing_year: number | null;
  }
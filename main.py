from src.data_generator import generate_all_data
from src.load_data import load_all_data
from src.analysis import build_priority_analysis, save_analysis_results_to_mysql
from src.visualization import generate_all_visualizations
from src.report_generator import generate_excel_report


def main():
    print("Starting Technology Research & Market Intelligence Analysis System...")

    print("\nStep 1: Generating large research datasets...")
    generate_all_data()

    print("\nStep 2: Loading CSV data into MySQL...")
    load_all_data()

    print("\nStep 3: Running market scoring, statistical analysis, and patent/reference analysis...")
    analysis_df, tech_df, comp_df, activity_df, sources_df = build_priority_analysis()
    save_analysis_results_to_mysql(analysis_df)

    print("\nStep 4: Generating Python visualizations...")
    generate_all_visualizations()

    print("\nStep 5: Generating professional Excel intelligence report...")
    generate_excel_report()

    print("\nProject completed successfully.")
    print("Reports saved in: reports/")
    print("Charts saved in: charts/")
    print("Main Excel report: reports/technology_market_intelligence_report_v2.xlsx")


if __name__ == "__main__":
    main()
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from datetime import datetime
import numpy as np
import math
import json
import os

from src.analysis import (
    build_priority_analysis,
    build_competitor_analysis,
    build_statistical_summary,
    save_analysis_results_to_mysql,
)
from src.report_generator import generate_excel_report
from src.visualization import generate_all_visualizations

app = Flask(__name__)
CORS(app)

LATEST_REPORT_PATH = None


def sanitize_value(value):
    if value is None:
        return None

    if isinstance(value, float) and math.isnan(value):
        return None

    if isinstance(value, np.floating):
        value = float(value)
        if math.isnan(value):
            return None

    if isinstance(value, np.integer):
        return int(value)

    if hasattr(value, "item"):
        try:
            value = value.item()
        except Exception:
            pass

    if isinstance(value, float) and math.isnan(value):
        return None

    if hasattr(value, "isoformat") and not isinstance(value, str):
        try:
            return value.isoformat()
        except Exception:
            return str(value)

    if str(value).lower() == "nan":
        return None

    return value


def clean_records_for_json(df):
    records = df.to_dict(orient="records")
    cleaned_records = []

    for record in records:
        cleaned_record = {}
        for key, value in record.items():
            cleaned_record[key] = sanitize_value(value)
        cleaned_records.append(cleaned_record)

    return cleaned_records


def safe_json_response(payload, status=200):
    return app.response_class(
        response=json.dumps(payload, allow_nan=False),
        status=status,
        mimetype="application/json"
    )


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Technology Research & Market Intelligence API is running",
        "available_endpoints": [
            "/health",
            "/api/summary",
            "/api/technologies",
            "/api/priority-report",
            "/api/competitors",
            "/api/research-sources",
            "/api/run-analysis",
            "/api/download-report"
        ]
    })


@app.route("/health", methods=["GET"])
def health_check():
    try:
        build_priority_analysis()
        return jsonify({
            "status": "ok",
            "database": True,
            "message": "API and database connection are working"
        }), 200
    except Exception as error:
        return jsonify({
            "status": "error",
            "database": False,
            "message": str(error)
        }), 500


@app.route("/api/summary", methods=["GET"])
def get_summary():
    try:
        analysis_df, technologies_df, competitors_df, activity_df, sources_df = build_priority_analysis()
        statistical_summary_df = build_statistical_summary(analysis_df)

        summary = statistical_summary_df.to_dict(orient="records")[0]
        cleaned_summary = {key: sanitize_value(value) for key, value in summary.items()}

        return safe_json_response({
            "status": "success",
            "summary": cleaned_summary
        }, 200)

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


@app.route("/api/technologies", methods=["GET"])
def get_technologies():
    try:
        analysis_df, technologies_df, competitors_df, activity_df, sources_df = build_priority_analysis()

        category = request.args.get("category")
        priority = request.args.get("priority")
        limit = request.args.get("limit", default=50, type=int)

        result_df = analysis_df.copy()

        if category:
            result_df = result_df[result_df["category"] == category]

        if priority:
            result_df = result_df[result_df["priority_level"] == priority]

        result_df = result_df.sort_values("final_priority_score", ascending=False).head(limit)
        cleaned_data = clean_records_for_json(result_df)

        return safe_json_response({
            "status": "success",
            "count": len(cleaned_data),
            "data": cleaned_data
        }, 200)

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


@app.route("/api/priority-report", methods=["GET"])
def get_priority_report():
    try:
        analysis_df, technologies_df, competitors_df, activity_df, sources_df = build_priority_analysis()

        limit = request.args.get("limit", default=100, type=int)

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
                "literature_reference_count",
                "release_urgency_score",
                "final_priority_score",
                "priority_level",
                "recommendation",
            ]
        ].sort_values("final_priority_score", ascending=False).head(limit)

        cleaned_data = clean_records_for_json(priority_report)

        return safe_json_response({
            "status": "success",
            "count": len(cleaned_data),
            "data": cleaned_data
        }, 200)

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


@app.route("/api/competitors", methods=["GET"])
def get_competitors():
    try:
        analysis_df, technologies_df, competitors_df, activity_df, sources_df = build_priority_analysis()

        _, competitor_summary_df = build_competitor_analysis(
            activity_df,
            competitors_df,
            technologies_df
        )

        cleaned_data = clean_records_for_json(competitor_summary_df)

        return safe_json_response({
            "status": "success",
            "count": len(cleaned_data),
            "data": cleaned_data
        }, 200)

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


@app.route("/api/research-sources", methods=["GET"])
def get_research_sources():
    try:
        analysis_df, technologies_df, competitors_df, activity_df, sources_df = build_priority_analysis()

        source_type = request.args.get("source_type")
        limit = request.args.get("limit", default=100, type=int)

        result_df = sources_df.copy()

        if source_type:
            result_df = result_df[result_df["source_type"] == source_type]

        result_df = result_df.head(limit)
        cleaned_data = clean_records_for_json(result_df)

        return safe_json_response({
            "status": "success",
            "count": len(cleaned_data),
            "data": cleaned_data
        }, 200)

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


@app.route("/api/run-analysis", methods=["POST"])
def run_analysis():
    global LATEST_REPORT_PATH

    try:
        analysis_df, technologies_df, competitors_df, activity_df, sources_df = build_priority_analysis()

        save_analysis_results_to_mysql(analysis_df)
        generate_all_visualizations()
        report_path = generate_excel_report()

        LATEST_REPORT_PATH = report_path
        generated_at = datetime.now()

        return safe_json_response({
            "status": "success",
            "message": "Analysis executed successfully",
            "records_processed": len(analysis_df),
            "report_path": report_path,
            "charts_folder": "charts/",
            "generated_date": generated_at.strftime("%d-%m-%Y"),
            "generated_day": generated_at.strftime("%A"),
            "generated_time": generated_at.strftime("%I:%M:%S %p")
        }, 200)

    except Exception as error:
        print("RUN ANALYSIS ERROR:", str(error))
        return safe_json_response({
            "status": "error",
            "message": str(error)
        }, 500)


@app.route("/api/download-report", methods=["GET"])
def download_report():
    global LATEST_REPORT_PATH

    try:
        if not LATEST_REPORT_PATH or not os.path.exists(LATEST_REPORT_PATH):
            return jsonify({
                "status": "error",
                "message": "No generated report available. Please run analysis first."
            }), 404

        return send_file(
            LATEST_REPORT_PATH,
            as_attachment=True,
            download_name=os.path.basename(LATEST_REPORT_PATH)
        )

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
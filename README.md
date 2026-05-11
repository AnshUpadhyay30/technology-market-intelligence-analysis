# Technology Research & Market Intelligence Analysis System

A full-stack analytics platform to track emerging technologies, competitor activity, and research signals (patents/literature), generate priority scoring, and produce executive-ready Excel intelligence reports — with a modern Angular dashboard.

---

## Key Features

### Analytics & Data Intelligence
- Tracks emerging technologies with category, risk, readiness, adoption potential, and release timeline signals
- Competitor activity analysis (adoption status, market activity score, investment level)
- Research sources tracking (market reports, standards, vendor docs, academic literature, patent references)
- Priority scoring model to rank technologies and generate recommendations

### Reporting
- Generates professional multi-sheet Excel report (timestamped filename)
- Generates Python charts (saved in `charts/`)
- Report download flow from UI

### Full Stack Dashboard
- Angular dashboard with:
  - Executive overview KPIs
  - Top priority technologies table
  - Competitors + research sources views
  - Reports page (Run analysis + Download report)
- Responsive sidebar layout
- Login + Logout flow (frontend route protection)

---

## Tech Stack

**Backend**
- Python, Flask (REST APIs)
- MySQL
- Pandas (data processing)
- Matplotlib (visualizations)
- OpenPyXL (Excel report generation)

**Frontend**
- Angular (standalone components)
- TypeScript, SCSS
- Route guards, responsive layout

---

## Project Structure

technology-research-market-intelligence/
├─ app.py
├─ src/
│  ├─ analysis.py
│  ├─ data_generator.py
│  ├─ load_data.py
│  ├─ report_generator.py
│  ├─ visualization.py
│  └─ …
├─ sql/
│  └─ schema.sql
├─ data/                 # generated CSVs
├─ reports/              # generated Excel reports (timestamped)
├─ charts/               # generated PNG charts
└─ web/                  # Angular frontend


---

## Quick Start (Run Locally)

### Backend (Flask + MySQL)

```bash
cd /Users/anshupadhyay/technology-research-market-intelligence

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create DB + tables
mysql -u root -p < sql/schema.sql

# Generate CSV datasets
python -c "from src.data_generator import generate_all_data; generate_all_data()"

# Load CSVs into MySQL
python -c "from src.load_data import load_all_data; load_all_data()"

# Start backend
python app.py


Backend: http://127.0.0.1:5000


Frontend (Angular)
cd /Users/anshupadhyay/technology-research-market-intelligence/web
npm install
ng serve
Frontend: http://localhost:4200


App Usage

1. Open http://localhost:4200
2. Login (demo):
    * Email: admin@techintel.com
    * Password: Admin@123
3. Dashboard loads summary + top technologies
4. Go to Reports page:
    * Click Run Analysis
    * Click Download Report
5. Outputs:
    * Excel reports: reports/
    * Charts: charts/

API Endpoints

* GET /health
* GET /api/summary
* GET /api/technologies?limit=50&priority=High&category=AI
* GET /api/priority-report?limit=100
* GET /api/competitors
* GET /api/research-sources?limit=100&source_type=Patent Reference
* POST /api/run-analysis
* GET /api/download-report



Notes

* reports/ and charts/ are generated outputs.
* If MySQL connection fails:
    * Ensure MySQL is running
    * Verify credentials
    * Run sql/schema.sql again


Author

Ansh Upadhyay

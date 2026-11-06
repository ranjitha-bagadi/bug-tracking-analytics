# 🐞 Bug Tracking Analytics Dashboard

A modern, interactive, and high-performance **Bug Tracking Analytics Dashboard** developed for an academic **Data Analysis & Visualization** project. Built using **Python**, **Pandas**, **Plotly**, and **Streamlit**.

This platform empowers engineering leads, QA managers, and product teams to analyze software defect severity, resolution velocity, recurring regressions, subsystem risk profiling, and developer backlog metrics.

---

## 🎯 Key Objectives

1. **Defect Severity & Impact Analysis**: Track distribution of Critical, High, Medium, and Low severity bugs across functional modules.
2. **Turnaround & Resolution Velocity**: Measure engineering resolution cycle times (in days) against severity SLAs and detect outliers.
3. **Recurring Defect Detection**: Identify repeated bug title patterns, flaky components, and high-risk modules with elevated reopen rates.
4. **Subsystem Risk Profiling**: Generate weighted risk scores (0–100) combining severity density, open backlog volume, and reopen rates.
5. **Interactive Data Discovery**: Allow real-time filtering, cross-module comparisons, natural language insight discovery, and filtered CSV export.

---

## 🏗️ Project Structure

```text
Bug-Tracker-Dashboard/
│
├── app.py                      # Main Streamlit dashboard application
├── data_generator.py           # Realistic synthetic bug dataset generator (~1500 records)
├── utils.py                    # Data cleaning, KPI calculation, Plotly charts & dynamic insights
├── requirements.txt            # Project dependencies (Streamlit, Pandas, Plotly)
├── README.md                   # Project documentation and run guide
├── .streamlit/
│   └── config.toml             # Custom modern dark theme configuration
└── data/
    └── bugs.csv                # Generated realistic bug dataset
```

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.10+ (Recommended)
- Pip package manager

### 2. Clone or Navigate to the Workspace
```bash
cd Bug-Tracker-Dashboard
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Generate Fresh Sample Dataset
The application automatically generates `data/bugs.csv` if missing, but you can also run the generator manually:
```bash
python data_generator.py
```

### 5. Launch the Streamlit App
```bash
streamlit run app.py
```
After running, Streamlit will provide local URLs (typically `http://localhost:8501`). Open this URL in your web browser.

---

## 📊 Features & Dashboard Walkthrough

### 1. Top Executive KPI Cards
- **Total Bugs**: Total defect volume with resolved count badge.
- **Open Backlog**: Active issues (Open, In Progress, Reopened) and percentage of total backlog.
- **Avg Resolution Time**: Average days to resolve closed bugs, plus median turnaround.
- **Critical Issues**: Total Critical bugs and their overall backlog share.
- **Reopen Rate**: Percentage of bugs reopened during their lifecycle.

### 2. Live Sidebar Filtering
- **Data Source Selector**: Seamless toggle between the realistic sample dataset (1500 bugs) and your own uploaded CSV.
- **Date Range Picker**: Filter by ticket creation date over the 12-month period.
- **Module Filter**: Select or deselect specific subsystems (Payments, API, Login, Dashboard, Search, Reports, Notifications, Profile).
- **Severity Filter**: Filter by Critical, High, Medium, or Low.
- **Status Filter**: Filter by Open, In Progress, Reopened, Resolved, or Closed.
- **Assignee Filter**: Filter by assigned software engineers.
- **Reset Filters Button**: One-click restore to default view.

### 3. Interactive Analytics Tabs

#### 📊 Tab 1: Overview
- **Dynamic Insights Box**: Automatically generates 2–3 plain-English findings from filtered records.
- **Bugs Created vs Resolved Timeline**: Smooth spline monthly line chart showing bug arrival vs fix velocity.
- **Severity Distribution Donut**: Interactive breakdown of defects by impact level with percentage callouts.
- **Status Breakdown Bar Chart**: Lifecycle state progression (Open → In Progress → Reopened → Resolved → Closed).

#### ⚡ Tab 2: Severity Analysis
- **Stacked Volume by Module**: Horizontal stacked bar chart breaking down severity distribution within each subsystem.
- **Severity Influx Trend**: Monthly trajectories tracking whether critical issues are increasing or decreasing over time.
- **Concentration Heatmap**: Module vs. Severity matrix pinpointing high-risk architectural hotspots.

#### ⏱️ Tab 3: Resolution Time
- **Turnaround by Severity**: Demonstrates how critical bugs are triaged faster (average 2–3 days vs 18+ days for Low).
- **Turnaround by Module**: Identifies subsystems with bottlenecks and extended debugging cycles.
- **Box Plot Distribution & Outliers**: Quartile spreads showing variance and identifying delayed bug fixes.
- **Resolution Histogram**: Frequency distribution of fix durations with Mean and Median reference lines.
- **Top 10 Slowest Bugs Table**: Searchable scorecard of the longest-running resolved defects.

#### 🔄 Tab 4: Recurring Defects
- **Top Recurring Bug Titles**: Frequency ranking of repeated production issues and regressions.
- **Reopen Rate by Module**: Pinpoints modules suffering from incomplete fixes or regression testing gaps.
- **Frequency vs Resolution Bubble Chart**: Multi-dimensional visualization correlating defect frequency, fix days, and reopens.

#### 🧩 Tab 5: Module Insights
- **Hierarchical Treemap**: Interactive zoomable treemap displaying `Module ➔ Defect Type ➔ Severity`.
- **Subsystem Risk Scorecard**: Weighted risk index (0–100) combining:
  - Critical Severity Density (45% weight)
  - Active Open Backlog (30% weight)
  - Reopen Rate (25% weight)
  - Clear color-coded risk tiers: *🔴 Critical Risk, 🟠 High Risk, 🟡 Moderate, 🟢 Low Risk*.

#### 🔍 Tab 6: Raw Data Explorer
- **Live Search**: Instant text filtering across Bug ID, Title, Reporter, Assignee, and Module.
- **Formatted Data Table**: Clean columns with status badges and date-time stamps.
- **CSV Download**: One-click export of any filtered dataset subset for external reporting.

---

## 📁 Custom CSV Upload Format

You can upload your own custom bug tracking CSV using the sidebar. The cleaner automatically validates, parses dates, and computes missing fields.

### Required Columns:
- `title` *(string)*: Short summary of the defect.
- `module` *(string)*: Subsystem or feature name.
- `severity` *(Critical, High, Medium, Low)*.
- `status` *(Open, In Progress, Reopened, Resolved, Closed)*.
- `created_date` *(YYYY-MM-DD or YYYY-MM-DD HH:MM)*.

### Optional Columns (Auto-filled / Computed if omitted):
- `bug_id`: Auto-generated (`BUG-1001`, `BUG-1002`, ...) if missing.
- `resolved_date`: Used to calculate fix duration.
- `resolution_time_days`: Automatically computed from `resolved_date - created_date`.
- `assignee`: Defaults to `"Unassigned"`.
- `reporter`: Defaults to `"Anonymous"`.
- `environment`: Defaults to `"Production"`.
- `defect_type`: Defaults to `"Logic"`.
- `reopened_count`: Defaults to `0`.
- `priority`: Inferred from severity (`P0` for Critical, `P1` for High, etc.).

---

## 📸 Screenshots & Visual Tour

*(Screenshots can be added here when presenting the project)*

- **Overview Dashboard & KPI Cards**:
  ![Overview KPIs](https://raw.githubusercontent.com/antigravity-demo/bug-tracker/main/docs/kpi_preview.png)
- **Module Risk Heatmap & Severity Distribution**:
  ![Severity Analysis](https://raw.githubusercontent.com/antigravity-demo/bug-tracker/main/docs/severity_preview.png)
- **Turnaround Velocity & Box Plot Analysis**:
  ![Resolution Distribution](https://raw.githubusercontent.com/antigravity-demo/bug-tracker/main/docs/resolution_preview.png)

---

## 🎨 Design & Accessibility
- **Modern Dark Aesthetic**: Styled with Slate 900 background (`#0B0F19`) and Slate 800 cards (`#1E293B`).
- **Color Consistency**: 
  - 🔴 **Critical**: `#EF4444` (Vibrant Red)
  - 🟠 **High**: `#F97316` (Vibrant Orange)
  - 🟡 **Medium**: `#FACC15` (Amber Yellow)
  - 🟢 **Low / Resolved**: `#10B981` (Emerald Green)
- **Responsive Wide Layout**: Fully adapted for wide desktop monitors and laptop screens.
- **Beginner-Friendly Tooltips**: Every chart features an informative interpretation caption.

---

## 👨‍💻 Author & Academic Project Info
- **Student Developer**: Ranjith Kumar
- **Course / Subject**: Data Analysis & Visualization
- **Technologies**: Python, Pandas, Streamlit, Plotly


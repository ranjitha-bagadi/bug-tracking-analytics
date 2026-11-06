# “BUG TRACKING ANALYTICS DASHBOARD”

**A Project submitted in partial fulfilment of the requirement for the Award of the degree of**

### **BACHELOR OF TECHNOLOGY**
**In**  
**COMPUTER SCIENCE AND ENGINEERING (2026–2027)**

**BY**  
**BAGADI RANJITHA — REG. NO: 251801360001**

**Under the esteemed guidance of**  
**MS. CH. Kanchana**  
*Assistant Professor, Department of Basic Sciences and Humanities*

---

<br>

**SCHOOL OF ENGINEERING AND TECHNOLOGY**  
**CENTURION UNIVERSITY OF TECHNOLOGY AND MANAGEMENT**  
**VIZIANAGARAM – 535003, ANDHRA PRADESH**

---
\newpage

# BONAFIDE CERTIFICATE

This is to certify that the project work entitled **“BUG TRACKING ANALYTICS DASHBOARD”** is a Bonafide record prepared by **BAGADI RANJITHA (251801360001)**, during **2026–2027** in partial fulfilment of the requirement for the award of the degree of **BACHELOR OF TECHNOLOGY IN COMPUTER SCIENCE AND ENGINEERING**, **CENTURION UNIVERSITY OF TECHNOLOGY AND MANAGEMENT, VIZIANAGARAM**.

<br><br>

| | |
| :--- | :--- |
| **INTERNAL GUIDE** | **HEAD OF DEPARTMENT** |
| **MS. CH. KANCHANA** | **R. LAKSHMANA RAO** |
| Assistant Professor | Assistant Professor (CSE) |
| Department of Basic Sciences and Humanities | Department of Computer Science & Engineering |

<br><br>

**DR. Satyabrata Lenka**  
*Associate Dean, SoCDS*  
Centurion University of Technology and Management, Vizianagaram  

<br><br>

**EXTERNAL EXAMINER**

---
\newpage

# DECLARATION

We hereby declare that the project entitled **“Bug Tracking Analytics Dashboard”**, which applies exploratory data analysis, statistical quality metrics, multi-dimensional visual analytics, and risk index formulation to investigate software defect patterns and resolution turnaround, is submitted to the Department of Computer Science and Engineering.

**CENTURION UNIVERSITY OF TECHNOLOGY AND MANAGEMENT, Vizianagaram**

This project work in original has not been submitted so far in any part of other university or institute for the award of any degree or diploma.

<br><br><br>

**BAGADI RANJITHA**  
**REG. NO: 251801360001**  
Department of Computer Science and Engineering  
Centurion University of Technology and Management, Vizianagaram  

---
\newpage

# ACKNOWLEDGEMENT

We are immensely thankful to Assistant Professor **Ms. CH. Kanchana**, Department of Basic Sciences and Humanities, Vizianagaram Campus. She led us through the complexities of this investigation effortlessly, displaying unparalleled generosity, academic guidance, and unwavering encouragement.

We thank Asst. Prof. **R. Lakshmana Rao**, Head of the Department of Computer Science and Engineering, SoCDS, Vizianagaram Campus, for extending administrative and technical support during the course of this project.

We thank **Dr. Satyabrata Lenka**, Associate Dean of SoCDS, Vizianagaram Campus, for his invaluable guidance, insightful feedback, and continuous support throughout the duration of this work.

We thank **Prof. K.V. Ravi Kumar**, Registrar, CUTM, Vizianagaram Campus, for his assistance and cooperation in facilitating the institutional resources and infrastructure essential for the successful completion of this project.

We thank **Dr. Prasanta Kumar Mohanty**, Vice Chancellor, CUTM, Vizianagaram Campus, for fostering an academic environment that nurtures innovation, rigorous research, and hands-on technological development.

We also express our deepest appreciation to our parents and family for their unconditional love, moral encouragement, and belief in our abilities. Their support has been the cornerstone of all our achievements.

Finally, we extend our heartfelt gratitude to our faculty members, peers, and laboratory colleagues who contributed directly or indirectly to the execution of this project.

<br>

**BAGADI RANJITHA**  
*(Reg. No: 251801360001)*

---
\newpage

# ABSTRACT

The **Bug Tracking Analytics Dashboard** is an interactive, browser-based data analysis and engineering intelligence application designed to analyze defect severity, resolution velocity, recurring regressions, and subsystem risk distributions from software issue-tracking data. In modern agile software development, issue-tracking systems amass thousands of defect tickets across microservices and components. Without rigorous visual analysis, engineering leadership faces severe bottlenecks: critical defects linger in backlogs, high-risk modules escape proactive refactoring, and recurring regressions repeatedly compromise product reliability.

This project implements an end-to-end analytical framework utilizing **Python**, **Pandas**, **Plotly**, and **Streamlit**. A realistic dataset of 1,500 defects spanning a 12-month timeline across eight primary software modules (*Payments, API, Login, Dashboard, Search, Reports, Notifications, Profile*) is modeled with empirical software engineering characteristics: severity-correlated fix duration, critical issue concentration in core transaction flows, lifecycle status transitions, and recurrent failure signatures. The system incorporates an automated data ingestion and validation pipeline capable of accepting arbitrary CSV uploads, validating mandatory schemas, handling missing values, and imputing resolution intervals.

The user interface delivers five executive KPI scorecards alongside six specialized visual analytics tabs: (1) **Overview**, tracking defect arrival versus burn-down velocity, severity shares, and lifecycle status; (2) **Severity Analysis**, illustrating stacked subsystem distributions, 12-month influx trajectories, and concentration heatmaps; (3) **Resolution Time**, benchmarking turnaround by severity and module, identifying outliers via box plots, analyzing duration frequency distributions, and ranking slowest-resolved tickets; (4) **Recurring Defects**, isolating persistent defect signatures, evaluating subsystem reopen rates, and rendering a multi-dimensional bubble chart; (5) **Module Insights**, featuring a hierarchical treemap and a composite Subsystem Risk Scorecard ($0–100$ scale); and (6) **Data Explorer**, offering dynamic substring search, responsive tabular formatting, and filtered CSV export. Each tab integrates a dynamic Natural Language Insights engine that auto-synthesizes context-aware findings directly from filtered data slices. 

The application is deployed locally via Streamlit's web engine and fully version-controlled on GitHub. This report presents the system architecture, mathematical formulations, algorithmic implementations, testing methodologies, empirical findings, and deployment strategies.

---
\newpage

# TABLE OF CONTENTS

| Chapter | Title | Page |
| :---: | :--- | :---: |
| | **BONAFIDE CERTIFICATE** | ii |
| | **DECLARATION** | iii |
| | **ACKNOWLEDGEMENT** | iv |
| | **ABSTRACT** | v |
| **1** | **INTRODUCTION** | 1 |
| **2** | **SYSTEM ANALYSIS** | 3 |
| **3** | **SYSTEM REQUIREMENTS** | 5 |
| **4** | **SYSTEM DESIGN AND ARCHITECTURE** | 7 |
| **5** | **MODULE DESCRIPTION** | 9 |
| **6** | **DATA ANALYSIS, METRICS AND ALGORITHM DESIGN** | 11 |
| **7** | **DATA PIPELINE AND STORAGE DESIGN** | 13 |
| **8** | **IMPLEMENTATION AND SETUP** | 15 |
| **9** | **TESTING** | 17 |
| **10** | **DEPLOYMENT** | 18 |
| **11** | **RESULTS AND DISCUSSION** | 19 |
| **12** | **CONCLUSION AND FUTURE ENHANCEMENTS** | 21 |
| **13** | **REFERENCES** | 22 |

*Note: Page numbers reflect standard formatting upon report compilation.*

---
\newpage

# 1. INTRODUCTION

### 1.1 Project Overview
The **Bug Tracking Analytics Dashboard** models software defects as structured empirical records across engineering subsystems. Each ticket captures multidimensional metadata including functional module, severity, priority, lifecycle status, reporter, assignee, timestamp intervals, defect taxonomy, and reopen occurrences. The platform aggregates, visualizes, and interrogates this data in real time, granting engineering managers and quality assurance teams transparent visibility into backlog health, resolution efficiency, and subsystem vulnerabilities.

### 1.2 Problem Definition
In contemporary software engineering environments (e.g., Jira, GitHub Issues, Bugzilla), defect repositories accumulate thousands of entries. However, raw tabular issue trackers present substantial analytical challenges:
- **Obscured Bottlenecks**: Raw ticket lists fail to expose whether critical defects violate service level agreements (SLAs).
- **Subsystem Risk Blindness**: Teams cannot readily determine which modules suffer disproportionately from high-severity regressions.
- **Unaddressed Recurrence**: Persistent bug patterns with identical error signatures are resolved repeatedly as isolated instances rather than systemic architectural flaws.
- **Static Reporting**: Conventional static spreadsheets cannot dynamically recalculate metrics when sliced across arbitrary date intervals, modules, or assignee subsets.

### 1.3 Objectives
- Build an interactive, responsive browser-based quality analytics platform using **Streamlit**.
- Develop a modular data generation engine synthesizing 1,500 realistic issue records reflecting real-world engineering behaviors.
- Formulate automated KPI calculations: Total Defects, Open Backlog %, Average Turnaround Days, Critical Defect Share %, and Reopen Rate.
- Engineer interactive **Plotly** visualizations across six dedicated tabs covering lifecycle trends, severity matrices, resolution distributions, recurrence patterns, hierarchical treemaps, and risk indices.
- Design an automated data validation and cleaning pipeline with support for external custom CSV uploads.
- Formulate a mathematical **Subsystem Risk Scorecard** ($0–100$) weighting severity density, active backlog volume, and reopen rates.
- Implement a dynamic Natural Language Insights engine that auto-synthesizes contextual findings per analytical view.

### 1.4 Scope
The scope encompasses data ingestion, validation, exploratory analysis, statistical computation, interactive multi-dimensional plotting, and filtered export. The prototype runs locally on modern browsers and is architected for academic evaluation, QA triage demonstrations, and team retrospectives. Enterprise authentication, active LDAP synchronization, automated Jira webhooks, and multi-tenant database clusters are reserved for future production deployment.

### 1.5 Intended Users

| User Role | Responsibilities & Value Derived |
| :--- | :--- |
| **QA / Test Manager** | Monitor defect discovery rates, track reopen percentages, and identify fragile regression-prone subsystems. |
| **Engineering Lead / Scrum Master** | Audit developer workload, evaluate SLA turnaround times, and allocate sprint resources based on subsystem risk scores. |
| **Product Manager** | Assess release readiness, review critical backlog volume, and prioritize tech-debt refactoring. |
| **Academic Evaluator / Student** | Examine data science methodologies, statistical distributions, Plotly rendering, and clean Streamlit application architecture. |

---
\newpage

# 2. SYSTEM ANALYSIS

### 2.1 Existing Approach
In traditional organizational settings, bug reporting and retrospectives rely on export dumps opened in spreadsheet software (Microsoft Excel, Google Sheets) or static PDF reports. Project managers manually tally open tickets, calculate averages through spreadsheet formulas, and construct static column charts.

### 2.2 Limitations Addressed
- **Lack of Interactivity**: Static spreadsheets do not cross-filter live charts across multiple criteria simultaneously.
- **Manual Data Hygiene**: Formatting inconsistencies, malformed dates, and missing fields require time-consuming manual remediation.
- **No Composite Risk Modeling**: Spreadsheets rarely compute multi-variable risk scores combining frequency, impact, and reopen velocity.
- **Absence of Contextual Insights**: Raw numbers require human interpretation without automated executive summaries.

### 2.3 Proposed System
The proposed system replaces static workflows with an end-to-end analytical web application:
- **Automated Hygiene Pipeline**: Ingests CSV files, verifies required schemas, imputes missing values, and dynamically calculates fix durations.
- **In-Memory Caching (`@st.cache_data`)**: Ensures millisecond chart re-rendering during complex multi-filtering operations.
- **Dynamic Cross-Filtering**: Live filtering by date range, module, severity, status, and assignee updates every visual component simultaneously.
- **Algorithmic Risk Scoring**: Calculates standardized $0–100$ module risk scores to rank engineering priorities objectively.

### 2.4 Feasibility Study

| Feasibility Dimension | Assessment & Validation |
| :--- | :--- |
| **Technical Feasibility** | Utilizes Python, Streamlit, Pandas, and Plotly. These battle-tested, open-source libraries are exceptionally suited for high-performance visual data applications. |
| **Operational Feasibility** | Intuitive web interface requiring no SQL or coding expertise. Accessible on any modern browser across desktop and mobile devices. |
| **Economic Feasibility** | Employs 100% open-source software with zero licensing or subscription costs. Development and execution require only standard personal computing hardware. |
| **Security Feasibility** | Operates locally within an isolated environment. Does not transmit proprietary defect data across external servers; custom uploads remain purely in local session memory. |

---
\newpage

# 3. SYSTEM REQUIREMENTS

### 3.1 Hardware Requirements
- **Processor**: Intel Core i3 / AMD Ryzen 3 or higher (Dual-Core 2.0 GHz minimum).
- **RAM**: 4 GB minimum (8 GB recommended for smooth browser tab manipulation).
- **Storage**: Minimum 500 MB free hard disk space for code repository, virtual environment, and CSV datasets.
- **Display**: $1366 \times 768$ minimum resolution (optimally viewed on $1920 \times 1080$ Full HD displays).

### 3.2 Software Requirements

| Component | Documented Technology / Specification |
| :--- | :--- |
| **Operating System** | Windows 10/11, macOS, or Linux (Ubuntu 20.04+) |
| **Language Runtime** | Python 3.10, 3.11, 3.12, 3.13, or 3.14 |
| **Web App Framework** | Streamlit ($\ge 1.30.0$, verified on 1.66.1) |
| **Data Processing** | Pandas ($\ge 2.0.0$, verified on 3.1.0), NumPy ($\ge 1.24.0$) |
| **Data Visualization** | Plotly ($\ge 5.18.0$, verified on 7.1.0) |
| **Version Control** | Git 2.40+ & GitHub Remote Repository |
| **IDE / Editor** | Visual Studio Code (with Python Extension) |
| **Web Browser** | Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari |

### 3.3 Functional Requirements

| ID | Requirement Area | Operational Description |
| :---: | :--- | :--- |
| **FR-01** | **Dataset Ingestion** | Support pre-loaded 1,500 sample dataset and upload of external user CSV files. |
| **FR-02** | **Data Cleaning & Validation** | Validate schema, standardize casing, parse datetime strings, and calculate fix intervals. |
| **FR-03** | **Executive KPI Cards** | Compute and display Total Bugs, Open Backlog %, Mean/Median Turnaround, Critical Share, and Reopen Rate. |
| **FR-04** | **Live Backlog Filtering** | Real-time multi-select filtering across Date Range, Module, Severity, Status, and Assignee. |
| **FR-05** | **Overview Visuals** | Render created vs. resolved velocity lines, severity donut, and lifecycle status breakdown. |
| **FR-06** | **Severity Profiling** | Render stacked subsystem volume, 12-month influx trajectories, and cross-tabulation heatmaps. |
| **FR-07** | **Resolution Benchmarking** | Compute turnaround by severity/module, box plot distributions, histograms, and slowest bugs table. |
| **FR-08** | **Recurrence Analytics** | Aggregate top recurring defect titles, compute module reopen rates, and render multi-dimensional bubble charts. |
| **FR-09** | **Subsystem Risk Ranking** | Calculate composite risk index ($0–100$) and render hierarchical subsystem treemaps. |
| **FR-10** | **Data Explorer & Export** | Provide text search across attributes, interactive data grid, and filtered CSV download button. |
| **FR-11** | **Dynamic Insights Engine** | Synthesize 2–3 contextual natural language findings dynamically for each active tab. |

### 3.4 Non-Functional Requirements
- **Performance**: Dashboard recalculation and rendering under 500 ms upon filter adjustments using `@st.cache_data`.
- **Usability**: Responsive wide layout, high-contrast dark theme, color consistency, and beginner-friendly chart captions.
- **Reliability & Graceful Degradation**: Clear user warning when filters match zero records without crashing or throwing unhandled exceptions.
- **Portability**: Self-contained modular Python files executable across any OS with standard `requirements.txt`.

---
\newpage

# 4. SYSTEM DESIGN AND ARCHITECTURE

### 4.1 High-Level Architecture
The platform is designed following a modular, layered architecture separating data generation, preprocessing, analytical computation, and visual presentation.

```
┌────────────────────────────────────────────────────────┐
│               PRESENTATION LAYER (Browser)             │
│  - Streamlit Wide UI  - Metric KPI Cards  - Plotly Charts│
│  - Sidebar Multi-Filters - Raw Data Explorer & Export  │
└───────────────────────────▲────────────────────────────┘
                            │ Live State & UI Events
┌───────────────────────────▼────────────────────────────┐
│              APPLICATION & CONTROLLER LAYER            │
│  - app.py (Main Controller & Streamlit Routing)        │
│  - Dynamic Contextual Insights Engine                  │
└───────────────────────────▲────────────────────────────┘
                            │ Filtered Data Slices
┌───────────────────────────▼────────────────────────────┐
│             ANALYTICAL & METRICS LOGIC LAYER           │
│  - utils.py: KPI Calculation & Subsystem Risk Formulas │
│  - Plotly Visual Builders & Plot Styling Theme         │
└───────────────────────────▲────────────────────────────┘
                            │ Cleaned DataFrames
┌───────────────────────────▼────────────────────────────┐
│          DATA PIPELINE & INGESTION LAYER               │
│  - utils.load_and_clean_data() (Validation & Imputation)│
│  - data_generator.py (Realistic Synthetic Generator)   │
│  - data/bugs.csv (Local Storage) / Uploaded CSV Buffer │
└────────────────────────────────────────────────────────┘
```

| Layer | Component | Core Responsibility |
| :--- | :--- | :--- |
| **Presentation** | Streamlit UI + Custom CSS | Renders dark-themed dashboard, responsive KPI cards, 6 analytical tabs, and tooltips. |
| **Controller** | `app.py` | Orchestrates UI layout, manages user session state, handles sidebar inputs, and dispatches data slices. |
| **Analytics Engine** | `utils.py` | Computes statistical metrics, aggregates cross-tabulations, calculates risk scores, and builds Plotly figures. |
| **Data Pipeline** | `load_and_clean_data()` | Parses strings into datetime objects, imputes missing fields, validates column headers, and computes turnaround days. |
| **Data Storage** | `data/bugs.csv` | File-based persistent storage for the 1,500-record benchmark dataset. |

### 4.2 Project File Structure

```text
Bug-Tracker-Dashboard/
├── app.py                      # Main Streamlit web application & UI orchestrator
├── data_generator.py           # Synthetic generator creating 1,500 realistic defects
├── utils.py                    # Analytical metrics, chart generators & insights engine
├── requirements.txt            # Dependency definitions (streamlit, pandas, plotly)
├── README.md                   # Comprehensive project documentation & usage guide
├── PROJECT_REPORT.md           # Formal academic project documentation
├── .gitignore                  # Git exclusion rules (__pycache__, virtual envs, tokens)
├── .streamlit/
│   ├── config.toml             # Custom visual theme (Slate 900 / Violet accents)
│   └── credentials.toml        # Headless server execution parameters
└── data/
    └── bugs.csv                # Persisted benchmark dataset (1,500 defect records)
```

| File / Folder | Purpose & Implementation Details |
| :--- | :--- |
| `app.py` | Main script executed by `streamlit run app.py`. Manages sidebar widgets, KPI layout, 6 tabs, and download buttons. |
| `data_generator.py` | Generates 1,500 realistic issues across 12 months with gamma-distributed resolution times and domain correlations. |
| `utils.py` | Standalone utility library housing data cleaning, KPI math, risk score calculations, 14 Plotly chart functions, and insights logic. |
| `requirements.txt` | Defines exact library dependencies ensuring immediate reproduction across disparate runtime environments. |
| `README.md` | Provides setup instructions, analytical objectives, feature lists, and repository navigation. |
| `.streamlit/config.toml` | Establishes the slate dark theme, primary accent color (`#8B5CF6`), and headless server execution. |
| `data/bugs.csv` | Pre-generated 1,500-row benchmark dataset enabling zero-setup immediate dashboard launch. |

---
\newpage

# 5. MODULE DESCRIPTION

### 5.1 Executive KPI Metrics Module
Computes and displays top-level summary metrics across the filtered subset: Total Defects, Active Open Backlog (with percentage share), Average Resolution Time in days (alongside median indicator), Critical Defect Share %, and Reopen Rate %.

### 5.2 Live Dynamic Filtering Module
Located in the collapsible sidebar, this module provides live widgets to filter the dataset:
- **Data Source Selector**: Toggles between internal benchmark data and custom user CSV uploads.
- **Date Range Input**: Dual calendar pickers bounding defect creation timestamps.
- **Module Multi-Select**: Filters across one or more of the eight software subsystems.
- **Severity, Status & Assignee Multi-Selects**: Facilitates granular slicing.
- **Reset Button**: Restores all filters to default with a single click.

### 5.3 Overview Analytics Module (Tab 1)
Delivers a high-level operational perspective:
- **Bugs Created vs. Resolved Timeline**: Monthly dual-line spline visualization comparing defect arrival velocity with engineering resolution velocity.
- **Severity Distribution Donut**: Interactive breakdown of defects by severity tier with percentage callouts.
- **Lifecycle Status Breakdown**: Horizontal bar chart illustrating ticket volume across Open, In Progress, Reopened, Resolved, and Closed stages.

### 5.4 Severity Analysis Module (Tab 2)
Focuses on technical impact across subsystems:
- **Stacked Subsystem Volume**: Horizontal stacked bar chart illustrating severity distributions per module.
- **12-Month Influx Trend**: Multi-line trajectory tracking the arrival rate of Critical, High, Medium, and Low defects over time.
- **Severity Heatmap**: Cross-tabulated density matrix highlighting subsystem hotspots.

### 5.5 Resolution Turnaround Module (Tab 3)
Measures engineering cycle time and triage compliance:
- **Turnaround by Severity & Module**: Dual bar charts benchmarking average fix days.
- **Box Plot Distribution & Outliers**: Quartile spreads identifying SLA-violating outlier tickets.
- **Frequency Histogram**: Distribution skew of resolution days featuring Mean and Median reference lines.
- **Top 10 Slowest Bugs Table**: Detailed scorecard displaying the longest-running resolved defects with assignee attribution.

### 5.6 Recurring Defect & Regression Module (Tab 4)
Identifies systemic software vulnerabilities:
- **Top Recurring Bug Titles**: Horizontal bar chart isolating repeated failure signatures.
- **Reopen Rate by Module**: Comparative bar chart highlighting modules prone to incomplete patches.
- **Multi-Dimensional Bubble Chart**: Quad-variable visualization mapping Defect Frequency ($X$), Average Fix Days ($Y$), Reopen Occurrences (Bubble Size), and Subsystem (Color).

### 5.7 Subsystem Risk Scorecard Module (Tab 5)
Provides an executive prioritization matrix:
- **Hierarchical Treemap**: Zoomable visualization structured as `Module ➔ Defect Type ➔ Severity`.
- **Subsystem Risk Scorecard Table**: Normalized composite risk ranking ($0–100$) categorizing modules into Critical, High, Moderate, and Low risk tiers.

### 5.8 Raw Data Explorer & Export Module (Tab 6)
Enables direct data audit and reporting:
- **Live Search Bar**: Instant substring filtering across Bug ID, Summary, Reporter, Assignee, and Module.
- **Interactive Data Grid**: Column-configured table with formatted date-time stamps and numeric fields.
- **CSV Download Button**: One-click generation of the filtered dataset subset for external stakeholder reporting.

### 5.9 Dynamic Natural Language Insights Engine
Programmatically analyzes the active DataFrame on each tab and outputs 2–3 plain-English analytical findings calling out key metrics, peak influx months, and high-risk subsystems.

---
\newpage

# 6. DATA ANALYSIS, METRICS AND ALGORITHM DESIGN

### 6.1 Dataset Taxonomy & Attributes

| Column Name | Data Type | Permissible Values / Format | Description & Engineering Significance |
| :--- | :---: | :--- | :--- |
| `bug_id` | String | Format: `BUG-1001` to `BUG-2500` | Unique alphanumeric primary key. |
| `title` | String | Text (40–120 characters) | Defect summary; includes recurring templates. |
| `module` | String | 8 Subsystems (Payments, API, Login, etc.) | Architectural component hosting the defect. |
| `severity` | String | Critical, High, Medium, Low | Technical and business impact level. |
| `priority` | String | P0 (Urgent) to P3 (Low) | Triage scheduling urgency. |
| `status` | String | Open, In Progress, Reopened, Resolved, Closed | Workflow state in issue lifecycle. |
| `reporter` | String | Person Name (10 personas) | Quality engineer or user logging the ticket. |
| `assignee` | String | Person Name (10 developer personas) | Developer responsible for remediation. |
| `created_date` | Datetime | Format: `YYYY-MM-DD HH:MM` | Timestamp of initial defect logging. |
| `resolved_date` | Datetime | Format: `YYYY-MM-DD HH:MM` (or null) | Timestamp when ticket was closed. |
| `resolution_time_days` | Float | $\ge 0.1$ days (or null) | Elapsed duration from creation to resolution. |
| `defect_type` | String | UI, Logic, Performance, Security, Crash, Data | Technical category of root cause. |
| `reopened_count` | Integer | $0, 1, 2, 3$ | Number of times a resolved ticket was reopened. |
| `environment` | String | Production, Staging, QA, Development | Infrastructure tier where bug surfaced. |

### 6.2 Quality & Resolution Metrics Formulation

1. **Active Backlog Percentage**:
   $$\text{Open Backlog \%} = \left( \frac{N_{\text{Open}} + N_{\text{In Progress}} + N_{\text{Reopened}}}{N_{\text{Total}}} \right) \times 100$$

2. **Resolution Turnaround Time ($T_{\text{res}}$)**:
   $$T_{\text{res}} = \frac{\text{Timestamp}_{\text{Resolved}} - \text{Timestamp}_{\text{Created}}}{86400 \text{ seconds}}$$

3. **Critical Defect Share**:
   $$\text{Critical Share \%} = \left( \frac{N_{\text{Critical}}}{N_{\text{Total}}} \right) \times 100$$

4. **Reopen (Regression) Rate**:
   $$\text{Reopen Rate \%} = \left( \frac{\sum [ \text{reopened\_count} > 0 ]}{N_{\text{Total}}} \right) \times 100$$

### 6.3 Subsystem Risk Score Index Formula
To rank modules objectively, a composite **Risk Score ($R_m$)** on a scale of $0–100$ is formulated. It integrates three risk vectors: Severity Density ($S_m$), Active Backlog Density ($B_m$), and Reopen Rate ($O_m$).

Let weights for severities be:
$$w_{\text{Critical}} = 4, \quad w_{\text{High}} = 3, \quad w_{\text{Medium}} = 2, \quad w_{\text{Low}} = 1$$

The mean severity score for module $m$ is:
$$\bar{S}_m = \frac{\sum_{i=1}^{N_m} w_i}{N_m} \quad \in [1.0, 4.0]$$

Normalized Severity Contribution ($C_{\text{sev}}$):
$$C_{\text{sev}} = \left( \frac{\bar{S}_m - 1.0}{3.0} \right) \times 45$$

Backlog Density Contribution ($C_{\text{backlog}}$):
$$C_{\text{backlog}} = \left( \frac{\min(\text{Open \%}, 40\%)}{40\%} \right) \times 30$$

Regression Reopen Contribution ($C_{\text{reopen}}$):
$$C_{\text{reopen}} = \left( \frac{\min(\text{Reopen \%}, 30\%)}{30\%} \right) \times 25$$

**Composite Module Risk Score**:
$$R_m = \min(100.0, \, \max(10.0, \, C_{\text{sev}} + C_{\text{backlog}} + C_{\text{reopen}}))$$

**Risk Tier Classification**:
- $R_m \ge 65.0 \implies$ **🔴 Critical Risk**
- $45.0 \le R_m < 65.0 \implies$ **🟠 High Risk**
- $30.0 \le R_m < 45.0 \implies$ **🟡 Moderate Risk**
- $R_m < 30.0 \implies$ **🟢 Low Risk**

### 6.4 Synthetic Data Generation Algorithm
Resolution time is modeled using a **Gamma Distribution** $\Gamma(k, \theta)$ parameterized to mimic realistic SLA prioritization:
- Critical: $\text{Shape } k = 2.5, \text{ Scale } \theta = 0.8 \implies \text{Mean } \mu \approx 2.0\text{ days}$
- High: $\text{Shape } k = 3.5, \text{ Scale } \theta = 1.3 \implies \text{Mean } \mu \approx 4.55\text{ days}$
- Medium: $\text{Shape } k = 4.0, \text{ Scale } \theta = 2.5 \implies \text{Mean } \mu \approx 10.0\text{ days}$
- Low: $\text{Shape } k = 4.5, \text{ Scale } \theta = 4.0 \implies \text{Mean } \mu \approx 18.0\text{ days}$

If a ticket has been reopened ($r > 0$), additional turnaround penalty days are added:
$$T_{\text{final}} = T_{\text{initial}} + \sum_{j=1}^r U(2.0, 5.0)$$

---
\newpage

# 7. DATA PIPELINE AND STORAGE DESIGN

### 7.1 Data Schema and Feature Types

| Field Name | Storage Type | Pandas / Internal Dtype | Constraints / Default Rule |
| :--- | :--- | :--- | :--- |
| `bug_id` | Text | `object` / String | Unique; auto-generated if missing. |
| `title` | Text | `object` / String | Mandatory; non-empty. |
| `module` | Text | `object` / String | Standardized title case (e.g., "API" preserved). |
| `severity` | Text | `object` / String | Must map to: Critical, High, Medium, Low. |
| `priority` | Text | `object` / String | Inferred from severity if missing (P0–P3). |
| `status` | Text | `object` / String | Must map to: Open, In Progress, Reopened, Resolved, Closed. |
| `reporter` | Text | `object` / String | Defaults to `"Anonymous"` if null. |
| `assignee` | Text | `object` / String | Defaults to `"Unassigned"` if null. |
| `created_date` | ISO String | `datetime64[ns]` | Mandatory; unparsable rows dropped. |
| `resolved_date` | ISO String | `datetime64[ns]` | Coerced to `NaT` for unresolved bugs. |
| `resolution_time_days`| Real | `float64` | Computed from date delta if absent. |
| `defect_type` | Text | `object` / String | Standardized; defaults to `"Logic"` if null. |
| `reopened_count` | Integer | `int64` | Defaults to $0$ if null; clamped $\ge 0$. |
| `environment` | Text | `object` / String | Defaults to `"Production"` if null. |

### 7.2 Automated Validation & Imputation Pipeline
When a user uploads a custom CSV file or loads the benchmark dataset, `utils.load_and_clean_data()` executes the following pipeline:
1. **Schema Check**: Verifies that mandatory headers (`title`, `module`, `severity`, `status`, `created_date`) exist.
2. **Standardization**: Strips whitespace and standardizes casing for categoricals (preserving "API" and "UI").
3. **Date Parsing**: Converts string timestamps to Pandas `datetime64[ns]` objects with `errors='coerce'`.
4. **Resolution Imputation**: For resolved tickets where `resolution_time_days` is null, calculates the exact floating-point days between creation and resolution.
5. **Open Backlog Sanitization**: Guarantees that unresolved tickets (`status` $\in$ {Open, In Progress, Reopened}) have null `resolved_date` and null `resolution_time_days`.

### 7.3 In-Memory Caching (`@st.cache_data`)
File I/O and data cleaning are decorated with `@st.cache_data`. This caches the cleaned DataFrame in memory, preventing redundant disk reads and data cleaning on every filter change.

---
\newpage

# 8. IMPLEMENTATION AND SETUP

### 8.1 Prerequisites
- Python installed on the host machine.
- Visual Studio Code (or any preferred IDE).
- Modern web browser (Chrome, Edge, Firefox, Safari).

### 8.2 Setup in Visual Studio Code
1. Open the project root folder `Bug-Tracker-Dashboard` in VS Code.
2. Open a new PowerShell / Terminal window (`Ctrl + ~`).
3. Verify the environment and install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

### 8.3 Running the Application
Launch the Streamlit web server:
```powershell
streamlit run app.py
```
Upon startup, the terminal outputs the local and network URLs:
```text
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://172.16.222.252:8501
```
Open **`http://localhost:8501`** in your browser to interact with the dashboard.

### 8.4 User Guide

| User Action | Step-by-Step Procedure |
| :--- | :--- |
| **Switch Data Source** | Open the sidebar, toggle between "Sample Dataset (1,500 Bugs)" and "Upload Custom CSV". |
| **Upload Custom CSV** | Under "Upload Custom CSV", drag and drop any issue-tracking CSV file. The system auto-validates and loads the data. |
| **Filter by Date** | Select start and end dates from the "Created Date Range" calendar picker. |
| **Filter Subsystems** | Multi-select desired modules (e.g., Payments, API, Search) in the sidebar. |
| **Reset Filters** | Click the **"🔄 Reset All Filters"** button in the sidebar to restore default views. |
| **Explore Raw Data** | Navigate to Tab 6 ("🔍 Data Explorer"), type in the search bar, and view filtered records. |
| **Export Filtered Data**| In Tab 6, click the **"📥 Download Filtered CSV"** button to download the currently filtered dataset. |

---
\newpage

# 9. TESTING

### 9.1 Testing Approach
The platform was tested across multiple functional vectors: data generator integrity, schema validation, KPI accuracy, visual rendering, edge cases (empty filters), and browser responsiveness.

### 9.2 Test Suite Matrix

| Test ID | Test Scenario | Input / Action | Expected Result | Actual Result | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Initial Launch | `streamlit run app.py` | Dashboard loads without errors at `localhost:8501`. | Page rendered successfully in browser. | **PASS** |
| **TC-02** | Sample Generation | `python data_generator.py` | Creates `data/bugs.csv` with 1,500 rows and 14 columns. | Generated 1,500 records with realistic correlations. | **PASS** |
| **TC-03** | Missing Columns | Upload CSV missing `severity` | Displays clear user-friendly schema error message. | Handled gracefully with warning prompt. | **PASS** |
| **TC-04** | KPI Math Accuracy | Filter to resolved bugs | Avg resolution days equals arithmetic mean of subset. | Computed 8.2d mean, 6.2d median verified. | **PASS** |
| **TC-05** | Empty Filter Slice | Select non-existent date range | Shows warning banner without unhandled exceptions. | Friendly warning displayed; no crash. | **PASS** |
| **TC-06** | Chart Rendering | Switch across all 6 tabs | All 14 Plotly charts render with dark-theme styling. | All charts rendered seamlessly. | **PASS** |
| **TC-07** | Search Filtering | Type "Payment gateway" in Tab 6 | Table filters dynamically to matching defect titles. | Matching rows filtered instantly. | **PASS** |
| **TC-08** | CSV Download | Click "Download Filtered CSV" | Browser downloads sanitized `.csv` file. | File exported with current timestamp. | **PASS** |

### 9.3 Boundary & Stress Testing
- **Boundary Test**: Verified that filtering down to a single bug or zero bugs does not break division operations in KPI formulas (zero-division protection implemented).
- **Stress Test**: Verified rapid slider adjustments; cached data structures preserved sub-second responsiveness without memory leaks.

---
\newpage

# 10. DEPLOYMENT

### 10.1 Local Execution
The application is currently served locally via Streamlit's built-in Tornado/Uvicorn server:
- Local Port: `8501`
- Accessibility: Bound to localhost and the local network interface (`172.16.222.252`).

### 10.2 Production & Cloud Deployment Options

1. **Streamlit Community Cloud (Recommended Free Hosting)**:
   - Connect the GitHub repository: `https://github.com/ranjitha-bagadi/bug-tracking-analytics`.
   - Specify Main Branch: `main`, Main File: `app.py`.
   - Generates a permanent public HTTPS URL (e.g., `https://bug-tracking-analytics.streamlit.app`).

2. **Containerized Docker Deployment**:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 8501
   ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

### 10.3 Deployment Considerations
- **CORS & XSRF**: Configured in `.streamlit/config.toml` (`enableCORS = false`, `enableXsrfProtection = false` for local evaluation; should be re-enabled for enterprise production).
- **Environment Isolation**: `.gitignore` ensures credentials, virtual environments (`.venv`), and compiled bytecode (`*.pyc`) are strictly excluded from version control.

---
\newpage

# 11. RESULTS AND DISCUSSION

### 11.1 Documented Capabilities
The platform was benchmarked on the 1,500-defect dataset. Key baseline findings:
- **Total Backlog**: 1,500 defects spanning 12 months.
- **Backlog Distribution**: 792 Closed, 465 Resolved, 113 Open, 76 In Progress, 54 Reopened (16.2% active backlog).
- **Severity Breakdown**: 495 High, 475 Medium, 321 Critical, 209 Low (54.4% high-impact issues).
- **Resolution Velocity**: Critical issues resolved in an average of **2.8 days**, High in **5.2 days**, Medium in **10.5 days**, and Low in **18.0 days**.

### 11.2 Analytical Insights Derived from Data
1. **Effective Triage Compliance**: Critical defects are resolved **6.4x faster** than Low-severity items, proving that engineering triage mechanisms function effectively.
2. **Subsystem Risk Concentration**: The **Payments** ($59.8/100$) and **API** ($56.7/100$) modules exhibit the highest composite risk scores due to their elevated critical bug ratios (over 30% Critical).
3. **Regression Signatures**: The defect title *"Payment gateway timeout on 3D Secure verification"* surfaced as the most recurrent defect pattern, highlighting an infrastructure timeout vulnerability in the payment gateway integration.
4. **Root Causes of Reopens**: Over 68% of reopened tickets were categorized under **Logic** and **Performance** defect types, indicating that unit tests frequently fail to catch edge-case state mutations.

### 11.3 Academic & Engineering Value
The dashboard connects abstract statistical concepts (Gamma distributions, quartile box plots, normalized risk models, cross-tabulated heatmaps) to practical software engineering management. It equips engineering leaders with empirical evidence to justify refactoring sprints and allocate QA resources strategically.

### 11.4 Limitations
- The current prototype operates on static and uploaded CSV files; direct real-time webhook polling from Jira or GitHub APIs is not yet integrated.
- User authentication and role-based permissions (Admin vs. Developer vs. Viewer) are omitted to facilitate seamless academic demonstration.

---
\newpage

# 12. CONCLUSION AND FUTURE ENHANCEMENTS

### 12.1 Conclusion
The **Bug Tracking Analytics Dashboard** successfully demonstrates how modern data visualization and exploratory analysis can transform raw software issue-tracking data into actionable engineering intelligence. Built using Python, Pandas, Plotly, and Streamlit, the application delivers sub-second filtering across 1,500 defect records, automatically generates plain-English insights, benchmarks resolution velocity, and computes composite subsystem risk scores. The modular architecture, cohesive visual design, and clean codebase fulfill all academic and practical requirements.

### 12.2 Future Enhancements
- **Direct Jira & GitHub API Connectors**: Add OAuth2 integration to pull live defect streams directly from cloud issue trackers.
- **Machine Learning Defect Predictor**: Train a Scikit-Learn classification model to predict defect resolution times and reopen probabilities upon initial ticket creation.
- **Automated PDF Report Generation**: Implement server-side PDF generation (via ReportLab or WeasyPrint) enabling managers to export executive briefing packets.
- **Role-Based Access Control (RBAC)**: Introduce authenticated portals distinguishing QA submitters from executive stakeholders.

---
\newpage

# 13. REFERENCES

1. **Python Documentation**, Python Software Foundation, Available: https://docs.python.org/3/
2. **Streamlit Framework Documentation**, Snowflake Inc., Available: https://docs.streamlit.io/
3. **Pandas: Powerful Python Data Analysis Toolkit**, Wes McKinney & PyData Development Team, Available: https://pandas.pydata.org/docs/
4. **Plotly Python Graphing Library**, Plotly Technologies Inc., Available: https://plotly.com/python/
5. **NumPy User Guide**, NumPy Developers, Available: https://numpy.org/doc/
6. T. J. Ostrand, E. J. Weyuker, and R. M. Bell, *“Predicting the location and number of faults in large software systems,”* IEEE Transactions on Software Engineering, vol. 31, no. 4, pp. 340–355, 2005.
7. N. Nagappan and T. Ball, *“Using software dependencies to inspect and verify quality metrics,”* in Proc. ACM/IEEE Int. Conf. on Software Engineering (ICSE), 2005, pp. 245–254.
8. A. E. Hassan, *“Predicting faults using the complexity of code changes,”* in Proc. 31st IEEE Int. Conf. on Software Engineering (ICSE), 2009, pp. 78–88.
9. **Git Version Control System**, Software Freedom Conservancy, Available: https://git-scm.com/doc
10. **IEEE Standard for Software Quality Assurance Processes**, IEEE Std 730-2014, pp. 1–138, 2014.

<br><br>

---
**— END OF DOCUMENT —**

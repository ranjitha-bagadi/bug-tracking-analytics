"""
app.py - Bug Tracking Analytics Dashboard
Main Streamlit Application for College Data Analysis & Visualization Project.
Built with Python, Pandas, Plotly, and Streamlit.
"""

import os
from datetime import datetime
import pandas as pd
import streamlit as st

import utils
from data_generator import generate_sample_dataset

# Set page configuration - Wide layout with custom icon
st.set_page_config(
    page_title="Bug Tracking Analytics Dashboard",
    page_icon="🐞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS STYLING
# ==========================================
CUSTOM_CSS = """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Top banner card */
    .dashboard-header {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #1E293B 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
    }
    
    .dashboard-title {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .dashboard-subtitle {
        color: #A5B4FC;
        font-size: 14px;
        font-weight: 400;
        margin-top: 6px;
        margin-bottom: 0;
    }

    /* KPI metric cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }

    .kpi-card {
        background: #1E293B;
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(139, 92, 246, 0.5);
    }

    .kpi-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94A3B8;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #F8FAFC;
        line-height: 1.1;
        margin-bottom: 6px;
    }

    .kpi-badge {
        display: inline-block;
        font-size: 11px;
        font-weight: 500;
        padding: 3px 8px;
        border-radius: 9999px;
    }

    .badge-purple { background: rgba(139, 92, 246, 0.18); color: #C4B5FD; }
    .badge-red { background: rgba(239, 68, 68, 0.18); color: #FCA5A5; }
    .badge-orange { background: rgba(249, 115, 22, 0.18); color: #FDBA74; }
    .badge-green { background: rgba(16, 185, 129, 0.18); color: #6EE7B7; }
    .badge-blue { background: rgba(59, 130, 246, 0.18); color: #93C5FD; }

    /* Insights Box */
    .insights-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
        border-left: 4px solid #8B5CF6;
        border-top: 1px solid rgba(148, 163, 184, 0.12);
        border-right: 1px solid rgba(148, 163, 184, 0.12);
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 22px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }

    .insights-title {
        font-size: 14px;
        font-weight: 600;
        color: #DDD6FE;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 10px;
    }

    .insights-list {
        margin: 0;
        padding-left: 20px;
        color: #CBD5E1;
        font-size: 13.5px;
        line-height: 1.6;
    }

    .insights-list li {
        margin-bottom: 5px;
    }

    /* Chart Container Card */
    .chart-box {
        background: #1E293B;
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
    }

    /* Footer styling */
    .dashboard-footer {
        text-align: center;
        padding: 30px 10px 20px 10px;
        margin-top: 40px;
        border-top: 1px solid rgba(148, 163, 184, 0.15);
        color: #94A3B8;
        font-size: 13px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==========================================
# DATA LOADING WITH CACHING
# ==========================================
@st.cache_data(show_spinner="Loading and cleaning bug tracking data...")
def load_data_source(file_path):
    """Cached loader for CSV data."""
    if not os.path.exists(file_path):
        generate_sample_dataset(1500, file_path)
    df, msg = utils.load_and_clean_data(file_path)
    return df, msg


def load_uploaded_csv(uploaded_file):
    """Processes uploaded CSV from file buffer."""
    return utils.load_and_clean_data(uploaded_file)


# ==========================================
# SIDEBAR CONTROLS & FILTERS
# ==========================================
def render_sidebar(default_df):
    """Renders sidebar data source selector and filters."""
    st.sidebar.markdown(
        """
        <div style="display: flex; align-items: center; gap: 10px; padding-bottom: 12px; border-bottom: 1px solid rgba(148, 163, 184, 0.2);">
            <span style="font-size: 26px;">🐞</span>
            <div>
                <h3 style="margin: 0; font-size: 17px; color: #F8FAFC;">BugScope AI</h3>
                <p style="margin: 0; font-size: 11px; color: #94A3B8;">Quality Analytics Hub</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown("### 📂 Data Source")
    data_source_mode = st.sidebar.radio(
        "Choose dataset:",
        ["Sample Dataset (1500 Bugs)", "Upload Custom CSV"],
        index=0,
        help="Analyze the pre-generated realistic dataset or upload your own issue-tracking CSV."
    )

    df_base = None
    if data_source_mode == "Sample Dataset (1500 Bugs)":
        data_path = "data/bugs.csv"
        df_base, load_msg = load_data_source(data_path)
        if df_base is None:
            st.sidebar.error(load_msg)
            return None
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Upload CSV File",
            type=["csv"],
            help="Required columns: title, module, severity, status, created_date"
        )
        if uploaded_file is not None:
            df_base, load_msg = load_uploaded_csv(uploaded_file)
            if df_base is None:
                st.sidebar.error(f"⚠️ {load_msg}")
                return None
            else:
                st.sidebar.success(f"✓ Successfully loaded {len(df_base)} bugs!")
        else:
            st.sidebar.info("👆 Please upload a CSV file to begin analysis.")
            return None

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎛️ Filter Backlog")

    # Date Range Filter
    min_date = df_base["created_date"].min().date()
    max_date = df_base["created_date"].max().date()

    date_range = st.sidebar.date_input(
        "Created Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Filter bugs by their initial reporting date."
    )

    # Handle single or double date input
    if isinstance(date_range, (list, tuple)):
        if len(date_range) == 2:
            start_date, end_date = date_range
        elif len(date_range) == 1:
            start_date = date_range[0]
            end_date = max_date
        else:
            start_date, end_date = min_date, max_date
    else:
        start_date, end_date = min_date, max_date

    # Module Filter
    available_modules = sorted(df_base["module"].unique().tolist())
    selected_modules = st.sidebar.multiselect(
        "Module / Subsystem",
        options=available_modules,
        default=available_modules,
        help="Select one or more functional modules."
    )

    # Severity Filter
    available_severities = ["Critical", "High", "Medium", "Low"]
    existing_severities = [s for s in available_severities if s in df_base["severity"].unique()]
    selected_severities = st.sidebar.multiselect(
        "Severity Level",
        options=existing_severities,
        default=existing_severities,
        help="Filter by bug impact level."
    )

    # Status Filter
    available_statuses = ["Open", "In Progress", "Reopened", "Resolved", "Closed"]
    existing_statuses = [s for s in available_statuses if s in df_base["status"].unique()]
    selected_statuses = st.sidebar.multiselect(
        "Status",
        options=existing_statuses,
        default=existing_statuses,
        help="Filter by current defect lifecycle status."
    )

    # Assignee Filter
    available_assignees = sorted(df_base["assignee"].unique().tolist())
    selected_assignees = st.sidebar.multiselect(
        "Assignee",
        options=available_assignees,
        default=available_assignees,
        help="Filter by engineer assigned to the issue."
    )

    # Reset Filters Button
    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

    # Apply Filters
    mask = (
        (df_base["created_date"].dt.date >= start_date) &
        (df_base["created_date"].dt.date <= end_date) &
        (df_base["module"].isin(selected_modules)) &
        (df_base["severity"].isin(selected_severities)) &
        (df_base["status"].isin(selected_statuses)) &
        (df_base["assignee"].isin(selected_assignees))
    )
    filtered_df = df_base[mask].copy()

    # Sidebar Dataset Summary Badge
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"""
        <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 8px; padding: 12px; font-size: 12px;">
            <div style="color: #94A3B8; margin-bottom: 4px;">Dataset Snapshot</div>
            <div style="color: #F8FAFC; font-weight: 600;">Showing {len(filtered_df):,} of {len(df_base):,} bugs</div>
            <div style="color: #64748B; font-size: 11px; margin-top: 4px;">Timespan: {start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    return filtered_df


# ==========================================
# TOP KPI CARDS
# ==========================================
def render_kpi_cards(kpis):
    """Renders top 5 modern KPI metric cards."""
    st.markdown(
        f"""
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-label"><span>📌</span> Total Bugs</div>
                <div class="kpi-value">{kpis['total_bugs']:,}</div>
                <span class="kpi-badge badge-purple">{kpis['resolved_count']:,} resolved</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-label"><span>⏳</span> Open Backlog</div>
                <div class="kpi-value">{kpis['open_bugs']:,}</div>
                <span class="kpi-badge badge-blue">{kpis['open_pct']}% of total</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-label"><span>⏱️</span> Avg Resolution</div>
                <div class="kpi-value">{kpis['avg_resolution_time']} <span style="font-size: 16px; font-weight: 400; color: #94A3B8;">days</span></div>
                <span class="kpi-badge badge-green">Median: {kpis['median_resolution_time']}d</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-label"><span>🚨</span> Critical Issues</div>
                <div class="kpi-value">{kpis['critical_count']:,}</div>
                <span class="kpi-badge badge-red">{kpis['critical_pct']}% critical share</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-label"><span>🔄</span> Reopen Rate</div>
                <div class="kpi-value">{kpis['reopen_rate']}%</div>
                <span class="kpi-badge badge-orange">{kpis['reopen_count']} reopened</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# INSIGHTS COMPONENT
# ==========================================
def render_insights_box(tab_name, df):
    """Renders dynamic plain-English findings for a given tab."""
    insights = utils.generate_insights(tab_name, df)
    bullets = "".join([f"<li>{item}</li>" for item in insights])
    st.markdown(
        f"""
        <div class="insights-card">
            <div class="insights-title">
                <span>💡</span> Key Insights & Pattern Discoveries ({tab_name})
            </div>
            <ul class="insights-list">
                {bullets}
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# MAIN APPLICATION WORKFLOW
# ==========================================
def main():
    # 1. Title Banner
    st.markdown(
        """
        <div class="dashboard-header">
            <h1 class="dashboard-title">
                <span>🐞</span> Bug Tracking Analytics Dashboard
            </h1>
            <p class="dashboard-subtitle">
                Academic Project in Data Analysis & Visualization • Comprehensive issue severity, resolution turnaround, recurrence patterns, and subsystem risk profiling.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Sidebar and Data Filtering
    filtered_df = render_sidebar(default_df=None)

    if filtered_df is None:
        st.stop()

    # Handle Empty Filter Results Gracefully
    if filtered_df.empty:
        st.warning("⚠️ No bugs match the current filter combination. Please broaden your selections in the sidebar (e.g., date range, modules, or severities).")
        st.stop()

    # 3. Top KPI Cards
    kpis = utils.calculate_kpis(filtered_df)
    render_kpi_cards(kpis)

    # 4. Tab Navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview",
        "⚡ Severity Analysis",
        "⏱️ Resolution Time",
        "🔄 Recurring Defects",
        "🧩 Module Insights",
        "🔍 Data Explorer"
    ])

    # ----------------------------------------------------
    # TAB 1: OVERVIEW
    # ----------------------------------------------------
    with tab1:
        render_insights_box("Overview", filtered_df)
        
        # Created vs Resolved Timeline
        fig_timeline = utils.chart_bugs_created_vs_resolved(filtered_df)
        st.plotly_chart(fig_timeline, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            fig_sev_pie = utils.chart_severity_distribution(filtered_df)
            st.plotly_chart(fig_sev_pie, use_container_width=True)
            st.caption("ℹ️ **Severity Distribution**: Proportions of defects categorized by business & technical impact.")

        with col2:
            fig_status = utils.chart_status_breakdown(filtered_df)
            st.plotly_chart(fig_status, use_container_width=True)
            st.caption("ℹ️ **Status Breakdown**: Distribution of bugs across different workflow stages in the issue lifecycle.")

    # ----------------------------------------------------
    # TAB 2: SEVERITY ANALYSIS
    # ----------------------------------------------------
    with tab2:
        render_insights_box("Severity", filtered_df)

        fig_sev_mod = utils.chart_severity_by_module(filtered_df)
        st.plotly_chart(fig_sev_mod, use_container_width=True)
        st.caption("ℹ️ **Stacked Volume**: Total volume and severity distribution across all active functional modules.")

        col1, col2 = st.columns(2)
        with col1:
            fig_sev_trend = utils.chart_severity_trend(filtered_df)
            st.plotly_chart(fig_sev_trend, use_container_width=True)
            st.caption("ℹ️ **Severity Influx**: Monthly trajectory of reported issues segmented by severity.")

        with col2:
            fig_heatmap = utils.chart_severity_module_heatmap(filtered_df)
            st.plotly_chart(fig_heatmap, use_container_width=True)
            st.caption("ℹ️ **Concentration Heatmap**: Pinpoints subsystem hotspots with high density of critical or high-severity defects.")

    # ----------------------------------------------------
    # TAB 3: RESOLUTION TIME
    # ----------------------------------------------------
    with tab3:
        render_insights_box("Resolution Time", filtered_df)

        col1, col2 = st.columns(2)
        with col1:
            fig_res_sev = utils.chart_resolution_by_severity(filtered_df)
            st.plotly_chart(fig_res_sev, use_container_width=True)
            st.caption("ℹ️ **Turnaround by Severity**: Evaluates whether high-priority and critical issues receive faster engineering triage.")

        with col2:
            fig_res_mod = utils.chart_resolution_by_module(filtered_df)
            st.plotly_chart(fig_res_mod, use_container_width=True)
            st.caption("ℹ️ **Turnaround by Module**: Identifies subsystems that suffer from lengthy engineering resolution cycles.")

        col3, col4 = st.columns(2)
        with col3:
            fig_box = utils.chart_resolution_box_plot(filtered_df)
            st.plotly_chart(fig_box, use_container_width=True)
            st.caption("ℹ️ **Distribution & Outliers**: Quartiles and outlier bugs that took significantly longer than standard SLA.")

        with col4:
            fig_hist = utils.chart_resolution_histogram(filtered_df)
            st.plotly_chart(fig_hist, use_container_width=True)
            st.caption("ℹ️ **Histogram with Central Tendencies**: Visualizes the skew of fix durations with Mean and Median markers.")

        # Slowest-10 Bugs Table
        st.markdown("#### 🐢 Top 10 Slowest Resolved Defects")
        slowest_df = utils.get_slowest_bugs(filtered_df, top_n=10)
        if not slowest_df.empty:
            st.dataframe(
                slowest_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Fix Days": st.column_config.NumberColumn(format="%.1f days"),
                    "Bug ID": st.column_config.TextColumn(width="small"),
                    "Severity": st.column_config.TextColumn(width="small"),
                    "Reopens": st.column_config.NumberColumn(width="small")
                }
            )
        else:
            st.info("No resolved bugs available in the current selection.")

    # ----------------------------------------------------
    # TAB 4: RECURRING DEFECTS
    # ----------------------------------------------------
    with tab4:
        render_insights_box("Recurring Defects", filtered_df)

        fig_recur = utils.chart_top_recurring_titles(filtered_df, top_n=10)
        st.plotly_chart(fig_recur, use_container_width=True)
        st.caption("ℹ️ **Recurring Patterns**: Defect titles that appear repeatedly, indicating persistent regression or fragile code paths.")

        col1, col2 = st.columns(2)
        with col1:
            fig_reopen = utils.chart_reopen_rate_by_module(filtered_df)
            st.plotly_chart(fig_reopen, use_container_width=True)
            st.caption("ℹ️ **Reopen Rate %**: Percentage of defects reopened after attempted resolution per module.")

        with col2:
            fig_bubble = utils.chart_recurring_bubble(filtered_df)
            st.plotly_chart(fig_bubble, use_container_width=True)
            st.caption("ℹ️ **Bubble Chart**: X = Occurrence Frequency, Y = Average Fix Days, Size = Reopened Count.")

    # ----------------------------------------------------
    # TAB 5: MODULE INSIGHTS
    # ----------------------------------------------------
    with tab5:
        render_insights_box("Module Insights", filtered_df)

        fig_tree = utils.chart_module_treemap(filtered_df)
        st.plotly_chart(fig_tree, use_container_width=True)
        st.caption("ℹ️ **Hierarchical Treemap**: Visualizes nested defect distributions by Module -> Defect Type -> Severity.")

        st.markdown("#### 🛡️ Subsystem Risk Assessment & Scorecard")
        st.caption("Risk Score (0-100) is a weighted metric factoring in Critical severity density (45%), active open backlog (30%), and reopen rate (25%).")
        
        risk_df = utils.calculate_module_risk_scores(filtered_df)
        if not risk_df.empty:
            st.dataframe(
                risk_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Risk Score": st.column_config.ProgressColumn(
                        "Risk Score (0-100)",
                        format="%.1f",
                        min_value=0,
                        max_value=100
                    ),
                    "Risk Level": st.column_config.TextColumn("Risk Tier"),
                    "Total Bugs": st.column_config.NumberColumn(format="%d"),
                    "Critical Bugs": st.column_config.NumberColumn(format="%d"),
                    "Open Backlog": st.column_config.NumberColumn(format="%d")
                }
            )

    # ----------------------------------------------------
    # TAB 6: DATA EXPLORER
    # ----------------------------------------------------
    with tab6:
        st.markdown("### 🔍 Raw Bug Data Explorer & Export")
        st.write("Search, filter, and inspect detailed records or export the filtered subset to CSV.")

        col_search, col_dl = st.columns([3, 1])
        with col_search:
            search_query = st.text_input(
                "Search bugs (by Bug ID, Title, Reporter, or Assignee):",
                placeholder="e.g. Payment gateway, BUG-1025, Sarah Lee..."
            )

        # Apply search filter
        display_df = filtered_df.copy()
        if search_query.strip():
            q = search_query.strip().lower()
            mask_q = (
                display_df["bug_id"].astype(str).str.lower().str.contains(q) |
                display_df["title"].astype(str).str.lower().str.contains(q) |
                display_df["reporter"].astype(str).str.lower().str.contains(q) |
                display_df["assignee"].astype(str).str.lower().str.contains(q) |
                display_df["module"].astype(str).str.lower().str.contains(q)
            )
            display_df = display_df[mask_q]

        with col_dl:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            csv_data = display_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Filtered CSV",
                data=csv_data,
                file_name=f"bug_data_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        st.caption(f"Displaying **{len(display_df):,}** matching bugs.")

        # Display table with formatting
        explorer_cols = [
            "bug_id", "title", "module", "severity", "priority",
            "status", "assignee", "created_date", "resolution_time_days",
            "defect_type", "reopened_count", "environment"
        ]
        available_exp_cols = [c for c in explorer_cols if c in display_df.columns]

        st.dataframe(
            display_df[available_exp_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "bug_id": st.column_config.TextColumn("Bug ID", width="small"),
                "title": st.column_config.TextColumn("Bug Summary", width="large"),
                "module": st.column_config.TextColumn("Module", width="small"),
                "severity": st.column_config.TextColumn("Severity", width="small"),
                "priority": st.column_config.TextColumn("Priority", width="small"),
                "status": st.column_config.TextColumn("Status", width="small"),
                "assignee": st.column_config.TextColumn("Assignee", width="medium"),
                "created_date": st.column_config.DatetimeColumn("Reported Date", format="YYYY-MM-DD HH:mm"),
                "resolution_time_days": st.column_config.NumberColumn("Fix Days", format="%.1f"),
                "defect_type": st.column_config.TextColumn("Type", width="small"),
                "reopened_count": st.column_config.NumberColumn("Reopens", format="%d"),
                "environment": st.column_config.TextColumn("Env", width="small")
            }
        )

    # 5. Dashboard Footer
    st.markdown(
        """
        <div class="dashboard-footer">
            <div><b>Bug Tracking Analytics Dashboard</b> • College Data Analysis & Visualization Project</div>
            <div style="margin-top: 6px; font-size: 12px; color: #64748B;">
                Designed & Developed by <b>Ranjith Kumar</b> • Built with Python, Pandas, Streamlit & Plotly
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()


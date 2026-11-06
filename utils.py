"""
utils.py - Bug Tracking Analytics Utility Functions
Contains data cleaning, KPI metrics calculation, Plotly chart generation,
and dynamic natural language insight synthesis.
"""

from datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Color Palettes ---
SEVERITY_COLORS = {
    "Critical": "#EF4444",
    "High": "#F97316",
    "Medium": "#FACC15",
    "Low": "#10B981"
}

STATUS_COLORS = {
    "Open": "#3B82F6",
    "In Progress": "#8B5CF6",
    "Reopened": "#EC4899",
    "Resolved": "#10B981",
    "Closed": "#64748B"
}

DEFECT_TYPE_COLORS = {
    "UI": "#60A5FA",
    "Logic": "#A78BFA",
    "Performance": "#F59E0B",
    "Security": "#EF4444",
    "Crash": "#F43F5E",
    "Data": "#14B8A6"
}

PLOT_TEMPLATE = "plotly_dark"
CHART_BG_COLOR = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(148, 163, 184, 0.15)"
TEXT_COLOR = "#F8FAFC"


def apply_theme(fig, title=None, height=400, show_legend=True):
    """Applies consistent dark-modern aesthetic to Plotly figures."""
    fig.update_layout(
        template=PLOT_TEMPLATE,
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(size=15, color=TEXT_COLOR, family="sans-serif"),
            x=0.01,
            y=0.96
        ),
        paper_bgcolor=CHART_BG_COLOR,
        plot_bgcolor=CHART_BG_COLOR,
        font=dict(family="sans-serif", color="#CBD5E1", size=12),
        height=height,
        margin=dict(l=40, r=30, t=55 if title else 25, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11)
        ) if show_legend else dict(visible=False),
        xaxis=dict(
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            showline=True,
            linecolor=GRID_COLOR
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            showline=True,
            linecolor=GRID_COLOR
        ),
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_size=12,
            font_family="sans-serif",
            bordercolor="#475569"
        )
    )
    return fig


def load_and_clean_data(file_source):
    """
    Loads bug dataset from path or uploaded file buffer.
    Performs validation, date parsing, missing value handling,
    and calculates resolution_time_days if missing.
    """
    try:
        df = pd.read_csv(file_source)
    except Exception as e:
        return None, f"Failed to read CSV: {str(e)}"

    # Required core columns
    required_cols = ["title", "module", "severity", "status", "created_date"]
    missing_required = [c for c in required_cols if c not in df.columns]
    if missing_required:
        return None, f"Missing required columns in CSV: {', '.join(missing_required)}"

    df = df.copy()

    # If bug_id is missing, auto-generate it
    if "bug_id" not in df.columns:
        df["bug_id"] = [f"BUG-{1000 + i}" for i in range(1, len(df) + 1)]

    # Standardize string fields
    for col in ["severity", "status", "environment"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    if "module" in df.columns:
        df["module"] = df["module"].astype(str).str.strip().apply(lambda m: "API" if m.upper() == "API" else m.title())

    if "defect_type" in df.columns:
        df["defect_type"] = df["defect_type"].astype(str).str.strip().apply(lambda d: "UI" if d.upper() == "UI" else d.title())

    # Standardize Severity labels
    sev_map = {"Critical": "Critical", "High": "High", "Medium": "Medium", "Low": "Low"}
    df["severity"] = df["severity"].apply(lambda s: sev_map.get(s, "Medium"))

    # Standardize Status labels
    status_map = {
        "Open": "Open", "In Progress": "In Progress",
        "Reopened": "Reopened", "Resolved": "Resolved", "Closed": "Closed"
    }
    df["status"] = df["status"].apply(lambda s: status_map.get(s, "Open"))

    # Parse dates
    df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
    # Drop rows where created_date couldn't be parsed
    df = df.dropna(subset=["created_date"])

    if "resolved_date" in df.columns:
        df["resolved_date"] = pd.to_datetime(df["resolved_date"], errors="coerce")
    else:
        df["resolved_date"] = pd.NaT

    # Compute resolution_time_days if missing or null for resolved bugs
    if "resolution_time_days" not in df.columns:
        df["resolution_time_days"] = np.nan

    mask_resolved = df["status"].isin(["Resolved", "Closed"]) & df["resolved_date"].notna()
    calculated_days = (df.loc[mask_resolved, "resolved_date"] - df.loc[mask_resolved, "created_date"]).dt.total_seconds() / 86400.0
    calculated_days = calculated_days.clip(lower=0.1).round(1)
    
    # Fill in calculated days where resolution_time_days was missing
    df.loc[mask_resolved, "resolution_time_days"] = df.loc[mask_resolved, "resolution_time_days"].fillna(calculated_days)

    # For open bugs, ensure resolved_date and resolution_time_days are null
    mask_open = df["status"].isin(["Open", "In Progress", "Reopened"])
    df.loc[mask_open, "resolved_date"] = pd.NaT
    df.loc[mask_open, "resolution_time_days"] = np.nan

    # Fill defaults for optional columns
    if "assignee" not in df.columns:
        df["assignee"] = "Unassigned"
    else:
        df["assignee"] = df["assignee"].fillna("Unassigned").astype(str).str.strip()

    if "reporter" not in df.columns:
        df["reporter"] = "Anonymous"
    else:
        df["reporter"] = df["reporter"].fillna("Anonymous").astype(str).str.strip()

    if "environment" not in df.columns:
        df["environment"] = "Production"
    else:
        df["environment"] = df["environment"].fillna("Not Specified").astype(str).str.strip()

    if "defect_type" not in df.columns:
        df["defect_type"] = "Logic"
    else:
        df["defect_type"] = df["defect_type"].fillna("Logic").astype(str).str.strip()

    if "reopened_count" not in df.columns:
        df["reopened_count"] = 0
    else:
        df["reopened_count"] = pd.to_numeric(df["reopened_count"], errors="coerce").fillna(0).astype(int)

    if "priority" not in df.columns:
        # Infer priority from severity
        p_map = {"Critical": "P0", "High": "P1", "Medium": "P2", "Low": "P3"}
        df["priority"] = df["severity"].map(p_map)
    else:
        df["priority"] = df["priority"].fillna("P2").astype(str).str.strip()

    # Add useful derived helper columns for grouping
    df["created_month"] = df["created_date"].dt.to_period("M").dt.to_timestamp()
    df["created_month_str"] = df["created_date"].dt.strftime("%Y-%m")
    
    return df, "Success"


def calculate_kpis(df):
    """Computes high-level KPI metrics for the header cards."""
    total_bugs = len(df)
    if total_bugs == 0:
        return {
            "total_bugs": 0,
            "open_bugs": 0,
            "open_pct": 0.0,
            "avg_resolution_time": 0.0,
            "median_resolution_time": 0.0,
            "critical_count": 0,
            "critical_pct": 0.0,
            "reopen_count": 0,
            "reopen_rate": 0.0,
            "resolved_count": 0
        }

    open_mask = df["status"].isin(["Open", "In Progress", "Reopened"])
    open_bugs = int(open_mask.sum())
    open_pct = round((open_bugs / total_bugs) * 100, 1)

    resolved_mask = df["status"].isin(["Resolved", "Closed"])
    resolved_count = int(resolved_mask.sum())

    res_times = df.loc[resolved_mask, "resolution_time_days"].dropna()
    avg_res_time = round(float(res_times.mean()), 1) if not res_times.empty else 0.0
    median_res_time = round(float(res_times.median()), 1) if not res_times.empty else 0.0

    critical_count = int((df["severity"] == "Critical").sum())
    critical_pct = round((critical_count / total_bugs) * 100, 1)

    reopen_count = int((df["reopened_count"] > 0).sum())
    reopen_rate = round((reopen_count / total_bugs) * 100, 1)

    return {
        "total_bugs": total_bugs,
        "open_bugs": open_bugs,
        "open_pct": open_pct,
        "avg_resolution_time": avg_res_time,
        "median_resolution_time": median_res_time,
        "critical_count": critical_count,
        "critical_pct": critical_pct,
        "reopen_count": reopen_count,
        "reopen_rate": reopen_rate,
        "resolved_count": resolved_count
    }


# ==========================================
# CHART BUILDERS
# ==========================================

# 1. Overview Tab Charts
def chart_bugs_created_vs_resolved(df):
    """Line chart tracking bugs created vs bugs resolved monthly."""
    # Monthly created
    created = df.set_index("created_date").resample("ME")["bug_id"].count().rename("Created")
    
    # Monthly resolved
    resolved_df = df.dropna(subset=["resolved_date"]).copy()
    if not resolved_df.empty:
        resolved = resolved_df.set_index("resolved_date").resample("ME")["bug_id"].count().rename("Resolved")
        timeline = pd.concat([created, resolved], axis=1).fillna(0).reset_index()
        timeline.rename(columns={"index": "Month"}, inplace=True)
    else:
        timeline = created.reset_index()
        timeline.rename(columns={"created_date": "Month"}, inplace=True)
        timeline["Resolved"] = 0

    timeline["Month_Str"] = pd.to_datetime(timeline["Month"]).dt.strftime("%b %Y")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timeline["Month_Str"],
        y=timeline["Created"],
        mode="lines+markers",
        name="Created",
        line=dict(color="#8B5CF6", width=3, shape="spline"),
        marker=dict(size=7, color="#8B5CF6")
    ))
    fig.add_trace(go.Scatter(
        x=timeline["Month_Str"],
        y=timeline["Resolved"],
        mode="lines+markers",
        name="Resolved",
        line=dict(color="#10B981", width=3, shape="spline", dash="dot"),
        marker=dict(size=7, color="#10B981")
    ))
    return apply_theme(fig, "Bugs Created vs Resolved Over Time (Monthly Velocity)", height=380)


def chart_severity_distribution(df):
    """Donut chart of severity breakdown."""
    counts = df["severity"].value_counts().reset_index()
    counts.columns = ["Severity", "Count"]
    
    # Ensure standard order
    order = ["Critical", "High", "Medium", "Low"]
    counts["Order"] = counts["Severity"].map(lambda x: order.index(x) if x in order else 99)
    counts = counts.sort_values("Order")

    fig = px.pie(
        counts,
        names="Severity",
        values="Count",
        hole=0.55,
        color="Severity",
        color_discrete_map=SEVERITY_COLORS
    )
    fig.update_traces(
        textinfo="percent+label",
        hoverinfo="label+value+percent",
        marker=dict(line=dict(color="#0F172A", width=2))
    )
    return apply_theme(fig, "Severity Distribution", height=380)


def chart_status_breakdown(df):
    """Horizontal bar chart showing status breakdown."""
    counts = df["status"].value_counts().reset_index()
    counts.columns = ["Status", "Count"]
    
    # Order: Open, In Progress, Reopened, Resolved, Closed
    status_order = ["Closed", "Resolved", "Reopened", "In Progress", "Open"]
    counts["Order"] = counts["Status"].map(lambda x: status_order.index(x) if x in status_order else 99)
    counts = counts.sort_values("Order")

    fig = px.bar(
        counts,
        x="Count",
        y="Status",
        orientation="h",
        color="Status",
        color_discrete_map=STATUS_COLORS,
        text="Count"
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(showlegend=False)
    return apply_theme(fig, "Bug Lifecycle Status Breakdown", height=380, show_legend=False)


# 2. Severity Analysis Charts
def chart_severity_by_module(df):
    """Stacked bar chart showing Severity count by Module."""
    crosstab = pd.crosstab(df["module"], df["severity"]).reset_index()
    
    # Order columns
    for col in ["Critical", "High", "Medium", "Low"]:
        if col not in crosstab.columns:
            crosstab[col] = 0
            
    crosstab["Total"] = crosstab["Critical"] + crosstab["High"] + crosstab["Medium"] + crosstab["Low"]
    crosstab = crosstab.sort_values("Total", ascending=True)

    fig = go.Figure()
    for sev in ["Low", "Medium", "High", "Critical"]:
        fig.add_trace(go.Bar(
            y=crosstab["module"],
            x=crosstab[sev],
            name=sev,
            orientation="h",
            marker=dict(color=SEVERITY_COLORS[sev])
        ))
    
    fig.update_layout(barmode="stack")
    return apply_theme(fig, "Severity Breakdown by Module (Stacked Volume)", height=420)


def chart_severity_trend(df):
    """Monthly trend of bug counts broken down by severity."""
    trend = df.groupby(["created_month_str", "severity"])["bug_id"].count().unstack(fill_value=0).reset_index()
    trend = trend.sort_values("created_month_str")

    fig = go.Figure()
    for sev in ["Critical", "High", "Medium", "Low"]:
        if sev in trend.columns:
            fig.add_trace(go.Scatter(
                x=trend["created_month_str"],
                y=trend[sev],
                mode="lines+markers",
                name=sev,
                line=dict(color=SEVERITY_COLORS[sev], width=2.5),
                marker=dict(size=6)
            ))
    return apply_theme(fig, "Severity Influx Trend Across Months", height=400)


def chart_severity_module_heatmap(df):
    """Heatmap showing concentration of bugs across Module vs Severity."""
    ct = pd.crosstab(df["module"], df["severity"])
    # Reindex columns
    cols = [c for c in ["Critical", "High", "Medium", "Low"] if c in ct.columns]
    ct = ct[cols]

    fig = px.imshow(
        ct,
        labels=dict(x="Severity", y="Module", color="Bug Count"),
        x=cols,
        y=ct.index,
        color_continuous_scale="Purples",
        text_auto=True
    )
    fig.update_coloraxes(showscale=False)
    return apply_theme(fig, "Concentration Heatmap: Module vs Severity", height=400, show_legend=False)


# 3. Resolution Time Charts
def chart_resolution_by_severity(df):
    """Bar chart for average resolution time by severity."""
    res_df = df.dropna(subset=["resolution_time_days"])
    if res_df.empty:
        return go.Figure()

    avg_sev = res_df.groupby("severity")["resolution_time_days"].agg(["mean", "median", "count"]).reset_index()
    order = ["Critical", "High", "Medium", "Low"]
    avg_sev["Order"] = avg_sev["severity"].map(lambda x: order.index(x) if x in order else 99)
    avg_sev = avg_sev.sort_values("Order")
    avg_sev["mean"] = avg_sev["mean"].round(1)

    fig = px.bar(
        avg_sev,
        x="severity",
        y="mean",
        color="severity",
        color_discrete_map=SEVERITY_COLORS,
        text="mean",
        labels={"severity": "Severity", "mean": "Avg Days to Fix"}
    )
    fig.update_traces(texttemplate="%{text} days", textposition="outside")
    fig.update_layout(showlegend=False)
    return apply_theme(fig, "Average Resolution Days by Severity", height=380, show_legend=False)


def chart_resolution_by_module(df):
    """Bar chart for average resolution time by module."""
    res_df = df.dropna(subset=["resolution_time_days"])
    if res_df.empty:
        return go.Figure()

    avg_mod = res_df.groupby("module")["resolution_time_days"].mean().reset_index()
    avg_mod["resolution_time_days"] = avg_mod["resolution_time_days"].round(1)
    avg_mod = avg_mod.sort_values("resolution_time_days", ascending=True)

    fig = px.bar(
        avg_mod,
        x="resolution_time_days",
        y="module",
        orientation="h",
        color="resolution_time_days",
        color_continuous_scale="Blues",
        text="resolution_time_days",
        labels={"module": "Module", "resolution_time_days": "Avg Fix Days"}
    )
    fig.update_traces(texttemplate="%{text} d", textposition="outside")
    fig.update_coloraxes(showscale=False)
    return apply_theme(fig, "Average Resolution Days by Module", height=380, show_legend=False)


def chart_resolution_box_plot(df):
    """Box plot showing resolution time spread across severities."""
    res_df = df.dropna(subset=["resolution_time_days"]).copy()
    if res_df.empty:
        return go.Figure()

    fig = px.box(
        res_df,
        x="severity",
        y="resolution_time_days",
        color="severity",
        category_orders={"severity": ["Critical", "High", "Medium", "Low"]},
        color_discrete_map=SEVERITY_COLORS,
        points="outliers",
        labels={"severity": "Severity", "resolution_time_days": "Days to Resolve"}
    )
    fig.update_layout(showlegend=False)
    return apply_theme(fig, "Resolution Days Distribution & Outliers (Box Plot)", height=380, show_legend=False)


def chart_resolution_histogram(df):
    """Histogram of resolution times with Mean and Median reference lines."""
    res_df = df.dropna(subset=["resolution_time_days"])
    if res_df.empty:
        return go.Figure()

    mean_val = res_df["resolution_time_days"].mean()
    median_val = res_df["resolution_time_days"].median()

    fig = px.histogram(
        res_df,
        x="resolution_time_days",
        nbins=35,
        color_discrete_sequence=["#8B5CF6"],
        labels={"resolution_time_days": "Resolution Time (Days)"}
    )
    fig.add_vline(x=mean_val, line_dash="dash", line_color="#EF4444", annotation_text=f"Mean: {mean_val:.1f}d", annotation_position="top right")
    fig.add_vline(x=median_val, line_dash="dot", line_color="#10B981", annotation_text=f"Median: {median_val:.1f}d", annotation_position="top left")
    return apply_theme(fig, "Resolution Time Frequency Distribution", height=380, show_legend=False)


def get_slowest_bugs(df, top_n=10):
    """Returns the top slowest resolved bugs."""
    res_df = df.dropna(subset=["resolution_time_days"]).copy()
    if res_df.empty:
        return pd.DataFrame()
    cols = ["bug_id", "title", "module", "severity", "resolution_time_days", "assignee", "defect_type", "reopened_count"]
    slowest = res_df.sort_values("resolution_time_days", ascending=False).head(top_n)[cols]
    slowest.rename(columns={
        "bug_id": "Bug ID",
        "title": "Bug Title",
        "module": "Module",
        "severity": "Severity",
        "resolution_time_days": "Fix Days",
        "assignee": "Assignee",
        "defect_type": "Defect Type",
        "reopened_count": "Reopens"
    }, inplace=True)
    return slowest


# 4. Recurring Defects Charts
def chart_top_recurring_titles(df, top_n=8):
    """Horizontal bar chart of top recurring bug titles."""
    top_titles = df["title"].value_counts().head(top_n).reset_index()
    top_titles.columns = ["Bug Title", "Occurrences"]
    top_titles = top_titles.sort_values("Occurrences", ascending=True)

    # Truncate long titles for neat display
    top_titles["Display_Title"] = top_titles["Bug Title"].apply(
        lambda t: (t[:45] + "...") if len(t) > 48 else t
    )

    fig = px.bar(
        top_titles,
        x="Occurrences",
        y="Display_Title",
        orientation="h",
        color="Occurrences",
        color_continuous_scale="Purples",
        text="Occurrences",
        custom_data=["Bug Title"]
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{customdata[0]}</b><br>Occurrences: %{x}<extra></extra>"
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(yaxis_title="")
    return apply_theme(fig, f"Top {top_n} Most Recurrent Bug Titles", height=400, show_legend=False)


def chart_reopen_rate_by_module(df):
    """Bar chart showing reopen rate percentage per module."""
    mod_stats = df.groupby("module").agg(
        total=("bug_id", "count"),
        reopened=("reopened_count", lambda s: (s > 0).sum())
    ).reset_index()
    mod_stats["Reopen_Rate"] = ((mod_stats["reopened"] / mod_stats["total"]) * 100).round(1)
    mod_stats = mod_stats.sort_values("Reopen_Rate", ascending=True)

    fig = px.bar(
        mod_stats,
        x="Reopen_Rate",
        y="module",
        orientation="h",
        color="Reopen_Rate",
        color_continuous_scale="Reds",
        text="Reopen_Rate",
        labels={"module": "Module", "Reopen_Rate": "Reopen Rate (%)"}
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_coloraxes(showscale=False)
    return apply_theme(fig, "Bug Reopen Rate by Module (%)", height=380, show_legend=False)


def chart_recurring_bubble(df):
    """
    Bubble chart showing Defect Types / Modules:
    X: Frequency (Count)
    Y: Avg Resolution Time
    Size: Reopen Count + 1
    Color: Module
    """
    res_df = df.dropna(subset=["resolution_time_days"]).copy()
    if res_df.empty:
        return go.Figure()

    grouped = res_df.groupby(["module", "defect_type"]).agg(
        Count=("bug_id", "count"),
        Avg_Fix_Days=("resolution_time_days", "mean"),
        Total_Reopened=("reopened_count", "sum"),
        Critical_Count=("severity", lambda s: (s == "Critical").sum())
    ).reset_index()

    grouped["Avg_Fix_Days"] = grouped["Avg_Fix_Days"].round(1)
    grouped["Bubble_Size"] = grouped["Total_Reopened"] + 8  # Scale for visibility

    fig = px.scatter(
        grouped,
        x="Count",
        y="Avg_Fix_Days",
        size="Bubble_Size",
        color="module",
        hover_name="defect_type",
        hover_data={"module": True, "Count": True, "Avg_Fix_Days": True, "Total_Reopened": True, "Bubble_Size": False},
        labels={
            "Count": "Defect Frequency",
            "Avg_Fix_Days": "Avg Fix Time (Days)",
            "module": "Module"
        }
    )
    fig.update_traces(marker=dict(opacity=0.85, line=dict(width=1, color="#1E293B")))
    return apply_theme(fig, "Defect Frequency vs Avg Resolution Time (Bubble Size = Reopens)", height=420)


# 5. Module Insights Charts
def chart_module_treemap(df):
    """Treemap of Module -> Defect Type hierarchy."""
    grouped = df.groupby(["module", "defect_type", "severity"])["bug_id"].count().reset_index()
    grouped.columns = ["Module", "Defect_Type", "Severity", "Count"]

    fig = px.treemap(
        grouped,
        path=["Module", "Defect_Type", "Severity"],
        values="Count",
        color="Module",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig.update_traces(
        textinfo="label+value+percent parent",
        hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>"
    )
    return apply_theme(fig, "Module & Defect Type Hierarchy Treemap", height=450, show_legend=False)


def calculate_module_risk_scores(df):
    """
    Computes weighted risk scores per module:
    Severity weights: Critical: 4, High: 3, Medium: 2, Low: 1
    Risk Index combines weighted severity, reopen rate, and open backlog percentage.
    """
    if df.empty:
        return pd.DataFrame()

    records = []
    sev_weights = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}

    for module, m_df in df.groupby("module"):
        total = len(m_df)
        crit_count = int((m_df["severity"] == "Critical").sum())
        high_count = int((m_df["severity"] == "High").sum())
        open_count = int(m_df["status"].isin(["Open", "In Progress", "Reopened"]).sum())
        reopened_bugs = int((m_df["reopened_count"] > 0).sum())

        avg_fix = m_df["resolution_time_days"].dropna().mean()
        avg_fix_str = f"{avg_fix:.1f}d" if pd.notna(avg_fix) else "N/A"

        # Severity score (1 to 4)
        sev_score = sum(m_df["severity"].map(sev_weights)) / total

        # Percentage components
        crit_pct = (crit_count / total) * 100
        open_pct = (open_count / total) * 100
        reopen_pct = (reopened_bugs / total) * 100

        # Composite risk score formula: 0 to 100
        # 45% based on severity, 30% based on open backlog, 25% based on reopen rate
        raw_risk = (
            ((sev_score - 1.0) / 3.0) * 45 +
            (min(open_pct, 40) / 40.0) * 30 +
            (min(reopen_pct, 30) / 30.0) * 25
        )
        risk_score = min(100.0, max(10.0, raw_risk))

        if risk_score >= 65:
            tier = "🔴 Critical Risk"
        elif risk_score >= 45:
            tier = "🟠 High Risk"
        elif risk_score >= 30:
            tier = "🟡 Moderate"
        else:
            tier = "🟢 Low Risk"

        records.append({
            "Module": module,
            "Total Bugs": total,
            "Critical Bugs": crit_count,
            "Critical %": f"{crit_pct:.1f}%",
            "Open Backlog": open_count,
            "Reopen Rate": f"{reopen_pct:.1f}%",
            "Avg Fix Time": avg_fix_str,
            "Risk Score": round(risk_score, 1),
            "Risk Level": tier
        })

    risk_df = pd.DataFrame(records).sort_values("Risk Score", ascending=False)
    return risk_df


# ==========================================
# DYNAMIC INSIGHTS ENGINE
# ==========================================
def generate_insights(tab_name, df):
    """
    Generates 2-3 dynamic, context-aware plain-English findings
    from the current filtered dataset.
    """
    if df.empty:
        return [
            "No bug records match the current filter criteria.",
            "Try broadening your date range or selecting more modules in the sidebar."
        ]

    total = len(df)
    insights = []

    if tab_name == "Overview":
        # 1. Open vs resolved insight
        open_count = int(df["status"].isin(["Open", "In Progress", "Reopened"]).sum())
        open_pct = round((open_count / total) * 100, 1)
        insights.append(
            f"Currently <b>{open_count} bugs ({open_pct}%)</b> are active in the development backlog, "
            f"while <b>{total - open_count} bugs</b> have been resolved or closed."
        )

        # 2. Critical & High share
        crit_high = int(df["severity"].isin(["Critical", "High"]).sum())
        crit_high_pct = round((crit_high / total) * 100, 1)
        top_module = df["module"].value_counts().index[0]
        top_module_cnt = df["module"].value_counts().iloc[0]
        insights.append(
            f"High-impact issues (Critical + High) make up <b>{crit_high_pct}%</b> of all reports, "
            f"with <b>{top_module}</b> reporting the highest volume ({top_module_cnt} defects)."
        )

        # 3. Time velocity
        res_df = df.dropna(subset=["resolution_time_days"])
        if not res_df.empty:
            avg_days = res_df["resolution_time_days"].mean()
            insights.append(
                f"Overall mean resolution turnaround is <b>{avg_days:.1f} days</b> across the filtered timeframe."
            )

    elif tab_name == "Severity":
        # 1. Highest critical share module
        crit_by_mod = df[df["severity"] == "Critical"]["module"].value_counts()
        if not crit_by_mod.empty:
            top_crit_mod = crit_by_mod.index[0]
            top_crit_cnt = crit_by_mod.iloc[0]
            mod_total = len(df[df["module"] == top_crit_mod])
            pct = round((top_crit_cnt / mod_total) * 100, 1) if mod_total > 0 else 0
            insights.append(
                f"<b>{top_crit_mod}</b> holds the highest critical bug ratio at <b>{pct}%</b> "
                f"({top_crit_cnt} out of {mod_total} bugs in that module)."
            )

        # 2. Distribution comparison
        crit_count = (df["severity"] == "Critical").sum()
        low_count = (df["severity"] == "Low").sum()
        insights.append(
            f"Critical defects ({crit_count}) represent <b>{round(crit_count/total*100, 1)}%</b> of issues, "
            f"compared to Low priority defects ({low_count}) at <b>{round(low_count/total*100, 1)}%</b>."
        )

        # 3. Trend insight
        monthly_crit = df[df["severity"] == "Critical"].groupby("created_month_str")["bug_id"].count()
        if len(monthly_crit) >= 2:
            latest_m = monthly_crit.index[-1]
            latest_v = monthly_crit.iloc[-1]
            insights.append(
                f"In the most recent recorded month (<b>{latest_m}</b>), <b>{latest_v} Critical defects</b> were opened."
            )

    elif tab_name == "Resolution Time":
        res_df = df.dropna(subset=["resolution_time_days"])
        if not res_df.empty:
            # 1. Critical vs Low speed
            crit_time = res_df[res_df["severity"] == "Critical"]["resolution_time_days"].mean()
            low_time = res_df[res_df["severity"] == "Low"]["resolution_time_days"].mean()
            if pd.notna(crit_time) and pd.notna(low_time) and crit_time > 0:
                speed_ratio = round(low_time / crit_time, 1)
                insights.append(
                    f"Engineering prioritized severity: Critical bugs were resolved in an average of <b>{crit_time:.1f} days</b>, "
                    f"which is <b>{speed_ratio}x faster</b> than Low severity items ({low_time:.1f} days)."
                )

            # 2. Fastest vs slowest module
            mod_means = res_df.groupby("module")["resolution_time_days"].mean()
            fastest_mod = mod_means.idxmin()
            slowest_mod = mod_means.idxmax()
            insights.append(
                f"<b>{fastest_mod}</b> boasts the fastest mean resolution at <b>{mod_means.min():.1f} days</b>, "
                f"while <b>{slowest_mod}</b> had the longest turnaround at <b>{mod_means.max():.1f} days</b>."
            )

            # 3. Median insight
            med = res_df["resolution_time_days"].median()
            insights.append(
                f"50% of all closed defects were resolved within <b>{med:.1f} days</b> (median resolution time)."
            )

    elif tab_name == "Recurring Defects":
        # 1. Top recurring bug
        top_title = df["title"].value_counts().index[0]
        top_cnt = df["title"].value_counts().iloc[0]
        insights.append(
            f"The single most repeated defect pattern is <i>\"{top_title}\"</i> with <b>{top_cnt} recorded instances</b>."
        )

        # 2. Highest reopen rate module
        mod_reopens = df.groupby("module").agg(
            total=("bug_id", "count"),
            reopened=("reopened_count", lambda s: (s > 0).sum())
        )
        mod_reopens["rate"] = (mod_reopens["reopened"] / mod_reopens["total"]) * 100
        worst_reopen_mod = mod_reopens["rate"].idxmax()
        worst_rate = mod_reopens["rate"].max()
        insights.append(
            f"<b>{worst_reopen_mod}</b> suffers the highest reopen rate at <b>{worst_rate:.1f}%</b>, "
            f"suggesting regressions or incomplete patch verification in this area."
        )

        # 3. Defect type distribution among reopens
        reopened_df = df[df["reopened_count"] > 0]
        if not reopened_df.empty:
            top_dt = reopened_df["defect_type"].value_counts().index[0]
            top_dt_cnt = reopened_df["defect_type"].value_counts().iloc[0]
            insights.append(
                f"<b>{top_dt}</b> is the most frequent defect type among reopened tickets ({top_dt_cnt} instances)."
            )

    elif tab_name == "Module Insights":
        risk_df = calculate_module_risk_scores(df)
        if not risk_df.empty:
            top_risk = risk_df.iloc[0]
            lowest_risk = risk_df.iloc[-1]
            insights.append(
                f"<b>{top_risk['Module']}</b> exhibits the highest cumulative risk score at <b>{top_risk['Risk Score']}/100</b> "
                f"({top_risk['Risk Level']}) driven by {top_risk['Critical Bugs']} Critical defects."
            )
            insights.append(
                f"<b>{lowest_risk['Module']}</b> has the healthiest profile with a risk score of <b>{lowest_risk['Risk Score']}/100</b> "
                f"({lowest_risk['Risk Level']})."
            )
            total_crit = int((df["severity"] == "Critical").sum())
            insights.append(
                f"Across all modules, {total_crit} critical bugs require SLA compliance monitoring."
            )

    return insights

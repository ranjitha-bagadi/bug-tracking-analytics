"""
data_generator.py - Realistic Bug Tracking Dataset Generator
Generates ~1500 realistic issue-tracking records spread across 12 months
with realistic correlation between module, severity, resolution time, and defect recurrence.
"""

import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

MODULES = [
    "Payments", "API", "Login", "Dashboard",
    "Search", "Reports", "Notifications", "Profile"
]

SEVERITIES = ["Critical", "High", "Medium", "Low"]
PRIORITIES = ["P0", "P1", "P2", "P3"]
DEFECT_TYPES = ["UI", "Logic", "Performance", "Security", "Crash", "Data"]
ENVIRONMENTS = ["Production", "Staging", "QA", "Development"]

REPORTERS = [
    "Alex Johnson", "Sarah Lee", "Priya Sharma", "David Kim",
    "Elena Rostova", "Marcus Chen", "Carlos Mendez", "Emily Watson",
    "Aiden Clark", "Rachel Green"
]

ASSIGNEES = [
    "Liam Scott", "Noah Martinez", "Emma Davies", "Sophia Wang",
    "Ethan Brown", "Olivia Miller", "Lucas Garcia", "Mia Tanaka",
    "James Wilson", "Chloe Taylor"
]

# Recurring bug title templates per module
RECURRING_TITLES = {
    "Payments": [
        "Payment gateway timeout on 3D Secure verification",
        "Duplicate transaction charge on double-click checkout",
        "Refund status webhook deserialization failure",
        "Stripe API rate limit exceeded during peak checkout",
        "Multi-currency conversion rounding error in invoice total",
        "PayPal button disabled when coupon applied"
    ],
    "API": [
        "500 Internal Server Error on /api/v2/orders endpoint",
        "JWT access token validation fails after refresh",
        "CORS policy header missing on preflight requests",
        "Database connection pool exhausted under concurrent load",
        "Rate limiter throttles valid authenticated webhooks",
        "GraphQL schema query timeout on nested relations"
    ],
    "Login": [
        "OAuth2 Google single sign-on redirect loop",
        "User session invalidated prematurely after 5 minutes",
        "Password reset token marked expired immediately",
        "MFA SMS one-time passcode delivery timeout",
        "Remember Me persistent auth cookie ignored on Safari",
        "Account lockout threshold triggers on valid logins"
    ],
    "Dashboard": [
        "Memory leak causing browser tab freeze on live metrics",
        "Widget cards overlap on 1366x768 display resolution",
        "KPI metrics card displays NaN when zero records match",
        "CSV export download fails when range exceeds 90 days",
        "WebSocket connection drops and fails to reconnect",
        "Dark theme contrast ratio fails accessibility check"
    ],
    "Search": [
        "Elasticsearch index timeout during bulk text query",
        "Special characters in search query trigger unhandled 500",
        "Pagination reset to page 1 upon sorting by date",
        "Fuzzy matching returns zero-confidence irrelevant items",
        "Auto-complete dropdown freezes after 3 rapid keystrokes",
        "Filters reset when user navigates back in browser"
    ],
    "Reports": [
        "PDF generation memory limit exceeded on large records",
        "Scheduled automated email report fails with SMTP auth error",
        "Mismatch between chart aggregate sum and tabular export",
        "Timezone shift alters daily aggregation bucket by 1 day",
        "Excel report formatting corrupted for non-ASCII characters",
        "Background worker worker-pool killed during monthly report"
    ],
    "Notifications": [
        "Push notification delivery delayed by over 45 minutes",
        "Unread badge counter out of sync with actual read state",
        "Email notification template renders raw HTML tags",
        "Duplicate notification dispatched on order status update",
        "Unsubscribe link in notification footer returns 404",
        "Slack webhook integration drops notification payloads"
    ],
    "Profile": [
        "Avatar image upload fails with 413 Payload Too Large",
        "Phone number validation regex rejects international prefix",
        "Profile update not immediately propagated to session claims",
        "Dark mode preference toggle does not persist across logins",
        "Account deletion cascade fails due to foreign key constraint",
        "User bio text field truncates UTF-8 emoji characters"
    ]
}

def generate_sample_dataset(num_records=1500, output_path="data/bugs.csv"):
    """Generates realistic bug tracking dataset."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    total_seconds = int((end_date - start_date).total_seconds())
    
    bugs = []
    
    # Define module distribution weights (Payments & API are busier)
    module_weights = [0.18, 0.17, 0.12, 0.12, 0.11, 0.10, 0.10, 0.10]
    
    for i in range(1, num_records + 1):
        bug_id = f"BUG-{1000 + i}"
        
        # Pick module
        module = np.random.choice(MODULES, p=module_weights)
        
        # Severity distribution: Payments & API have higher critical/high share
        if module in ["Payments", "API"]:
            sev_weights = [0.32, 0.38, 0.22, 0.08]
        elif module in ["Reports", "Dashboard"]:
            sev_weights = [0.12, 0.32, 0.40, 0.16]
        else:
            sev_weights = [0.14, 0.28, 0.38, 0.20]
        severity = np.random.choice(SEVERITIES, p=sev_weights)
        
        # Priority correlated with Severity
        if severity == "Critical":
            priority = np.random.choice(PRIORITIES, p=[0.80, 0.18, 0.02, 0.00])
        elif severity == "High":
            priority = np.random.choice(PRIORITIES, p=[0.15, 0.70, 0.14, 0.01])
        elif severity == "Medium":
            priority = np.random.choice(PRIORITIES, p=[0.02, 0.20, 0.70, 0.08])
        else: # Low
            priority = np.random.choice(PRIORITIES, p=[0.00, 0.02, 0.20, 0.78])
            
        # Defect Type correlation
        if severity in ["Critical", "High"] and module in ["API", "Payments"]:
            defect_type = np.random.choice(
                DEFECT_TYPES, 
                p=[0.05, 0.30, 0.25, 0.20, 0.15, 0.05]
            )
        elif module in ["Dashboard", "Profile"]:
            defect_type = np.random.choice(
                DEFECT_TYPES,
                p=[0.45, 0.25, 0.15, 0.02, 0.05, 0.08]
            )
        else:
            defect_type = np.random.choice(
                DEFECT_TYPES,
                p=[0.25, 0.25, 0.18, 0.10, 0.12, 0.10]
            )
            
        # Title: 70% chance of a recurring title template, 30% generic variant
        if random.random() < 0.72:
            title = random.choice(RECURRING_TITLES[module])
        else:
            # Variations
            variations = [
                f"{defect_type} issue detected in {module} flow",
                f"Unexpected behavior in {module} component on {random.choice(ENVIRONMENTS)}",
                f"Intermittent latency spike observed in {module}",
                f"Failed assertion during {module} automated test suite",
                f"Missing validation feedback on {module} user interface"
            ]
            title = random.choice(variations)
            
        # Status distribution (~15% unresolved: Open, In Progress, Reopened)
        status = np.random.choice(
            ["Closed", "Resolved", "Open", "In Progress", "Reopened"],
            p=[0.54, 0.31, 0.07, 0.05, 0.03]
        )
        
        # Created Date spread over 12 months
        # Add slight surge in recent months (e.g. sprint cycles)
        rand_sec = int(np.random.beta(a=1.5, b=1.2) * total_seconds)
        created_dt = start_date + timedelta(seconds=rand_sec)
        
        # Reopened Count
        if status == "Reopened":
            reopened_count = np.random.choice([1, 2, 3], p=[0.65, 0.25, 0.10])
        elif status in ["Resolved", "Closed"]:
            reopened_count = np.random.choice([0, 1, 2, 3], p=[0.82, 0.13, 0.04, 0.01])
        else:
            reopened_count = 0
            
        # Resolution Time based on Severity (Critical fixed fastest)
        # Critical: 0.5 - 4 days, High: 2 - 9 days, Medium: 5 - 18 days, Low: 10 - 32 days
        if status in ["Resolved", "Closed"]:
            if severity == "Critical":
                days = max(0.2, np.random.gamma(shape=2.5, scale=0.8))  # Mean ~2.0 days
            elif severity == "High":
                days = max(1.0, np.random.gamma(shape=3.5, scale=1.3))  # Mean ~4.55 days
            elif severity == "Medium":
                days = max(2.5, np.random.gamma(shape=4.0, scale=2.5))  # Mean ~10.0 days
            else: # Low
                days = max(4.0, np.random.gamma(shape=4.5, scale=4.0))  # Mean ~18.0 days
                
            # If bug was reopened, it takes extra days
            if reopened_count > 0:
                days += reopened_count * np.random.uniform(2.0, 5.0)
                
            resolution_days = round(float(days), 1)
            resolved_dt = created_dt + timedelta(days=resolution_days)
            # Ensure resolved date does not exceed current time
            if resolved_dt > end_date:
                resolved_dt = end_date
                resolution_days = round((resolved_dt - created_dt).total_seconds() / 86400, 1)
                if resolution_days < 0.1:
                    resolution_days = 0.5
            resolved_str = resolved_dt.strftime("%Y-%m-%d %H:%M")
        else:
            resolved_str = None
            resolution_days = np.nan
            
        # Reporter and Assignee
        reporter = random.choice(REPORTERS)
        assignee = random.choice(ASSIGNEES)
        environment = random.choice(ENVIRONMENTS)
        
        # Inject realistic missing values
        # ~3% unassigned (especially for open bugs)
        if (status in ["Open", "In Progress"] and random.random() < 0.20) or random.random() < 0.02:
            assignee = None
            
        # ~2% missing environment
        if random.random() < 0.02:
            environment = None
            
        # ~1% missing reporter
        if random.random() < 0.01:
            reporter = None
            
        bugs.append({
            "bug_id": bug_id,
            "title": title,
            "module": module,
            "severity": severity,
            "priority": priority,
            "status": status,
            "reporter": reporter,
            "assignee": assignee,
            "created_date": created_dt.strftime("%Y-%m-%d %H:%M"),
            "resolved_date": resolved_str,
            "resolution_time_days": resolution_days,
            "defect_type": defect_type,
            "reopened_count": int(reopened_count),
            "environment": environment
        })
        
    df = pd.DataFrame(bugs)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} bugs -> {output_path}")
    print(f"Severity counts:\n{df['severity'].value_counts()}")
    print(f"Status counts:\n{df['status'].value_counts()}")
    print(f"Missing assignees: {df['assignee'].isna().sum()}, Missing envs: {df['environment'].isna().sum()}")
    return df

if __name__ == "__main__":
    generate_sample_dataset()

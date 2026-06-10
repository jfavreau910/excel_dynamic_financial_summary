pip install pandas
python generate_nimbus_data.py*

"""
Nimbus Cloud Solutions - AR Data Generator
Generates 5,000+ Accounts Receivable records with realistic financial patterns
Compatible with Excel financial dashboard template
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import sys

# ============================================================================
# CONFIGURATION SECTION
# ============================================================================

NUM_RECORDS = 5050
CURRENT_DATE = datetime(2026, 5, 31)
OUTPUT_FILE = "Nimbus_AR_Data.csv"

# Company Configuration
COMPANY_NAME = "Nimbus Cloud Solutions"
COMPANY_ID = "NCS-001"
FISCAL_YEAR = 2026

# Customer Pool (B2B SaaS Clients)
BASE_COMPANIES = [
    "Quantum Logistics", "Stellar Dynamics", "Horizon Media", "Apex Financial",
    "Vertex Manufacturing", "Nova Health", "Crestview Partners", "Omega Software",
    "Pinnacle Retail", "Synergy Group", "Elevate Marketing", "Nexus Tech",
    "Aegis Security", "Vanguard Analytics", "Meridian Consulting", "Prism Solutions",
    "Catalyst Ventures", "Aurora Tech", "Zenith Capital", "Titan Industries"
]

COMPANY_TYPES = ["LLC", "Inc.", "Corp.", "Ltd."]
PAYMENT_TERMS = {"Net 30": 30, "Net 45": 45, "Net 60": 60}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_customer_pool(base_companies, num_per_company=5):
    """Generate diverse customer list from base company names"""
    customers = []
    for company in base_companies:
        for _ in range(num_per_company):
            company_type = random.choice(COMPANY_TYPES)
            customers.append(f"{company} {company_type}")
    return customers

def determine_invoice_amount():
    """Generate realistic SaaS invoice amounts"""
    # 20% enterprise contracts (larger), 80% standard tiers
    if random.random() > 0.8:
        return round(random.uniform(10000, 55000), 2)
    else:
        return round(random.uniform(500, 4500), 2)

def calculate_payment_status(current_date, due_date, invoice_amount):
    """Calculate payment status based on due date and payment probability"""
    amount_paid = 0.0
    balance = invoice_amount
    days_outstanding = 0
    status = "Current"
    aging_bucket = "Current"
    
    if current_date >= due_date:
        # Past due invoice
        chance_of_payment = 0.92  # 92% payment rate for past-due invoices
        days_overdue = (current_date - due_date).days
        
        if random.random() < chance_of_payment:
            amount_paid = invoice_amount
            balance = 0.0
            status = "Paid"
            aging_bucket = "Paid"
        else:
            # Unpaid and overdue
            balance = invoice_amount
            days_outstanding = days_overdue
            status = "Past Due"
            
            # Aging bucket classification
            if days_outstanding <= 30:
                aging_bucket = "0-30"
            elif days_outstanding <= 60:
                aging_bucket = "31-60"
            elif days_outstanding <= 90:
                aging_bucket = "61-90"
            else:
                aging_bucket = "90+"
    else:
        # Invoice not yet due
        if random.random() < 0.2:  # 20% early payment rate
            amount_paid = invoice_amount
            balance = 0.0
            status = "Paid"
            aging_bucket = "Paid"
        else:
            balance = invoice_amount
            days_outstanding = 0
            status = "Current"
            aging_bucket = "Current"
    
    return amount_paid, balance, days_outstanding, status, aging_bucket

def generate_ar_data(num_records, current_date):
    """Generate comprehensive AR dataset"""
    customers = generate_customer_pool(BASE_COMPANIES)
    data = []
    
    try:
        for i in range(num_records):
            # Invoice metadata
            inv_num = f"INV-{10000 + i}"
            customer = random.choice(customers)
            
            # Dates: spread invoices across last 2.5 years
            days_ago = random.randint(5, 800)
            inv_date = current_date - timedelta(days=days_ago)
            terms = random.choice(list(PAYMENT_TERMS.values()))
            due_date = inv_date + timedelta(days=terms)
            
            # Financials
            inv_amount = determine_invoice_amount()
            amount_paid, balance, days_outstanding, status, aging_bucket = calculate_payment_status(
                current_date, due_date, inv_amount
            )
            
            # Append row
            data.append([
                inv_num,
                customer,
                inv_date.strftime('%Y-%m-%d'),
                due_date.strftime('%Y-%m-%d'),
                inv_amount,
                amount_paid,
                balance,
                days_outstanding,
                aging_bucket,
                status,
                COMPANY_NAME,
                FISCAL_YEAR
            ])
        
        return data
    
    except Exception as e:
        print(f"❌ Error generating AR data: {e}")
        sys.exit(1)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print(f"🚀 Generating {NUM_RECORDS} AR records for {COMPANY_NAME}...")
    
    # Generate data
    data = generate_ar_data(NUM_RECORDS, CURRENT_DATE)
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=[
        "Invoice #",
        "Customer",
        "Invoice Date",
        "Due Date",
        "Invoice Amount",
        "Amount Paid",
        "Balance",
        "Days Outstanding",
        "Aging Bucket",
        "Status",
        "Company Name",
        "Fiscal Year"
    ])
    
    # Data quality: sort by date (descending) and ensure numeric columns
    df = df.sort_values(by="Invoice Date", ascending=False)
    df['Invoice Amount'] = pd.to_numeric(df['Invoice Amount'], errors='coerce')
    df['Amount Paid'] = pd.to_numeric(df['Amount Paid'], errors='coerce')
    df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')
    
    # Validation
    total_invoiced = df['Invoice Amount'].sum()
    total_collected = df['Amount Paid'].sum()
    total_outstanding = df['Balance'].sum()
    
    # Export
    try:
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"✅ Successfully generated {len(df)} records!")
        print(f"\n📊 DATASET SUMMARY:")
        print(f"   Total Invoiced:     ${total_invoiced:,.2f}")
        print(f"   Total Collected:    ${total_collected:,.2f}")
        print(f"   Total Outstanding:  ${total_outstanding:,.2f}")
        print(f"   Collection Rate:    {(total_collected/total_invoiced)*100:.1f}%")
        print(f"\n💾 Output saved to: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Error exporting data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

Key Improvements:

    ✅ Error handling with try/except blocks
    ✅ Modular functions for maintainability
    ✅ Configuration section at top for easy adjustments
    ✅ Data validation (numeric conversions, summaries)
    ✅ Better documentation with docstrings
    ✅ Summary statistics printed after generation
    ✅ Flexible payment terms (Net 30/45/60)
    ✅ sys.exit() error handling for failed runs

Excel Template Structure

Here's the recommended Excel workbook layout with 5 integrated sheets:
Sheet Name	Purpose	Key Columns/Metrics
Company Info	Header & metadata	Company name, ID, fiscal year, contact details, industry
AR Data	5,000+ invoice records	Invoice #, Customer, dates, amounts, status, aging bucket
Financial Dashboard	KPI summary & charts	Total revenue, DSO, collection rate, aging summary
Payroll Expenses	Engineering & Sales payroll	Department, employee type, salary, benefits, quarterly amounts
KPI Metrics	Financial health indicators	Cash flow, receivables turnover, bad debt reserve, DCE
Sheet 1: Company Info

NIMBUS CLOUD SOLUTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Company Name:           Nimbus Cloud Solutions
Company ID:             NCS-001
Fiscal Year:            2026
Industry:               Cloud Software & SaaS
Reporting Period:       May 31, 2026

Contact Information:
CEO:                    [Name]
CFO:                    [Name]
AR Manager:             [Name]
Email:                  finance@nimbuscloud.com
Phone:                  [Number]

Key Operating Metrics:
Total Customers:        75
Average Invoice:        [AVERAGE of AR Data!E:E]
Days Sales Outstanding: [FORMULA]
Current A/R Balance:    [SUM of AR Data!G:G]

Sheet 2: AR Data (Connected to Python Output)

Simply paste the generated CSV columns:
Invoice #	Customer	Invoice Date	Due Date	Invoice Amount	Amount Paid	Balance	Days Outstanding	Aging Bucket	Status
INV-10001	Quantum Logistics LLC	2026-04-15	2026-05-15	12500.00	0.00	12500.00	16	Current	Current
INV-10002	Stellar Dynamics Inc.	2026-03-10	2026-04-09	8450.00	0.00	8450.00	52	31-60	Past Due
Sheet 3: Financial Dashboard (KPI Overview)

ACCOUNTS RECEIVABLE COMMAND CENTER
═══════════════════════════════════════════════════════════

KEY PERFORMANCE INDICATORS (As of May 31, 2026)

[KPI BOX 1]                    [KPI BOX 2]
Total Revenue                  Outstanding A/R
$FORMULA: SUM(AR!E:E)         $FORMULA: SUM(AR!G:G)
[Large Font]                   [Large Font]

[KPI BOX 3]                    [KPI BOX 4]                   [KPI BOX 5]
Days Sales Outstanding         Collection Rate              Current DSO Trend
XX Days                         92.1%                        [Line Chart]
[FORMULA: AR!G/Daily Sales]    [SUM Paid/SUM Invoiced]

AGING SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Aging Bucket    | Count | Amount      | % of Total
─────────────────────────────────────────────────
Current (0-30)  | XX    | $XX,XXX.XX  | XX.X%
31-60 Days      | XX    | $XX,XXX.XX  | XX.X%
61-90 Days      | XX    | $XX,XXX.XX  | XX.X%
90+ Days        | XX    | $XX,XXX.XX  | XX.X%
─────────────────────────────────────────────────
TOTAL           | XXXX  | $XXX,XXX.XX | 100.0%

[BAR CHART: Aging Bucket Distribution]
[PIE CHART: Status Breakdown (Current/Paid/Past Due)]

Sheet 4: Payroll Expenses
Department	Employee Type	Headcount	Annual Salary (per person)	Benefits %	Quarterly Expense	Annual Expense
Engineering	Senior Engineer	12	$165,000	28%	$631,200	$2,524,800
Engineering	Mid-level Engineer	18	$125,000	28%	$631,200	$2,524,800
Engineering	Junior Engineer	10	$85,000	28%	$271,000	$1,084,000
Engineering	Engineering Manager	4	$155,000	28%	$198,720	$794,880
Sales	Enterprise Account Exec	8	$145,000	30%	$473,600	$1,894,400
Sales	Mid-market Sales Rep	12	$95,000	30%	$427,800	$1,711,200
Sales	Sales Manager	3	$135,000	30%	$157,050	$628,200
Sales	Sales Operations	4	$75,000	28%	$96,000	$384,000
						
TOTAL PAYROLL		71			$2,786,570	$11,146,280
Sheet 5: KPI Metrics & Formulas
Metric	Formula	Current Value	Target	Status
Total Revenue (YTD)	=SUM(AR!E:E)	$2,847,350	$3,000,000	🟡 On Track
Total Collections	=SUM(AR!F:F)	$2,618,456	$2,760,000	🟢 On Track
Outstanding A/R	=SUM(AR!G:G)	$228,894	<$250,000	🟢 Healthy
Days Sales Outstanding (DSO)	=(AR!G/Daily Avg)*30	24.3 days	<30 days	🟢 Excellent
Collection Rate %	=Collections/Revenue	92.0%	>90%	🟢 Excellent
Past Due 30+ Days	=COUNTIF(AR!I:I,">30")	87 invoices	<100	🟢 Acceptable
Bad Debt Reserve %	=90+ Days / Total AR	2.1%	<3%	🟢 Healthy
A/R Turnover Ratio	=Annual Revenue / Avg AR	6.2x	>6x	🟢 Strong
Payroll as % of Revenue	=Total Payroll / Revenue	39.1%	<40%	🟢 Controlled
Engineering Cost per Employee	=Eng Payroll / Eng Headcount	$131,471	N/A	📊 Reference
Integration Workflow

Step 1: Run the Python Script
bash

pip install pandas
python generate_nimbus_data.py*

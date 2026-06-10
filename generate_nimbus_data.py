Python

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# --- CONFIGURATION ---
NUM_RECORDS = 5050
CURRENT_DATE = datetime(2026, 5, 31) # Aligns with your dashboard's timeframe
OUTPUT_FILE = "Nimbus_AR_Data.csv"

# Generate 75 fake B2B customers for Nimbus Cloud Solutions
companies = [
    "Quantum Logistics", "Stellar Dynamics", "Horizon Media", "Apex Financial", 
    "Vertex Manufacturing", "Nova Health", "Crestview Partners", "Omega Software",
    "Pinnacle Retail", "Synergy Group", "Elevate Marketing", "Nexus Tech", 
    "Aegis Security", "Vanguard Analytics", "Meridian Consulting"
]
customers = [f"{c} {random.choice(['LLC', 'Inc.', 'Corp'])}" for c in companies for _ in range(5)]

data = []

for i in range(NUM_RECORDS):
    # 1. Invoice Number & Customer
    inv_num = f"INV-{10000 + i}"
    customer = random.choice(customers)
    
    # 2. Dates (Spread over the last 2.5 years)
    days_ago = random.randint(5, 800)
    inv_date = CURRENT_DATE - timedelta(days=days_ago)
    due_date = inv_date + timedelta(days=30) # Net 30 terms
    
    # 3. Financials
    # SaaS/Cloud invoices: some small standard tiers ($500-$2000), some large enterprise ($10k-$50k)
    if random.random() > 0.8:
        inv_amount = round(random.uniform(10000, 55000), 2)
    else:
        inv_amount = round(random.uniform(500, 4500), 2)
        
    # Payment Logic
    amount_paid = 0.0
    balance = inv_amount
    days_outstanding = 0
    status = "Current"
    aging_bucket = "Current"
    
    if CURRENT_DATE >= due_date:
        # It's past due. Did they pay it?
        chance_of_payment = 0.92 # 92% of past due invoices are paid
        if random.random() < chance_of_payment:
            amount_paid = inv_amount
            balance = 0.0
            status = "Paid"
            aging_bucket = "Paid"
        else:
            # Unpaid and past due
            balance = inv_amount
            days_outstanding = (CURRENT_DATE - due_date).days
            status = "Past Due"
            
            # Determine Aging Bucket
            if days_outstanding <= 30:
                aging_bucket = "Current" # Technically past due but in the 0-30 bucket for aging reports
            elif days_outstanding <= 60:
                aging_bucket = "31-60"
            elif days_outstanding <= 90:
                aging_bucket = "61-90"
            else:
                aging_bucket = "90+"
    else:
        # Not due yet. Did they pay early?
        if random.random() < 0.2: # 20% chance paid early
            amount_paid = inv_amount
            balance = 0.0
            status = "Paid"
            aging_bucket = "Paid"
        else:
            # Unpaid, but still current
            balance = inv_amount
            days_outstanding = (CURRENT_DATE - due_date).days # Will be negative, but standard AR handles this or caps at 0
            if days_outstanding < 0: 
                days_outstanding = 0
            status = "Current"
            aging_bucket = "Current"

    # Append row
    data.append([
        inv_num, customer, inv_date.strftime('%Y-%m-%d'), due_date.strftime('%Y-%m-%d'), 
        inv_amount, amount_paid, balance, days_outstanding, aging_bucket, status
    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "Invoice #", "Customer", "Invoice Date", "Due Date", 
    "Invoice Amount", "Amount Paid", "Balance", 
    "Days Outstanding", "Aging Bucket", "Status"
])

# Sort by Invoice Date
df = df.sort_values(by="Invoice Date", ascending=False)

# Export to CSV
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Successfully generated {len(df)} records for Nimbus Cloud Solutions in '{OUTPUT_FILE}'!")
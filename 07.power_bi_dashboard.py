"""
07. Power BI Style Sales Data Cleaning & Executive Dashboard Generator
Cleans raw sales data (07.sales_raw.csv -> 07.sales_clean.csv) and renders a multi-panel
executive analytics dashboard (07.sales_dashboard.png).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def clean_sales_data(raw_csv: str = "07.sales_raw.csv", clean_csv: str = "07.sales_clean.csv") -> pd.DataFrame:
    df = pd.read_csv(raw_csv)
    # Remove duplicates
    df = df.drop_duplicates(subset=["Order_ID"]).copy()
    # Standardize Region strings & fill missing values
    df["Region"] = df["Region"].fillna("North").astype(str).str.strip().str.title()
    df["Discount"] = df["Discount"].fillna(0.0).astype(float)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Gross_Sales"] = (df["Units_Sold"] * df["Unit_Price"]).round(2)
    df["Net_Revenue"] = (df["Gross_Sales"] * (1.0 - df["Discount"])).round(2)
    df.to_csv(clean_csv, index=False)
    return df

def generate_dashboard(df: pd.DataFrame, output_png: str = "07.sales_dashboard.png"):
    fig, axes = plt.subplots(2, 2, figsize=(13, 8.5), dpi=150)
    fig.suptitle("Executive Sales & Revenue Analytics Dashboard", fontsize=16, fontweight="bold", y=0.97)

    # 1. Monthly Revenue Trend
    monthly = df.groupby("Month")["Net_Revenue"].sum().reset_index()
    ax1 = axes[0, 0]
    ax1.plot(monthly["Month"], monthly["Net_Revenue"] / 1000, marker="o", linewidth=2.5, color="#1d4ed8")
    ax1.fill_between(range(len(monthly)), monthly["Net_Revenue"] / 1000, color="#93c5fd", alpha=0.35)
    ax1.set_title("Monthly Net Revenue Trend ($K)", fontweight="bold")
    ax1.set_ylabel("Revenue ($K)")
    ax1.tick_params(axis="x", rotation=45)
    ax1.grid(True, linestyle="--", alpha=0.4)

    # 2. Revenue by Product Category
    cat_rev = df.groupby("Category")["Net_Revenue"].sum().sort_values(ascending=True) / 1000
    ax2 = axes[0, 1]
    bars = ax2.barh(cat_rev.index, cat_rev.values, color=["#3b82f6", "#0ea5e9", "#6366f1", "#1e40af"])
    ax2.set_title("Net Revenue by Product Category ($K)", fontweight="bold")
    ax2.set_xlabel("Revenue ($K)")
    ax2.grid(axis="x", linestyle="--", alpha=0.4)
    for bar in bars:
        w = bar.get_width()
        ax2.annotate(f"${w:.1f}K", xy=(w, bar.get_y() + bar.get_height()/2),
                     xytext=(4, 0), textcoords="offset points", va="center", fontsize=9, fontweight="bold")

    # 3. Regional Share
    reg_rev = df.groupby("Region")["Net_Revenue"].sum()
    ax3 = axes[1, 0]
    ax3.pie(reg_rev.values, labels=reg_rev.index, autopct="%1.1f%%", startangle=140,
            colors=["#2563eb", "#38bdf8", "#818cf8", "#64748b"], wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    ax3.set_title("Regional Revenue Distribution", fontweight="bold")

    # 4. Top Sales Representatives
    rep_rev = df.groupby("Sales_Rep")["Net_Revenue"].sum().sort_values(ascending=False) / 1000
    ax4 = axes[1, 1]
    rbars = ax4.bar(rep_rev.index, rep_rev.values, color="#0284c7", edgecolor="#0369a1", width=0.55)
    ax4.set_title("Performance by Sales Representative ($K)", fontweight="bold")
    ax4.set_ylabel("Net Revenue ($K)")
    ax4.grid(axis="y", linestyle="--", alpha=0.4)
    for rbar in rbars:
        h = rbar.get_height()
        ax4.annotate(f"${h:.1f}K", xy=(rbar.get_x() + rbar.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha="center", fontsize=9, fontweight="bold")

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(output_png)
    plt.close()

if __name__ == "__main__":
    clean_df = clean_sales_data()
    generate_dashboard(clean_df)
    print(f"Processed {len(clean_df)} clean records and generated 07.sales_dashboard.png")

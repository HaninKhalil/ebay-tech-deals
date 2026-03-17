import pandas as pd
import numpy as np

RAW_FILE     = "ebay_tech_deals.csv"
CLEANED_FILE = "cleaned_ebay_deals.csv"


def clean_price(val):
    """Remove 'US $', commas, and extra whitespace."""
    if pd.isna(val):
        return val
    return str(val).replace("US $", "").replace(",", "").strip()


def clean():
    # Load everything as strings
    df = pd.read_csv(RAW_FILE, dtype=str)

    # ── Price columns ──────────────────────────────────────────────────────────
    df["price"]          = df["price"].apply(clean_price)
    df["original_price"] = df["original_price"].apply(clean_price)

    # Replace missing / "N/A" original_price with price
    mask = df["original_price"].isna() | (df["original_price"].str.upper() == "N/A") | (df["original_price"] == "")
    df.loc[mask, "original_price"] = df.loc[mask, "price"]

    # ── Shipping column ────────────────────────────────────────────────────────
    df["shipping"] = df["shipping"].fillna("N/A")
    shipping_mask = (
        (df["shipping"].str.upper() == "N/A") |
        (df["shipping"].str.strip() == "")
    )
    df.loc[shipping_mask, "shipping"] = "Shipping info unavailable"

    # ── Convert to numeric ─────────────────────────────────────────────────────
    df["price"]          = pd.to_numeric(df["price"],          errors="coerce")
    df["original_price"] = pd.to_numeric(df["original_price"], errors="coerce")

    # ── Discount percentage ────────────────────────────────────────────────────
    df["discount_percentage"] = (
        (1 - df["price"] / df["original_price"]) * 100
    ).round(2)

    # Handle division by zero → NaN already; keep NaN where original_price == 0
    df.loc[df["original_price"] == 0, "discount_percentage"] = np.nan

    # ── Save ───────────────────────────────────────────────────────────────────
    df.to_csv(CLEANED_FILE, index=False)
    print(f"Cleaned data saved to '{CLEANED_FILE}' ({len(df)} rows).")


if __name__ == "__main__":
    clean()

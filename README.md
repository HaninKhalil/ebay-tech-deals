# eBay Tech Deals – Data Pipeline
**COSC 482 | Spring 2026 | Dr. Roaa Soloh**

---

## Project Structure
```
├── scraper.py               # Selenium scraper
├── clean_data.py            # Data cleaning script
├── EDA.ipynb                # Exploratory Data Analysis notebook
├── ebay_tech_deals.csv      # Raw scraped data
├── cleaned_ebay_deals.csv   # Cleaned data
└── .github/
    └── workflows/
        └── scrape.yml       # GitHub Actions workflow (cron: 0 */3 * * *)
```

---

## Methodology

### Task 1 – Web Scraping
`scraper.py` uses Selenium in headless Chrome to open the eBay Global Tech Deals page, scroll to the bottom to trigger lazy loading, then extract: `timestamp`, `title`, `price`, `original_price`, `shipping`, and `item_url` for every product. Results are appended to `ebay_tech_deals.csv`.

### Task 2 – GitHub Actions Automation
The workflow in `.github/workflows/scrape.yml` runs on cron `0 */3 * * *` (every 3 hours). It installs dependencies, runs the scraper, then commits and pushes the updated CSV automatically. The scraper ran for approximately two days to build a robust dataset.

### Task 3 – Data Cleaning
`clean_data.py`:
- Strips `"US $"` and commas from price columns.
- Fills missing `original_price` with `price`.
- Replaces empty/N/A shipping with `"Shipping info unavailable"`.
- Converts prices to `float`.
- Computes `discount_percentage = (1 - price / original_price) × 100`.

### Task 4 – EDA
`EDA.ipynb` covers:
1. **Time Series** – bar chart of deals per hour.
2. **Price & Discount** – histogram, boxplot, scatter plot, discount distribution.
3. **Shipping** – bar chart of shipping option frequencies.
4. **Text Analysis** – keyword frequency in product titles.
5. **Price Difference** – histogram of absolute discounts.
6. **Top 5 Deals** – sorted by highest discount percentage.

---

## Key Findings
- Most scraping activity is concentrated at 3-hour intervals, visible in the time series chart.
- The majority of products are priced under $200, with a long tail of high-value items.
- Free shipping is the most common shipping option.
- Apple and Samsung are the most frequently appearing brands in product titles.
- The top 5 deals typically offer 40–70% discounts off original price.

---

## Challenges
- eBay uses dynamic/lazy-loaded content — solved by scrolling to the bottom before scraping.
- Some products have no original price listed — handled by substituting the current price (0% discount).
- GitHub Actions rate limits can occasionally delay scheduled runs slightly.

---

## Potential Improvements
- Add proxy rotation to avoid rate limiting.
- Store data in a database (SQLite/PostgreSQL) instead of CSV for better querying.
- Expand scraping to multiple eBay deal categories.
- Add sentiment analysis on product titles.
- Build a live dashboard with Streamlit.

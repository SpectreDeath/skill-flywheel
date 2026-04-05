---
name: web-scraper-agent
description: "Use when: scraping websites, extracting data from pages, crawling sites, building data pipelines from web, handling pagination, avoiding bot detection, extracting tables/prices/reviews, scraping social media (Twitter/Instagram), or exporting to CSV/JSON/Notion. Triggers: 'scrape', 'crawl', 'extract data', 'web fetch', 'parse html', 'get prices', 'monitor website', 'apify', 'firecrawl', 'crawlee'. NOT for: accessing authenticated pages (use browser tools), or when robots.txt prohibits."
---

# Web Scraper Agent

Intelligent multi-strategy web scraping with bot evasion, AI enrichment, and automatic learning.

## Features

- Multi-strategy scraping (requests, Crawlee, Apify, Firecrawl)
- Bot detection evasion with automatic fallback
- AI-powered data enrichment
- Pagination handling
- Learning from user feedback
- Export to CSV/JSON/Notion/Supabase

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Web Scraper Agent                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  URL Input                                                      │
│      │                                                          │
│      v                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Strategy Selector                           │    │
│  │  • requests (simple)                                    │    │
│  │  • Crawlee (resilient)                                   │    │
│  │  • Apify (social media)                                  │    │
│  │  • Firecrawl (AI extraction)                            │    │
│  └─────────────────────────────────────────────────────────┘    │
│      │                                                          │
│      v                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Extract    │  │   Transform  │  │   Enrich     │         │
│  │  • HTML      │  │  • Clean     │  │  • AI LLM    │         │
│  │  • JSON      │  │  • Normalize │  │  • Classify  │         │
│  │  • Tables    │  │  • Validate  │  │  • Extract   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│      │                                                          │
│      v                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Output & Storage                            │    │
│  │  • CSV    • JSON    • Notion    • Sheets    • Supabase  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Usage

### Basic Scraping

```bash
# Scrape a single URL
scrape https://example.com/products

# Extract specific data
scrape https://example.com/products --selector ".product-item"
```

### With Apify (Social Media, E-commerce)

```python
from apify_client import ApifyClient

client = ApifyClient("your-token")

# Twitter scraping
actor_call = client.actor("apify/twitter-scraper").call(
    input={
        "urls": ["https://twitter.com/user/status/123"],
        "maxItems": 10
    }
)

# Amazon product data
actor_call = client.actor("apify/amazon-scraper").call(
    input={"urls": ["https://amazon.com/product/123"]}
)
```

### With Crawlee (Bot Evasion)

```python
from crawlee import PlaywrightCrawler

class ProductCrawler(PlaywrightCrawler):
    async def handle_page(self, request, page):
        products = await page.query_selector_all(".product")
        for product in products:
            item = {
                "title": await product.query_eval(".title"),
                "price": await product.query_eval(".price"),
                "url": await product.query_eval("a@href")
            }
            await self.add_to_result(item)

crawler = ProductCrawler(maxConcurrency=5)
await crawler.run(["https://example.com/products"])
```

### With Firecrawl (AI Extraction)

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="your-key")

# AI-powered structured extraction
result = app.extract(
    urls=["https://example.com/blog"],
    prompt="Extract article title, author, date, and main content"
)
```

### Pagination

```python
class PaginatedScraper:
    def __init__(self, crawler):
        self.crawler = crawler
        
    async def scrape_all(self, base_url, max_pages=10):
        results = []
        for page in range(1, max_pages + 1):
            url = f"{base_url}?page={page}"
            items = await self.crawler.scrape(url)
            if not items:
                break
            results.extend(items)
        return results
```

## AI Enrichment

```python
import requests

def enrich_with_llm(data: list, gemini_key: str) -> list:
    """Enrich scraped data with AI."""
    
    prompt = f"""
    Analyze this product data and add:
    - category classification
    - sentiment (if reviews)
    - key attributes
    
    Data: {data[:5]}  # First 5 items
    """
    
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
        headers={"Authorization": f"Bearer {gemini_key}"},
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    
    return response.json()
```

## Storage Options

### CSV/JSON

```python
import csv
import json

def save_csv(data: list, filename: str):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def save_json(data: list, filename: str):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
```

### Notion

```python
from notion_client import Client

notion = Client(auth="your-token")

def save_to_notion(data: list, database_id: str):
    for item in data:
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {"title": [{"text": {"content": item["title"]}}]},
                "Price": {"number": item.get("price")},
                "URL": {"url": item.get("url")}
            }
        )
```

### Supabase

```python
from supabase import create_client

supabase = create_client("url", "key")

def save_to_supabase(data: list, table: str):
    supabase.table(table).insert(data).execute()
```

## Learning from Feedback

```python
class LearningScraper:
    def __init__(self):
        self.success_patterns = []
        self.failures = []
        
    def record_success(self, url, selectors):
        self.success_patterns.append({
            "url_pattern": self.extract_domain(url),
            "selectors": selectors
        })
        
    def record_failure(self, url, error):
        self.failures.append({
            "url": url,
            "error": error
        })
        
    def get_recommended_selector(self, url: str) -> dict:
        """Get best selector based on past successes."""
        domain = self.extract_domain(url)
        matches = [p for p in self.success_patterns 
                   if self.extract_domain(p["url_pattern"]) == domain]
        if matches:
            return max(matches, key=lambda x: x["selectors"])
        return {}
```

## Scheduled Scraping (GitHub Actions)

```yaml
# .github/workflows/scrape.yml
name: Scheduled Scraper
on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM
    
jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: python scrape.py
        env:
          APIFY_TOKEN: ${{ secrets.APIFY_TOKEN }}
          NOTION_KEY: ${{ secrets.NOTION_KEY }}
```

## Error Handling

```python
class ResilientScraper:
    def __init__(self, max_retries=3, backoff_factor=2):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        
    async def scrape_with_retry(self, url: str) -> dict:
        for attempt in range(self.max_retries):
            try:
                return await self.do_scrape(url)
            except BotDetectionError:
                # Switch strategy
                self.strategy = self.get_next_strategy()
                await self.sleep(self.backoff_factor ** attempt)
            except RateLimitError:
                await self.sleep(60 * (attempt + 1))
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                await self.sleep(self.backoff_factor ** attempt)
        raise MaxRetriesExceeded(url)
```

## Constraints

- MUST respect robots.txt and rate limits
- SHOULD use proxy rotation for large-scale scraping
- MUST handle CAPTCHAs appropriately
- SHOULD implement exponential backoff
- SHOULD cache results to avoid re-scraping
- MUST handle various content types (HTML, JSON, PDF)
- SHOULD log all scraping operations for debugging
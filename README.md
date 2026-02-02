**Robust and fast redfin.com crawler**  
Tech stack: pure Scrapy  
*Features*: Async concurrency, 100% data extraction (no nulls), duplicate filtering via pipelines  
Performance: Scraped 4,000 listings in less than 2 minutes  
How to use it:  
   cd redfin  
   pip install -r requirements  
   scrapy crawl crawler -o data.csv (or json if you want)

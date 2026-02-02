import scrapy

class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    allowed_domains = ["redfin.com"]

    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Referer": "https://www.redfin.com/",
    }

    pagination = 1

    def build_request(self):
        url = f"https://www.redfin.com/city/30818/TX/Austin/page-{self.pagination}"
        return scrapy.Request(url=url, callback=self.parse, headers=self.headers,
            #                   meta={"playwright": True, "playwright_page_methods":[
            # PageMethod("evaluate", "window.scrollTo(0, document.body.scrollHeight)"),
            # PageMethod("wait_for_timeout", 1000),]}
            )

    async def start(self):
        yield self.build_request()

    def parse(self, response):
        items = response.xpath("//div[@class='HomeCardsContainer flex flex-wrap reversePosition widerHomecardsContainer']/div[contains(@class, 'widerHomecardsContainer')]")
        for item in items:
            try:
                link = "www.redfin.com" + item.xpath(".//a[contains(@class, 'bp-Homecard__Address')]/@href").get()
            except :
                link = "N/A"
            yield {
                "price": item.xpath(".//span[@class='bp-Homecard__Price--value']/text()").get().replace(",", "").replace("$", ""),
                "street": item.xpath(".//a[contains(@class, 'bp-Homecard__Address')]/text()").get(),
                "beds": item.xpath(".//span[contains(@class, 'bp-Homecard__Stats--beds')]/text()").get(),
                "baths": item.xpath(".//span[contains(@class, 'bp-Homecard__Stats--baths')]/text()").get(),
                "sq ft": item.xpath(".//span[@class='bp-Homecard__LockedStat--value']/text()").get(),
                "link": link,
            }
        self.pagination += 1
        if self.pagination >= 102:
            return
        yield self.build_request()
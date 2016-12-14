import scrapy

class SanaSpider(scrapy.Spider):
    name = 'sanaspider'
    domain = 'https://www.sana.de'
    start_urls = [domain + '/karriere/jobangebote.html?no_cache=1']

    def parse(self, response):
        for row in response.css('div.event'):
            details_url = row.css('div.headline > a::attr(href)').extract_first()
            request = scrapy.Request(self.domain + details_url, callback=self.parse_details)
            item = {
                'title': row.css('div.meta ::text').extract_first()
            }
            request.meta['item'] = item
            yield request

        next_page = response.css('div.pagebrowser a.next ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_details(self, response):
        item = response.meta['item']
        def get_jobdetails():
            sibling_selector = 'div[@class="label" and text()="Anstellung:"]'
            self_selector = 'div[@class="feld"]'
            jobdetails = '//div['+sibling_selector+']/'+self_selector+'/text()'
            item['jobdetails'] = response.xpath(jobdetails).extract_first()

        get_jobdetails()
        return item

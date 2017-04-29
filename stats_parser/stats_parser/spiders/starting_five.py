import scrapy

class StartingFiveSpider(scrapy.Spider):
    name = "starting_five"

    def start_requests(self):
        urls = [
            'http://plk.pl/mecz/45043/polski-cukier-torun---anwil-wloclawek.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for row in response.xpath("//tr[td//i[@class='ico-star']]"):
            yield {'nazwisko': row.xpath(".//a//strong/text()").extract()}

import scrapy

class LentaSpider(scrapy.Spider):
    name = "lenta"
    
    def start_requests(self):
        urls = [
            'http://lenta.ru/parts/news/',
           # 'http://quotes.toscrape.com/page/1/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        #page = response.url.split("/")[-2]
        #filename = f'quotes-{page}.html'
        
        filename = 'example_lenta.txt'
        with open(filename, 'wb') as f:
            f.write(response.body)	
        self.log(f'Saved file{filename}')

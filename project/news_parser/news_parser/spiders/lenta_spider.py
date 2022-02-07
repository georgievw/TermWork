import scrapy

class LentaSpider(scrapy.Spider):
    name = "lenta"
    
    def start_requests(self):
        urls = [
            'http://lenta.ru/parts/news/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response, main=True):
       if main:
           for item in response.css('li.parts-page__item'):
               yield {
                   'title': item.css('h3::text').get(),
                   'content': "Пока что пусто",
                   'published': item.css('div time::text').get(),
                   'link': response.urljoin(item.css('a').xpath('@href').get()) if item.css('a').xpath('@href').get()[0] == '/' else item.css('a').xpath('@href').get(),
               }
           
               next_page = response.css('li._more a::attr(href)').get()
               if next_page is not None:
                   next_page = response.urljoin(next_page)
                   yield scrapy.Request(next_page, callback=self.parse)
       else:
           yield response

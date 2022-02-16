import scrapy
import random
import pickle
import bayess
import datetime
from bayess import TextBayes
from nltk.stem.snowball import SnowballStemmer
from collections import Counter
from AllNews.models import Article, Site, Tag
from django.contrib.auth.models import User    

   
GEOTAGS = ['Россия', 'Мир']
MAINTAGS = ['Политика', 'Экономика', 'Культура', 'Наука и техника', 'Спорт']

def choose(d):
  foo = max(d.values())
  for tag in d:
    if d.get(tag) == foo:
      return tag

urls_list = {
    'https://ria.ru/lenta/' : ['div.list-item', 'div a.list-item__title::text', 'div.list-item__info div.list-item__date::text', 'a::attr(href)'],
    'https://lenta.ru/parts/news/' : ['li.parts-page__item', 'h3::text', 'div time::text', 'a::attr(href)'],
    'https://echo.msk.ru/news/' : ['div.preview', 'h3 a::text', 'h3 span::text', 'h3 a::attr(href)']
}
    
class LentaSpider(scrapy.Spider):
    name = "lenta"
    start_urls = urls_list
         
    def parse(self, response):
           clf_topic = TextBayes()
           clf_geogr = TextBayes()
           with open('settings_topic.pickle', 'rb') as f:
               settings_topic = pickle.load(f)
           with open('settings_geogr.pickle', 'rb') as f:
               settings_geogr = pickle.load(f)
           clf_topic.set_settings(settings_topic)    
           clf_geogr.set_settings(settings_geogr)
           
           for item in response.css( urls_list.get(response.url)[0] ):
               title = item.css( urls_list.get(response.url)[1] ).get()
               published = item.css( urls_list.get(response.url)[2] ).get()
               link_part = item.css( urls_list.get(response.url)[3] ).get()
               link = response.urljoin(link_part) if link_part[0] == '/' else link_part
               tags = [choose(clf_geogr.predict(title)), choose(clf_topic.predict(title))]
               
               site = Site.objects.get_or_create(link=response.url)[0]               
               (article, check) = Article.objects.get_or_create(title=title, link=link, site=site)
               
               if not check:
                   return 0
                   
               tag1 = Tag.objects.get_or_create(tag = tags[0])[0]
               tag2 = Tag.objects.get_or_create(tag = tags[1])[0]
                
               article.published = datetime.datetime.now()                 
               article.tags.add(tag1, tag2)
               article.save()
               
               yield {
                   'title': title,
                   'content': "Читайте подробнее в оригинальном источнике",
                   'tags': tags,
                   'published': published,
                   'link': link,
               }   
                      
           next_page = response.css('li._more a::attr(href)').get()
           if next_page is not None:
              next_page = response.urljoin(next_page)
              yield scrapy.Request(next_page, callback=self.parse)                  

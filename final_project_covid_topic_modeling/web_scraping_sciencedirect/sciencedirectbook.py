import scrapy
from Crawling.items import AbstractItem
import time
class ScienceirectBook(scrapy.Spider):
  name = 'scidir'
  domain = 'https://www.sciencedirect.com'
  param = '/search?qs="COVID-19"%20OR%20"2019-nCoV"%20OR%20"SARS-nCOV-2"%20OR%20"SARS-COV-2"&date=2020&show=100&publicationTitles=271074%2C272604%2C272991%2C272414%2C271800%2C272254%2C277359%2C272892'
  param2 = '&lastSelectedFacet=publicationTitles'
  url = domain + param + param2
  init_idx = 100
  start_urls = url
  url_article = ''
  headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
  def start_requests(self):
    yield scrapy.Request(url=self.start_urls, callback=self.parse, headers= self.headers)
  
  def parse(self, response, header= headers):
    a = response.css(".result-list-title-link").xpath('./@href').getall()    
    
    for link in a:
      self.url_article = self.domain + link
      yield scrapy.Request(url=self.url_article, callback=self.open_article, headers= self.headers)
    
    param_page = '&offset=' + str(self.init_idx)
    url_nextpage = self.domain + self.param + param_page
    print('start next day' + str(self.init_idx))
    print('waiting ' + str(30) + ' second to continue')
    time.sleep(15)
    self.init_idx = self.init_idx + 100
    yield scrapy.Request(url=url_nextpage, callback=self.parse, headers= self.headers)
  
  def open_article(self, response, header= headers):
    title = response.css(".title-text::text").get()
    abstract = response.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' abstract ') and contains(concat(' ', normalize-space(@class), ' '), ' author ')]").xpath("//div/p/text()").get()
    item = AbstractItem()
    item['title'] = title
    item['abstract'] = abstract
    item['url'] = self.url_article
    yield item


class Scienceirect(scrapy.Spider):
  name = 'scidir1'
  domain = 'https://www.sciencedirect.com/browse/journals-and-books?'
  param = 'contentType=JL&accessType=openAccess&subject=medicine-and-dentistry&acceptsSubmissions=true'
  url = domain + param
  init_idx = 1
  start_urls = url
  headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
  def start_requests(self):
    yield scrapy.Request(url=self.start_urls, callback=self.parse, headers= self.headers)
  def parse(self, response, header= headers):
    for title in response.css("a.js-publication-title span.anchor-text::text").extract():
      yield {
          'Book Title': title
      }
    self.init_idx = self.init_idx + 1
    start_nextPage = self.domain + "page=" + str(self.init_idx) + "&" + self.param
    yield scrapy.Request(start_nextPage, callback=self.parse, headers= self.headers)
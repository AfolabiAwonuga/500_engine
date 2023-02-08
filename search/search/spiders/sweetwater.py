import scrapy
from search.items import SweetItem
from scrapy.loader import ItemLoader
from search.variables import sweet_headers
from scrapy.utils.reactor import install_reactor


install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')  

API_KEY = 'db803e566bb5ba1e75789254fb3b8bdb'

class SweetwaterSpider(scrapy.Spider):
    name = 'sweetwater'
    # allowed_domains = ['sweetwater.com']
    # start_urls = ['https://www.sweetwater.com/c1036--500_Series?all']

    def start_requests(self):
        meta = {
            "proxy": f"http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001"
            }
        yield scrapy.Request('https://www.sweetwater.com/c1036--500_Series?all', 
                            headers = sweet_headers, meta=meta
                            )

   
    def parse(self, response):
        for link in response.css('h2.product-card__name a::attr(href)'):
            yield response.follow(link.get(), callback = self.parse_product, headers = sweet_headers)
        
        # next_page = response.urljoin(response.css('li.next a::attr(href)').get())
        # if next_page:
        #     yield scrapy.Request(next_page, callback = self.parse_product)

   
    def parse_product(self, response):
        loader = ItemLoader(item = SweetItem(), selector = response)
        store = 'Sweetwater'
        
        desc = response.css('div.webtext-block.webtext-block--mixed-content p::text').get()
        title = response.css('h1.product__name span::text').getall()
        if desc != None:
            description = desc
        else:
            description = ''.join(title)    

        loader.add_value('store', store)
        loader.add_css('image', 'img[itemprop = image]::attr(src)')
        loader.add_css('title', 'h1.product__name span')
        loader.add_value('url', response.url)
        loader.add_css('price', 'div.product-price--final price dollars')
        loader.add_value('description', description)

        yield loader.load_item()
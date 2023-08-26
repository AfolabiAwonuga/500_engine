import scrapy
from search.items import SweetItem
from scrapy.loader import ItemLoader
from search.variables import sweet_headers
from scrapy.utils.reactor import install_reactor


install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')  

API_KEY = 'db803e566bb5ba1e75789254fb3b8bdb'
meta = {
    "proxy": f"http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001"
    }


class SweetwaterSpider(scrapy.Spider):
    """
    Spider for crawling product information from Sweetwater website.

    Attributes:
        name (str): The name of the spider.

    """
    name = 'sweetwater'

    def start_requests(
            self
    ):
        """
        Generates the initial requests to crawl the Sweetwater website.

        Yields:
            scrapy.Request: Initial request to start crawling.

        """
        
        yield scrapy.Request('https://www.sweetwater.com/c1036--500_Series?all', 
                            headers = sweet_headers, meta=meta
                            )
        
    def parse(
            self, 
            response
    ):
        """
        Parses the product listing page to extract product links.

        Args:
            response (scrapy.http.Response): The response from the request.

        Yields:
            scrapy.Request: Requests for individual product pages.

        """
        for link in response.css('h2.product-card__name a::attr(href)'):
            yield response.follow(link.get(), callback = self.parse_product, headers = sweet_headers, meta=meta)

    def parse_product(
            self, 
            response
    ):
        """
        Parses an individual product page to extract product details.

        Args:
            response (scrapy.http.Response): The response from the request.

        Yields:
            SweetItem: Extracted product information.

        """
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
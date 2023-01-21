import scrapy
from search.items import ThomannItem
from scrapy.loader import ItemLoader
from search.variables import thom_headers
from scrapy_playwright.page import PageMethod
from scrapy.utils.reactor import install_reactor

install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')  

class ThomannSpider(scrapy.Spider):
    name = 'thomann'
   

    def start_requests(self):
        
        yield scrapy.Request('https://www.thomann.de/gb/componente_sistem-500.html', 
                            meta = dict(
                            playwright =  True,
                            playwright_include_page = True,
                            playwright_page_methods = [PageMethod("wait_for_selector", "div.search-pagination__pages")]
                        ), headers = thom_headers 
                    )
   
   
    def parse(self, response):
        total_pages = response.css('button[appearance = secondary]::text').getall()
        # for page in range(1, int(total_pages[-1]) + 1):
        for page in range(1, 3):
            yield scrapy.Request(f'https://www.thomann.de/gb/componente_sistem-500.html?ls=25&pg={page}',
                                meta = dict(
                                playwright =  True,
                                playwright_include_page = True,
                                playwright_page_methods = [PageMethod("wait_for_selector", "div.product-listings")]
                        ), callback=self.parse_page, headers = thom_headers)


    def parse_page(self, response):
        for product in response.css('div.product a.product__content::attr(href)'):
            yield response.follow(product.get(), callback = self.parse_product,
                                 headers = thom_headers)


    def parse_product(self, response):
        loader = ItemLoader(item = ThomannItem(), selector = response)
        store = 'Thomann'
        image = response.css('picture.ZoomImagePicture img::attr(src)').get()
        desc1 = response.css('h2::text').get()
        desc2 = response.css('ul.fx-list.product-text__list li span::text').getall()
        description = [i for i in desc2]
        description.append(desc1)
        description.append(response.css('h1::text').get())

        loader.add_value('store', store)
        loader.add_value('image', response.urljoin(image))
        loader.add_css('title', 'h1')
        loader.add_value('url', response.url)
        loader.add_css('price', 'div.price')
        loader.add_value('description', description)


        yield loader.load_item()


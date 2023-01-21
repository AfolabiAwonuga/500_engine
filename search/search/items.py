import scrapy
import requests
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags 
import string


def price_sweet(lst):
    
    # for price in lst:
    price = ''
    for char in lst[0]:
        if char not in string.punctuation:
            price += str(char)

    amount = float(price)
    gbp = requests.get(f'https://api.frankfurter.app/latest?amount={amount}&from=USD&to=GBP')
    price_usd = '$' + str(amount)
    price_gbp = '£' + str(round(gbp.json()['rates']['GBP'], 2))
   
    return (price_usd, price_gbp)    
    

def price_thomann(lst):
    striped = lst[0].strip().replace('£', '')

    price = ''
    for char in striped:
        if char not in string.punctuation:
            price += str(char)
    
    amount = float(price)
    usd = requests.get(f'https://api.frankfurter.app/latest?amount={amount}&from=GBP&to=USD')
    price_usd = '$' + str(round(usd.json()['rates']['USD'], 2))
    price_gbp = '£' + str(amount)
    
    return (price_usd, price_gbp) 

def join(lst):
    return ''.join(lst)

class SweetItem(scrapy.Item):

    store = scrapy.Field(
        output_processor = TakeFirst()
    )

    image = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

    title = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = join
        )

    url = scrapy.Field(
        output_processor = TakeFirst()
    )    

    price = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = price_sweet
    )    

    description = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )    


class ThomannItem(scrapy.Item):

    store = scrapy.Field(
        output_processor = TakeFirst()
    )

    image = scrapy.Field(
        output_processor = TakeFirst()
    )

    title = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

    url = scrapy.Field(
        output_processor = TakeFirst()
    )

    price = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = price_thomann
    )    

    description = scrapy.Field(
        output_processor = join
    )    
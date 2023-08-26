import string
import scrapy
import requests
from typing import List, Tuple
from w3lib.html import remove_tags 
from itemloaders.processors import TakeFirst, MapCompose


def price_sweet(
        lst: List[str]
) -> Tuple[str, str]:
    """
    Convert a price from USD to GBP.

    Args:
        lst (list): A list containing the price as a string.

    Returns:
        tuple: A tuple containing the price in USD and GBP.

    """
    price = ''
    for char in lst[0]:
        if char not in string.punctuation:
            price += str(char)

    amount = float(price)
    gbp = requests.get(f'https://api.frankfurter.app/latest?amount={amount}&from=USD&to=GBP')
    price_usd = '$' + str(amount)
    price_gbp = '£' + str(round(gbp.json()['rates']['GBP'], 2))
   
    return (price_usd, price_gbp)    
    

def price_thomann(
        lst: List[str]
) -> Tuple[str, str]:
    """
    Convert a price from GBP to USD.

    Args:
        lst (list): A list containing the price as a string.

    Returns:
        tuple: A tuple containing the price in USD and GBP.

    """
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


def join(
        lst: List[str]
) -> str:
    """
    Joins a list of strings into a single string.

    Args:
        lst (list): A list of strings to be joined.

    Returns:
        str: The concatenated string.

    """
    return ''.join(lst)


class SweetItem(scrapy.Item):
    """
    Item class to store scraped product information from Sweetwater.

    Attributes:
        store (scrapy.Field): The store name.
        image (scrapy.Field): The image URL of the product.
        title (scrapy.Field): The title of the product.
        url (scrapy.Field): The URL of the product page.
        price (scrapy.Field): The price of the product.
        description (scrapy.Field): The description of the product.

    """
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
    """
    Item class to store scraped product information from Thomann.

    Attributes:
        store (scrapy.Field): The store name.
        image (scrapy.Field): The image URL of the product.
        title (scrapy.Field): The title of the product.
        url (scrapy.Field): The URL of the product page.
        price (scrapy.Field): The price of the product.
        description (scrapy.Field): The description of the product.

    """
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
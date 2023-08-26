from itemadapter import ItemAdapter
import pymongo


class SearchPipeline:
    """
    Scrapy pipeline for processing and storing items in a MongoDB collection.

    Attributes:
        collection_name (str): The name of the MongoDB collection.

    """
    collection_name = 'data'

    def __init__(
            self, 
            mongo_uri,
            mongo_db
    ):
        """
        Initialize the pipeline.

        Args:
            mongo_uri (str): The MongoDB connection URI.
            mongo_db (str): The name of the MongoDB database.

        """
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(
        cls, 
        crawler
    ):
        """
        Create an instance of the pipeline using Scrapy settings.

        Args:
            crawler (scrapy.crawler.Crawler): The Scrapy crawler object.

        Returns:
            SearchPipeline: An instance of the SearchPipeline class.

        """
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'engine')
        )

    def open_spider(
            self,
            spider
    ):
        """
        Initialize MongoDB connection when the spider is opened.

        Args:
            spider (scrapy.Spider): The Scrapy spider object.

        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # self.db[self.collection_name].delete_many({})

    def close_spider(
            self, 
            spider
    ):
        """
        Close the MongoDB connection when the spider is closed.

        Args:
            spider (scrapy.Spider): The Scrapy spider object.

        """
        self.client.close()

    def process_item(
            self, 
            item, 
            spider
    ):
        """
        Process and store the item in the MongoDB collection.

        Args:
            item (scrapy.Item): The scraped item.
            spider (scrapy.Spider): The Scrapy spider object.

        Returns:
            scrapy.Item: The processed item.

        """
        data = ItemAdapter(item).asdict()
        self.db[self.collection_name].update_one(data, {'$set':data}, upsert=True)
        return item
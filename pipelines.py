from scrapy.exceptions import DropItem
from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader

class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        # Check for duplicates based on the company title or link
        if item['title'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item['title']}")
        else:
            self.ids_seen.add(item['title'])
            return item

    def filter_null(value):
        if value is None or value.strip() == "":
            return None  # Returning None here tells the loader to ignore it
        return value.strip()

    class RedfinLoader(ItemLoader):
        default_output_processor = TakeFirst()
        # Apply the filter to specific fields
        price_in = MapCompose(filter_null)
        agent_name_in = MapCompose(filter_null)

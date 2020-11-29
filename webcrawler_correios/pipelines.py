import json
import os
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class DuplicatesPipeline:

    def __init__(self):
        self.keys_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)                        
        if adapter['key'] in self.keys_seen:                    
            raise DropItem(f"Duplicate item found: {item!r}")        
        else:
            self.keys_seen.add(adapter['key'])
            return item


class JsonWriter:
    
    def open_spider(self, spider):        
        if not os.path.exists('output'):
            os.makedirs('output')
        self.file = open('output/output.jsonl', 'w', encoding='UTF-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        del item['key']
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        
        self.file.write(line)
        return item

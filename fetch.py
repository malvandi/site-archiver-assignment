import sys
from typing import List

from downloader import Downloader
from json_db import JsonDB
from model.metadata import Metadata
from util import get_site_key

db_json_file = './db.json'
db = JsonDB(db_json_file)


def download(site: str):

    key = get_site_key(site)
    downloader = Downloader(site, '')
    result = downloader.run()
    metadata = Metadata(key, result['num_links'], result['images'])
    db.update_record(metadata)


def print_metadata(site: str):
    print(f'---------- {site} ----------')
    record = db.find_record(get_site_key(site))
    if None == record:
        print('Not yet fetched')
        return

    print('site: %s' % record.site)
    print('num_links: %s' % record.num_links)
    print('images: %s' % record.images)
    print('last_fetched: %s' % record.last_fetch)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    first_argument = sys.argv[1]
    if first_argument == '--metadata':
        entries = sys.argv[2:]
        for entry in entries:
            print_metadata(entry)
        exit()

    entries = sys.argv[1:]
    for entry in entries:
        download(entry)

    for entry in entries:
        print_metadata(entry)

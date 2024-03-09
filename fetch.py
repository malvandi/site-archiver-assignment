import sys

from downloader import Downloader
from json_db import JsonDB
from model.metadata import Metadata

db_json_file = './db.json'
db = JsonDB(db_json_file)


def download():
    url = sys.argv[1]

    downloader = Downloader(url, '')
    result = downloader.run()
    metadata = Metadata(url, result['num_links'], result['images'])
    db.update_record(metadata)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    download()

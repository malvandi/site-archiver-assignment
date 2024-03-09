import datetime


class Metadata:
    url: str = ''
    num_links: int = 0
    images: int = 0
    last_fetch = datetime.datetime.now()

    def __init__(self, url: str, num_links: int, images: int):
        self.url = url
        self.num_links = num_links
        self.images = images


def metadata_encoder(obj):
    if isinstance(obj, Metadata):
        return {
            'url': obj.url,
            'num_links': obj.num_links,
            'images': obj.images,
            'last_fetch': obj.last_fetch.strftime('%Y-%m-%d %H:%M:%S')
        }
    return obj


def metadata_decoder(obj):
    if 'url' in obj:
        return Metadata(obj['url'], obj['num_links'], obj['images'])
    return obj
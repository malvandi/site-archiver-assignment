import sys

from downloader import Downloader


def download():
    url = sys.argv[1]

    downloader = Downloader(url, '')
    downloader.run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    download()

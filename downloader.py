import os
import re
import shutil
import urllib
from typing import Dict
from urllib.parse import urlparse

import requests
import unicodedata

from bs4 import BeautifulSoup


class Downloader:
    url: str
    url_with_http: str
    html_content: str
    soup: BeautifulSoup
    directory: str
    assets_directory: str

    def __init__(self, url: str, directory: str):
        self.url = url
        self.url_with_http = self.url if self.url.startswith('http://') else f'https://{self.url}'
        self.directory = directory
        self.assets_directory = self._get_valid_assets_directory()

    def run(self) -> Dict[int, int]:
        self._create_directories()
        self.html_content = self._download_page()
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

        self._download_css()
        self._download_js()
        image_counts = self._download_img()

        self._save_index_file()

        return {
            'num_links': self._get_hyperlink_counts(),
            'images': image_counts
        }

    def _download_js(self):
        print('Downloading js files ...')
        js_links = [link for link in self.soup.find_all('script', {'src': re.compile(r'.*\.js$')})]
        for js_link in js_links:
            href = js_link.get('src')
            self._download_asset_then_register_in_html(href)

    def _download_css(self):
        print('Downloading css files ...')
        css_links = [link for link in self.soup.find_all('link', {'rel': 'stylesheet'})]
        for css_link in css_links:
            href = css_link.get('href')
            self._download_asset_then_register_in_html(href)

    def _download_img(self) -> int:
        print('Downloading image files ...')
        urls = []
        img_tags = self.soup.find_all('img')
        for img_tag in img_tags:
            urls.append(img_tag.get('src', ''))
            srcset_attr = img_tag.get('srcset', '')
            urls.extend([url.strip().split(' ')[0] for url in srcset_attr.split(',')])

        # img_links = [img.get('src') for img in self.soup.find_all('img')]
        icon_links = [icon.get('href') for icon in
                      self.soup.find_all('link', {'rel': ['shortcut icon', 'apple-touch-icon']})]
        for url in (urls + icon_links):
            self._download_asset_then_register_in_html(url)

        return len(img_tags)

    def _get_hyperlink_counts(self) -> int:
        return len(self.soup.find_all('a'))

    def _download_asset_then_register_in_html(self, url: str):
        if url == '':
            return

        file_name = self._get_valid_asset_name(url)
        directory = f'{self.assets_directory}/{file_name}'
        valid_url = self._get_valid_url(url)
        self._download_asset(valid_url, directory)
        asset_url = self._get_valid_assets_url(file_name)
        print('Replace URL[%s] with [%s]' % (url, asset_url))
        self.html_content = self.html_content.replace(url, asset_url)

    # Function to download webpage
    def _download_page(self) -> str:
        url = self.url_with_http
        print('<<<<<<< Downloading URL Page: %s >>>>>>>' % url)
        response = requests.get(url, verify=True)
        return response.content.decode('UTF-8')

    def _save_index_file(self):
        file_directory = self._get_valid_html_file_directory()
        with open(file_directory, 'w', encoding='utf-8') as f:  # Specify encoding as UTF-8
            f.write(self.html_content)

    def _create_directories(self):
        os.makedirs(self.assets_directory, exist_ok=True)

    def _get_valid_html_file_directory(self) -> str:
        return f'{self.directory}/{self.url}.html' if self.directory != '' else f'{self.url}.html'

    def _get_valid_assets_directory(self) -> str:
        return f'{self.directory}/{self.url}' if self.directory != '' else f'./{self.url}'

    def _get_valid_assets_url(self, file_name: str) -> str:
        return f'./{self.url}/{file_name}'

    def _get_valid_url(self, url: str) -> str:
        if url.startswith('http'):
            return url

        if url.startswith('www'):
            return f'http://{url}'

        parsed_url = urlparse(self.url_with_http)
        return f"{parsed_url.scheme}://{parsed_url.netloc}{url}"

    @staticmethod
    def _download_asset(valid_url: str, directory: str):
        response = requests.get(valid_url, stream=True, verify=True)
        with open(directory, 'wb') as f:
            shutil.copyfileobj(response.raw, f)

    @staticmethod
    def _get_valid_asset_name(url: str) -> str:
        asset_filename = urllib.parse.unquote(url.split('/')[-1])  # Decode URL-encoded characters
        asset_filename = ''.join(c for c in unicodedata.normalize('NFD', asset_filename) if
                                 unicodedata.category(c) != 'Mn')  # Remove diacritics
        return asset_filename.split('?')[0]

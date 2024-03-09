from typing import Dict

import requests


class Downloader:
    url: str
    html_content: str
    directory: str

    def __init__(self, url: str, directory: str):
        self.url = url
        self.directory = directory

    def run(self) -> Dict[int, int]:
        self.html_content = self._download_page()
        self._save_index_file()
        return {
            'num_links': 12,
            'images': 10
        }

    # Function to download webpage
    def _download_page(self) -> str:
        url = self._get_valid_url()
        print('Downloading url: %s' % url)
        response = requests.get(url, verify=True)
        return response.content.decode('UTF-8')

    def _save_index_file(self):
        file_directory = self._get_valid_html_file_directory()
        with open(file_directory, 'w', encoding='utf-8') as f:  # Specify encoding as UTF-8
            f.write(self.html_content)

    def _get_valid_url(self) -> str:
        # TODO
        return f'https://{self.url}'

    def _get_valid_html_file_directory(self) -> str:
        return f'{self.directory}/{self.url}.html' if self.directory != '' else f'{self.url}.html'

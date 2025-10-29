import requests
from bs4 import BeautifulSoup

base_url = 'https://hololyzer.net'

response_string_en = requests.get(base_url + "/youtube/locales/string_en.json")
response_string_en.raise_for_status()
response_string_en.encoding = "utf-8"
string_en = response_string_en.json()

response_string_ja = requests.get(base_url + "/youtube/locales/string_ja.json")
response_string_ja.raise_for_status()
response_string_ja.encoding = "utf-8"
string_ja = response_string_ja.json()

class Channel:
    def __init__(self, id, en_name, ja_name, en_category, ja_category):
        self.id = id
        self.en_name = en_name
        self.ja_name = ja_name
        self.en_category = en_category
        self.ja_category = ja_category


class Video:
    def __init__(self, id, title, channel):
        self.id = id
        self.title = title
        self.channel = channel


def channels(categories = None, ids = None, names = None):
    response = requests.get(base_url)
    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, 'html.parser')
    
    channel_labels = soup.find_all(attrs={"data-i18n": "label.sidemenu.list"})
    channels = []

    for channel_label in channel_labels:
        id = channel_label.parent.get('href').split('/')[-1].replace('.html', '')

        channel_parent = channel_label.find_parent('details')
        label_name = channel_parent.select_one('[data-i18n^="label.name."]').get('data-i18n').split('.')[-1]
        en_name = string_en['label']['name'].get(label_name, channel_parent.find('summary').text)
        ja_name = string_ja['label']['name'].get(label_name, channel_parent.find('summary').text)

        category_parent = channel_parent.find_parent('details')
        label_category = category_parent.select_one('[data-i18n^="label.category."]').get('data-i18n').split('.')[-1]
        en_category = string_en['label']['category'].get(label_category, category_parent.find('summary').text)
        ja_category = string_ja['label']['category'].get(label_category, category_parent.find('summary').text)

        channels.append(Channel(id, en_name, ja_name, en_category, ja_category))

    return channels

def main():
    found_channels = channels()

    for channel in found_channels:
        print(channel.__dict__)


if __name__ == "__main__":
    main()

import json
import sys
import re

import requests

from emotions import emotions as all_emotions

mention_re = re.compile('\@\w+')

# Taken from https://mathiasbynens.be/demo/url-regex, regex by @diegoperini
urls_re = re.compile(
    '(?:(?:https?|ftp)://)?(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})'
    '(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})'
    '(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))'
    '|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*'
    '[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?',
)
emotions_re = re.compile('\((\w+)\)')

title_re = re.compile('<title>(.*)</title>')


def get_page_title(url):
    if not (url.startswith('http') or url.startswith('ftp')):
        url = 'http://' + url
    response = requests.get(url, allow_redirects=True)
    if response.status_code != 200:
        return None
    title = re.search(title_re, response.text)
    if title is None:
        return None
    return title.group(1)


def message_info(msg):
    mentions = re.findall(mention_re, msg)

    urls = re.findall(urls_re, msg)

    emotions = list(set(re.findall(emotions_re, msg)) & all_emotions)

    urls_with_titles = [dict(url=url, title=get_page_title(url)) for url in urls]

    result = dict(
        mentions=mentions,
        emotions=emotions,
        urls=urls_with_titles,
    )

    return json.dumps(result, indent=2)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        msg = sys.stdin.read()
    else:
        msg = ' '.join(sys.argv[1:])
    # print('Message: ' + msg)
    print(message_info(msg))

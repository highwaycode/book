
import os
import urllib.parse
import urllib.request
from urllib.parse import urlparse
import json
import re

def findall(pattern, string):
    return [m.groupdict() for m in compile_pattern(pattern).finditer(string)]

def findfirst(pattern, string):
    m = compile_pattern(pattern).search(string)
    return m.groupdict() if m else None

def compile_pattern(pattern):
    try:
        return re.compile(pattern, flags=re.MULTILINE|re.DOTALL|re.IGNORECASE)
    except Exception as e:
        print(pattern)
        raise

def download_file(url):
    print(url)
    parsed_url = urllib.parse.urlparse(url)
    path = os.path.join('html', parsed_url.netloc, parsed_url.path[1:])
    if os.path.splitext(path)[1] == '':
        path += '.html'
        isHtml = True
    else:
        isHtml = False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    urllib.request.urlretrieve(url, path)
    if isHtml:
        with open(path, 'r') as file:
            for match in findall(r'<img +src="(?P<src>[^"]+)"', file.read()):
                download_file(match['src'])


with open('scripts/hwc_pages.txt', 'r') as file:
    urls = filter(lambda url: len(url) > 0, file.read().split("\n"))

for url in urls:
    download_file(url)

# print(json.dumps(list(urls), sort_keys=True, indent=2))



# urllib.request.urlretrieve(url, file_name)
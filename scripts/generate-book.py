import os.path
import re
import subprocess
from html.parser import HTMLParser

def main():
    file_list = """html/www.gov.uk/guidance/the-highway-code.html
html/www.gov.uk/guidance/the-highway-code/introduction.html
html/www.gov.uk/guidance/the-highway-code/rules-for-pedestrians-1-to-35.html
html/www.gov.uk/guidance/the-highway-code/rules-for-users-of-powered-wheelchairs-and-mobility-scooters-36-to-46.html
html/www.gov.uk/guidance/the-highway-code/rules-about-animals-47-to-58.html
html/www.gov.uk/guidance/the-highway-code/rules-for-cyclists-59-to-82.html
html/www.gov.uk/guidance/the-highway-code/rules-for-motorcyclists-83-to-88.html
html/www.gov.uk/guidance/the-highway-code/rules-for-drivers-and-motorcyclists-89-to-102.html
html/www.gov.uk/guidance/the-highway-code/general-rules-techniques-and-advice-for-all-drivers-and-riders-103-to-158.html
html/www.gov.uk/guidance/the-highway-code/using-the-road-159-to-203.html
html/www.gov.uk/guidance/the-highway-code/road-users-requiring-extra-care-204-to-225.html
html/www.gov.uk/guidance/the-highway-code/driving-in-adverse-weather-conditions-226-to-237.html
html/www.gov.uk/guidance/the-highway-code/waiting-and-parking-238-to-252.html
html/www.gov.uk/guidance/the-highway-code/motorways-253-to-273.html
html/www.gov.uk/guidance/the-highway-code/breakdowns-and-incidents-274-to-287.html
html/www.gov.uk/guidance/the-highway-code/road-works-level-crossings-and-tramways-288-to-307.html
html/www.gov.uk/guidance/the-highway-code/light-signals-controlling-traffic.html
html/www.gov.uk/guidance/the-highway-code/signals-to-other-road-users.html
html/www.gov.uk/guidance/the-highway-code/signals-by-authorised-persons.html
html/www.gov.uk/guidance/the-highway-code/traffic-signs.html
html/www.gov.uk/guidance/the-highway-code/road-markings.html
html/www.gov.uk/guidance/the-highway-code/vehicle-markings.html
html/www.gov.uk/guidance/the-highway-code/annex-1-you-and-your-bicycle.html
html/www.gov.uk/guidance/the-highway-code/annex-2-motorcycle-licence-requirements.html
html/www.gov.uk/guidance/the-highway-code/annex-3-motor-vehicle-documentation-and-learner-driver-requirements.html
html/www.gov.uk/guidance/the-highway-code/annex-4-the-road-user-and-the-law.html
html/www.gov.uk/guidance/the-highway-code/annex-5-penalties.html
html/www.gov.uk/guidance/the-highway-code/annex-6-vehicle-maintenance-safety-and-security.html
html/www.gov.uk/guidance/the-highway-code/annex-7-first-aid-on-the-road.html
html/www.gov.uk/guidance/the-highway-code/annex-8-safety-code-for-new-drivers.html
html/www.gov.uk/guidance/the-highway-code/other-information.html
html/www.gov.uk/guidance/the-highway-code/index.html"""
    file_list = file_list.split("\n")
    # print(file_list)

    buffer = """<html>
    <head>
    <title>The Highway Code</title>
    <meta name="author" content="Department for Transport">
    <meta name="rights" content="&copy; Crown copyright.\nAll content is available under the Open Government Licence v3.0, except where otherwise stated">
    </head>
    <body>
    """

    hrefs = set()

    def mapped_href(match):
        hrefs.add(match.group(1))
        return "href='" + match.group(1) + "'"

    for path in file_list:
        name = os.path.splitext(os.path.basename(path))[0]
        print(name, path)
        with open(path, 'r') as file:
            page = file.read()
            parser = MyHTMLParser()
            parser.name = name
            parser.feed(page)
            buffer += parser.buffer

    for href in sorted(hrefs):
        print(href)

    # print(hrefs)

    subprocess.run(['mkdir', '-p', 'build'])
    with open('build/the-highway-code.html', 'w') as file:
        file.write(buffer)

    subprocess.run(['pandoc', '--standalone', 'build/the-highway-code.html', '-o', 'build/the-highway-code.epub', '--to', 'epub3', '--css', 'stylesheet.css'])

class MyHTMLParser(HTMLParser):

    def __init__(self, *args):
        super(MyHTMLParser, self).__init__(*args)
        self.buffer = ''
        self.keep = False
        self.skip_tags = {'div', 'span'}

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            return
        if not self.keep:
            if tag == 'article': self.keep = True
            return
        self.buffer += f'<{tag}'
        for name, content in attrs:
            if name in {'src', 'id', 'alt', 'href'}:
                if name == 'id' and content == 'section-title':
                    content = self.name
                if name == 'href': # and content.startswith('/guidance/the-highway-code/'):
                    # content = re.sub(r"href='[^']*?\.md#", "href='#", content)
                    content = re.sub(r"^/guidance/the-highway-code/([^#]+)$", "#\\1", content)
                    content = re.sub(r"^/guidance/the-highway-code/.*?(#rule[^#]+)$", "\\1", content)
                    # content = re.sub(r"href='#(\d+)'", "href='#rule\\1'", content)
                    # content = re.sub(r"href='#rule%20", "href='#rule", content)
                    # content = re.sub(r"href='#rule160%5D'", "href='#rule160'", content)
                    # content = re.sub(r"<h2 id='([^'])'>\n([^\n])\n</h2>", "<h3 id='\\1'>\\2</h3>", content)
                    pass
                if name == 'src':
                    content = re.sub(r"^https?://", "html/", content)

                self.buffer += f' {name}="{content}"'
        self.buffer += f'>'

    def handle_endtag(self, tag):
        if tag in self.skip_tags: return
        if not self.keep: return
        if tag == 'article': self.keep = False
        self.buffer += f'</{tag}>'

    def handle_data(self, data):
        if not self.keep: return
        self.buffer += data

    def handle_charref(self, name):
        exit(name)

    def handle_entityref(self, name):
        self.handle_data(f'&{name};')

def read_file(path):
    with open(path, 'r') as file:
        return file.read()

def write_file(path, content):
    if path:
        with open(path, "w") as file:
            file.write(content)
    else:
        print(outputContent)


if __name__ == "__main__":
    main()
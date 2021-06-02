from html.parser import HTMLParser
from html.entities import name2codepoint
import argparse
import json
import re
import os
import subprocess

def walk(root, *path):
    for name in os.listdir(os.path.join(root, *path)):
        yield path, name
        if os.path.isdir(os.path.join(root, *path, name)):
            yield from walk(root, *path, name)

def main():
    parser = argparse.ArgumentParser(description='', epilog="""""", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--input', help='Files to be parsed')
    parser.add_argument('--output')
    args = parser.parse_args()

    parser = MyHTMLParser(convert_charrefs=False)
    parser.skip = {'div'}

    for path, name in walk(args.input):
        if not name.endswith('.html'): continue

        with open(os.path.join(args.input, *path, name), 'r') as file:
            text = file.read()
            parser.feed(text)
            root = parser.stack[0]['$children'][0]
            outputContent = json.dumps(parser.stack[0], sort_keys=True, indent=2)
            root = handleFrames(parser.stack[0])
            print(name)
            # print(outputContent)
            markdown = convert_to_markdown(root['article'])
            markdown = re.sub(r" *\n *", "\n", markdown)
            markdown = re.sub(r"\n+", "\n", markdown)
            markdown = re.sub(r"([‘\(\)]) <", "\\1<", markdown)
            markdown = re.sub(r"> ([’\(\)])", ">\\1", markdown)
            markdown = re.sub(r"\n*$", "\n", markdown)
            if args.output:
                subprocess.run(['mkdir', '-p', os.path.join(args.output, *path)])
                base = os.path.splitext(name)[0]
                write_file(os.path.join(args.output, *path, base+'.md'), markdown)
            else:
                print(outputContent)

def handleFrames(frame, buffer=dict()):
    if not isinstance(frame, dict): return
    if frame['$isa'] == 'article':
        buffer['article'] = frame
    for child in frame['$children']:
        handleFrames(child, buffer)
    return buffer

def convert_to_markdown(frame, *tags):
    if not isinstance(frame, dict): return frame
    buffer = "".join(map(lambda child: convert_to_markdown(child, *tags, frame['$isa']), frame['$children']))

    tag = frame['$isa']

    # if frame['$isa'] == 'h1':
    #     return f"\n# {buffer}\n"
    # elif frame['$isa'] == 'h2':
    #     return f"\n## {buffer}\n"
    # elif frame['$isa'] == 'h3':
    #     return f"\n### {buffer}\n"
    # elif frame['$isa'] == 'p':
    #     return f"\n\n{buffer}\n\n"
    # elif frame['$isa'] == 'strong':
    #     return f"**{buffer}**"
    # elif frame['$isa'] == 'br':
    #     return f"<br/>"
    if frame['$isa'] == 'a':
        href = frame['$attrs']['href']
        if not href.startswith('http:') and not href.startswith('https:'):
            href = re.sub(r'\.html','.md', href)
        return f"<a href='{href}'>{buffer}</a>"
    # elif frame['$isa'] == 'li':
    #     indent = '\t' * (tags.count('ul') + tags.count('ol') - 1)
    #     if tags[-1] == 'ol':
    #         return f"\n{indent}1. {buffer}"
    #     else:
    #         return f"\n{indent}* {buffer}"
    # elif frame['$isa'] in {'ul', 'ol'}:
    #     return f"{buffer}\n"

    attrs = ''
    if '$attrs' in frame and 'id' in frame['$attrs']:
        attrs = f" id='{frame['$attrs']['id']}'"

    if frame['$isa'] in {'h1', 'h2', 'h3', 'p', 'strong', 'li', 'ol', 'ul', 'h1', 'table', 'tbody', 'thead', 'tr', 'th', 'td'}:
        return f"<{tag}{attrs}>{buffer}</{tag}>\n"

    return buffer

class MyHTMLParser(HTMLParser):

    def reset(self):
        super().reset()
        self.stack = list()
        frame = dict()
        frame['$isa'] = None
        self.stack.append(frame)


    def handle_starttag(self, tag, attrs):
        # print("≤"+self.get_starttag_text()+"≥")
        if tag in self.skip: return
        frame = dict()
        frame['$isa'] = tag
        frame['$children'] = list()
        if len(attrs):
            frame['$attrs'] = dict(attrs)
        if '$children' not in self.stack[-1]:
            self.stack[-1]['$children'] = list()
        self.stack[-1]['$children'].append(frame)
        if tag not in {'link', 'img', 'meta', 'br'}:
            self.stack.append(frame)


    def handle_endtag(self, tag):
        if tag in self.skip: return
        self.stack.pop()
        # print("End tag  :", tag)

    def handle_data(self, data):
        # data = data.lstrip()
        # data = data.rstrip()
        if len(data):
            if '$children' not in self.stack[-1]:
                self.stack[-1]['$children'] = list()
            self.stack[-1]['$children'].append(data)

    def handle_charref(self, name):
        exit(name)

    def handle_entityref(self, name):
        self.handle_data(f'&{name};')

        # print("Data     :", data)
    #
    # def handle_comment(self, data):
    #     # print("Comment  :", data)
    #
    # def handle_entityref(self, name):
    #     c = chr(name2codepoint[name])
    #     # print("Named ent:", c)
    #
    # def handle_charref(self, name):
    #     if name.startswith('x'):
    #         c = chr(int(name[1:], 16))
    #     else:
    #         c = chr(int(name))
    #     # print("Num ent  :", c)
    #
    # def handle_decl(self, data):
    #     # print("Decl     :", data)


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

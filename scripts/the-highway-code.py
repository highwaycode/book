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

    parser = MyHTMLParser()
    parser.skip = {'div'}

    for path, name in walk(args.input):
        if not name.endswith('.html'): continue

        with open(os.path.join(args.input, *path, name), 'r') as file:
            text = file.read()
            parser.feed(text)
            root = parser.stack[0]['$children'][0]
            root = handleFrames(root)
            outputContent = json.dumps(root, sort_keys=True, indent=2)
            markdown = convert_to_markdown(root['article'])
            markdown = re.sub(r"\n( *\n)+", "\n\n", markdown)
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

def convert_to_markdown(frame):
    if not isinstance(frame, dict): return frame
    buffer = " ".join(map(lambda child: convert_to_markdown(child), frame['$children']))


    if frame['$isa'] == 'h1':
        return f"\n# {buffer}\n"
    elif frame['$isa'] == 'h2':
        return f"\n## {buffer}\n"
    elif frame['$isa'] == 'h3':
        return f"\n### {buffer}\n"
    elif frame['$isa'] == 'p':
        return f"\n\n{buffer}\n\n"
    elif frame['$isa'] == 'strong':
        return f"**{buffer}**"
    elif frame['$isa'] == 'a':
        return "["+buffer + "](" + frame['$attrs']['href'] + ")"
    elif frame['$isa'] == 'li':
        return f"* {buffer}\n"




    return buffer

    if frame['$isa'] == 'h1':
        buffer += "\n# "
    elif frame['$isa'] == 'h2':
        buffer += "\n## "
    elif frame['$isa'] == 'h3':
        buffer += "\n### "
    elif frame['$isa'] == 'p':
        buffer += "\n\n"
    elif frame['$isa'] == 'article':
        pass
    elif frame['$isa'] == 'section':
        pass
    elif frame['$isa'] == 'span':
        pass
    elif frame['$isa'] == 'img':
        buffer += " !["
    elif frame['$isa'] == 'figcaption':
        pass
    elif frame['$isa'] == 'ul':
        pass
    elif frame['$isa'] == 'li':
        pass
    elif frame['$isa'] == 'strong':
        buffer += "**"
    elif frame['$isa'] == 'abbr':
        pass
    elif frame['$isa'] == 'table':
        pass
    elif frame['$isa'] == 'tbody':
        pass
    elif frame['$isa'] == 'tr':
        pass
    elif frame['$isa'] == 'td':
        pass
    elif frame['$isa'] == 'thead':
        pass
    elif frame['$isa'] == 'th':
        pass
    elif frame['$isa'] == 'br':
        buffer += "\n\n"
    elif frame['$isa'] == 'th':
        pass
    elif frame['$isa'] == 'button':
        return ""
    elif frame['$isa'] == 'form':
        pass
    elif frame['$isa'] == 'input':
        return ""
    elif frame['$isa'] == 'th':
        pass
    elif frame['$isa'] == 'th':
        pass
    elif frame['$isa'] == 'th':
        pass
    elif frame['$isa'] == 'th':
        pass
    elif frame['$isa'] == 'th':
        pass
    elif frame['$isa'] == 'th':
        pass
    elif frame['$isa'] == 'a':
        buffer += "["
    else:
        exit(frame['$isa'])

    for child in frame['$children']:
        buffer += convert_to_markdown(child)

    if frame['$isa'] == 'h1':
        buffer += "\n"
    elif frame['$isa'] == 'h2':
        buffer += "\n"
    elif frame['$isa'] == 'h3':
        buffer += "\n"
    elif frame['$isa'] == 'p':
        buffer += "\n\n"
    elif frame['$isa'] == 'a':
        buffer += "](" + frame['$attrs']['href'] + ")"
    elif frame['$isa'] == 'img':
        buffer += frame['$attrs']['src'] + "](" + frame['$attrs']['src'] + ")"
    elif frame['$isa'] == 'strong':
        buffer += "**"


    return buffer



class MyHTMLParser(HTMLParser):

    def reset(self):
        super().reset()
        self.stack = list()
        self.stack.append(dict())

    def handle_starttag(self, tag, attrs):
        if tag in self.skip: return
        frame = dict()
        frame['$isa'] = tag
        frame['$children'] = list()
        if len(attrs):
            frame['$attrs'] = dict(attrs)
        if '$children' not in self.stack[-1]:
            self.stack[-1]['$children'] = list()
        self.stack[-1]['$children'].append(frame)
        if tag not in {'link', 'img', 'meta'}:
            self.stack.append(frame)


    def handle_endtag(self, tag):
        if tag in self.skip: return
        self.stack.pop()
        # print("End tag  :", tag)

    def handle_data(self, data):
        data = data.lstrip()
        data = data.rstrip()
        if len(data):
            if '$children' not in self.stack[-1]:
                self.stack[-1]['$children'] = list()
            self.stack[-1]['$children'].append(data)

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

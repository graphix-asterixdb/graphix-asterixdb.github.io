from html.parser import HTMLParser
from pathlib import Path
from fileinput import FileInput

import re
import shutil
import sys
import os

SCALE_FACTOR = 0.9

class BottlecapsHTMLParser(HTMLParser):
    def error(self, message):
        pass

    def __init__(self):
        super().__init__()
        self.figure_sizes = {}
        self.working_name = None

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and len(attrs) == 1 and attrs[0][0] == 'name':
            self.working_name = attrs[0][1]
            print(self.working_name)

        elif self.working_name is not None and tag == 'img':
            figure_height = int([a[1] for a in attrs if a[0] == 'height'][0]) * SCALE_FACTOR
            figure_width = int([a[1] for a in attrs if a[0] == 'width'][0]) * SCALE_FACTOR
            self.figure_sizes[self.working_name] = {
                'height': int(figure_height),
                'width': int(figure_width)
            }

    def handle_endtag(self, tag):
        if self.working_name is not None and tag == 'img':
            self.working_name = None


def main():
    if len(sys.argv) != 2:
        print('Usage: python3 bottlecaps.py [bottlecaps ui directory]')
        sys.exit(1)

    try:
        os.mkdir('images')
    except FileExistsError:
        pass

    # First: copy the SVG files from this directory to our image directory.
    ui_directory = sys.argv[1]
    for svg_file in os.listdir(f'{ui_directory}/diagram'):
        if svg_file.startswith('rr-') and svg_file.endswith('svg'):
            continue
        elif svg_file.endswith('svg'):
            shutil.copy2(f'{ui_directory}/diagram/{svg_file}', f'images/{svg_file}')

    # Second: Parse the index.xhtml file for the sizes.
    parser = BottlecapsHTMLParser()
    with open(f'{ui_directory}/index.xhtml') as bottlecaps_file:
        bottlecaps_file_content = bottlecaps_file.read().replace('\n', '')
        parser.feed(bottlecaps_file_content)

    # Third, iterate through all files in our docs. We will replace these in-place (FileInput hijacks stdout).
    for path in Path('docs').rglob('*.md'):
        with FileInput(path, inplace=True) as md_file:
            for line in md_file:
                m = re.match(r' *<img src="[./]*images/(\w+).svg"', line)
                if m is None:
                    print(line, end='')
                    continue
                if m.group(1) not in parser.figure_sizes:
                    print(line, end='')
                    continue
                figure_sizes = parser.figure_sizes[m.group(1)]
                line = re.sub(r'height="\d+"', f'height="{figure_sizes["height"]}"', line)
                print(re.sub(r'width="\d+"', f'width="{figure_sizes["width"]}"', line), end='')

if __name__ == '__main__':
    main()

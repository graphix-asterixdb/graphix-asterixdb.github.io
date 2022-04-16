from html.parser import HTMLParser
import sys
import os


class BottlecapsHTMLParser(HTMLParser):
    def error(self, message):
        pass

    def __init__(self):
        super().__init__()
        self.line_numbers = {}
        self.working_name = None

    def handle_starttag(self, tag, attrs):
        if tag == 'xhtml:a' and len(attrs) == 1 and attrs[0][0] == 'name':
            self.working_name = attrs[0][1]
            print(self.working_name)

        elif self.working_name is not None and tag == 'svg':
            self.line_numbers[self.working_name] = {'start': self.offset}

    def handle_endtag(self, tag):
        if self.working_name is not None and tag == 'svg':
            self.line_numbers[self.working_name]['end'] = self.offset
            print(self.line_numbers[self.working_name])
            self.working_name = None


def main():
    if len(sys.argv) != 2:
        print('Usage: python3 bottlecaps.py [bottlecaps.xhtml file]')
        sys.exit(1)

    parser = BottlecapsHTMLParser()
    with open(sys.argv[1]) as bottlecaps_file:
        bottlecaps_file_content = bottlecaps_file.read().replace('\n', '')
        parser.feed(bottlecaps_file_content)

    for svg_name, svg_numbers in parser.line_numbers.items():
        try:
            os.mkdir('images')
        except FileExistsError:
            pass

        with open(f'images/{svg_name}.svg', 'w') as svg_file:
            svg_file.write(bottlecaps_file_content[svg_numbers['start']:svg_numbers['end']] + '</svg>')


if __name__ == '__main__':
    main()

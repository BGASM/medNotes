#!/usr/bin/env python

import argparse
import sys
import markdown
import codecs
import jinja2
from pathlib import Path
import markdown.extensions.toc
import markdown.extensions.tables
import markdown.extensions.sane_lists
import markdown.extensions.attr_list

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    <style>
        body {
            font-family: sans-serif;
        }
        code, pre {
            font-family: monospace;
        }
        h1 code,
        h2 code,
        h3 code,
        h4 code,
        h5 code,
        h6 code {
            font-size: inherit;
        }
    </style>
</head>
<body>
<div class="container">
{{content}}
</div>
</body>
</html>
"""


def parse_args(args=None):
    d = 'Make a complete, styled HTML document from a Markdown file.'
    parser = argparse.ArgumentParser(description=d)
    parser.add_argument('-d', '--path', type=str)
    parser.add_argument('-od', '--outpath', type=str)
    parser.add_argument('-f', '--mdfile', type=argparse.FileType('r'), nargs='?',
                        default=sys.stdin,
                        help='File to convert. Defaults to stdin.')
    parser.add_argument('-o', '--out', type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='Output file name. Defaults to stdout.')
    return parser.parse_args(args)

def writeFile(doc, name, path):
    p = Path(path)
    t = p / f'{name}.html'
    with codecs.open(t, "w", "utf-8", errors='ignore') as file:
        file.write(doc)


def main(args=None):
    args = parse_args(args)
    docs = []
    p = Path.cwd()
    if args.path != '':
        docs = readMany(args.path)
    else:        
        docs.append(args.mdfile.read())
    if args.outpath != '':
        p = sorted(Path('.').glob(f'**/{args.outpath}'))[0]
        print(f'------------------{p}')
    for page in docs:
        writeout(page, p)          


def writeout(page, path):
    swap = [f'<table>',f'<table class="table-bordered table-hover">']
    extensions = ['extra', 'smarty', 'toc', 'tables', 'sane_lists', 'attr_list']
    html = markdown.markdown(page[1], extensions=extensions)
    doc = jinja2.Template(TEMPLATE).render(content=html)
    st = doc.replace(swap[0], swap[1])
    writeFile(st, page[0], path)


def readMany(path):
    p = Path(path)
    documents = []
    for child in p.iterdir():
        if '.md' in str(child):
            with child.open(mode='r', encoding="utf8", errors='ignore') as f:
                q  = f.read()
            documents.append((child.stem, q))
    return documents
    

        
    
if __name__ == '__main__':
    sys.exit(main())
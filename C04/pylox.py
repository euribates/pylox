#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

from errors import report
from scanner import Scanner


def get_options():
    parser = argparse.ArgumentParser(description='Pylox inerpreter / repl')
    parser.add_argument(
        'script',
        nargs="?",
        help='script to be executed',
        default=None,
    )
    return parser.parse_args()


def run(source):
    scanner = Scanner(source)
    for token in scanner.scan_tokens():
        print(token)


def run_file(filename):
    if os.path.isfile(filename):
        with open(filename, 'r') as source:
            run(source.read())
    else:
        report(0, f"No existe el fichero indicado: {filename}")


def run_prompt():
    while True:
        line = input('pylox> ').strip()
        if line == 'exit':
            break
        run(line)


def main():
    args = get_options()
    if args.script:
        run_file(args.script)
    else:
        run_prompt()


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

NUM_ERRORS = 0


def report(line, message, where=''):
    global NUM_ERRORS
    print(f"[{line}] Error {where}: {message}")
    NUM_ERRORS += 1


def had_error():
    return NUM_ERRORS > 0


def reset_errors():
    global NUM_ERRORS
    NUM_ERRORS = 0


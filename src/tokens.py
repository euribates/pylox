#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class TokenType(Enum):
    
    # Single character tokens
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    COMMA = 5
    DOT = 6
    MINUS = 7
    PLUS = 8
    SEMICOLON = 9
    SLASH = 10
    STAR = 11
    
    # One or two character tokens
    BANG = 12
    BANG_EQUAL = 13
    EQUAL_EQUAL = 14
    GREATER = 15
    GREATER_EQUAL = 16
    LESS = 17
    LESS_EQUAL = 18
    
    # Literals
    IDENTIFIER = 19
    STRING = 20
    NUMBER = 21

    # Keywords
    AND = 22
    CLASS = 23
    ELSE = 24
    FALSE = 25
    FUN = 26
    FOR = 27
    IF = 28
    NIL = 29
    OR = 30
    PRINT = 31
    RETURN = 32
    SUPER = 33
    THIS = 34
    TRUE = 35
    VAR = 36
    WHILE = 37
    EOF = 38

class Token:

    def __init__(self, token_type, lexeme, literal, line):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tokens import TokenType, Token
from errors import report

DIGITS = '0123456789'

KEYWORDS = {
    'and': TokenType.AND,
    'class': TokenType.CLASS,
    'else': TokenType.ELSE,
    'false': TokenType.FALSE,
    'for': TokenType.FOR,
    'fun': TokenType.FUN,
    'if': TokenType.IF,
    'nil': TokenType.NIL,
    'or': TokenType.OR,
    'print': TokenType.PRINT,
    'return': TokenType.RETURN,
    'super': TokenType.SUPER,
    'this': TokenType.THIS,
    'true': TokenType.TRUE,
    'var': TokenType.VAR,
    'while': TokenType.WHILE,
}


class Scanner:

    def __init__(self, source):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.length = len(source)

    def scan_tokens(self):
        result = []
        while not self.is_at_end():
            self.start = self.current
            token = self.scan_token()
            if token is not None:
                result.append(token)
        result.append(Token(TokenType.EOF, "", None, None))
        return result

    def is_at_end(self):
        return self.current >= self.length

    def new_token(self, token_type, literal=None):
        text = self.source[self.start:self.current]
        return Token(token_type, text, literal, self.line)

    def advance(self):
        result = self.source[self.current]
        self.current += 1
        return result

    def match(self, c):
        if self.is_at_end():
            return False
        if self.source[self.current] != c:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 > self.length:
            return '\0'
        return self.source[self.current+1]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            report(self.line, "Unterminated string")
            return None
        self.advance()  # the closing "
        value = self.source[self.start + 1:self.current - 1]
        return self.new_token(TokenType.STRING, value)

    def number(self):
        while self.peek() in DIGITS:
            self.advance()
        if self.peek() == '.' and self.peek_next() in DIGITS:
            self.advance()  # Consume the "."
            while self.peek() in DIGITS:
                self.advance()
        value = float(self.source[self.start:self.current])
        return self.new_token(TokenType.NUMBER, value)

    def identifier(self):
        while self.peek().isalnum():
            self.advance
        value = self.source[self.start:self.current]
        token_type = KEYWORDS.get(value, TokenType.IDENTIFIER)
        return self.new_token(token_type, value)

    def scan_token(self):
        c = self.advance()
        if c == '(':
            return self.new_token(TokenType.LEFT_PAREN)
        elif c == ')':
            return self.new_token(TokenType.LEFT_PAREN)
        elif c == '{':
            return self.new_token(TokenType.LEFT_BRACE)
        elif c == '}':
            return self.new_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            return self.new_token(TokenType.COMMA)
        elif c == '.':
            return self.new_token(TokenType.DOT)
        elif c == '-':
            return self.new_token(TokenType.MINUS)
        elif c == '+':
            return self.new_token(TokenType.PLUS)
        elif c == ';':
            return self.new_token(TokenType.SEMICOLON)
        elif c == '*':
            return self.new_token(TokenType.STAR)
        elif c == '!':
            return self.new_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            return self.new_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<':
            return self.new_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>':
            return self.new_token(TokenType.GRESTER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '/':
            if self.match('/'):  # A comment goes until end of the line
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
                return None
            else:
                return self.new_token(TokenType.SLASH)
        elif c == '"':
            return self.string()
        elif c in DIGITS:
            return self.number()
        elif c.isalpha():
            return self.identifier()
        elif c in [' ', '\r', '\t']:
            return None
        elif c == '\n':
            self.line += 1
            return None
        else:
            report(self.line, f"Unexpected character: {c}")


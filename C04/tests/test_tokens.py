#!/usr/bin/env python3

import pytest

from tokens import Token, TokenType


def test_token_creation():
    token = Token(TokenType.IDENTIFIER, 'lexema', 'alfa', 1)
    assert token.type == TokenType.IDENTIFIER
    assert token.lexeme == 'lexema'
    assert token.literal == 'alfa'
    assert token.line == 1


if __name__ == '__main__':
    pytest.main()

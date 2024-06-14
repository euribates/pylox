import pytest

from tokens import Token, TokenType
import expr


def test_print_simple_expression():
    expression = expr.Binary(
        left=expr.Literal('a'),
        operator=Token(TokenType.STAR, '*', None, 1),
        right=expr.Literal('123'),
    )
    assert str(expr.ASTPrinter(expression)) == '(* a 123)'


def test_print_complex_expression():
    expression = expr.Binary(
        expr.Unary(
            Token(TokenType.MINUS, '-', None, -1),
            expr.Literal('123'),
            ),
        Token(TokenType.STAR, '*', None, -1),
        expr.Grouping(
            expr.Literal('45.67')
        ),
    )
    assert str(expr.ASTPrinter(expression)) == '(* (- 123) (group 45.67))'

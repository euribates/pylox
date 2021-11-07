#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from tokens import Token, Value

class Expr:
    def accept(self, visitor):
        raise NotImplementedError(
            f"Class {self.__class__.__name__} must implement"
            " its own version of accept"
        )


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit_binary(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor):
        return visitor.visit_grouping(self)


@dataclass
class Literal(Expr):
    value: Value

    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit_unary(self)
 

#
#  Visitor example
#

class ASTPrinter:

    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return self.expr.accept(self)

    def parenthesize(self, name, *args):
        buff = ["(", name]
        for expr in args:
            buff.append(" ")
            buff.append(expr.accept(self))
        buff.append(")")
        return ''.join(buff)

    def visit_binary(self, expr):
        return self.parenthesize(
            expr.operator.lexeme,
            expr.left,
            expr.right,
        )
    
    def visit_grouping(self, expr):
        return self.parenthesize(
            "group",
            expr.expression,
        )
    
    def visit_literal(self, expr):
        if expr.value is None:
            return 'nil'
        return str(expr.value)

    def visit_unary(self, expr):
        return self.parenthesize(
            expr.operator.lexeme,
            expr.right,
        )

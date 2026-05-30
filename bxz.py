#!/usr/bin/env python3
# bxz.py - BXZ Language v4.0 - Stable Version

import sys
import os
import re
import math
import json
import time
import random
import hashlib
import base64
import sqlite3
import threading
import subprocess
import tempfile
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Callable

# ============ VERSION ============
__version__ = "1.1.5"

# ============ TOKEN TYPES ============
class TokenType:
    # Keywords
    LET = "let"
    CONST = "const"
    FUNC = "func"
    IF = "if"
    ELSE = "else"
    ELIF = "elif"
    FOR = "for"
    WHILE = "while"
    BREAK = "break"
    CONTINUE = "continue"
    RETURN = "return"
    TRY = "try"
    CATCH = "catch"
    FINALLY = "finally"
    THROW = "throw"
    IMPORT = "import"
    FROM = "from"
    AS = "as"
    IN = "in"
    IS = "is"
    # Types
    INT = "int"
    FLOAT = "float"
    STR = "str"
    BOOL = "bool"
    LIST = "list"
    DICT = "dict"
    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    NULL = "NULL"
    IDENTIFIER = "IDENTIFIER"
    # Operators
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    POW = "**"
    ASSIGN = "="
    EQ = "=="
    NE = "!="
    LT = "<"
    GT = ">"
    LE = "<="
    GE = ">="
    AND = "&&"
    OR = "||"
    NOT = "!"
    # Symbols
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACK = "["
    RBRACK = "]"
    COMMA = ","
    DOT = "."
    COLON = ":"
    SEMICOLON = ";"
    ARROW = "->"
    EOF = "EOF"

class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# ============ AST NODES ============
class ASTNode: pass

class Program(ASTNode):
    def __init__(self, statements): self.statements = statements

class LetStatement(ASTNode):
    def __init__(self, name, value, is_const=False): self.name = name; self.value = value; self.is_const = is_const

class PrintStatement(ASTNode):
    def __init__(self, value): self.value = value

class IfStatement(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None): self.condition = condition; self.then_branch = then_branch; self.else_branch = else_branch

class WhileStatement(ASTNode):
    def __init__(self, condition, body): self.condition = condition; self.body = body

class ForStatement(ASTNode):
    def __init__(self, variable, iterable, body): self.variable = variable; self.iterable = iterable; self.body = body

class FunctionStatement(ASTNode):
    def __init__(self, name, params, body): self.name = name; self.params = params; self.body = body

class ReturnStatement(ASTNode):
    def __init__(self, value): self.value = value

class BreakStatement(ASTNode): pass
class ContinueStatement(ASTNode): pass

class TryStatement(ASTNode):
    def __init__(self, try_body, catch_var, catch_body, finally_body): self.try_body = try_body; self.catch_var = catch_var; self.catch_body = catch_body; self.finally_body = finally_body

class ThrowStatement(ASTNode):
    def __init__(self, value): self.value = value

class BlockStatement(ASTNode):
    def __init__(self, statements): self.statements = statements

class ExpressionStatement(ASTNode):
    def __init__(self, expression): self.expression = expression

class NumberLiteral(ASTNode):
    def __init__(self, value): self.value = value

class StringLiteral(ASTNode):
    def __init__(self, value): self.value = value

class BooleanLiteral(ASTNode):
    def __init__(self, value): self.value = value

class Identifier(ASTNode):
    def __init__(self, name): self.name = name

class BinaryOp(ASTNode):
    def __init__(self, left, operator, right): self.left = left; self.operator = operator; self.right = right

class UnaryOp(ASTNode):
    def __init__(self, operator, operand): self.operator = operator; self.operand = operand

class CallExpression(ASTNode):
    def __init__(self, name, arguments): self.name = name; self.arguments = arguments

class ArrayLiteral(ASTNode):
    def __init__(self, elements): self.elements = elements

class ObjectLiteral(ASTNode):
    def __init__(self, properties): self.properties = properties

class LambdaExpression(ASTNode):
    def __init__(self, params, body): self.params = params; self.body = body

# ============ LEXER ============
class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        
        self.keywords = {
            'let': TokenType.LET, 'const': TokenType.CONST, 'func': TokenType.FUNC,
            'if': TokenType.IF, 'else': TokenType.ELSE, 'elif': TokenType.ELIF,
            'for': TokenType.FOR, 'while': TokenType.WHILE, 'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE, 'return': TokenType.RETURN, 'try': TokenType.TRY,
            'catch': TokenType.CATCH, 'finally': TokenType.FINALLY, 'throw': TokenType.THROW,
            'import': TokenType.IMPORT, 'from': TokenType.FROM, 'as': TokenType.AS,
            'in': TokenType.IN, 'is': TokenType.IS,
            'int': TokenType.INT, 'float': TokenType.FLOAT, 'str': TokenType.STR,
            'bool': TokenType.BOOL, 'list': TokenType.LIST, 'dict': TokenType.DICT,
            'true': TokenType.BOOLEAN, 'false': TokenType.BOOLEAN, 'null': TokenType.NULL,
        }
    
    def tokenize(self):
        tokens = []
        while self.pos < len(self.source):
            ch = self.source[self.pos]
            
            if ch in ' \t\r':
                self._advance()
            elif ch == '\n':
                self.line += 1
                self.col = 1
                self.pos += 1
            elif ch.isdigit():
                tokens.append(self._read_number())
            elif ch.isalpha() or ch == '_':
                tokens.append(self._read_identifier())
            elif ch == '"' or ch == "'":
                tokens.append(self._read_string())
            elif ch == '+':
                self._advance()
                tokens.append(Token(TokenType.PLUS, '+', self.line, self.col-1))
            elif ch == '-':
                self._advance()
                tokens.append(Token(TokenType.MINUS, '-', self.line, self.col-1))
            elif ch == '*':
                self._advance()
                tokens.append(Token(TokenType.MUL, '*', self.line, self.col-1))
            elif ch == '/':
                self._advance()
                tokens.append(Token(TokenType.DIV, '/', self.line, self.col-1))
            elif ch == '%':
                self._advance()
                tokens.append(Token(TokenType.MOD, '%', self.line, self.col-1))
            elif ch == '=':
                self._advance()
                if self._peek() == '=':
                    self._advance()
                    tokens.append(Token(TokenType.EQ, '==', self.line, self.col-2))
                else:
                    tokens.append(Token(TokenType.ASSIGN, '=', self.line, self.col-1))
            elif ch == '!':
                self._advance()
                if self._peek() == '=':
                    self._advance()
                    tokens.append(Token(TokenType.NE, '!=', self.line, self.col-2))
                else:
                    tokens.append(Token(TokenType.NOT, '!', self.line, self.col-1))
            elif ch == '<':
                self._advance()
                if self._peek() == '=':
                    self._advance()
                    tokens.append(Token(TokenType.LE, '<=', self.line, self.col-2))
                else:
                    tokens.append(Token(TokenType.LT, '<', self.line, self.col-1))
            elif ch == '>':
                self._advance()
                if self._peek() == '=':
                    self._advance()
                    tokens.append(Token(TokenType.GE, '>=', self.line, self.col-2))
                else:
                    tokens.append(Token(TokenType.GT, '>', self.line, self.col-1))
            elif ch == '&':
                self._advance()
                if self._peek() == '&':
                    self._advance()
                    tokens.append(Token(TokenType.AND, '&&', self.line, self.col-2))
                else:
                    tokens.append(Token(TokenType.BIT_AND, '&', self.line, self.col-1))
            elif ch == '|':
                self._advance()
                if self._peek() == '|':
                    self._advance()
                    tokens.append(Token(TokenType.OR, '||', self.line, self.col-2))
                else:
                    tokens.append(Token(TokenType.BIT_OR, '|', self.line, self.col-1))
            elif ch == '(':
                self._advance()
                tokens.append(Token(TokenType.LPAREN, '(', self.line, self.col-1))
            elif ch == ')':
                self._advance()
                tokens.append(Token(TokenType.RPAREN, ')', self.line, self.col-1))
            elif ch == '{':
                self._advance()
                tokens.append(Token(TokenType.LBRACE, '{', self.line, self.col-1))
            elif ch == '}':
                self._advance()
                tokens.append(Token(TokenType.RBRACE, '}', self.line, self.col-1))
            elif ch == '[':
                self._advance()
                tokens.append(Token(TokenType.LBRACK, '[', self.line, self.col-1))
            elif ch == ']':
                self._advance()
                tokens.append(Token(TokenType.RBRACK, ']', self.line, self.col-1))
            elif ch == ',':
                self._advance()
                tokens.append(Token(TokenType.COMMA, ',', self.line, self.col-1))
            elif ch == '.':
                self._advance()
                tokens.append(Token(TokenType.DOT, '.', self.line, self.col-1))
            elif ch == ':':
                self._advance()
                tokens.append(Token(TokenType.COLON, ':', self.line, self.col-1))
            elif ch == ';':
                self._advance()
                tokens.append(Token(TokenType.SEMICOLON, ';', self.line, self.col-1))
            else:
                raise SyntaxError(f"Unknown character '{ch}' at line {self.line}, col {self.col}")
        
        tokens.append(Token(TokenType.EOF, None, self.line, self.col))
        return tokens
    
    def _advance(self):
        self.pos += 1
        self.col += 1
    
    def _peek(self):
        return self.source[self.pos] if self.pos < len(self.source) else None
    
    def _read_number(self):
        start = self.pos
        has_dot = False
        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
            if self.source[self.pos] == '.':
                has_dot = True
            self._advance()
        num_str = self.source[start:self.pos]
        if has_dot:
            value = float(num_str)
        else:
            value = int(num_str)
        return Token(TokenType.NUMBER, value, self.line, self.col - (self.pos - start))
    
    def _read_identifier(self):
        start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self._advance()
        ident = self.source[start:self.pos]
        token_type = self.keywords.get(ident, TokenType.IDENTIFIER)
        if token_type == TokenType.BOOLEAN:
            value = True if ident == 'true' else False
            return Token(token_type, value, self.line, self.col - (self.pos - start))
        return Token(token_type, ident, self.line, self.col - (self.pos - start))
    
    def _read_string(self):
        quote = self.source[self.pos]
        self._advance()
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos] != quote:
            if self.source[self.pos] == '\n':
                raise SyntaxError("Unterminated string")
            self._advance()
        value = self.source[start:self.pos]
        self._advance()
        return Token(TokenType.STRING, value, self.line, self.col - (self.pos - start))

# ============ PARSER ============
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else Token(TokenType.EOF, None, 0, 0)
    
    def eat(self, token_type):
        token = self.current()
        if token.type == token_type:
            self.pos += 1
            return token
        raise SyntaxError(f"Expected {token_type}, got {token.type}")
    
    def parse(self):
        statements = []
        while self.current().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self):
        token = self.current()
        
        if token.type == TokenType.LET:
            return self.parse_let(False)
        elif token.type == TokenType.CONST:
            return self.parse_let(True)
        elif token.type == TokenType.PRINT:
            return self.parse_print()
        elif token.type == TokenType.IF:
            return self.parse_if()
        elif token.type == TokenType.WHILE:
            return self.parse_while()
        elif token.type == TokenType.FOR:
            return self.parse_for()
        elif token.type == TokenType.FUNC:
            return self.parse_function()
        elif token.type == TokenType.RETURN:
            return self.parse_return()
        elif token.type == TokenType.BREAK:
            self.eat(TokenType.BREAK)
            return BreakStatement()
        elif token.type == TokenType.CONTINUE:
            self.eat(TokenType.CONTINUE)
            return ContinueStatement()
        elif token.type == TokenType.TRY:
            return self.parse_try()
        elif token.type == TokenType.THROW:
            return self.parse_throw()
        elif token.type == TokenType.LBRACE:
            return self.parse_block()
        else:
            expr = self.parse_expression()
            if self.current().type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
            return ExpressionStatement(expr)
    
    def parse_let(self, is_const):
        self.eat(TokenType.LET if not is_const else TokenType.CONST)
        name = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.ASSIGN)
        value = self.parse_expression()
        if self.current().type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        return LetStatement(name, value, is_const)
    
    def parse_print(self):
        self.eat(TokenType.PRINT)
        value = self.parse_expression()
        if self.current().type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        return PrintStatement(value)
    
    def parse_if(self):
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.parse_expression()
        self.eat(TokenType.RPAREN)
        then_branch = self.parse_block().statements
        
        else_branch = None
        if self.current().type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            else_branch = self.parse_block().statements
        
        return IfStatement(condition, then_branch, else_branch)
    
    def parse_while(self):
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        condition = self.parse_expression()
        self.eat(TokenType.RPAREN)
        body = self.parse_block().statements
        return WhileStatement(condition, body)
    
    def parse_for(self):
        self.eat(TokenType.FOR)
        self.eat(TokenType.LPAREN)
        var = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.IN)
        iterable = self.parse_expression()
        self.eat(TokenType.RPAREN)
        body = self.parse_block().statements
        return ForStatement(var, iterable, body)
    
    def parse_function(self):
        self.eat(TokenType.FUNC)
        name = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.LPAREN)
        
        params = []
        if self.current().type != TokenType.RPAREN:
            params.append(self.eat(TokenType.IDENTIFIER).value)
            while self.current().type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                params.append(self.eat(TokenType.IDENTIFIER).value)
        
        self.eat(TokenType.RPAREN)
        body = self.parse_block().statements
        return FunctionStatement(name, params, body)
    
    def parse_return(self):
        self.eat(TokenType.RETURN)
        value = None
        if self.current().type != TokenType.SEMICOLON:
            value = self.parse_expression()
        if self.current().type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        return ReturnStatement(value)
    
    def parse_try(self):
        self.eat(TokenType.TRY)
        try_body = self.parse_block().statements
        
        catch_var = None
        catch_body = None
        if self.current().type == TokenType.CATCH:
            self.eat(TokenType.CATCH)
            self.eat(TokenType.LPAREN)
            catch_var = self.eat(TokenType.IDENTIFIER).value
            self.eat(TokenType.RPAREN)
            catch_body = self.parse_block().statements
        
        finally_body = None
        if self.current().type == TokenType.FINALLY:
            self.eat(TokenType.FINALLY)
            finally_body = self.parse_block().statements
        
        return TryStatement(try_body, catch_var, catch_body, finally_body)
    
    def parse_throw(self):
        self.eat(TokenType.THROW)
        value = self.parse_expression()
        if self.current().type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        return ThrowStatement(value)
    
    def parse_block(self):
        self.eat(TokenType.LBRACE)
        statements = []
        while self.current().type != TokenType.RBRACE:
            statements.append(self.parse_statement())
        self.eat(TokenType.RBRACE)
        return BlockStatement(statements)
    
    def parse_expression(self):
        return self.parse_assignment()
    
    def parse_assignment(self):
        left = self.parse_logical_or()
        
        if self.current().type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            right = self.parse_assignment()
            return BinaryOp(left, '=', right)
        
        return left
    
    def parse_logical_or(self):
        left = self.parse_logical_and()
        
        while self.current().type == TokenType.OR:
            self.eat(TokenType.OR)
            right = self.parse_logical_and()
            left = BinaryOp(left, '||', right)
        
        return left
    
    def parse_logical_and(self):
        left = self.parse_comparison()
        
        while self.current().type == TokenType.AND:
            self.eat(TokenType.AND)
            right = self.parse_comparison()
            left = BinaryOp(left, '&&', right)
        
        return left
    
    def parse_comparison(self):
        left = self.parse_addition()
        
        while self.current().type in [TokenType.EQ, TokenType.NE, TokenType.LT, 
                                       TokenType.GT, TokenType.LE, TokenType.GE]:
            op = self.current()
            self.eat(op.type)
            right = self.parse_addition()
            left = BinaryOp(left, op.value, right)
        
        return left
    
    def parse_addition(self):
        left = self.parse_multiplication()
        
        while self.current().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current()
            self.eat(op.type)
            right = self.parse_multiplication()
            left = BinaryOp(left, op.value, right)
        
        return left
    
    def parse_multiplication(self):
        left = self.parse_primary()
        
        while self.current().type in [TokenType.MUL, TokenType.DIV, TokenType.MOD]:
            op = self.current()
            self.eat(op.type)
            right = self.parse_primary()
            left = BinaryOp(left, op.value, right)
        
        return left
    
    def parse_primary(self):
        token = self.current()
        
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumberLiteral(token.value)
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return StringLiteral(token.value)
        elif token.type == TokenType.BOOLEAN:
            self.eat(TokenType.BOOLEAN)
            return BooleanLiteral(token.value)
        elif token.type == TokenType.NULL:
            self.eat(TokenType.NULL)
            return None
        elif token.type == TokenType.IDENTIFIER:
            name = token.value
            self.eat(TokenType.IDENTIFIER)
            if self.current().type == TokenType.LPAREN:
                return self.parse_call(name)
            return Identifier(name)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return expr
        elif token.type == TokenType.LBRACK:
            return self.parse_array()
        elif token.type == TokenType.LBRACE:
            return self.parse_object()
        
        raise SyntaxError(f"Unexpected token: {token.type}")
    
    def parse_call(self, name):
        self.eat(TokenType.LPAREN)
        args = []
        if self.current().type != TokenType.RPAREN:
            args.append(self.parse_expression())
            while self.current().type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                args.append(self.parse_expression())
        self.eat(TokenType.RPAREN)
        return CallExpression(name, args)
    
    def parse_array(self):
        self.eat(TokenType.LBRACK)
        elements = []
        if self.current().type != TokenType.RBRACK:
            elements.append(self.parse_expression())
            while self.current().type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                elements.append(self.parse_expression())
        self.eat(TokenType.RBRACK)
        return ArrayLiteral(elements)
    
    def parse_object(self):
        self.eat(TokenType.LBRACE)
        properties = {}
        if self.current().type != TokenType.RBRACE:
            key = self.eat(TokenType.IDENTIFIER).value
            self.eat(TokenType.COLON)
            value = self.parse_expression()
            properties[key] = value
            while self.current().type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                key = self.eat(TokenType.IDENTIFIER).value
                self.eat(TokenType.COLON)
                value = self.parse_expression()
                properties[key] = value
        self.eat(TokenType.RBRACE)
        return ObjectLiteral(properties)

# ============ INTERPRETER ============
class Interpreter:
    def __init__(self, debug=False):
        self.vars = {}
        self.funcs = {}
        self.debug = debug
        self.return_val = None
        self.break_flag = False
        self.continue_flag = False
    
    def log(self, msg):
        if self.debug:
            print(f"[DEBUG] {msg}")
    
    def evaluate(self, node):
        if isinstance(node, NumberLiteral):
            return node.value
        elif isinstance(node, StringLiteral):
            return node.value
        elif isinstance(node, BooleanLiteral):
            return node.value
        elif isinstance(node, Identifier):
            if node.name in self.vars:
                return self.vars[node.name]
            raise RuntimeError(f"Undefined variable: {node.name}")
        elif isinstance(node, BinaryOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            
            ops = {
                '+': lambda: left + right,
                '-': lambda: left - right,
                '*': lambda: left * right,
                '/': lambda: left / right if right != 0 else 0,
                '%': lambda: left % right,
                '**': lambda: left ** right,
                '==': lambda: left == right,
                '!=': lambda: left != right,
                '<': lambda: left < right,
                '>': lambda: left > right,
                '<=': lambda: left <= right,
                '>=': lambda: left >= right,
                '&&': lambda: left and right,
                '||': lambda: left or right,
                '=': lambda: right,
            }
            
            if node.operator in ops:
                result = ops[node.operator]()
                return result
            raise RuntimeError(f"Unknown operator: {node.operator}")
        elif isinstance(node, UnaryOp):
            operand = self.evaluate(node.operand)
            if node.operator == '!':
                return not operand
            elif node.operator == '-':
                return -operand
            return operand
        elif isinstance(node, CallExpression):
            if node.name == 'print':
                args = [self.evaluate(arg) for arg in node.arguments]
                print(*args)
                return None
            elif node.name == 'len':
                return len(self.evaluate(node.arguments[0]))
            elif node.name == 'range':
                start = self.evaluate(node.arguments[0]) if len(node.arguments) > 0 else 0
                end = self.evaluate(node.arguments[1]) if len(node.arguments) > 1 else start
                step = self.evaluate(node.arguments[2]) if len(node.arguments) > 2 else 1
                return list(range(start, end, step))
            elif node.name == 'input':
                prompt = self.evaluate(node.arguments[0]) if node.arguments else ""
                return input(prompt)
            elif node.name == 'int':
                return int(self.evaluate(node.arguments[0]))
            elif node.name == 'float':
                return float(self.evaluate(node.arguments[0]))
            elif node.name == 'str':
                return str(self.evaluate(node.arguments[0]))
            elif node.name == 'type':
                return type(self.evaluate(node.arguments[0])).__name__
            elif node.name in self.funcs:
                return self._call_function(node.name, node.arguments)
            elif node.name == 'server':
                port = self.evaluate(node.arguments[0]) if node.arguments else 8080
                self.start_server(port)
                return None
            elif node.name == 'json':
                return json.dumps(self.evaluate(node.arguments[0]))
            elif node.name == 'parse_json':
                return json.loads(self.evaluate(node.arguments[0]))
            raise RuntimeError(f"Undefined function: {node.name}")
        elif isinstance(node, ArrayLiteral):
            return [self.evaluate(elem) for elem in node.elements]
        elif isinstance(node, ObjectLiteral):
            result = {}
            for key, value in node.properties.items():
                result[key] = self.evaluate(value)
            return result
        return None
    
    def _call_function(self, name, args_nodes):
        func = self.funcs[name]
        old_vars = self.vars.copy()
        
        for i, param in enumerate(func.params):
            if i < len(args_nodes):
                self.vars[param] = self.evaluate(args_nodes[i])
        
        self.return_val = None
        for stmt in func.body:
            self.execute(stmt)
            if self.return_val is not None:
                break
        
        result = self.return_val
        self.vars = old_vars
        self.return_val = None
        return result
    
    def start_server(self, port):
        try:
            from http.server import HTTPServer, SimpleHTTPRequestHandler
            server = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
            url = f'http://localhost:{port}'
            print(f"\n{'='*40}")
            print(f"🚀 Server: {url}")
            print(f"{'='*40}")
            webbrowser.open(url)
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")
    
    def execute(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.execute(stmt)
                if self.return_val is not None:
                    break
        elif isinstance(node, LetStatement):
            value = self.evaluate(node.value)
            if node.is_const:
                self.vars[node.name] = value
            else:
                self.vars[node.name] = value
        elif isinstance(node, PrintStatement):
            value = self.evaluate(node.value)
            print(value)
        elif isinstance(node, IfStatement):
            condition = self.evaluate(node.condition)
            if condition:
                for stmt in node.then_branch:
                    self.execute(stmt)
            elif node.else_branch:
                for stmt in node.else_branch:
                    self.execute(stmt)
        elif isinstance(node, WhileStatement):
            self.break_flag = False
            while self.evaluate(node.condition) and not self.break_flag:
                for stmt in node.body:
                    self.execute(stmt)
                    if self.continue_flag:
                        self.continue_flag = False
                        break
        elif isinstance(node, ForStatement):
            iterable = self.evaluate(node.iterable)
            self.break_flag = False
            for item in iterable:
                if self.break_flag:
                    break
                if self.continue_flag:
                    self.continue_flag = False
                    continue
                self.vars[node.variable] = item
                for stmt in node.body:
                    self.execute(stmt)
        elif isinstance(node, FunctionStatement):
            self.funcs[node.name] = node
        elif isinstance(node, ReturnStatement):
            self.return_val = self.evaluate(node.value) if node.value else None
        elif isinstance(node, BreakStatement):
            self.break_flag = True
        elif isinstance(node, ContinueStatement):
            self.continue_flag = True
        elif isinstance(node, TryStatement):
            try:
                for stmt in node.try_body:
                    self.execute(stmt)
            except Exception as e:
                if node.catch_var:
                    self.vars[node.catch_var] = str(e)
                    for stmt in node.catch_body:
                        self.execute(stmt)
                else:
                    raise
            finally:
                if node.finally_body:
                    for stmt in node.finally_body:
                        self.execute(stmt)
        elif isinstance(node, ThrowStatement):
            raise RuntimeError(str(self.evaluate(node.value)))
        elif isinstance(node, ExpressionStatement):
            self.evaluate(node.expression)
        elif isinstance(node, BlockStatement):
            for stmt in node.statements:
                self.execute(stmt)

# ============ MAIN ============
def run_file(filename, debug=False):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found!")
        return False
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter(debug)
        interpreter.execute(ast)
        return True
    except Exception as e:
        print(f"Error: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        return False

def repl(debug=False):
    print("=" * 60)
    print(f"⚡ BXZ Language v{__version__}")
    print("Commands: print(), len(), range(), input(), server()")
    print("Type 'exit' to quit, 'help' for commands")
    print("=" * 60)
    
    interpreter = Interpreter(debug)
    
    while True:
        try:
            code = input("\n>>> ")
            if code.strip() in ['exit', 'quit']:
                print("Goodbye!")
                break
            if code.strip() == 'help':
                print("""
Available commands:
  print("text")     - Print text
  let x = value     - Create variable
  x + y, x * y      - Math operations
  func name(p) {}   - Define function
  if (cond) {}      - Conditional
  while (cond) {}   - Loop
  for item in arr {} - For-each loop
  server(port)      - Start web server
  json(obj)         - Convert to JSON
  parse_json(str)   - Parse JSON
  len(arr)          - Get length
  range(start, end) - Create range
  input(prompt)     - Get user input
  int(), float(), str(), type()
""")
                continue
            if code.strip():
                lexer = Lexer(code)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                ast = parser.parse()
                interpreter.execute(ast)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            if debug:
                import traceback
                traceback.print_exc()

def main():
    import argparse
    parser = argparse.ArgumentParser(description=f"BXZ Language v{__version__}")
    parser.add_argument("file", nargs="?", help="BXZ file to execute")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive REPL")
    parser.add_argument("-d", "--debug", action="store_true", help="Debug mode")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")
    parser.add_argument("-s", "--server", action="store_true", help="Start web server")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Server port")
    
    args = parser.parse_args()
    
    if args.version:
        print(f"BXZ Language v{__version__}")
        return
    
    if args.server:
        Interpreter().start_server(args.port)
    elif args.interactive or not args.file:
        repl(args.debug)
    else:
        success = run_file(args.file, args.debug)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
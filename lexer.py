from enum import Enum
import re
from typing import List, NamedTuple

class TokenType(Enum):
    KEYWORD = "KEYWORD"        # jika, selain, keluaran
    IDENTIFIER = "IDENTIFIER"  # x, y, skor
    NUMBER = "NUMBER"          # 10, 100, 0
    ASSIGN = "ASSIGN"          # =
    COMP_OP = "COMP_OP"        # <, >, ==
    LPAREN = "LPAREN"          # (
    RPAREN = "RPAREN"          # )
    LBRACE = "LBRACE"          # {
    RBRACE = "RBRACE"          # }
    EOF = "EOF"

class Token(NamedTuple):
    type: TokenType
    value: str

    @staticmethod
    def tokenize(code: str) -> List['Token']:
        tokens = []
        token_patterns = [
            (TokenType.KEYWORD,    r'\bjika\b|\bselain\b|\bkeluaran\b'),
            (TokenType.IDENTIFIER, r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            (TokenType.NUMBER,     r'\b\d+\b'),
            (TokenType.COMP_OP,    r'==|<|>'),
            (TokenType.ASSIGN,     r'='),
            (TokenType.LPAREN,     r':'),
            (TokenType.RPAREN,     r';'),
            (TokenType.LBRACE,     r'\bp\b'),
            (TokenType.RBRACE,     r'\bq\b'),
        ]
        
        master_pattern = '|'.join(f'(?P<{kind.name}>{pattern})' for kind, pattern in token_patterns)
        
        for mo in re.finditer(master_pattern, code):
            kind = mo.lastgroup
            if kind is not None:
                value = mo.group(kind)
                tokens.append(Token(TokenType[kind], value))
        
        tokens.append(Token(TokenType.EOF, ""))
        return tokens
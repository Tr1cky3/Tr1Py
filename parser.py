from dataclasses import dataclass
from typing import List, Any
from lexer import Token, TokenType

class ASTNode:
    pass

@dataclass
class NodeAngka(ASTNode):
    value : str

@dataclass
class NodeVariabel(ASTNode):
    name: str

@dataclass
class NodeOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass
class NodeIsiVar(ASTNode):
    var_name: str
    expr: ASTNode

@dataclass
class NodeKeluaran(ASTNode):
    expr: ASTNode

@dataclass
class NodePercabangan(ASTNode):
    condition: NodeOp
    then_branch: List[ASTNode]
    else_branch: List[ASTNode]

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> Token:
        return self.tokens[self.pos]
    
    def consume(self, expected_type: TokenType) -> Token:
        token = self.current_token()
        if token.type == expected_type:
            self.pos += 1
            return token
        raise SyntaxError(f"[Syntax Error] Ekspektasi Token {expected_type}, tapi dapat {token.type} pada posisi {self.pos}")
    
    def parse(self) -> List[ASTNode]:
        nodes = []
        while self.current_token().type !=  TokenType.EOF:
            nodes.append(self.parse_statement())
        return nodes
    
    def parse_statement(self) -> ASTNode:
        token = self.current_token()
        if token.type == TokenType.KEYWORD and token.value == "keluaran":
            self.consume(TokenType.KEYWORD)
            self.consume(TokenType.LPAREN)
            expr = self.parse_ekspresi()
            self.consume(TokenType.RPAREN)
            return NodeKeluaran(expr=expr)
        
        elif token.type == TokenType.KEYWORD and token.value == "jika":
            return self.parse_jika()
        
        elif token.type == TokenType.IDENTIFIER:
            var_name = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.ASSIGN)
            expr = self.parse_ekspresi()
            return NodeIsiVar(var_name=var_name, expr=expr)
        
        raise SyntaxError(f"[Syntax Error] Tidak dapat mengenali statement pada posisi {self.pos}")
    
    def parse_jika(self) -> NodePercabangan:
        self.consume(TokenType.KEYWORD)
        self.consume(TokenType.LPAREN)

        left = self.parse_ekspresi()
        op = self.consume(TokenType.COMP_OP).value
        right = self.parse_ekspresi()
        condition = NodeOp(left=left, operator=op, right=right)
        
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.LBRACE)
        then_branch = []

        while self.current_token().type != TokenType.RBRACE:
            then_branch.append(self.parse_statement())
        self.consume(TokenType.RBRACE)

        else_branch = []
        if self.current_token().type == TokenType.KEYWORD and self.current_token().value == "selain":
            self.consume(TokenType.KEYWORD)
            self.consume(TokenType.LBRACE)
            while self.current_token().type != TokenType.RBRACE:
                else_branch.append(self.parse_statement())
            self.consume(TokenType.RBRACE)
            
        return NodePercabangan(condition=condition, then_branch=then_branch, else_branch=else_branch)
    
    def parse_ekspresi(self) -> ASTNode:
        token = self.current_token()
        if token.type == TokenType.NUMBER:
            return NodeAngka(value=self.consume(TokenType.NUMBER).value)
        elif token.type == TokenType.IDENTIFIER:
            return NodeVariabel(name=self.consume(TokenType.IDENTIFIER).value)
        raise SyntaxError(f"Ekspresi tidak valid: '{token.value}'")
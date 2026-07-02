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


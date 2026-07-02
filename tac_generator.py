from typing import List
from parser import ASTNode, NodeIsiVar, NodePercabangan, NodeOp, NodeVariabel, NodeAngka, NodeKeluaran

class TACGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.code = []
    
    def new_temp(self) -> str:
        self.temp_counter += 1
        return f"t{self.temp_counter}"
    
    def new_label(self) -> str:
        self.label_counter += 1
        return f"L{self.label_counter}"
    
    def generate(self, ast: List[ASTNode]) -> List[str]:
        for node in ast:
            self.visit(node)
        return self.code
    
    def visit(self, node: ASTNode) -> str:
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name)
        return visitor(node)
    
    def visit_NodeIsiVar(self, node: NodeIsiVar):
        expr_res = self.visit(node.expr)
        self.code.append(f"{node.var_name} = {expr_res}")
        return node.var_name
    
    def visit_NodeAngka(self, node: NodeAngka) -> str:
        return node.value
    
    def visit_NodeVariabel(self, node: NodeVariabel) -> str:
        return node.name
    
    def visit_NodeOp(self, node: NodeOp) -> str:
        left = self.visit(node.left)
        right = self.visit(node.right)
        temp = self.new_temp()
        self.code.append(f"{temp} = {left} {node.operator} {right}")
        return temp
    
    def visit_NodeKeluaran(self, node: NodeKeluaran):
        expr_res = self.visit(node.expr)
        self.code.append(f"param {expr_res}")
        self.code.append("call keluaran, 1")

    def visit_NodePercabangan(self, node: NodePercabangan):
        cond_res = self.visit(node.condition)

        label_false = self.new_label()
        label_end = self.new_label()

        self.code.append(f"ifFalse {cond_res} goto {label_false}")

        for stmt in node.then_branch:
            self.visit(stmt)
        self.code.append(f"goto {label_end}")
        self.code.append(f"{label_false}:")
        for stmt in node.else_branch:
            self.visit(stmt)
        self.code.append(f"{label_end}:")
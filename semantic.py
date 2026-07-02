from typing import List, Any
from parser import ASTNode, NodeAngka, NodeVariabel, NodeOp, NodeIsiVar, NodeKeluaran, NodePercabangan

class SemanticAnalyzer:
    def __init__(self):
        self.declared_variables = set()
    
    def analyze(self, ast: List[ASTNode]):
        for node in ast:
            self.visit(node)
    
    def visit(self, node: ASTNode):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        visitor(node)

    def generic_visit(self, node: ASTNode):
        raise Exception(f"Metode visit_{type(node).__name__} belum didefinisikan di Semantik.")
    
    def visit_NodeIsiVar(self, node: NodeIsiVar):
        self.declared_variables.add(node.var_name)
        self.visit(node.expr)

    def visit_NodePercabangan(self, node: NodePercabangan):
        self.visit(node.condition)
        for stmt in node.then_branch:
            self.visit(stmt)
        for stmt in node.else_branch:
            self.visit(stmt)

    def visit_NodeOp(self, node: NodeOp):
        self.visit(node.left)
        self.visit(node.right)
    
    def visit_NodeVariabel(self, node: NodeVariabel):
        if node.name not in self.declared_variables:
            raise Exception(f"[Semantic Error] Variabel '{node.name}' belum dideklarasikan.")
        
    def visit_NodeAngka(self, node: NodeAngka):
        pass  # Tidak ada pemeriksaan semantik untuk angka

    def visit_NodeKeluaran(self, node: NodeKeluaran):
        self.visit(node.expr)
import ast
import os
import json
import argparse
from typing import List, Dict, Set

# ==============================================================================
# TRACE™ Structural Auditor - Zero-Trust Extractor (Open Source Edition)
# ==============================================================================
# This script is designed to run LOCALLY on the client's machine.
# It uses Abstract Syntax Tree (AST) parsing to extract ONLY the structural
# topology of the codebase (Classes, Functions, and their calls).
# 
# ZERO-TRUST GUARANTEE:
# ❌ Does NOT read strings, comments, or business logic.
# ❌ Does NOT read passwords, API keys, or environment variables.
# ❌ Does NOT send anything automatically. It generates a local JSON file.
# ==============================================================================

class TopologyVisitor(ast.NodeVisitor):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.current_class = None
        self.current_function = None
        self.nodes = set()
        self.edges = []

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.nodes.add(f"Class::{node.name}")
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        func_name = node.name
        if self.current_class:
            func_name = f"{self.current_class}.{func_name}"
            self.edges.append((f"Class::{self.current_class}", f"Function::{func_name}", "contains"))
            
        self.current_function = func_name
        self.nodes.add(f"Function::{func_name}")
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if self.current_function:
            if isinstance(node.func, ast.Name):
                target = node.func.id
                self.edges.append((f"Function::{self.current_function}", f"Call::{target}", "calls"))
            elif isinstance(node.func, ast.Attribute):
                target = node.func.attr
                self.edges.append((f"Function::{self.current_function}", f"Call::{target}", "calls"))
        self.generic_visit(node)

def analyze_file(filepath: str) -> Dict:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
            
        visitor = TopologyVisitor(filepath)
        visitor.visit(tree)
        
        return {
            "file": filepath,
            "nodes": list(visitor.nodes),
            "edges": [{"source": src, "target": tgt, "type": rel} for src, tgt, rel in visitor.edges]
        }
    except Exception as e:
        return {"file": filepath, "error": str(e)}

def run_extraction(target_dir: str, output_file: str):
    print(f"[*] TRACE Zero-Trust Extractor v0.1")
    print(f"[*] Target Directory: {target_dir}")
    print(f"[*] Scanning for AST topology (ignores strings/logic)...")
    
    all_data = []
    py_files_count = 0
    
    for root, _, files in os.walk(target_dir):
        if ".git" in root or "node_modules" in root or "venv" in root:
            continue
            
        for file in files:
            if file.endswith('.py'):
                py_files_count += 1
                filepath = os.path.join(root, file)
                file_data = analyze_file(filepath)
                if "error" not in file_data:
                    all_data.append(file_data)
                    
    # Aggregate graph
    graph = {
        "metadata": {
            "files_scanned": py_files_count,
            "extractor": "trace_ast_os_v0.1"
        },
        "topology": all_data
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2)
        
    print(f"[+] Extraction complete! Found {py_files_count} files.")
    print(f"[+] Saved topology to {output_file}")
    print(f"[!] You may inspect {output_file} to verify no business logic or secrets were captured.")
    print(f"[!] Please send {output_file} to your TRACE Structural Auditor.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TRACE Structural Audit - AST Extractor")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to scan")
    parser.add_argument("--output", default="trace_topology_export.json", help="Output JSON file")
    
    args = parser.parse_args()
    run_extraction(args.directory, args.output)

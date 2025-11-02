#!/usr/bin/env python3
"""
Demo script for Dependency Visualizer - Stage 4
"""

import subprocess
import sys
import os

def run_demo():
    print("=== Dependency Visualizer Demo - Stage 4 ===\n")
    
    if not os.path.exists("dependency_visualizer.py"):
        print("ERROR: dependency_visualizer.py not found!")
        return
    
    tests = [
        ("1. Reverse dependencies for G", "config_stage4_reverse.toml"),
        ("2. Leaf package (no reverse deps)", "config_stage4_leaf.toml"),
        ("3. Reverse deps with cycles", "config_stage4_cycle_reverse.toml"),
        ("4. Standard tree without reverse deps", "config_stage3_test.toml")
    ]
    
    for test_name, config_file in tests:
        print(test_name + ":")
        print("-" * 40)
        
        if not os.path.exists(config_file):
            print(f"Config file {config_file} not found!")
            continue
            
        result = subprocess.run(
            [sys.executable, "dependency_visualizer.py", config_file],
            capture_output=True, 
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
    
    print("=" * 50)
    print("Demo completed!")

if __name__ == "__main__":
    run_demo()
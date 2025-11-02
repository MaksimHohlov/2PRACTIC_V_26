#!/usr/bin/env python3
"""
Demo script for Dependency Visualizer - Stage 3
"""

import subprocess
import sys
import os

def run_demo():
    print("=== Dependency Visualizer Demo - Stage 3 ===\n")
    
    if not os.path.exists("dependency_visualizer.py"):
        print("ERROR: dependency_visualizer.py not found!")
        return
    
    # Создаем тестовый репозиторий
    with open("test_repo.txt", "w") as f:
        f.write("""A: B, C
B: D, E
C: F
D: G
E: G, H
F: H
G: I
H: I
I:
J: K, L
K: J
L: M
M:
""")
    
    tests = [
        ("1. Test mode with file repository", "config_stage3_test.toml"),
        ("2. With package filtering", "config_stage3_filter.toml"),
        ("3. Cyclic dependencies", "config_stage3_cycle.toml"),
        ("4. Real mode (limited depth)", "config_stage3_real.toml")
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
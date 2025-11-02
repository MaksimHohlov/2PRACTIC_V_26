#!/usr/bin/env python3
"""
Demo script for Dependency Visualizer - Stage 2
"""

import subprocess
import sys
import os

def run_demo():
    print("=== Dependency Visualizer Demo - Stage 2 ===\n")
    
    if not os.path.exists("dependency_visualizer.py"):
        print("ERROR: dependency_visualizer.py not found!")
        return
    
    print("1. Real mode - fetching from PyPI:")
    print("-" * 40)
    result = subprocess.run([sys.executable, "dependency_visualizer.py", "config.toml"], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    print("2. Test mode - using mock data:")
    print("-" * 40)
    
    # Сначала проверим существование config_test.toml
    if not os.path.exists("config_test.toml"):
        print("ERROR: config_test.toml not found! Creating default...")
        with open("config_test.toml", "w") as f:
            f.write("""package_name = "django"
repository_url = "https://pypi.org/simple/"
test_mode = true
test_repository_path = ""
ascii_tree = true
max_depth = 2
filter_substring = ""
show_reverse_deps = false
""")
        print("Created default config_test.toml")
    
    result = subprocess.run([sys.executable, "dependency_visualizer.py", "config_test.toml"], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    print("3. Package without dependencies:")
    print("-" * 40)
    
    # Сначала проверим существование config_numpy.toml
    if not os.path.exists("config_numpy.toml"):
        print("ERROR: config_numpy.toml not found! Creating default...")
        with open("config_numpy.toml", "w") as f:
            f.write("""package_name = "numpy"
repository_url = "https://pypi.org/simple/"
test_mode = true
test_repository_path = ""
ascii_tree = true
max_depth = 2
filter_substring = ""
show_reverse_deps = false
""")
        print("Created default config_numpy.toml")
    
    result = subprocess.run([sys.executable, "dependency_visualizer.py", "config_numpy.toml"], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    print("4. Error handling - invalid config:")
    print("-" * 40)
    
    # Сначала проверим существование test_config.toml
    if not os.path.exists("test_config.toml"):
        print("ERROR: test_config.toml not found! Creating default...")
        with open("test_config.toml", "w") as f:
            f.write("""package_name = ""
repository_url = 123
test_mode = "yes"
max_depth = -1
filter_substring = 456
ascii_tree = "true"
""")
        print("Created default test_config.toml")
    
    result = subprocess.run([sys.executable, "dependency_visualizer.py", "test_config.toml"], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    print("5. Error handling - file not found:")
    print("-" * 40)
    result = subprocess.run([sys.executable, "dependency_visualizer.py", "nonexistent.toml"], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    print("\n" + "="*50)
    print("Demo completed!")

if __name__ == "__main__":
    run_demo()
#!/usr/bin/env python3
"""
Скрипт для создания файлов Этапа 4
"""

import os

files = {
    "config_stage4_reverse.toml": """package_name = "G"
repository_url = "https://pypi.org/simple/"
test_mode = true
test_repository_path = "test_repo.txt"
ascii_tree = true
max_depth = 4
filter_substring = ""
show_reverse_deps = true
""",

    "config_stage4_leaf.toml": """package_name = "I"
repository_url = "https://pypi.org/simple/"
test_mode = true
test_repository_path = "test_repo.txt"
ascii_tree = true
max_depth = 4
filter_substring = ""
show_reverse_deps = true
""",

    "config_stage4_cycle_reverse.toml": """package_name = "K"
repository_url = "https://pypi.org/simple/"
test_mode = true
test_repository_path = "test_repo.txt"
ascii_tree = true
max_depth = 4
filter_substring = ""
show_reverse_deps = true
"""
}

def create_files():
    print("Creating files for Stage 4...")
    
    for filename, content in files.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f" Created {filename}")
    
    print("\n Verification:")
    for filename in files.keys():
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f" {filename}: {size} bytes")

if __name__ == "__main__":
    create_files()
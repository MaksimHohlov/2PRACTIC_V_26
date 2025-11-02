#!/usr/bin/env python3
"""
Скрипт для создания файлов Этапа 3
"""

import os

# Содержимое файлов
files = {
    "test_repo.txt": """A: B, C
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
""",
    
    "config_stage3_test.toml": """package_name = "A"
repository_url = "https://pypi.org/simple/"
test_mode = true
test_repository_path = "test_repo.txt"
ascii_tree = true
max_depth = 4
filter_substring = ""
show_reverse_deps = false
""",

    "config_stage3_filter.toml": """package_name = "A"
repository_url = "https://pypi.org/simple/"
test_mode = true
test_repository_path = "test_repo.txt"
ascii_tree = true
max_depth = 4
filter_substring = "G"
show_reverse_deps = false
""",

    "config_stage3_cycle.toml": """package_name = "J"
repository_url = "https://pypi.org/simple/"
test_mode = true
test_repository_path = "test_repo.txt"
ascii_tree = true
max_depth = 10
filter_substring = ""
show_reverse_deps = false
""",

    "config_stage3_real.toml": """package_name = "requests"
repository_url = "https://pypi.org/simple/"
test_mode = false
test_repository_path = ""
ascii_tree = true
max_depth = 2
filter_substring = ""
show_reverse_deps = false
"""
}

# Создаем файлы
for filename, content in files.items():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f" Создан {filename} ({len(content)} байт)")

print("\n Проверка созданных файлов:")
for filename in files.keys():
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f" {filename}: {size} байт")
    else:
        print(f" {filename}: НЕ НАЙДЕН")
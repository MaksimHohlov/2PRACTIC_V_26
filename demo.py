#!/usr/bin/env python3
"""
Демонстрация работы инструмента визуализации зависимостей - Этап 1
"""

import subprocess
import sys
import os

def run_demo():
    print("=== Демонстрация инструмента визуализации зависимостей - Этап 1 ===\n")
    
    # Демонстрация успешной загрузки конфигурации
    print("1. Успешная загрузка корректной конфигурации:")
    print("-" * 50)
    result = subprocess.run([sys.executable, "dependency_visualizer.py", "config.toml"], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    print("\n2. Демонстрация обработки ошибок (неверная конфигурация):")
    print("-" * 50)
    result = subprocess.run([sys.executable, "dependency_visualizer.py", "test_config.toml"], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    print("\n3. Демонстрация обработки ошибок (файл не существует):")
    print("-" * 50)
    result = subprocess.run([sys.executable, "dependency_visualizer.py", "nonexistent.toml"], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

if __name__ == "__main__":
    run_demo()
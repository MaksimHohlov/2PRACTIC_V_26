#!/usr/bin/env python3
"""
Dependency Graph Visualizer Tool
Stage 2: Data Collection
"""

import tomllib
import sys
import urllib.request
import json
import re
from pathlib import Path
from typing import List, Dict, Any


class ConfigError(Exception):
    pass


class DependencyVisualizer:
    def __init__(self):
        self.config: Dict[str, Any] = {}
    
    def load_config(self, config_path: str) -> None:
        """Load configuration from TOML file"""
        try:
            config_file_path = Path(config_path)
            if not config_file_path.exists():
                raise ConfigError(f"Config file not found: {config_path}")
            
            print(f"DEBUG: Loading {config_path}")
            
            # Читаем файл и сразу выводим содержимое для отладки
            with open(config_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"DEBUG: File content:\n{content}")
            
            # Парсим TOML
            with open(config_file_path, 'rb') as f:
                self.config = tomllib.load(f)
                print(f"DEBUG: Parsed config: {self.config}")
                
        except tomllib.TOMLDecodeError as e:
            raise ConfigError(f"Invalid TOML format: {e}")
        except Exception as e:
            raise ConfigError(f"Error reading file: {e}")
    
    def validate_config(self) -> None:
        """Validate configuration parameters"""
        print(f"DEBUG: Validating config with keys: {list(self.config.keys())}")
        
        # ПРОСТАЯ ПРОВЕРКА - если config пустой, сразу ошибка
        if not self.config:
            raise ConfigError("Config is empty or could not be parsed")
        
        if 'package_name' not in self.config:
            raise ConfigError("Missing required parameter 'package_name'")
        
        package_name = self.config['package_name']
        if not isinstance(package_name, str) or not package_name.strip():
            raise ConfigError("Parameter 'package_name' must be non-empty string")
    
    def get_dependencies_from_pypi(self, package_name: str) -> List[str]:
        """Get direct dependencies from PyPI"""
        try:
            print(f"Fetching dependencies for '{package_name}' from PyPI...")
            
            url = f"https://pypi.org/pypi/{package_name}/json"
            req = urllib.request.Request(url, headers={'User-Agent': 'DependencyVisualizer/1.0'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                dependencies = []
                
                if 'info' in data and 'requires_dist' in data['info']:
                    requires_dist = data['info']['requires_dist']
                    if requires_dist:
                        print(f"Found {len(requires_dist)} dependency entries")
                        for dep in requires_dist:
                            if dep:
                                dep_name = re.split(r'[<>=!]', dep)[0].strip()
                                if '[' in dep_name:
                                    dep_name = dep_name.split('[')[0]
                                dep_name = dep_name.strip(' ;()')
                                if dep_name and dep_name not in dependencies:
                                    dependencies.append(dep_name)
                        print(f"After cleaning: {len(dependencies)} unique dependencies")
                
                return dependencies
                
        except Exception as e:
            raise ConfigError(f"Error fetching dependencies: {e}")
    
    def get_test_dependencies(self, package_name: str) -> List[str]:
        """Get test dependencies"""
        test_deps = {
            'requests': ['urllib3', 'chardet', 'certifi', 'idna'],
            'numpy': [],
            'django': ['asgiref', 'sqlparse', 'tzdata'],
            'flask': ['Werkzeug', 'Jinja2', 'itsdangerous', 'click']
        }
        return test_deps.get(package_name, [])
    
    def get_config_value(self, key: str) -> Any:
        return self.config.get(key)
    
    def display_config(self) -> None:
        print("=== Configuration ===")
        if self.config:
            for key, value in self.config.items():
                print(f"{key}: {value}")
        else:
            print("No configuration loaded")
        print("=" * 50)
    
    def get_direct_dependencies(self) -> List[str]:
        package_name = self.get_config_value('package_name')
        
        if self.get_config_value('test_mode'):
            print(f"Test mode: Using mock dependencies for '{package_name}'")
            return self.get_test_dependencies(package_name)
        else:
            return self.get_dependencies_from_pypi(package_name)


def main():
    if len(sys.argv) != 2:
        print("Usage: python dependency_visualizer.py <config_file.toml>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    visualizer = DependencyVisualizer()
    
    try:
        print(f"Loading configuration from {config_file}...")
        visualizer.load_config(config_file)
        visualizer.validate_config()
        
        print("\n" + "="*50)
        visualizer.display_config()
        
        print("\n=== Stage 2: Direct Dependencies Analysis ===")
        dependencies = visualizer.get_direct_dependencies()
        
        package_name = visualizer.get_config_value('package_name')
        if dependencies:
            print(f"\nDirect dependencies of '{package_name}':")
            for i, dep in enumerate(dependencies, 1):
                print(f"  {i}. {dep}")
            print(f"\nTotal: {len(dependencies)} direct dependencies")
        else:
            print(f"\nNo direct dependencies found for '{package_name}'")
        
        print("\nSUCCESS: Stage 2 completed!")
        
    except ConfigError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
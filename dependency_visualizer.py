#!/usr/bin/env python3
"""
Dependency Graph Visualizer Tool
Stage 3: Graph Operations
"""

import tomllib
import sys
import urllib.request
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple
from collections import deque

# Fix encoding for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class ConfigError(Exception):
    pass


class DependencyVisualizer:
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.dependency_graph: Dict[str, List[str]] = {}
        self.visited: Set[str] = set()
        
    def load_config(self, config_path: str) -> None:
        """Load configuration from TOML file"""
        try:
            config_file_path = Path(config_path)
            if not config_file_path.exists():
                raise ConfigError(f"Config file not found: {config_path}")
            
            with open(config_file_path, 'rb') as f:
                self.config = tomllib.load(f)
                
        except tomllib.TOMLDecodeError as e:
            raise ConfigError(f"Invalid TOML format: {e}")
        except Exception as e:
            raise ConfigError(f"Error reading file: {e}")
    
    def validate_config(self) -> None:
        """Validate configuration parameters"""
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
        """Get test dependencies for demonstration"""
        test_deps = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F'],
            'D': ['G'],
            'E': ['G', 'H'],
            'F': ['H'],
            'G': ['I'],
            'H': ['I'],
            'I': [],
            'J': ['K', 'L'],
            'K': ['J'],  # Циклическая зависимость
            'L': ['M'],
            'M': []
        }
        return test_deps.get(package_name, [])
    
    def load_test_repository(self, file_path: str) -> Dict[str, List[str]]:
        """Load test repository from file"""
        try:
            graph = {}
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        package, deps_str = line.split(':', 1)
                        package = package.strip()
                        dependencies = [dep.strip() for dep in deps_str.split(',') if dep.strip()]
                        graph[package] = dependencies
            return graph
        except Exception as e:
            raise ConfigError(f"Error loading test repository: {e}")
    
    def should_filter_package(self, package_name: str) -> bool:
        """Check if package should be filtered out"""
        filter_substring = self.get_config_value('filter_substring')
        if filter_substring and filter_substring in package_name:
            return True
        return False
    
    def build_dependency_graph(self) -> None:
        """Build complete dependency graph using DFS without recursion"""
        start_package = self.get_config_value('package_name')
        max_depth = self.get_config_value('max_depth')
        
        print(f"\nBuilding dependency graph for '{start_package}' (max depth: {max_depth})...")
        
        # Stack for DFS: (package_name, current_depth)
        stack = [(start_package, 0)]
        self.dependency_graph = {}
        self.visited = set()
        cycles_detected = []
        
        while stack:
            current_package, depth = stack.pop()
            
            # Skip if beyond max depth
            if depth > max_depth:
                continue
            
            # Skip if already visited at this depth or shallower
            if current_package in self.visited:
                # Check for cycles
                if current_package in [p for p, _ in stack]:
                    cycles_detected.append(current_package)
                continue
            
            self.visited.add(current_package)
            
            # Skip if filtered
            if self.should_filter_package(current_package):
                print(f"  Filtered out: {current_package}")
                continue
            
            # Get dependencies based on mode
            if self.get_config_value('test_mode') and self.get_config_value('test_repository_path'):
                # Test repository mode
                test_graph = self.load_test_repository(self.get_config_value('test_repository_path'))
                dependencies = test_graph.get(current_package, [])
            elif self.get_config_value('test_mode'):
                # Mock data mode
                dependencies = self.get_test_dependencies(current_package)
            else:
                # Real PyPI mode
                dependencies = self.get_dependencies_from_pypi(current_package)
            
            self.dependency_graph[current_package] = dependencies
            
            # Add dependencies to stack for further processing
            for dep in reversed(dependencies):  # reversed to maintain order
                if not self.should_filter_package(dep):
                    stack.append((dep, depth + 1))
        
        if cycles_detected:
            print(f"⚠️  Detected potential cycles: {list(set(cycles_detected))}")
    
    def display_dependency_tree(self) -> None:
        """Display dependency tree in simple ASCII format"""
        if not self.dependency_graph:
            print("No dependencies found.")
            return
        
        start_package = self.get_config_value('package_name')
        
        print(f"\n=== Dependency Tree for '{start_package}' ===")
        
        def print_tree(package: str, depth: int = 0):
            if depth > self.get_config_value('max_depth'):
                return
                
            indent = "  " * depth
            print(f"{indent}- {package}")
            
            if package in self.dependency_graph:
                for dep in self.dependency_graph[package]:
                    if not self.should_filter_package(dep):
                        print_tree(dep, depth + 1)
        
        print_tree(start_package)
    
    def get_config_value(self, key: str) -> Any:
        return self.config.get(key)
    
    def display_config(self) -> None:
        """Display all configuration parameters in key-value format"""
        print("=== Configuration ===")
        
        config_items = [
            ("Package name", "package_name"),
            ("Repository URL", "repository_url"), 
            ("Test mode", "test_mode"),
            ("Test repository path", "test_repository_path"),
            ("ASCII tree output", "ascii_tree"),
            ("Max analysis depth", "max_depth"),
            ("Filter substring", "filter_substring"),
            ("Show reverse dependencies", "show_reverse_deps")
        ]
        
        for display_name, config_key in config_items:
            value = self.get_config_value(config_key)
            print(f"{display_name}: {value}")
        
        print("=" * 50)
    
    def analyze_dependencies(self) -> None:
        """Main analysis method for Stage 3"""
        self.build_dependency_graph()
        
        if self.get_config_value('ascii_tree'):
            self.display_dependency_tree()
        
        # Display statistics
        total_packages = len(self.dependency_graph)
        if total_packages > 0:
            total_dependencies = sum(len(deps) for deps in self.dependency_graph.values())
            print(f"\n📊 Graph Statistics:")
            print(f"   Total packages: {total_packages}")
            print(f"   Total dependencies: {total_dependencies}")
            print(f"   Max depth reached: {self.get_config_value('max_depth')}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python dependency_visualizer.py <config_file.toml>")
        print("Example: python dependency_visualizer.py config.toml")
        sys.exit(1)
    
    config_file = sys.argv[1]
    visualizer = DependencyVisualizer()
    
    try:
        print(f"Loading configuration from {config_file}...")
        visualizer.load_config(config_file)
        visualizer.validate_config()
        
        print("\n" + "="*50)
        visualizer.display_config()
        
        print("\n=== Stage 3: Dependency Graph Analysis ===")
        visualizer.analyze_dependencies()
        
        print("\n✅ Stage 3 completed successfully!")
        
    except ConfigError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
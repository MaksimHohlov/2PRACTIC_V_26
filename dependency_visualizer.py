import tomllib
import sys
from pathlib import Path

class ConfigError(Exception):
    pass

class DependencyVisualizer:
    def __init__(self):
        self.config = {}
        self.default_config = {
            'package_name': 'example-package',
            'repository_url': 'https://pypi.org/simple/',
            'test_mode': False,
            'test_repository_path': '',
            'ascii_tree': True,
            'max_depth': 3,
            'filter_substring': '',
            'show_reverse_deps': False
        }
    
    def load_config(self, config_path):
        try:
            config_file_path = Path(config_path)
            if not config_file_path.exists():
                raise ConfigError(f"Config file not found: {config_path}")
            
            with open(config_file_path, 'rb') as f:
                self.config = tomllib.load(f)
                
        except Exception as e:
            raise ConfigError(f"Error reading file: {e}")
    
    def validate_config(self):
        if 'package_name' not in self.config:
            raise ConfigError("Missing 'package_name'")
        
        package_name = self.config['package_name']
        if not isinstance(package_name, str) or not package_name.strip():
            raise ConfigError("'package_name' must be non-empty string")
        
        test_mode = self.config.get('test_mode', False)
        if not isinstance(test_mode, bool):
            raise ConfigError("'test_mode' must be boolean")
        
        max_depth = self.config.get('max_depth', 3)
        if not isinstance(max_depth, int) or max_depth < 1:
            raise ConfigError("'max_depth' must be integer > 0")
    
    def get_config_value(self, key):
        return self.config.get(key, self.default_config.get(key))
    
    def display_config(self):
        print("=== Configuration ===")
        print(f"Package name: {self.get_config_value('package_name')}")
        print(f"Repository URL: {self.get_config_value('repository_url')}")
        print(f"Test mode: {self.get_config_value('test_mode')}")
        print(f"ASCII tree: {self.get_config_value('ascii_tree')}")
        print(f"Max depth: {self.get_config_value('max_depth')}")
        print(f"Filter: {self.get_config_value('filter_substring')}")
        print("=" * 50)

def main():
    if len(sys.argv) != 2:
        print("Usage: python dependency_visualizer.py config.toml")
        sys.exit(1)
    
    config_file = sys.argv[1]
    visualizer = DependencyVisualizer()
    
    try:
        visualizer.load_config(config_file)
        visualizer.validate_config()
        visualizer.display_config()
        print("SUCCESS: Configuration loaded!")
    except ConfigError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
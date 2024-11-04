# tests/test_collector.py
import os
import tempfile
import unittest
from pathlib import Path

from llm_code_materializer.collector import (
    collect_project_structure,
    collect_file_contents,
    generate_output_content
)

class TestCollector(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Create a simple project structure
        self.create_test_project()
    
    def tearDown(self):
        # Clean up temporary directory
        self.clean_test_project()
    
    def create_test_project(self):
        """Create a test project structure."""
        # Create directories
        os.makedirs(os.path.join(self.test_dir, 'utils'))
        os.makedirs(os.path.join(self.test_dir, 'data', 'maps'))
        
        # Create test files
        files = {
            'main.py': 'def main():\n    print("Hello")\n',
            'utils/helper.py': 'def helper():\n    return True\n',
            'data/maps/map.txt': '##########\n#....P...#\n##########\n'
        }
        
        for path, content in files.items():
            full_path = os.path.join(self.test_dir, path)
            with open(full_path, 'w') as f:
                f.write(content)
    
    def clean_test_project(self):
        """Clean up test project files."""
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)
    
    def test_collect_project_structure(self):
        """Test project structure collection."""
        structure = collect_project_structure(self.test_dir)
        
        # Verify structure
        expected_structure = [
            '- utils/',
            '    - helper.py',
            '- data/',
            '    - maps/',
            '        - map.txt',
            '- main.py'
        ]
        
        self.assertEqual(structure, expected_structure)
    
    def test_collect_file_contents(self):
        """Test file content collection."""
        files = collect_file_contents(self.test_dir)
        
        # Sort files by path for consistent comparison
        files = sorted(files, key=lambda x: x[0])
        
        # Verify collected files
        self.assertEqual(len(files), 3)
        
        # Check each file
        main_py = next(f for f in files if f[0] == 'main.py')
        self.assertEqual(main_py[2], 'python')
        self.assertIn('def main():', main_py[1])
        
        helper_py = next(f for f in files if f[0] == 'utils/helper.py')
        self.assertEqual(helper_py[2], 'python')
        self.assertIn('def helper():', helper_py[1])
        
        map_txt = next(f for f in files if f[0] == 'data/maps/map.txt')
        self.assertEqual(map_txt[2], 'text')
        self.assertIn('#....P...#', map_txt[1])
    
    def test_generate_output_content(self):
        """Test output content generation."""
        structure = ['- main.py']
        files = [('main.py', 'print("test")', 'python')]
        
        output = generate_output_content(structure, files)
        
        # Verify output format
        self.assertIn('# Project Structure', output)
        self.assertIn('```\n- main.py\n```', output)
        self.assertIn('### main.py', output)
        self.assertIn('```python', output)
        self.assertIn('print("test")', output)

if __name__ == '__main__':
    unittest.main()
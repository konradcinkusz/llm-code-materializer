# tests/test_generator.py
import os
import tempfile
import unittest
from pathlib import Path
from llm_code_materializer.generator import (
    parse_structure_section,
    extract_code_blocks,
    create_project_files
)

class TestGenerator(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Sample input content
        self.sample_content = """
# Project Structure
```
- main.py
- utils/
    - helper.py
```
## File Contents
### main.py
```python
# main.py
def main():
    print("Hello")
```
### utils/helper.py
```python
# utils/helper.py
def helper():
    return True
```
"""
    
    def tearDown(self):
        # Clean up temporary directory
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)
    
    def test_parse_structure_section(self):
        """Test parsing of project structure section."""
        structure = parse_structure_section(self.sample_content)
        expected = [
            '- main.py',
            '- utils/',
            '    - helper.py'
        ]
        self.assertEqual(structure, expected)
    
    def test_parse_structure_section_missing(self):
        """Test handling of missing structure section."""
        invalid_content = "# No structure here\n### Just some content"
        with self.assertRaises(ValueError):
            parse_structure_section(invalid_content)
    
    def test_extract_code_blocks(self):
        """Test extraction of code blocks from content."""
        files = extract_code_blocks(self.sample_content)
        
        # Check number of files
        self.assertEqual(len(files), 2)
        
        # Check main.py content
        self.assertIn('main.py', files)
        main_content, main_type = files['main.py']
        self.assertEqual(main_type, 'python')
        self.assertIn('def main():', main_content)
        self.assertNotIn('# main.py', main_content)  # Should remove filename comment
        
        # Check helper.py content
        self.assertIn('utils/helper.py', files)
        helper_content, helper_type = files['utils/helper.py']
        self.assertEqual(helper_type, 'python')
        self.assertIn('def helper():', helper_content)
        self.assertNotIn('# utils/helper.py', helper_content)
    
    def test_extract_code_blocks_with_special_files(self):
        """Test extraction of non-Python code blocks."""
        content_with_map = self.sample_content + """
### data/map.txt
```
##########
#....P...#
##########
```
"""
        files = extract_code_blocks(content_with_map)
        self.assertEqual(len(files), 3)
        self.assertIn('data/map.txt', files)
        map_content, map_type = files['data/map.txt']
        self.assertEqual(map_type, '')  # Should be empty for non-Python files
        self.assertIn('#....P...#', map_content)
    
    def test_create_project_files(self):
        """Test creation of project files."""
        # Extract files from sample content
        files = extract_code_blocks(self.sample_content)
        
        # Create the files
        create_project_files(files, self.test_dir)
        
        # Check main.py
        main_path = os.path.join(self.test_dir, 'main.py')
        self.assertTrue(os.path.exists(main_path))
        with open(main_path, 'r') as f:
            content = f.read()
            self.assertIn('def main():', content)
        
        # Check utils/helper.py
        helper_path = os.path.join(self.test_dir, 'utils', 'helper.py')
        self.assertTrue(os.path.exists(helper_path))
        with open(helper_path, 'r') as f:
            content = f.read()
            self.assertIn('def helper():', content)
    
    def test_create_project_files_nested(self):
        """Test creation of deeply nested project files."""
        files = {
            'deep/nested/path/file.py': ('print("test")', 'python'),
            'another/deep/path/test.py': ('def test(): pass', 'python')
        }
        
        create_project_files(files, self.test_dir)
        
        # Check first nested file
        path1 = os.path.join(self.test_dir, 'deep', 'nested', 'path', 'file.py')
        self.assertTrue(os.path.exists(path1))
        with open(path1, 'r') as f:
            self.assertEqual(f.read(), 'print("test")')
        
        # Check second nested file
        path2 = os.path.join(self.test_dir, 'another', 'deep', 'path', 'test.py')
        self.assertTrue(os.path.exists(path2))
        with open(path2, 'r') as f:
            self.assertEqual(f.read(), 'def test(): pass')
    
    def test_create_project_files_empty_directories(self):
        """Test handling of empty directories in file paths."""
        files = {
            'empty/dir/': ('', ''),  # Empty directory marker
            'empty/dir/file.py': ('print("test")', 'python')
        }
        
        create_project_files(files, self.test_dir)
        
        # Check that directory was created
        dir_path = os.path.join(self.test_dir, 'empty', 'dir')
        self.assertTrue(os.path.isdir(dir_path))
        
        # Check that file was created
        file_path = os.path.join(dir_path, 'file.py')
        self.assertTrue(os.path.exists(file_path))
    
    def test_create_project_files_overwrite(self):
        """Test overwriting existing files."""
        # Create initial file
        os.makedirs(os.path.join(self.test_dir, 'test'))
        initial_path = os.path.join(self.test_dir, 'test', 'file.py')
        with open(initial_path, 'w') as f:
            f.write('initial content')
        
        # Overwrite with new content
        files = {
            'test/file.py': ('new content', 'python')
        }
        create_project_files(files, self.test_dir)
        
        # Check content was overwritten
        with open(initial_path, 'r') as f:
            self.assertEqual(f.read(), 'new content')

if __name__ == '__main__':
    unittest.main()
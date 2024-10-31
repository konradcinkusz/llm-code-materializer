import os
import re

def extract_code_blocks(content):
    """
    Extract code blocks from markdown-style content.
    Returns a dictionary of filenames and their corresponding code.
    """
    # Pattern to match Python file paths in the project structure
    structure_pattern = r'- ([^/\n]+/)*[^/\n]+\.py'
    
    # Pattern to match code blocks
    code_block_pattern = r'```python\n(.*?)```'
    
    # Find all code blocks
    code_blocks = re.finditer(code_block_pattern, content, re.DOTALL)
    
    # Find all file paths mentioned in the structure
    file_paths = re.finditer(structure_pattern, content)
    
    # Create a list of valid Python files
    valid_files = [match.group().strip('- ') for match in file_paths]
    
    # Dictionary to store filename-code pairs
    files_dict = {}
    
    # Current file being processed
    current_file = None
    
    # Process the content line by line to associate files with code
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Check if line contains a Python file reference
        for file_path in valid_files:
            if file_path in line and not line.startswith('```'):
                current_file = file_path
                break
        
        # If we find a Python code block and have a current file
        if line.strip() == '```python' and current_file:
            code_lines = []
            j = i + 1
            while j < len(lines) and not lines[j].strip() == '```':
                code_lines.append(lines[j])
                j += 1
            
            # Store the code for the current file
            if current_file not in files_dict:
                files_dict[current_file] = '\n'.join(code_lines)

    return files_dict

def create_python_files(files_dict, base_dir='.'):
    """
    Create Python files and directories based on the parsed structure.
    """
    for file_path, content in files_dict.items():
        # Create full path
        full_path = os.path.join(base_dir, file_path)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write the file
        with open(full_path, 'w') as f:
            f.write(content)
        
        print(f"Created: {file_path}")

def create_map_file(content, base_dir='.'):
    """
    Create the map file if it exists in the content.
    """
    map_pattern = r'```\n((?:[\.#PEINn\s]+)+)\n```'
    map_match = re.search(map_pattern, content)
    
    if map_match:
        map_dir = os.path.join(base_dir, 'maps')
        os.makedirs(map_dir, exist_ok=True)
        
        map_path = os.path.join(map_dir, 'map.txt')
        with open(map_path, 'w') as f:
            f.write(map_match.group(1))
        print("Created: maps/map.txt")

def main():
    # Read the project structure file
    try:
        with open('project_structure.txt', 'r') as f:
            content = f.read()
        
        # Extract and create Python files
        files_dict = extract_code_blocks(content)
        create_python_files(files_dict)
        
        # Create map file
        create_map_file(content)
        
        print("\nProject generation completed successfully!")
        
    except FileNotFoundError:
        print("Error: project_structure.txt not found in the current directory.")
    except Exception as e:
        print(f"Error processing project structure: {str(e)}")

if __name__ == "__main__":
    main()
# src/llm_code_materializer/generator.py
import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def parse_structure_section(content: str) -> List[str]:
    """
    Extract the project structure section from the content.
    
    Args:
        content: The full content string
    
    Returns:
        List of structure lines
    """
    structure_pattern = r'```\n((?:[-\s].*\n)+)```'
    match = re.search(structure_pattern, content)
    if not match:
        raise ValueError("Could not find project structure section")
    return [line.strip() for line in match.group(1).split('\n') if line.strip()]

def extract_code_blocks(content: str) -> Dict[str, Tuple[str, str]]:
    """
    Extract all code blocks from the content.
    
    Args:
        content: The full content string
    
    Returns:
        Dictionary mapping filenames to tuple of (content, type)
    """
    files = {}
    
    # Pattern to match code blocks with optional type
    pattern = r'### (.*?)\n```(\w*)\n(.*?)```'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        filename = match.group(1).strip()
        block_type = match.group(2).strip()
        content = match.group(3).strip()
        
        # Remove filename comment if it's at the start of the content
        content = re.sub(r'^#\s*' + re.escape(filename), '', content).strip()
        
        files[filename] = (content, block_type)
    
    return files

def create_project_files(files: Dict[str, Tuple[str, str]], base_dir: str) -> None:
    """
    Create all project files in the specified directory.
    
    Args:
        files: Dictionary of filename to (content, type) mappings
        base_dir: Base directory to create files in
    """
    for file_path, (content, _) in files.items():
        full_path = os.path.join(base_dir, file_path)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write file content
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

def create_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        description='Generate project files from LLM response document.'
    )
    parser.add_argument(
        'input_file',
        nargs='?',
        default='project_structure.txt',
        help='Input structure file (default: project_structure.txt)'
    )
    parser.add_argument(
        '--output-dir', '-o',
        default='.',
        help='Output directory for generated files (default: current directory)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    return parser

def main() -> None:
    """Main entry point for the generator command."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        if args.verbose:
            print(f"Reading structure from: {args.input_file}")
        
        # Read input file
        with open(args.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse structure and extract code blocks
        structure = parse_structure_section(content)
        if args.verbose:
            print(f"Found {len(structure)} structure elements")
        
        files = extract_code_blocks(content)
        if args.verbose:
            print(f"Found {len(files)} files to generate")
        
        # Create output directory if it doesn't exist
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Create all project files
        create_project_files(files, args.output_dir)
        
        if args.verbose:
            print("\nFiles generated:")
            for file_path in files:
                print(f"  - {file_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
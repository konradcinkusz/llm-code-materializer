# src/llm_code_materializer/collector.py
import argparse
import os
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional

def collect_project_structure(start_path: str) -> List[str]:
    """
    Collect and return project structure in a tree-like format.
    
    Args:
        start_path: Root directory to start collection from
    
    Returns:
        List of strings representing the project structure
    """
    structure = []
    
    for root, dirs, files in os.walk(start_path):
        # Skip special directories
        dirs[:] = [d for d in dirs if not d.startswith(('__', '.'))]
        
        # Calculate relative path and indentation
        rel_path = os.path.relpath(root, start_path)
        level = 0 if rel_path == '.' else rel_path.count(os.sep) + 1
        indent = '    ' * level
        
        # Add directory to structure (skip root)
        if level > 0:
            structure.append(f'{indent}- {os.path.basename(root)}/')
        
        # Add files to structure
        for file in sorted(files):
            if file.endswith('.py') or file == 'map.txt':
                structure.append(f'{indent}- {file}')
    
    return structure

def collect_file_contents(start_path: str) -> List[Tuple[str, str, str]]:
    """
    Collect contents of all relevant files.
    
    Args:
        start_path: Root directory to start collection from
    
    Returns:
        List of tuples (file_path, content, file_type)
    """
    collected = []
    
    for root, _, files in os.walk(start_path):
        for file in sorted(files):
            if file.endswith('.py') or file == 'map.txt':
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, start_path)
                
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    file_type = 'python' if file.endswith('.py') else 'text'
                    collected.append((rel_path, content, file_type))
                except Exception as e:
                    print(f"Warning: Could not read {rel_path}: {e}", file=sys.stderr)
    
    return collected

def generate_output_content(structure: List[str], files: List[Tuple[str, str, str]]) -> str:
    """
    Generate the final output content in the desired format.
    
    Args:
        structure: List of strings representing project structure
        files: List of tuples containing file information
    
    Returns:
        Formatted string containing the complete output
    """
    output = []
    
    # Add header and structure
    output.extend([
        "# Project Structure\n",
        "The project is organized as follows:\n",
        "```",
        *structure,
        "```\n",
        "## File Contents\n"
    ])
    
    # Add file contents
    for file_path, content, file_type in files:
        output.extend([
            f"### {file_path}\n",
            f"```{file_type}" if file_type == 'python' else "```",
            f"# {file_path}" if file_type == 'python' else "",
            content,
            "```\n"
        ])
    
    return "\n".join(line for line in output if line is not None)

def create_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        description='Collect Python project files into a single structured document.'
    )
    parser.add_argument(
        'project_dir',
        nargs='?',
        default='.',
        help='Directory containing the Python project (default: current directory)'
    )
    parser.add_argument(
        '--output', '-o',
        default='collected_project_structure.txt',
        help='Output file path (default: collected_project_structure.txt)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    return parser

def main() -> None:
    """Main entry point for the collector command."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # Normalize paths
        project_dir = os.path.abspath(args.project_dir)
        
        if args.verbose:
            print(f"Collecting project structure from: {project_dir}")
        
        # Collect project information
        structure = collect_project_structure(project_dir)
        if args.verbose:
            print(f"Found {len(structure)} structure elements")
        
        files = collect_file_contents(project_dir)
        if args.verbose:
            print(f"Collected {len(files)} files")
        
        # Generate output
        output_content = generate_output_content(structure, files)
        
        # Write output
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_content)
        
        if args.verbose:
            print(f"\nOutput written to: {args.output}")
            print(f"Total size: {len(output_content)} characters")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
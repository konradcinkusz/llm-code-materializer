# src/llm_code_materializer/utils.py
import os
import sys
from pathlib import Path
from typing import List, Tuple

def ensure_directory(path: str) -> None:
    """Ensure directory exists, create if it doesn't."""
    os.makedirs(path, exist_ok=True)

def is_valid_python_file(filename: str) -> bool:
    """Check if file is a valid Python file to process."""
    return filename.endswith('.py') and not filename.startswith('__')

def is_special_file(filename: str) -> bool:
    """Check if file is a special file we want to process (like map.txt)."""
    special_files = ['map.txt']
    return filename in special_files

def get_relative_path(file_path: str, start_path: str) -> str:
    """Get relative path from start_path to file_path."""
    return os.path.relpath(file_path, start_path)

def format_path_for_output(path: str) -> str:
    """Format path for consistent output."""
    return path.replace('\\', '/')
# LLM Code Materializer

A tool that transforms Large Language Model (LLM) code responses into a fully structured project with all necessary files and directories.

## Overview
When you get a comprehensive solution from an LLM (like GPT), it typically outputs a complete project structure with multiple files, code blocks, and explanations in a single response. This tool automatically converts that output into a proper directory structure with all the necessary files.

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llm-code-materializer.git
cd llm-code-materializer
```

2. Run the generator:
```bash
python python_script_generator.py
```

That's it! The tool will use the included `project_structure.txt` example file to generate a complete game project with multiple Python files and resources.

## Included Example
The repository comes with an example `project_structure.txt` that contains a complete 2D game project structure from an LLM response. Running the generator will create:

```
game/
├── main.py
├── settings.py
├── player.py
├── npc.py
├── enemy.py
├── item.py
├── obstacle.py
├── camera.py
├── map_loader.py
└── maps/
    └── map.txt
```

This example demonstrates:
- Multiple Python files with proper imports
- Class definitions and game logic
- Resource files (map.txt)
- Nested directory structure

## Using with Your Own LLM Responses

1. Save your LLM response as `project_structure.txt`
2. Ensure it follows the format:
   ```
   ## Project Structure
   - your/
       - file.py
       - structure.py

   ```python
   # file.py
   your code here
   ```

   ```python
   # structure.py
   more code here
   ```
   ```

3. Run the generator

## Input Format Requirements
The tool expects LLM responses to be formatted with:

1. **Project Structure Section**
   - Tree-like structure showing files and directories
   - Files must have `.py` extension to be recognized

2. **Code Blocks**
   - Enclosed in triple backticks with `python` specification
   - Filename in comment at start of block
   - Must match files in project structure

3. **Additional Resources**
   - Other files can be included in simple code blocks
   - Will be created in specified directories

## Best Practices for LLM Prompting

When asking an LLM to generate a project:
1. Request complete file contents
2. Ask for a clear project structure
3. Request any necessary additional files
4. Ask for proper imports between files

Example prompt:
```
Create a complete Python project for [your purpose]. Please include:
1. Full project structure with all necessary files
2. Complete code for each file including imports
3. Any required resource files
4. Clear file organization
```

## Limitations
- Requires specific formatting in LLM response
- Code blocks must be marked with ```python
- Filename comments must match project structure
- Will overwrite existing files with same names

## Future Improvements
- Support for multiple LLM output formats
- Interactive mode to select files to generate
- Syntax validation before file creation
- Support for non-Python files
- Direct LLM API integration

## Contributing
Feel free to:
- Submit issues for bugs or feature requests
- Create pull requests with improvements
- Share examples of successful LLM prompts
- Suggest format improvements

## License
MIT License - feel free to use, modify, and distribute.

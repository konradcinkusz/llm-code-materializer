# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="llm-code-materializer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to materialize code from LLM responses and collect Python projects into LLM-friendly format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/llm-code-materializer",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'llm-collect=llm_code_materializer.collector:main',
            'llm-generate=llm_code_materializer.generator:main',
        ],
    },
    install_requires=[
        # Add any required dependencies here
    ],
)
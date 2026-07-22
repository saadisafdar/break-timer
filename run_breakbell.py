"""Standalone entry point for PyInstaller.

cli.py uses a relative import (`from .app import ...`), which breaks when
PyInstaller/Python runs it directly as a top-level script ("attempted
relative import with no known parent package"). This wrapper imports the
installed breakbell package normally instead, so PyInstaller can freeze
it into a working executable.
"""
from breakbell.cli import main

if __name__ == "__main__":
    main()

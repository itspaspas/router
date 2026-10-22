"""Thin wrapper: run from the repository root after `pip install -e .`."""
from gateway.probe import discover_main

if __name__ == "__main__":
    discover_main()

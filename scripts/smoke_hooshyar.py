"""Thin wrapper: run from the repository root after `pip install -e .`."""
from gateway.probe import smoke_main

if __name__ == "__main__":
    smoke_main()

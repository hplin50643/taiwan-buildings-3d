"""Rebuild this release in an isolated output directory."""
import sys
sys.dont_write_bytecode=True
from export_display_webp import cli
if __name__=="__main__":cli(rebuild=True)

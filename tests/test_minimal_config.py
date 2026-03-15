# tests/test_simple.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spion.config import configure, get_config, LogLevel

def test_config():
    configure(show_timestamp=False, color_enabled=False)
    assert get_config('show_timestamp') is False
    assert get_config('color_enabled') is False
    print("✅ test_config passed")

if __name__ == "__main__":
    test_config()
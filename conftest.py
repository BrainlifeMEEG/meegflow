import sys
from pathlib import Path

# Make the src layout importable without needing `pip install -e .`
sys.path.insert(0, str(Path(__file__).parent / "src"))

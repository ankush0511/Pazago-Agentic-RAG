import patch_sqlite
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.streamlit_app import main

if __name__ == "__main__":
    main()
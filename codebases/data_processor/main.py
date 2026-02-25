import sys
import os

# Ensure the root of the data_processor is in sys.path
# This allows 'import app' to work correctly from within the app package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import main

if __name__ == "__main__":
    main()

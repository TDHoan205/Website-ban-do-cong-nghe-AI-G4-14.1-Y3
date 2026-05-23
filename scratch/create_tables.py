import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Data.database import engine, Base
import Models  # This imports all models and registers them with Base.metadata

print("Creating tables if they don't exist...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")

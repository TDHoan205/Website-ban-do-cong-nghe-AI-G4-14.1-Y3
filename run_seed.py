from Data.database import engine
from sqlalchemy import text

def run_seed():
    print("Reading seed_data.sql...")
    with open("SQL/seed_data.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    # Split by GO and execute each block
    statements = sql.split("GO")
    
    with engine.connect() as conn:
        for statement in statements:
            if statement.strip():
                try:
                    conn.execute(text(statement))
                except Exception as e:
                    print(f"Error executing statement: {e}")
        conn.commit()
    print("Seed data executed successfully.")

if __name__ == '__main__':
    run_seed()

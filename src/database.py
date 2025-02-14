import sqlite3

DB_PATH = "data/database/vaccination_records.db"

def create_database():
    """Creates an SQLite database and table for vaccination records."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vaccination_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name TEXT,
            bcg_date TEXT,
            opv_0_date TEXT,
            opv_1_date TEXT,
            opv_2_date TEXT,
            opv_3_date TEXT,
            opv_4_date TEXT,
            pcv_1_date TEXT,
            pcv_2_date TEXT,
            pcv_3_date TEXT,
            dpt_hepb_hib_1_date TEXT,
            dpt_hepb_hib_2_date TEXT,
            dpt_hepb_hib_3_date TEXT,
            measles_1_date TEXT,
            measles_2_date TEXT,
            rota_1_date TEXT,
            rota_2_date TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database and table created successfully.")

if __name__ == "__main__":
    create_database()

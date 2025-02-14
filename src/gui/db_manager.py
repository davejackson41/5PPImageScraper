import sqlite3
import os
import logging
from tkinter import messagebox

DB_PATH = "data/database/vaccination_records.db"

# Set up logging
LOG_FILE = "logs/gui_debug.log"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


def migrate_database():
    """Migrate database to add missing 'extracted_text' column without losing data."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if extracted_text column already exists
        cursor.execute("PRAGMA table_info(vaccination_records);")
        columns = [col[1] for col in cursor.fetchall()]

        if "extracted_text" not in columns:
            logging.info("🛠️ Adding missing 'extracted_text' column...")
            cursor.execute("ALTER TABLE vaccination_records ADD COLUMN extracted_text TEXT;")
            conn.commit()
            logging.info("✅ Column added successfully!")
        else:
            logging.info("✅ 'extracted_text' column already exists.")

        conn.close()

    except Exception as e:
        logging.error(f"❌ Database Migration Failed: {e}")
        messagebox.showerror("Migration Error", f"Failed to update the database schema!\n{e}")

# Ensure schema is correct
migrate_database()


def insert_new_record(image_name, extracted_text_path):
    """Insert a new vaccination record into the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Read extracted text
        with open(extracted_text_path, "r") as file:
            extracted_text = file.read()

        # Save to database
        cursor.execute("""
            INSERT INTO vaccination_records (image_name, extracted_text) 
            VALUES (?, ?)""", (image_name, extracted_text))
        conn.commit()
        conn.close()

        logging.info(f"✅ Successfully inserted record: {image_name}")
        messagebox.showinfo("Success", f"New record added: {image_name}")

    except sqlite3.IntegrityError:
        logging.warning(f"⚠️ Record already exists: {image_name}")
        messagebox.showwarning("Duplicate", f"Record for {image_name} already exists.")
    
    except Exception as e:
        logging.error(f"❌ Database Error: {e}")
        messagebox.showerror("Database Error", f"Failed to save record!\n\n{e}")


def fetch_all_records():
    """Fetch all vaccination records from the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, image_name FROM vaccination_records ORDER BY id DESC")
        records = cursor.fetchall()
        conn.close()

        if not records:
            logging.info("ℹ️ No records found in the database.")
        
        return records

    except Exception as e:
        logging.error(f"❌ Error fetching records: {e}")
        return []
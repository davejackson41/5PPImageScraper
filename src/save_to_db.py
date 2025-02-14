import sqlite3
import re
import os

DB_PATH = "data/database/vaccination_records.db"
OCR_TEXT_PATH = "data/extracted_text/extracted_1713782940159.txt"

def extract_dates(text):
    """Extracts vaccination dates from OCR text using regex."""
    date_pattern = r"(\d{2}/\d{2}/\d{2})"  # Matches date format (DD/MM/YY)
    return re.findall(date_pattern, text)

def parse_vaccination_data(text):
    """Parses OCR extracted text and maps it to the database fields."""
    extracted_dates = extract_dates(text)
    fields = [
        "bcg_date", "opv_0_date", "opv_1_date", "opv_2_date", "opv_3_date",
        "opv_4_date", "pcv_1_date", "pcv_2_date", "pcv_3_date",
        "dpt_hepb_hib_1_date", "dpt_hepb_hib_2_date", "dpt_hepb_hib_3_date",
        "measles_1_date", "measles_2_date", "rota_1_date", "rota_2_date"
    ]

    # Ensure we don't exceed the expected field count
    data_dict = {field: extracted_dates[i] if i < len(extracted_dates) else None for i, field in enumerate(fields)}
    
    return data_dict

def insert_data(image_name, text):
    """Inserts parsed OCR data into the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    data = parse_vaccination_data(text)

    cursor.execute('''
        INSERT INTO vaccination_records (image_name, bcg_date, opv_0_date, opv_1_date, opv_2_date, opv_3_date, opv_4_date,
                                         pcv_1_date, pcv_2_date, pcv_3_date, dpt_hepb_hib_1_date, dpt_hepb_hib_2_date,
                                         dpt_hepb_hib_3_date, measles_1_date, measles_2_date, rota_1_date, rota_2_date)
        VALUES (:image_name, :bcg_date, :opv_0_date, :opv_1_date, :opv_2_date, :opv_3_date, :opv_4_date,
                :pcv_1_date, :pcv_2_date, :pcv_3_date, :dpt_hepb_hib_1_date, :dpt_hepb_hib_2_date,
                :dpt_hepb_hib_3_date, :measles_1_date, :measles_2_date, :rota_1_date, :rota_2_date)
    ''', {**data, "image_name": image_name})

    conn.commit()
    conn.close()
    print(f"✅ Data inserted into database for {image_name}")

if __name__ == "__main__":
    # Read OCR extracted text
    with open(OCR_TEXT_PATH, "r") as file:
        ocr_text = file.read()

    image_name = os.path.basename(OCR_TEXT_PATH).replace(".txt", "")

    insert_data(image_name, ocr_text)

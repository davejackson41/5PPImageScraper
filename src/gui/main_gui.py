import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sqlite3
import logging
from PIL import Image, ImageTk

# Fix Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gui.image_processor import preprocess_image, extract_text_from_image
from gui.db_manager import insert_new_record, fetch_all_records

# Database Path
DB_PATH = "data/database/vaccination_records.db"
IMAGE_DIR = "data/images/vaccination_cards/"

# Set up logging
LOG_FILE = "logs/gui_debug.log"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


class VaccinationReviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vaccination Card Review & Edit")
        self.root.geometry("1000x600")

        logging.info("✅ GUI started.")
        self.setup_ui()
        self.update_record_dropdown()

    def setup_ui(self):
        """Initialize the GUI layout."""
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, fill=tk.X)

        tk.Button(top_frame, text="Load New Image", command=self.load_new_image, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(top_frame, text="Save Changes", command=self.save_record, font=("Arial", 12), bg="green", fg="white").pack(side=tk.LEFT, padx=10)

        self.record_var = tk.StringVar()
        self.record_dropdown = ttk.Combobox(top_frame, textvariable=self.record_var, state="readonly")
        self.record_dropdown.pack(side=tk.RIGHT, padx=10)
        self.record_dropdown.bind("<<ComboboxSelected>>", lambda e: self.load_record(self.record_var.get()))

        # Main Frame for Image and Data
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Left Panel: Image Display
        left_panel = tk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        self.image_label = tk.Label(left_panel)
        self.image_label.pack()

        # Right Panel: Extracted Text Fields
        self.data_frame = tk.Frame(main_frame)
        self.data_frame.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)

    def load_new_image(self):
        """Load new image, preprocess it, extract text, and store in DB."""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if not file_path:
            return

        filename = os.path.basename(file_path)
        save_path = os.path.join(IMAGE_DIR, filename)
        os.system(f"cp '{file_path}' '{save_path}'")

        logging.info(f"📷 New image loaded: {filename}")

        # Process Image & Run OCR
        processed_path = preprocess_image(save_path)
        extracted_text_path = extract_text_from_image(processed_path)

        if extracted_text_path:
            insert_new_record(filename, extracted_text_path)
            messagebox.showinfo("✅ Success", f"Image processed and OCR extracted for: {filename}")

        self.update_record_dropdown()
        self.load_record(f"1 - {filename}")  # Auto-load the new image

    def update_record_dropdown(self):
        """Fetch all processed records and update dropdown with all images."""
        records = fetch_all_records()
        
        if records:
            self.record_dropdown["values"] = [f"{rec[0]} - {rec[1]}" for rec in records]
            if len(records) > 0:
                self.record_dropdown.current(0)  # Auto-select first record
                messagebox.showinfo("Records Loaded", f"{len(records)} records available.")

        logging.info(f"🔄 Updated record dropdown. {len(records)} records loaded.")

    def load_record(self, record_info):
        """Load a processed record from the database and display the image + extracted text."""
        if not record_info:
            return

        record_id, image_name = record_info.split(" - ")
        logging.info(f"📄 Loading record ID: {record_id} (Image: {image_name})")

        try:
            # Fetch the record data from the database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vaccination_records WHERE id = ?", (record_id,))
            record = cursor.fetchone()
            conn.close()

            if not record:
                logging.warning(f"⚠️ Record ID {record_id} not found.")
                messagebox.showerror("Error", "Record not found.")
                return

            # Load and display the image
            self.image_path = self.find_image(image_name)
            if self.image_path:
                logging.info(f"✅ Image found: {self.image_path}")
                img = Image.open(self.image_path)
                img = img.resize((350, 350), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                self.image_label.config(image=img)
                self.image_label.image = img
            else:
                logging.warning(f"⚠️ Image file not found: {image_name}")
                messagebox.showwarning("Warning", f"Image file not found: {image_name}")

            # Load extracted text fields
            field_labels = [
                "BCG Date", "OPV 0 Date", "OPV 1 Date", "OPV 2 Date", "OPV 3 Date",
                "OPV 4 Date", "PCV 1 Date", "PCV 2 Date", "PCV 3 Date",
                "DPT-HepB-Hib 1 Date", "DPT-HepB-Hib 2 Date", "DPT-HepB-Hib 3 Date",
                "Measles 1 Date", "Measles 2 Date", "Rota 1 Date", "Rota 2 Date"
            ]

            self.entry_fields = []
            for i, label_text in enumerate(field_labels):
                tk.Label(self.data_frame, text=label_text, font=("Arial", 10, "bold")).grid(row=i, column=0, padx=5, pady=5, sticky="w")
                entry = tk.Entry(self.data_frame, width=20)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entry.insert(0, record[i + 2] if record[i + 2] else "")
                self.entry_fields.append(entry)

            logging.info(f"✅ Successfully loaded record {record_id} from database.")

        except Exception as e:
            logging.error(f"❌ Error loading record: {e}")

    def find_image(self, image_name):
        """Find the original image file for the given vaccination record."""
        possible_paths = [
            os.path.join(IMAGE_DIR, f"{image_name}"),
            os.path.join(IMAGE_DIR, f"{image_name}.jpg"),
            os.path.join(IMAGE_DIR, f"{image_name}.png")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logging.info(f"✅ Found image: {path}")
                return path

        logging.warning(f"⚠️ Image file not found: {image_name}")
        return None

    def save_record(self):
        """Save manually corrected data to the database"""
        messagebox.showinfo("Save", "Feature not implemented yet.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VaccinationReviewApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sqlite3
import os
import logging
from PIL import Image, ImageTk

# Set up logging
LOG_FILE = "logs/gui_debug.log"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Database Path
DB_PATH = "data/database/vaccination_records.db"

class VaccinationReviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vaccination Card Review & Edit")
        self.root.geometry("1000x600")

        logging.info("GUI started.")

        # Top Buttons
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10, fill=tk.X)

        tk.Button(top_frame, text="Load New Image", command=self.load_new_image, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(top_frame, text="Save Changes", command=self.save_record, font=("Arial", 12), bg="green", fg="white").pack(side=tk.LEFT, padx=10)

        # Dropdown for Viewing Processed Cards
        self.record_var = tk.StringVar()
        self.record_dropdown = ttk.Combobox(top_frame, textvariable=self.record_var, state="readonly")
        self.record_dropdown.pack(side=tk.RIGHT, padx=10)
        self.record_dropdown.bind("<<ComboboxSelected>>", lambda e: self.load_record(self.record_var.get()))

        self.update_record_dropdown()

        # Main Frame (Image Left / Data Right)
        main_frame = tk.Frame(root)
        main_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Image Panel (Left)
        self.image_label = tk.Label(main_frame)
        self.image_label.pack(side=tk.LEFT, padx=10, expand=True)

        # Data Panel (Right)
        self.data_frame = tk.Frame(main_frame)
        self.data_frame.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)

    def update_record_dropdown(self):
        """Fetch all processed records and update the dropdown."""
        logging.info("Updating record dropdown.")
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, image_name FROM vaccination_records ORDER BY id DESC")
            records = cursor.fetchall()
            conn.close()

            if records:
                self.record_dropdown["values"] = [f"{rec[0]} - {rec[1]}" for rec in records]
                self.record_dropdown.current(0)
                logging.info(f"Loaded {len(records)} records into dropdown.")
        except Exception as e:
            logging.error(f"Error updating dropdown: {e}")

    def load_new_image(self):
        """Open a file dialog to select a new vaccination card image for processing."""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if not file_path:
            return

        filename = os.path.basename(file_path)
        save_path = f"data/images/vaccination_cards/{filename}"
        os.system(f"cp '{file_path}' '{save_path}'")

        logging.info(f"New image loaded: {filename}")

        messagebox.showinfo("Success", f"Image loaded: {filename}\nRun OCR processing separately.")
        self.update_record_dropdown()

    def load_record(self, record_info):
        """Load a processed record from the database"""
        if not record_info:
            return

        record_id, image_name = record_info.split(" - ")
        logging.info(f"Loading record ID: {record_id} (Image: {image_name})")

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vaccination_records WHERE id = ?", (record_id,))
            record = cursor.fetchone()
            conn.close()

            if not record:
                logging.warning(f"Record ID {record_id} not found.")
                messagebox.showerror("Error", "Record not found.")
                return

            # Load and display the image
            self.image_path = self.find_image(image_name)
            if self.image_path:
                logging.info(f"Image found: {self.image_path}")
                img = Image.open(self.image_path)
                img = img.resize((350, 350), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                self.image_label.config(image=img)
                self.image_label.image = img
            else:
                logging.warning(f"Image file not found for record: {image_name}")
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

        except Exception as e:
            logging.error(f"Error loading record: {e}")

    def find_image(self, image_name):
        """Find an image file for the given vaccination record."""
        possible_paths = [
            f"data/images/vaccination_cards/{image_name}.jpg",
            f"data/images/vaccination_cards/processed_{image_name}.jpg",
            f"data/images/vaccination_cards/{image_name}.png"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def save_record(self):
        """Save manually corrected data to the database"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            field_names = [
                "bcg_date", "opv_0_date", "opv_1_date", "opv_2_date", "opv_3_date",
                "opv_4_date", "pcv_1_date", "pcv_2_date", "pcv_3_date",
                "dpt_hepb_hib_1_date", "dpt_hepb_hib_2_date", "dpt_hepb_hib_3_date",
                "measles_1_date", "measles_2_date", "rota_1_date", "rota_2_date"
            ]

            data = {field_names[i]: self.entry_fields[i].get() for i in range(len(field_names))}
            data["id"] = self.record_var.get().split(" - ")[0]

            cursor.execute(f"""
                UPDATE vaccination_records
                SET {", ".join([f"{key} = :{key}" for key in field_names])}
                WHERE id = :id
            """, data)

            conn.commit()
            conn.close()
            logging.info(f"Changes saved for record ID {data['id']}")
            messagebox.showinfo("Success", "Changes saved successfully.")
        except Exception as e:
            logging.error(f"Error saving record: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VaccinationReviewApp(root)
    root.mainloop()
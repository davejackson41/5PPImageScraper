# 5PP Image Scraper

## Project Overview
The **5PP Image Scraper** is a local application designed to extract handwritten text from photographed images of vaccination cards. These images are captured by field volunteers, and the extracted data is structured and stored in a SQLite database. The project leverages the **OpenAI stack** to improve extraction accuracy over time through machine learning, incorporating a **human-in-the-loop** correction mechanism.

## Project Objectives
1. **Automate Data Extraction**: Convert handwritten text from images into structured digital records.
2. **Database Integration**: Store extracted data in a **SQLite** database, mapping it to appropriate tables.
3. **AI Learning & Improvement**: Utilize OpenAI models to enhance OCR capabilities through **feedback and human corrections**.
4. **User Interface for Human Review**: Provide an interface for manual validation and correction of extracted data.
5. **Local Execution on macOS**: Ensure full compatibility with macOS, using **Terminal and Sublime Text**.

## Project Scope
### In-Scope
- Processing two types of forms:
  - **Child Particulars** (e.g., name, date of birth, guardian details)
  - **Vaccination Records** (e.g., vaccine name, date, batch number)
- **Image-to-text extraction** using AI-powered OCR.
- **Data validation & correction interface**.
- **Storage in SQLite database** with **image-data linking**.
- **Improvement of AI model based on user corrections**.

### Out-of-Scope
- Cloud-based storage or web applications (local execution only).
- Processing of non-vaccination documents.
- Mobile application development.

## Key Deliverables
1. **Image Processing Pipeline**
   - Load and pre-process images.
   - Perform OCR using OpenAI models.
   - Parse and map extracted text to the data model.
2. **SQLite Database Structure**
   - Tables for **Child Particulars** and **Vaccination Records**.
   - Unique ID mapping between images and extracted data.
3. **Human-in-the-Loop Correction Interface**
   - Allow manual validation and correction.
   - Feedback loop to enhance AI model performance.
4. **AI Model Integration & Learning**
   - Implement OpenAI-based text extraction.
   - Improve accuracy based on human-reviewed edits.
5. **Project Documentation**
   - Installation and usage guide.
   - Ongoing enhancement plan.

## Success Criteria
- **80%+ accuracy in text extraction** after iterative model improvements.
- **Seamless integration of SQLite storage** with structured form data.
- **Efficient human validation process** with easy corrections.
- **Functional local execution on macOS** without dependencies on cloud services.

## Repository Structure
📂 **Root Directory: **  
- 📂  → Stores **images, extracted text, and SQLite database**  
- 📂  → **Main Python scripts** for processing images, AI learning, and UI  
- 📂  → Tracks **OCR errors & debugging information**  
- 📂  → Unit tests for **OCR extraction accuracy**  
- 📂  → Documentation & **API references**  
- 📂  → AI **training data & fine-tuned OCR models**  
- 📂  → Utility scripts (e.g., **GitHub commits, database backups**)  

## Contribution Guidelines
- **Step-by-step execution (One task at a time)**
- **Validate results before committing**
- **Follow structured commit messages**
- **Use logging for debugging & tracking AI performance**

## License
This project is licensed under **[MIT License](LICENSE)**.


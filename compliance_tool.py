import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import re
import os
from pypdf import PdfReader

# --- THE LOGIC (Same "Operations Intelligence" as before) ---
def scan_pdf(file_path):
    text = ""
    issues = []
    
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    except Exception as e:
        return [f"Error reading file: {str(e)}"]

    # Rule 1: Check for Liability/Risk keywords
    # regex: (?i) means case-insensitive
    if re.search(r"(?i)liability|indemnity|lawsuit", text):
        issues.append("Flag: Liability Clause Found")

    # Rule 2: Check for missing info placeholders (e.g., underscores ________)
    if re.search(r"_{4,}", text):
        issues.append("Flag: Missing Information (Blank Lines)")
        
    # Rule 3: Check for Placeholder Text
    if "[CLIENT NAME]" in text or "[DATE]" in text:
        issues.append("CRITICAL: Placeholder Text Found")

    return issues if issues else ["OK - Clean"]

# --- THE APP INTERFACE (Tkinter - Built into Python 3.14) ---
def run_audit():
    # 1. Open file selector
    filepaths = filedialog.askopenfilenames(
        title="Select Contracts to Audit",
        filetypes=[("PDF Files", "*.pdf")]
    )
    
    if not filepaths:
        return

    results = []
    
    # 2. Update Status Label
    lbl_status.config(text=f"Processing {len(filepaths)} files...")
    window.update()

    # 3. Loop through files
    for filepath in filepaths:
        filename = os.path.basename(filepath)
        flags = scan_pdf(filepath)
        
        # Join multiple flags with a semicolon
        status_string = "; ".join(flags)
        results.append([filename, status_string])

    # 4. Save Report
    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="Compliance_Report.csv",
        title="Save Audit Report"
    )
    
    if save_path:
        with open(save_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Filename", "Audit Status"]) # Header
            writer.writerows(results) # Data
        
        lbl_status.config(text="Done! Report Saved.")
        messagebox.showinfo("Success", f"Audited {len(filepaths)} files.\nReport saved successfully.")
    else:
        lbl_status.config(text="Save cancelled.")

# --- GUI SETUP ---
window = tk.Tk()
window.title("Legal Compliance Automator (v1)")
window.geometry("400x250")

# Styling
lbl_title = tk.Label(window, text="⚖️ Compliance Sentinel", font=("Arial", 16, "bold"))
lbl_title.pack(pady=20)

lbl_instr = tk.Label(window, text="Select PDF contracts to scan for\nrisk clauses and missing signatures.", justify="center")
lbl_instr.pack(pady=10)

btn_run = tk.Button(window, text="Select Files & Run Audit", command=run_audit, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
btn_run.pack(pady=20)

lbl_status = tk.Label(window, text="Ready", fg="gray")
lbl_status.pack(pady=5)

window.mainloop()
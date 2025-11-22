import os
import random
from fpdf import FPDF

# --- CONFIGURATION ---
OUTPUT_FOLDER = "test_contracts"
FILE_COUNT = 50

# --- DATA BANKS (The Random Ingredients) ---
TITLES = [
    "Independent Contractor Agreement",
    "Non-Disclosure Agreement (NDA)",
    "Master Service Agreement",
    "Vendor Supply Contract",
    "Software Licensing Agreement",
    "Employment Contract"
]

CLIENTS = [
    "Acme Industries", "Stark Enterprises", "Wayne Corp", 
    "Cyberdyne Systems", "Massive Dynamic", "Hooli Inc."
]

RISK_PHRASES = [
    "INDEMNIFICATION: The Vendor agrees to indemnify and hold harmless the Client for all damages.",
    "LIMITATION OF LIABILITY: The Client shall not be liable for any damages exceeding $1.00.",
    "The Vendor assumes full LIABILITY for all operational failures.",
    "In the event of a lawsuit, the Vendor pays all legal fees."
]

SAFE_PHRASES = [
    "The Service Provider agrees to perform duties in a professional manner.",
    "Payment terms are Net-30 days from receipt of invoice.",
    "This agreement may be terminated with 30 days written notice.",
    "All intellectual property created remains the property of the Client."
]

# --- SETUP FOLDER ---
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# --- PDF GENERATOR FUNCTION ---
def generate_random_contract(index):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # 1. Roll the dice to decide the "Type" of contract
    # Roll 1-10: 
    #   1-6 = Clean (60%)
    #   7-8 = Risky (20%)
    #   9-10 = Incomplete/Missing Info (20%)
    roll = random.randint(1, 10)
    
    title = random.choice(TITLES)
    client = random.choice(CLIENTS)
    content = ""
    
    # HEADER
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, title, ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    
    # LOGIC: Build the content based on the dice roll
    if roll <= 6: 
        # === CLEAN CONTRACT ===
        status = "Clean"
        content += f"Date: 11/{random.randint(1, 30)}/2025\n\n"
        content += f"Between: {client} and The Vendor.\n\n"
        content += "TERMS:\n" + random.choice(SAFE_PHRASES) + "\n" + random.choice(SAFE_PHRASES)
        content += "\n\nSigned: _________________ (John Doe)"
        
    elif roll <= 8:
        # === RISKY CONTRACT ===
        status = "Risky"
        content += f"Date: 11/{random.randint(1, 30)}/2025\n\n"
        content += f"Between: {client} and The Vendor.\n\n"
        content += "TERMS:\n" + random.choice(SAFE_PHRASES) + "\n"
        content += "\n*** " + random.choice(RISK_PHRASES) + " ***\n" # Insert the risk
        content += "\nSigned: _________________ (John Doe)"

    else:
        # === INCOMPLETE CONTRACT ===
        status = "Incomplete"
        content += "Date: __________ (To be filled)\n\n" # Missing Date
        content += "Between: [CLIENT NAME] and The Vendor.\n\n" # Placeholder Text
        content += "TERMS:\n" + random.choice(SAFE_PHRASES) + "\n"
        content += "\nSignature: _______________________" # Missing Name
        content += "\n(Sign above)"

    # Write content to PDF
    pdf.multi_cell(0, 10, content)
    
    # Save file
    filename = f"Contract_{index:03d}_{status}.pdf"
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    pdf.output(filepath)
    
    return filename, status

# --- EXECUTION LOOP ---
if __name__ == "__main__":
    print(f"--- Generating {FILE_COUNT} Random Contracts ---")
    
    for i in range(1, FILE_COUNT + 1):
        name, type_generated = generate_random_contract(i)
        print(f"[{i}/{FILE_COUNT}] Created {name}")
        
    print("-------------------------------------------")
    print(f"✅ Done! {FILE_COUNT} files are waiting in the '{OUTPUT_FOLDER}' folder.")
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io
import fitz
import re

app = FastAPI()

class AadhaarData(BaseModel):
    aadhaar_number: str = ""
    name: str = ""
    guardian_name: str = ""
    dob: str = ""
    gender: str = ""
    address: str = ""
    vtc: str = ""
    po: str = ""
    sub_district: str = ""
    district: str = ""
    state: str = ""
    pincode: str = ""
    phone: str = ""

def extract_text_from_image(image: Image.Image) -> str:
    custom_config = r'--oem 3 --psm 6'
    return pytesseract.image_to_string(image, config=custom_config, lang='eng')

def extract_text_from_pdf(pdf_bytes: bytes, password: str = None) -> str:
    text = ""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    if doc.needs_pass and password:
        doc.authenticate(password)
    
    for page in doc:
        text += page.get_text("text")
    return text

def parse_aadhaar_details(text: str) -> AadhaarData:
    data = AadhaarData()
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Extract Aadhaar Number
    aadhaar_match = re.search(r'\b(\d{4}\s\d{4}\s\d{4})\b', text)
    if aadhaar_match:
        data.aadhaar_number = aadhaar_match.group(1)

    # Extract Guardian Name (S/o, C/o, D/o) and remove from address
    guardian_match = re.search(r'(S/o|C/o|D/o)[.:]?\s*([A-Za-z\s]+)', text, re.IGNORECASE)
    if guardian_match:
        data.guardian_name = guardian_match.group(2).strip()
        text = text.replace(guardian_match.group(0), '')  # Remove guardian from text

    # Extract Name (first meaningful name-like line after guardian name)
    for line in lines:
        if re.match(r'^[A-Za-z\s]+$', line) and len(line.split()) > 1 and not re.search(r'(S/o|C/o|D/o)', line, re.IGNORECASE):
            data.name = line
            break

    # Improved DOB Extraction
    dob_match = re.search(r'(DOB|Date of Birth|D\.O\.B)[:\s]*?(\d{1,2}[/-]\d{1,2}[/-]\d{4})', text, re.IGNORECASE)
    if dob_match:
        data.dob = dob_match.group(2).replace('-', '/')

    # Extract Gender
    gender_match = re.search(r'\b(Male|Female|Transgender|M|F|T)\b', text, re.IGNORECASE)
    if gender_match:
        data.gender = gender_match.group(1).capitalize()

    # Extract Address (excluding Guardian Name, PO, District, State, Pincode, Aadhaar Number)
    address_match = re.search(r'(?i)address[:\s]*(.*?)(?=\nVTC|\nPO|\nSub District|\nDistrict|\nState|\n\d{6}|\nVID|\nDigitally|$)', text, re.DOTALL)
    if address_match:
        address_text = address_match.group(1).strip()
        address_text = re.sub(r'(S/o|C/o|D/o)[.:]?\s*[A-Za-z\s]+', '', address_text, flags=re.IGNORECASE)  # Remove guardian name
        address_text = re.sub(r'\b\d{4}\s\d{4}\s\d{4}\b', '', address_text)  # Remove Aadhaar Number
        address_text = re.sub(r'\b(VTC|PO|Sub District|District|State|\d{6})[:\s]*.*', '', address_text, flags=re.IGNORECASE)  # Remove other fields
        address_text = re.sub(r'(?i)\b(dist|state)\b.*', '', address_text)  # Remove "DIST" and "STATE" words
        address_text = re.sub(r'\n+', ' ', address_text).strip()  # Remove newlines
        address_text = re.sub(r'\s+', ' ', address_text).strip()  # Normalize spaces
        data.address = address_text
    
    vtc_match = re.search(r'VTC[:\s]*(.*)', text, re.IGNORECASE)
    if vtc_match:
        data.vtc = vtc_match.group(1).strip()
    
    po_match = re.search(r'PO[:\s]*(.*)', text, re.IGNORECASE)
    if po_match:
        data.po = po_match.group(1).strip()
    
    sub_district_match = re.search(r'Sub District[:\s]*(.*)', text, re.IGNORECASE)
    if sub_district_match:
        data.sub_district = sub_district_match.group(1).strip()
    
    district_match = re.search(r'District[:\s]*(.*)', text, re.IGNORECASE)
    if district_match:
        data.district = district_match.group(1).strip()
    
    state_match = re.search(r'State[:\s]*(.*)', text, re.IGNORECASE)
    if state_match:
        data.state = state_match.group(1).strip()

    pincode_match = re.search(r'\b(\d{6})\b', text)
    if pincode_match:
        data.pincode = pincode_match.group(1)

    phone_match = re.search(r'\b(\d{10})\b', text)
    if phone_match:
        data.phone = phone_match.group(1)

    return data

@app.post("/extract")
async def extract_aadhaar(file: UploadFile = File(...), password: str = Form(None)):
    contents = await file.read()
    text = ""
    
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(contents, password)
    else:
        image = Image.open(io.BytesIO(contents))
        text = extract_text_from_image(image)
    
    aadhaar_data = parse_aadhaar_details(text)
    return aadhaar_data

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

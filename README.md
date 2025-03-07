# Aadhaar OCR Extraction API

## Overview
This project provides a **FastAPI-based Aadhaar OCR Extraction API** that allows users to upload Aadhaar card images or PDFs (including password-protected PDFs) to extract structured details. The extracted information includes:

- Aadhaar Number
- Name
- Guardian Name (S/o, C/o, D/o, W/o)
- Date of Birth (DOB)
- Gender
- Address (Standardized)
- Village/Town/City (VTC)
- Post Office (PO)
- Sub-District
- District
- State
- Pincode
- Phone Number (if available)

The API utilizes **Tesseract OCR**, **PyMuPDF (fitz)**, and **pdf2image** for text extraction and **regex parsing** to structure the extracted details.

---

## Features
- Supports **both images (JPG, PNG) and PDFs**
- Handles **password-protected PDFs**
- Uses **Tesseract OCR** for image text extraction
- Uses **PyMuPDF (fitz)** for PDF text extraction
- **Regex-based parsing** ensures structured and standardized output
- **FastAPI framework** for easy API deployment

---

## Installation
Ensure you have **Python 3.8+** installed. Then, install the required dependencies:

```sh
pip install fastapi uvicorn pytesseract pdf2image pillow pymupdf
```

You may also need to install **Tesseract OCR** separately.

For Windows, download it from: [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

For Linux, install using:
```sh
sudo apt install tesseract-ocr
```

For Mac (via Homebrew):
```sh
brew install tesseract
```

---

## Running the API
Start the FastAPI server using Uvicorn:

```sh
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at `http://127.0.0.1:8000`

---

## API Endpoints
### 1. Extract Aadhaar Details
**Endpoint:**
```
POST /extract
```

**Request Parameters:**
- `file`: Aadhaar card file (Image or PDF)
- `password` (optional): If the PDF is password-protected, provide the password

**Example Request (cURL):**
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/extract' \
  -F 'file=@aadhaar_sample.pdf' \
  -F 'password=your_password_here'
```

**Example JSON Response:**
```json
{
  "aadhaar_number": "1234 5678 9012",
  "name": "John Doe",
  "guardian_name": "Richard Doe",
  "dob": "01/01/1980",
  "gender": "Male",
  "address": "1234, ABC Street, XYZ Town",
  "vtc": "XYZ Town",
  "po": "XYZ Post Office",
  "sub_district": "XYZ Sub-District",
  "district": "XYZ District",
  "state": "XYZ State",
  "pincode": "123456",
  "phone": "9876543210"
}
```

---

## Technologies & Libraries Used
- **Python 3.x**
- **FastAPI**
- **Tesseract OCR (`pytesseract`)**
- **PDF handling (`pdf2image`, `pymupdf` aka `fitz`)**
- **Image processing (`PIL` from `Pillow`)**
- **Regular expressions (`re` for text parsing)**
- **Uvicorn (for running FastAPI server)**

---

## Text Extraction Methods
### 1. Extracting Text from Images
- Uses **pytesseract** (Tesseract OCR) with a custom configuration:
```python
custom_config = r'--oem 3 --psm 6'
pytesseract.image_to_string(image, config=custom_config, lang='eng')
```

### 2. Extracting Text from PDFs
- Uses **PyMuPDF (fitz)** to read PDF text.
- Handles **password-protected PDFs**:
```python
doc = fitz.open(stream=pdf_bytes, filetype="pdf")
if doc.needs_pass and password:
    doc.authenticate(password)
```

---

## Regex-Based Data Parsing
### Aadhaar Number
```python
aadhaar_match = re.search(r'\b(\d{4}\s\d{4}\s\d{4})\b', text)
```

### Guardian Name (S/o, C/o, D/o, W/o)
```python
guardian_match = re.search(r'(S/o|C/o|D/o|W/o)[.:]?\s*([A-Za-z\s]+)', text, re.IGNORECASE)
```

### Date of Birth (DOB)
```python
dob_match = re.search(r'(DOB|Date of Birth|D\.O\.B)[:\s]*?(\d{1,2}[/\-]\d{1,2}[/\-]\d{4})', text, re.IGNORECASE)
```

### Gender
```python
gender_match = re.search(r'\b(Male|Female|Transgender|M|F|T)\b', text, re.IGNORECASE)
```

### Address Extraction (Removing Unwanted Elements)
```python
address_text = re.sub(r'(S/o|C/o|D/o|W/o)[.:]?\s*[A-Za-z\s]+', '', address_text, flags=re.IGNORECASE)
address_text = re.sub(r'\b\d{4}\s\d{4}\s\d{4}\b', '', address_text)  # Remove Aadhaar Number
address_text = re.sub(r'(?i)\b(dist|state)\b.*', '', address_text)
address_text = re.sub(r'\n+', ' ', address_text).strip()
address_text = re.sub(r'\s+', ' ', address_text).strip()
```

---

## Testing the API
You can test the API using **Postman** or **cURL**.

- **Postman**:
  1. Select `POST` method.
  2. Enter `http://127.0.0.1:8000/extract`.
  3. Upload a file.
  4. Click `Send`.
- **cURL**: See the example request above.

---

## Future Enhancements
- **Improve OCR accuracy** by using **Tesseract training models**.
- **Integrate Machine Learning** for more accurate name and address parsing.
- **Enhance error handling** for better user experience.

---

## License
This project is licensed under the **Apache 2.0 License**.

---

## Author
Developed by **Kumaran**

---

## Disclaimer
This tool is for **educational purposes only** and should not be used for unauthorized data extraction.

---

## Conclusion
The **Aadhaar OCR Extraction API** provides a structured way to extract Aadhaar details from images and PDFs using **FastAPI**, **Tesseract OCR**, and **Regex Parsing**. It ensures accuracy and consistency while maintaining ease of use.


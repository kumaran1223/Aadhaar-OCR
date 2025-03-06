# Aadhaar OCR API

## Overview
The Aadhaar OCR API extracts details from Aadhaar card images or PDF files using Optical Character Recognition (OCR). It supports text extraction from both scanned images and password-protected PDFs.

## Features
- Extracts key Aadhaar details such as Name, DOB, Gender, Address, etc.
- Supports both images and PDFs (including password-protected ones)
- Uses Tesseract OCR and PDF processing libraries
- Built with FastAPI for high performance
- API endpoint for easy integration

## Technologies & Libraries Used
- Python 3.x
- FastAPI
- Tesseract OCR (`pytesseract`)
- PDF handling (`pdf2image`, `pymupdf` aka `fitz`)
- Image processing (`PIL` from `Pillow`)
- Regular expressions (`re` for text parsing)
- Uvicorn (for running FastAPI server)

## Installation
### Prerequisites
Ensure you have Python installed. You also need Tesseract OCR. Install it using:
- **Windows**: Download from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- **Linux/macOS**: Install via package manager (`sudo apt install tesseract-ocr`)

### Install Dependencies
```sh
pip install fastapi uvicorn pytesseract pdf2image Pillow pymupdf
```

## Running the API
```sh
uvicorn main:app --host 127.0.0.1 --port 8000
```

## API Endpoints
### `POST /extract`
**Description**: Extracts Aadhaar details from uploaded images or PDFs.

**Request Parameters:**
- `file`: Upload Aadhaar image or PDF
- `password`: (Optional) Enter password if the PDF is locked

**Example cURL Request:**
```sh
curl -X 'POST' 'http://127.0.0.1:8000/extract' -F 'file=@aadhaar.pdf' -F 'password=1234'
```

## Testing the API
You can test the API using **Postman** or **cURL**.
- **Postman**: 
  1. Select `POST` method.
  2. Enter `http://127.0.0.1:8000/extract`.
  3. Upload a file.
  4. Click `Send`.
- **cURL**: See the example request above.

## Sample Output (JSON)
```json
{
  "aadhaar_number": "XXXX-XXXX-XXXX",
  "name": "John Doe",
  "guardian_name": "Richard Doe",
  "dob": "01/01/1990",
  "gender": "Male",
  "address": "123, Main Street, City, State, Pincode",
  "district": "District Name",
  "state": "State Name",
  "pincode": "123456",
  "phone": "9876543210"
}
```

## License
This project is licensed under the **Apache License 2.0**. See [LICENSE](LICENSE) file for details.


## Author
Developed by kumaran

---
**Disclaimer**: This tool is for educational purposes only and should not be used for unauthorized data extraction.

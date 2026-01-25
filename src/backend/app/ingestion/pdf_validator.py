from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
from pypdf.errors import PdfReadError

def validate_pdf(file: UploadFile):
    # 1. Extension check
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    try:
        # 2. Try reading PDF
        reader = PdfReader(file.file)

        # 3. Encrypted PDF check
        if reader.is_encrypted:
            raise HTTPException(
                status_code=400,
                detail="Encrypted PDFs are not supported"
            )

        # 4. Page count check
        if len(reader.pages) == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty PDF file"
            )

    except PdfReadError:
        # True corruption case
        raise HTTPException(
            status_code=400,
            detail="PDF file is corrupted or unreadable"
        )

    finally:
        file.file.seek(0)  # Reset file pointer after reading
from fastapi import UploadFile

def validate_file(file: UploadFile):
    # Check file size (e.g., max 10MB)
    if file.size > 10 * 1024 * 1024:
        raise ValueError("File size exceeds the limit of 10MB")

    # Check file type
    allowed_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        "text/plain"
    }
    if file.content_type not in allowed_types:
        raise ValueError("File type not allowed. Please upload PDF, DOCX, XLXS or TXT files.")

    return True
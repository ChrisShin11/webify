from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.file_validator import validate_file
# from app.services.document_processor import process_document

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        validate_file(file)
        # Save the file and get the file path
        file_path = await save_file(file)
        # Process the document (to be implemented)
        # await process_document(file_path)
        return {"message": "File uploaded and processed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

async def save_file(file: UploadFile) -> str:
    # Implement file saving logic here
    # Return the path where the file is saved
    pass
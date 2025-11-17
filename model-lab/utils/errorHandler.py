import logging
from fastapi import Request,HTTPException,status, UploadFile

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from PIL import Image, UnidentifiedImageError
import io
import re


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s-%(message)s")

def validate_email(email: str):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="write your email correctly"
    )

def check_email_exists(email: str, db: Session):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already exists."
        )


async def model_load_error(req:Request, excp:Exception):
    err_msg=f'model loading error {req.url}:{excp}'
    logger.error(err_msg)
    return JSONResponse(
         status_code=500,
         content={"detail":"Model Loading error,please try again after some time"}
    )

def validate_image_file(file: UploadFile) -> Image.Image:
    try:
        
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise HTTPException(status_code=415, detail="Unsupported image format.")

       
        image_bytes = file.file.read()                                        
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()
        image = Image.open(io.BytesIO(image_bytes))
        return image

    except UnidentifiedImageError:
        logger.error(f"Corrupt or unreadable image file: {file.filename}")
        raise HTTPException(status_code=400, detail="Uploaded image is corrupt or unreadable.")

async def UnhandledError(req:Request,excp:Exception ):
    err_msg=f'Unhandled error for request {req.url}:{excp}'
    logging.error(err_msg)
    return JSONResponse(
        status_code=500,
        content={"detail":"An Internal server error,please try again after some time"}
    )

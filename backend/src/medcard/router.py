from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
from fastapi import APIRouter, Depends, status

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.auth.schemas import UserRead

from src.auth.models import User
from pydantic import BaseModel

from src.doctor.models import Doctor
from src.messages.models import Message

from starlette.concurrency import run_in_threadpool

from src.auth.base_config import get_current_user
from src.doctor.base_config import get_current_doctor
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime
from src.scan.models import Scan, ScanFolder, EyeScan, SkinScan
from src.scan.schemas import ScanResponse,ScanInfo, ScanAddNew,Folder
from pydantic import BaseModel
from src.logger import logger
from src.scan.body_checker import validate_body_scan
from src.scan.ml.classification_model import get_result
from src.scan.test_support import generate_user_report
from src.doctor.models import DoctorScan
from src.scan.ml.segmnetation import png_to_base64, get_segmentation

from src.scan.ml.skin_disease_analysis import get_skin_answer
from src.scan.ml.eye_disease_analysis import get_eye_answer
import os
from src.scan.doctor_support import generate_doctor_report
from src.scan.ml.abcd_generate import get_absd_score


router = APIRouter(
    prefix="/medcard",
    tags=["Med Card"]
)

# Папка для сохранения загруженных файлов
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload")
async def upload_audio_file(audio: UploadFile = File(...), user: User|None = Depends(get_current_user)) -> JSONResponse:
    
    if audio.content_type != "audio/wav":
        return JSONResponse(
            content={"message": "Invalid file type. Please upload a WAV file."},
            status_code=400,
        )

    # Путь для сохранения файла
    file_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    
    # Сохранение файла
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    
    return JSONResponse(
        status_code=200,
        content={"message": f"File {audio.filename} uploaded successfully!"}
    )


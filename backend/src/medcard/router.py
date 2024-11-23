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
from src.medcard.scan_reader import process_image, process_image_to_json
from src.medcard.models import MedCard

router = APIRouter(
    prefix="/medcard",
    tags=["Med Card"]
)

class MedCardRead(BaseModel):
    type_analysis : str
    data : datetime
    text : str
    
UPLOAD_FOLDER = "upload_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload_document")
async def upload_and_process_file(
    file: UploadFile = File(...),
    user: User | None = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    # Проверяем, авторизован ли пользователь
    if user is None:
        return JSONResponse(
            status_code=401,
            content = {"detail" : "Unauthorized"}
        )

    # Допустимые типы файлов
    allowed_content_types = ["application/pdf", "image/jpeg", "image/png"]
    if file.content_type not in allowed_content_types:
        return JSONResponse(
            content={"detail": "Неверный тип документы. Пожалуйста загрузите PDF, JPG, или PNG файл."},
            status_code=400,
        )

    # Сохранение файла
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail":f"Ошибка сохранения файла: {e}"})

    # Препроцессинг файла
    try:
        answer = await process_image_to_json(file_path)
        data = datetime(
            int(answer["data"].split('.')[2]), 
            int(answer["data"].split('.')[1]), 
            int(answer["data"].split('.')[0]),
        ) 
        medcard = MedCard(
            user_id = user.id,
            type_analysis = answer["type_analysis"],
            data = data,
            text = answer["text"]
        )
        session.add(medcard)
        await session.commit()
        return JSONResponse(
            status_code=200,
            content={"detail": "File processed successfully!"},
        )
    except ValueError as ve:
        return JSONResponse(
            status_code=400,
            content={"detail": str(ve)},
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail":f"Error processing file: {e}"})

@router.get("/get_my_documents")
async def get_my_documents(
    user: User | None = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    
    if user is None:
        return JSONResponse(
            status_code=401,
            content = {"detail" : "Unauthorized"}
        )


    result = await session.execute(select(MedCard).where(MedCard.user_id==user.id))
    
    all_documents = [
        {
            'type_analysis' : document.type_analysis,
            'data' : document.data.isoformat() if isinstance(document.data, datetime) else document.data,
            'text' : document.text
        }
        for document in result.scalars().all()
    ]
    return JSONResponse(
        status_code=200,
        content=all_documents
    )
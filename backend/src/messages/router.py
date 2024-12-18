

from fastapi import APIRouter, Depends, status

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

from src.auth.models import User
from src.doctor.models import Doctor
from pydantic import BaseModel
from sqlalchemy import select

from src.auth.base_config import get_current_user
from src.doctor.base_config import get_current_doctor
from fastapi.responses import JSONResponse
from src.messages.schemas import MessageRead, MessageAdd
from src.messages.models import Message
from typing import Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel
from src.myredis import redis_fastapi

def format(all_messages : list[MessageRead], receivers_type : str = 'doctor'):
    answer = {}
    for message in all_messages:
        if message["receiver_type"] == receivers_type:
            if str(message["receiver_id"]) not in answer:
                answer[str(message["receiver_id"])] = [message]
            else:
                answer[str(message["receiver_id"])].append(message)
        elif message["sender_type"] == receivers_type:
            if str(message["sender_id"]) not in answer:
                answer[str(message["sender_id"])] = [message]
            else:
                answer[str(message["sender_id"])].append(message)
    return answer

router = APIRouter(
    prefix="/messages",
    tags=["Message"]
)
    
class ResponseModel(BaseModel):
    status: int
    detail: str

class ConferenceRegister(BaseModel):
    receiver_id: int 
    conference_time: datetime

class ConferenceRead(BaseModel):
    conference_time: datetime
    
    class Config:
        from_attributes = True
    

async def get_role(
    user: User = Depends(get_current_user),
    doctor: Doctor = Depends(get_current_doctor)
):
    if isinstance(doctor, JSONResponse):
        doctor = False
        pass
    if isinstance(user, JSONResponse):
        user = False
        pass
    
    if not doctor and not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Вы не авторизованы"}
        )

    elif doctor:
        return {"role" : "doctor", "uid" : doctor.id}
    else:
        return {"role" : "user", "uid" : user.id}


@router.post('/conference', response_model=MessageRead)
async def send_message(form : ConferenceRegister, info = Depends(get_role), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(info,JSONResponse):
        return info
    
    conference_time = datetime(
        form.conference_time.year, 
        form.conference_time.month, 
        form.conference_time.day, 
        form.conference_time.hour, 
        0, 0, 0,
    )  # Убираем информацию о временной зоне, если она не требуется

    # Создаем сообщение с передачей корректного объекта datetime
    message = Message(
        sender_id=info['uid'],
        sender_type=info['role'],
        receiver_id=form.receiver_id,
        receiver_type=next(role for role in ['user', 'doctor'] if role != info['role']),
        conference_time=conference_time,
        content="",
    )
    
    session.add(message)
    await session.commit()
    await session.refresh(message)
    
    if info['role'] == 'user':
        receiver = (await session.execute(select(Doctor).where(Doctor.id==message.receiver_id))).scalar_one_or_none()
    else:
        receiver = (await session.execute(select(User).where(User.id==message.receiver_id))).scalar_one_or_none()
    
    if not receiver:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Собеседник с заданным id не найден"}
        )
        
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "id": message.id,
            "sender_id": message.sender_id,
            "sender_type": message.sender_type,
            "receiver_id": message.receiver_id,
            "receiver_type": message.receiver_type,
            "receiver_name": f"{receiver.last_name} {receiver.first_name}",
            "content": message.content,
            "image_base64": message.image_base64,
            "conference_time": message.conference_time.isoformat() if isinstance(message.conference_time, datetime) else message.conference_time,
            "have_link" : message.have_link,
            "created_at": message.created_at.isoformat() if isinstance(message.created_at, datetime) else message.created_at
        }
    )
    
@router.post('/send', response_model=MessageRead)
async def send_message(form : MessageAdd, info = Depends(get_role), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(info,JSONResponse):
        return info
    
    message = Message(
        sender_id = info['uid'],
        sender_type = info['role'],
        receiver_id = form.receiver_id,
        receiver_type = next(role for role in ['user','doctor'] if role != info['role']),
        content = form.content,
        image_base64 = form.image_base64
    )
    
    session.add(message)
    await session.commit()
    await session.refresh(message)
    
    if info['role'] == 'user':
        receiver = (await session.execute(select(Doctor).where(Doctor.id==message.receiver_id))).scalar_one_or_none()
    else:
        receiver = (await session.execute(select(User).where(User.id==message.receiver_id))).scalar_one_or_none()
    
    if not receiver:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Собеседник с заданным id не найден"}
        )
        
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "id": message.id,
            "sender_id": message.sender_id,
            "sender_type": message.sender_type,
            "receiver_id": message.receiver_id,
            "receiver_type": message.receiver_type,
            "receiver_name": f"{receiver.last_name} {receiver.first_name}",
            "content": message.content,
            "image_base64": message.image_base64,
            "created_at": message.created_at.isoformat() if isinstance(message.created_at, datetime) else message.created_at
        }
    )


@router.get("/get_chats",response_model=Dict[str, List[MessageRead]])
async def get_all_chats(info : str = Depends(get_role), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(info,JSONResponse):
        return info

    all_messages = await session.execute(
        select(Message).where(
            or_(
                and_(
                    Message.sender_type == info['role'],
                    Message.sender_id == info['uid']
                ),
                and_(
                    Message.receiver_type == info['role'],
                    Message.receiver_id == info['uid']
                )
            )
        )
    )
    

        
    all_messages = [
        {
            "id": message.id,
            "sender_id": message.sender_id,
            "sender_type": message.sender_type,
            "receiver_id": message.receiver_id,
            "receiver_type": message.receiver_type,
            "content": message.content,
            "conference_time": message.conference_time.isoformat() if isinstance(message.conference_time, datetime) else message.conference_time,
            "have_link" : message.have_link,
            "abcd_score" : message.abcd_score,
            "doctor_result" : message.doctor_result,
            "image_base64": message.image_base64,
            "segmentation_base64": message.segmentation_base64,
            "created_at": message.created_at.isoformat() if isinstance(message.created_at, datetime) else message.created_at
        } 
        for message in (all_messages.scalars().all())]
    
    for message in all_messages:
        receiver_id = message['receiver_id']
        receiver_type = message['receiver_type']
        if receiver_type == 'doctor':
            receiver = (await session.execute(select(Doctor).where(Doctor.id==receiver_id))).scalar_one_or_none()
        else:
            receiver = (await session.execute(select(User).where(User.id==receiver_id))).scalar_one_or_none()
        if not receiver:
            all_messages.remove(message)
        
        if receiver:
            message['receiver_name'] = f"{receiver.last_name} {receiver.first_name}"
        else:
            message['receiver_name'] = "Unknown Receiver"

    receivers_type = next(role for role in ['user','doctor'] if role != info['role'])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=(format(all_messages=all_messages, receivers_type=receivers_type))
    )


@router.get("/get_chat/{id_}", response_model=List[MessageRead])
async def get_chat_by_id(id_ : str, info = Depends(get_role), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(info,JSONResponse):
        return info

    all_messages = await session.execute(
        select(Message).where(
            or_(
                and_(
                    Message.sender_type == info['role'],
                    Message.sender_id == info['uid']
                ),
                and_(
                    Message.receiver_type == info['role'],
                    Message.receiver_id == info['uid']
                )
            )
        )
    )

    all_messages = [
        {
            "id": message.id,
            "sender_id": message.sender_id,
            "sender_type": message.sender_type,
            "receiver_id": message.receiver_id,
            "receiver_type": message.receiver_type,
            "content": message.content,
            "conference_time": message.conference_time.isoformat() if isinstance(message.conference_time, datetime) else message.conference_time,
            "have_link" : message.have_link,
            "abcd_score" : message.abcd_score,
            "doctor_result" : message.doctor_result,
            "image_base64": message.image_base64,
            "segmentation_base64": message.segmentation_base64,
            "created_at": message.created_at.isoformat() if isinstance(message.created_at, datetime) else message.created_at
        } 
        for message in (all_messages.scalars().all())]
    
    for message in all_messages:
        receiver_id = message['receiver_id']
        receiver_type = message['receiver_type']
        if receiver_type == 'doctor':
            receiver = (await session.execute(select(Doctor).where(Doctor.id==receiver_id))).scalar_one_or_none()
        else:
            receiver = (await session.execute(select(User).where(User.id==receiver_id))).scalar_one_or_none()
        if not receiver:
            all_messages.remove(message)
            continue
        
        message['receiver_name'] = f"{receiver.last_name} {receiver.first_name}"

    receivers_type = next(role for role in ['user','doctor'] if role != info['role'])
    answer = (format(all_messages=all_messages, receivers_type=receivers_type))
    if id_ in answer:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=answer[id_]
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=[]
        )

@router.get("get_all_coference/{id_}")
async def get_all_conference(id_ : str, session: AsyncSession = Depends(get_async_session)):
    
    result = await session.execute(
        select(Message).where(Message.conference_time != None
            )
        )
    all_conference = [
        {
          "conference_time" : message.conference_time.isoformat() if isinstance(message.conference_time, datetime) else message.conference_time
        }
        for message in result.scalars().all()
    ]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=all_conference
    )
        
async def conference_updater():
    
    async for session in get_async_session():
    # Выполняем запрос с фильтрацией по conference_time
        result = await session.execute(
            select(Message).where(Message.conference_time != None)
        )

        # Извлекаем все сообщения
        all_messages = [
            Message(
                sender_id=message.sender_id,
                sender_type=message.sender_type,
                receiver_id=message.receiver_id,
                receiver_type=message.receiver_type,
                content=message.content,
                conference_time=message.conference_time,
                have_link=True  # Устанавливаем have_link в True
            )
            for message in result.scalars().all() if message.conference_time<=datetime.now(tz=timezone.utc).replace(tzinfo=None)  # Получаем все сообщения из результата запроса
        ]

        for message in all_messages:
            result = await session.execute(
                select(Message).where(
                    and_
                    (
                        Message.sender_id == message.sender_id,
                        Message.conference_time == message.conference_time
                    )
                )
            
            )
            is_exists = len(result.scalars().all())!=0
            if is_exists:
                continue
            else:
                session.add(message)
                await session.commit()



from aiogram.filters.callback_data import CallbackData
from typing import Optional


class MainCallbackData(CallbackData, prefix='fabnum'):
    action: str
    student_id: Optional[int] = None
    party_id: Optional[int] = None
    party_name: Optional[str] = None
    lesson_id: Optional[int] = None

import os
import json
import datetime
import requests
from dotenv import load_dotenv

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, FSInputFile

import kb
import text
from logging_config import logger
from functions import file_to_text, text_to_docx, text_to_pdf, get_dates

# ---------------------------------------------
# ИНИЦИАЛИЗАЦИЯ
# ---------------------------------------------
router = Router()
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000/api")
USER_API = f"{BASE_URL}/create-user"
MSG_API = f"{BASE_URL}/create-message"
LLM_API = f"{BASE_URL}/create-llm-message"

# FSM
class GenerateProcess(StatesGroup):
    waiting_file = State()
    generated_text = State()


# ---------------------------------------------
# /start — регистрация пользователя
# ---------------------------------------------
@router.message(CommandStart())
async def start_handler(msg: Message):
    user_tg_id = msg.from_user.id
    logger.info(f"Запуск /start от пользователя {user_tg_id}")

    try:
        res = requests.post(USER_API)
        if res.status_code != 200:
            raise Exception(res.text)
        data = res.json()
        user_id = data.get("user_id")
        logger.info(f"Создан пользователь с id={user_id}")

        await msg.answer(
            text.greet.format(name=msg.from_user.full_name),
            reply_markup=kb.buttons_menu
        )
    except Exception as e:
        logger.error(f"Ошибка создания пользователя: {e}")
        await msg.answer("⚠️ Ошибка при подключении к API. Попробуйте позже.")


# ---------------------------------------------
# /menu
# ---------------------------------------------
@router.message(Command('menu'))
@router.message(F.text == "Menu")
async def menu_handler(msg: Message):
    await msg.answer("Вы находитесь в главном меню", reply_markup=kb.buttons_menu)


# ---------------------------------------------
# /add_services
# ---------------------------------------------
@router.message(Command('add_services'))
@router.message(F.text == "Add services")
async def services_handler(msg: Message):
    await msg.answer(text.service_text, reply_markup=kb.services_menu)


# ---------------------------------------------
# /generate — начало генерации протокола
# ---------------------------------------------
@router.message(Command('generate'))
@router.message(F.text == "Generate")
async def generate_command(msg: Message, state: FSMContext):
    await msg.answer(text.generate_text, reply_markup=kb.buttons_menu)
    await state.set_state(GenerateProcess.waiting_file)


# ---------------------------------------------
# Получение текста / файла от пользователя
# ---------------------------------------------
@router.message(GenerateProcess.waiting_file)
async def process_generate(msg: Message, state: FSMContext):
    text_input = None

    # 1️⃣ Текст
    if msg.text:
        text_input = msg.text
    # 2️⃣ Документ
    elif msg.document:
        try:
            text_input = await file_to_text(msg.bot, msg.document.file_id)
        except Exception as e:
            await msg.answer("❌ Не удалось обработать документ. Попробуйте другой файл.")
            logger.error(f"Ошибка обработки документа: {e}")
            return
    else:
        await msg.answer("Пожалуйста, отправьте текст или документ.")
        return

    await msg.answer("⏳ Формирую протокол, пожалуйста, подождите...")

    try:
        # -----------------------------------------
        # 1️⃣ Создаём сообщение пользователя через API
        # -----------------------------------------
        payload_msg = {
            "user_id": msg.from_user.id,  # Telegram ID как user_id
            "chat_id": 1,  # если чаты не используются
            "text": text_input,
            "is_bot": False,
            "answer_to": None
        }

        res_msg = requests.post(MSG_API, json=payload_msg)
        if res_msg.status_code != 200:
            raise Exception(res_msg.text)
        logger.info("Сообщение пользователя сохранено в API")

        # -----------------------------------------
        # 2️⃣ Запрашиваем ответ от LLM
        # -----------------------------------------
        payload_llm = {"chat_id": 1}
        res_llm = requests.post(LLM_API, json=payload_llm)
        if res_llm.status_code != 200:
            raise Exception(res_llm.text)

        llm_data = res_llm.json()["data"]
        txt = llm_data["text"]

        # -----------------------------------------
        # 3️⃣ Отправляем ответ пользователю
        # -----------------------------------------
        await msg.answer(txt, reply_markup=kb.buttons_menu)
        await msg.answer("Хотите получить протокол в другом формате?", reply_markup=kb.format_menu)

        await state.update_data(generated_text=txt)

    except Exception as e:
        logger.error(f"Ошибка при взаимодействии с API: {e}")
        await msg.answer("⚠️ Ошибка при обращении к API. Попробуйте позже.")


# ---------------------------------------------
# Выбор формата: Word / PDF / без файла
# ---------------------------------------------
@router.callback_query(F.data.in_(['format_word', 'format_pdf', 'format_no']))
async def process_format_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text_data = data.get("generated_text")

    if not text_data:
        await callback.message.answer("❌ Текст для экспорта не найден. Начните заново.")
        await state.clear()
        await callback.answer()
        return

    try:
        if callback.data == 'format_word':
            path = text_to_docx(text_data)
            file = FSInputFile(path)
            await callback.message.answer_document(file, caption="📄 Ваш протокол в формате Word")

        elif callback.data == 'format_pdf':
            path = text_to_pdf(text_data)
            file = FSInputFile(path)
            await callback.message.answer_document(file, caption="📄 Ваш протокол в формате PDF")

        elif callback.data == 'format_no':
            await callback.message.answer("Окей, завершаем обработку.", reply_markup=kb.buttons_menu)

    except Exception as e:
        logger.error(f"Ошибка при экспорте файла: {e}")
        await callback.message.answer("⚠️ Ошибка при создании файла.")

    await state.clear()
    await callback.answer()


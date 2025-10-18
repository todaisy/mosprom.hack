from api import LLM_UUID
from db import engine, Base
from models import *
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from models import User
from db import engine

async def init_models():
    async with engine.begin() as conn:
        print("💣 Удаляю все таблицы...")
        await conn.run_sync(Base.metadata.drop_all)   # ⬅️ сначала дропаем всё

        print("🧱 Создаю таблицы заново...")
        await conn.run_sync(Base.metadata.create_all) # ⬅️ потом пересоздаём

    print("✅ Таблицы успешно пересозданы!")
    async with AsyncSession(engine) as session:
        from models import User
        llm_user = User(uuid=LLM_UUID)
        session.add(llm_user)
        await session.commit()
        print(f"🤖 Добавлен системный пользователь LLM: {LLM_UUID}")

if __name__ == "__main__":
    asyncio.run(init_models())

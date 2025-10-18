from db import engine, Base
from models import *
import asyncio

async def init_models():
    async with engine.begin() as conn:
        print("🧱 Создаю таблицы в БД...")
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Таблицы успешно созданы!")

if __name__ == "__main__":
    asyncio.run(init_models())
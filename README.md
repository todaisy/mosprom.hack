# mosprom.hack

  
Прототип полностью не запускается:( ошибка на фронтенде  
И докер не успели собрать
Для запуска Backend - из папки /back вызвать: uvicorn main:app --reload  
Для запуска Frontend - из папки /front вызвать: npm start   
Скачать две модельки SLM - Qwen3 сохраняется автоматически в папку .ollama/,   
ru-en-RoSBERTa необходимо сохранить в папку ai_models/     


Модель данных обращений, действий с ними и ответов на них:
<img width="1214" height="557" alt="Фото" src="https://github.com/user-attachments/assets/5a91e65a-3389-431f-a8a6-ba55a0a68c01" />


Stack: 
- Backend - Python, FastAPI  
- Frontend - React JS  
- База данных – PostgreSQL  
- Векторная база данных - Qdrant
- Кэш - Redis (будет сделан позже)  
- SLM 1 - Qwen3:4b (open source - https://ollama.com/library/qwen3)   
- SLM 2 - ru-en-RoSBERTa (open source - https://huggingface.co/ai-forever/ru-en-RoSBERTa)  
 

------------------------------------
*developed by vibeкодеры*

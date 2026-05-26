from deep_translator import GoogleTranslator
import asyncio

async def get_translate(input_data: str) -> str:
    for attempt in range(3):
        try:
            trans = GoogleTranslator(source='en', target='ru')
            translate = await asyncio.to_thread(trans.translate, input_data)
            break 
        except Exception as e:
            wait_time = (attempt + 1) * 3
            print(f"[-] Гугл ругается (Попытка {attempt + 1}/3). Ждем {wait_time} сек... Ошибка: {e}")
            await asyncio.sleep(wait_time)
        if not translate:
            print(f"[!] Не удалось перевести строку, оставляем оригинал: {input_data[:30]}...")
            translate = input_data

    return translate
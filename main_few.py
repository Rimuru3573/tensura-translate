import asyncio
import urllib.parse
import nodriver as uc
import requests
from gptranslate import get_translate
from pdf import PDFBook


def download_image_bytes(url: str) -> bytes:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    img = requests.get(url, headers=headers)
    return img.content


# 1. Переносим логику в функцию, которая принимает номер тома
async def process_volume(tom: str):
    # Включаем headless=True для экономии ресурсов. Если нужно видеть процесс, верните False.
    browser = await uc.start(headless=True)
    base_url = f"https://tensurafan.github.io/read/v{tom}"

    page = await browser.get(base_url)

    elements = await page.select_all(
            'h1.ch-number, h1.ch-name, p[id^="line_"], img.full'
        )
    PDF = PDFBook(tom)

    for el in elements:
        if el.tag == "img":
            src = el.attrs["src"]
            abs_url = urllib.parse.urljoin(base_url, src)
            encoded_url = urllib.parse.quote(abs_url, safe=":/?&=~")

            print(f"[Том {tom}] Скачиваю иллюстрацию: {encoded_url}")
            try:
                img_bytes = await asyncio.to_thread(
                        download_image_bytes, encoded_url
                    )
                PDF.add_image(img_bytes)
            except Exception as e:
                print(
                        f"[Том {tom}] Не удалось скачать картинку {encoded_url}: {e}"
                    )
            continue

        raw_text = el.text_all.strip()
        if raw_text == "":
            continue

        translate = await get_translate(raw_text)

        if translate is None:
            print(
                    f"[Том {tom}] Гугл вернул None для строки: '{raw_text[:40]}...'. Оставляю оригинал."
                )
            translate = raw_text

        if el.tag == "h1":
            PDF.add_header(translate)
        else:
            PDF.add_paragraph(translate)

            # Чтобы файлы разных томов не перемешивались, пишем логи в отдельные файлы
        with open(
            f"test_v{tom}.txt", "a", encoding="utf-8"
            ) as file:
            file.write(translate + "\n")

    PDF.save()
    print(f"[+] Том {tom} успешно сохранен!")




# 2. Главный оркестратор
async def main():
    # Создаем список томов от 1 до 20
    # tasks = ["9", "10", "11", "15", "16", "17", "18", "19", "20"]
    volumes = ["6", "7", "8", "8_5"]

    # Ограничение: максимум 3 тома обрабатываются ОДНОВРЕМЕННО.
    # Если у вас мощный ПК и стабильный прокси/интернет, можете поднять до 5-7.
    MAX_CONCURRENT_TASKS = 20
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

    async def worker(tom):
        async with semaphore:
            try:
                print(f"[*] Запуск обработки Тома {tom}...")
                await process_volume(tom)
            except Exception as e:
                print(f"[!] Критическая ошибка в Томе {tom}: {e}")

    # Формируем список зада
    tasks = [worker(tom) for tom in volumes]

    # Запускаем всё конкурентно
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
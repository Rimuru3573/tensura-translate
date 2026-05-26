from gptranslate import get_translate
from pdf import PDF
import asyncio
import nodriver as uc
import urllib.request
import requests

async def download_image_bytes(url: str) -> bytes:
    # Качаем картинку асинхронно через стандартную библиотеку в фоновом потоке
    def _download():
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req) as response:
            return response.read()
    return await asyncio.to_thread(_download)

def new_download(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    img = requests.get(url, headers=headers)
    return img.content



async def main():
    browser = await uc.start(headless=False)
    base_url = "https://tensurafan.github.io/read/v12"
    page = await browser.get(base_url)

    elements = await page.select_all('h1.ch-number, h1.ch-name, p[id^="line_"], img.full')

    for x, el in enumerate(elements):

        raw_text = el.text_all.strip()
        if raw_text == "":
            continue
        translate = await get_translate(raw_text)
        print(f"asd: {translate}")
        if x == 15: break 

    


if __name__ == "__main__":
    asyncio.run(main())
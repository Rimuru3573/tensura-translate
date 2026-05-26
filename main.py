from gptranslate import get_translate
from pdf import PDFBook
import asyncio
import nodriver as uc
import requests
import urllib.parse

tom = "12"

def download_image_bytes(url: str) -> bytes:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    img = requests.get(url, headers=headers)
    return img.content


async def main():
    browser = await uc.start(headless=False)
    base_url = f"https://tensurafan.github.io/read/v{tom}"
    page = await browser.get(base_url)

    elements = await page.select_all('h1.ch-number, h1.ch-name, p[id^="line_"], img.full')
    PDF = PDFBook(tom)

    for el in elements:
        
        if el.tag == "img":
            src = el.attrs["src"]
            
            abs_url = urllib.parse.urljoin(base_url, src)
                
            encoded_url = urllib.parse.quote(abs_url, safe=':/?&=~')
                
            print(f"[+] Скачиваю иллюстрацию: {encoded_url}")
            try:
                img_bytes = img_bytes = await asyncio.to_thread(download_image_bytes, encoded_url)
                PDF.add_image(img_bytes)
            except Exception as e:
                print(f"[-] Не удалось скачать картинку {encoded_url}: {e}")
                
            continue

        raw_text = el.text_all.strip()
        if raw_text == "":
            continue

        translate = await get_translate(raw_text)

        if el.tag == "h1":
            PDF.add_header(translate)
        else:
            PDF.add_paragraph(translate)

        with open("test.txt", "a", encoding="utf-8") as file:
            file.write(translate + "\n")
    PDF.save()




if __name__ == "__main__":
    asyncio.run(main())
from fpdf import FPDF
import io

class PDFBook:
    def __init__(self, tom: str):
        self.pdf = FPDF()
        self.tom = tom
        self.pdf.add_font("Roboto", "", "RobotoMono-Regular.ttf")
        self.pdf.set_author("Rimuru, https://https://github.com/rimuru3573")
        self.pdf.set_title(f"TenSura_tom_{self.tom}_russia")
        self.pdf.set_subject("Фанатский перевод тенсуры на русский язык (с помощью гугл переводчика)")
        self.pdf.set_keywords(f"Slime, TenSura, {self.tom}, russia, translate, перевод, русский, Tensei Shitara Slime Datta Ken, О моем перерождении в слизь")
        self.pdf.add_page()
        self.add_predislovie()
        
    def add_predislovie(self):
        self.pdf.set_font("Roboto", size=16)
        self.pdf.multi_cell(w=0, h=10, text="ПРЕДИСЛОВИЕ", align="C")
        self.pdf.ln(10)
        
        self.pdf.set_font("Roboto", size=12)
        text_body = (
            "Данный файл книги был автоматически сгенерирован и переведен "
            "с помощью асинхронного парсера Tensura Translate. Скрипт собрал "
            "оригинальный текст, скачал иллюстрации и упаковал всё в формат PDF.\n\n"
            "• Автор проекта: Rimuru\n"
            "• Код доступен по ссылке: https://github.com/Rimuru3573/tensura-translate\n\n"
            "📢 ТЕЛЕГРАМ-КАНАЛ С ГОТОВЫМИ ТОМАМИ:\n"
            "Свежие релизы, обсуждения глав и готовые сборки ранобэ доступны в сообществе:\n"
            "👉 https://t.me/tensura_russia\n\n"
            "-----------------------------------------------------------------------------------------\n"
            "Дисклеймер: Перевод выполнен в автоматическом режиме исключительно для ознакомления. "
            "Все права на оригинальный контент и персонажей принадлежат авторам."
        )
        self.pdf.multi_cell(w=0, h=6, text=text_body)


    def add_header(self, text: str) -> None:
        self.pdf.set_font("Roboto", size=18)
        self.pdf.multi_cell(w=0, h=8, text=text, align="C")
        self.pdf.ln(8)

    def add_paragraph(self, text: str) -> None:
        self.pdf.set_font("Roboto", size=12)
        self.pdf.multi_cell(w=0, h=6, text=text)
        self.pdf.ln(4)
    
    def add_image(self, img_bytes: bytes) -> None:
        self.pdf.ln(2)
        try:
            self.pdf.image(io.BytesIO(img_bytes), w=self.pdf.epw)
        except Exception as e:
            print(f"[-] Ошибка при добавлении картинки в PDF: {e}")

    def save(self):
        self.pdf.output(f"TenSura_tom_{self.tom}_russia.pdf")
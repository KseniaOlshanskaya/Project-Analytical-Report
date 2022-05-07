from fpdf import FPDF

WIDTH = 210
title = "Обзор внешней торговли НСО и Казахстана"

class PDF(FPDF):
    def __init__(self):
        super().__init__()

    def header(self):
        # Arial bold 15
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 0, 255)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 255)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')


    def chapter_title(self, title):
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, title, 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def print_overal_info(self, title, overal_info_text):
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 10)
        self.add_page()
        self.chapter_title(title)
        for text in overal_info_text:
            self.multi_cell(0, 5, text)
            self.ln()

    def print_export_info_russia(self, title, figureExportRussiaPie, figureExportRussiaBar):
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 10)
        self.add_page()
        self.chapter_title(title)
        self.image(figureExportRussiaPie, x=10, y=35, w=WIDTH / 2.5, type='PNG')
        self.image(figureExportRussiaBar, x=WIDTH / 2.5 + 40, y=35, w=WIDTH / 2.5, type='PNG')



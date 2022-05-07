from fpdf import FPDF

title = 'Торговля России с Казахстаном'
WIDTH = 210

class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
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


    def chapter_title(self, num, label):
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, 'Раздел %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_overal_info_body(self, text):
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 10)
        # Output justified text
        self.multi_cell(0, 5, text)
        # Line break
        self.ln()

    def print_overal_info_chapter(self, num, title, list_of_text):
        self.add_page()
        self.chapter_title(num, title)
        for text in list_of_text:
            self.chapter_overal_info_body(text)
        self.image("Figure.png", x = 0, y=160, w=WIDTH/2, type='PNG')
        self.image("Figure.png", x= WIDTH/2, y=160, w=WIDTH / 2, type='PNG')

    def print_export_info_chapter(self, num, title, list_of_text):
        self.add_page()
        self.chapter_title(num, title)
        for text in list_of_text:
            self.chapter_overal_info_body(text)





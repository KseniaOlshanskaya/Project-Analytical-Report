from docxtpl import DocxTemplate
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import itertools

doc = DocxTemplate("Template.docx")
context = {}
with open("Kazakhstan.txt", "r", encoding="UTF-8") as file:
    text = file.readline()
context['country'] = 'Казахстан'
context['region'] = 'Новосибирская область'
context['year'] = '2021'
context['text'] = text

# определяем словарь переменных контекста,
# которые определены в шаблоне документа DOCX
imagen = InlineImage(doc, 'ExportRussiaPie.png', width=Mm(150)) # width is in millimetres
context['image'] = imagen


context = {}
for row, col in itertools.product(df.index, df.columns):
    context[f'{row}_{col}'] = df.loc[row, col]
# подставляем контекст в шаблон
doc.render(context)
# сохраняем и смотрим, что получилось
doc.save("generated_docx.docx")
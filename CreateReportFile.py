from docxtpl import DocxTemplate
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import itertools


class CreateDocFile():
    def __init__(self, name):
        self.name = name

    def create_report(self, context):
        doc = DocxTemplate("Template.docx")

from tkinter import *
from tkinter.ttk import Combobox, Button, Progressbar
from Organizer import Organizer
import threading

class Interface:
    def __init__(self):
        self.org = Organizer()
        self.parser1 = self.org.parser1
        self.parser2 = self.org.parser2
        self.region = ''
        self.country = ''
        self.year_current = ''

    def get_values(self):
        self.region = self.combobox.get()
        self.country = self.combobox2.get()
        self.year_current = int(self.combobox3.get())
        self.master.destroy()

    def interface(self):
        self.master = Tk()
        self.list_regions = list(self.parser2.region_links.keys())
        self.list_countries = list(self.parser1.countries_links.keys())
        self.list_years = [2021, 2020]
        self.master.title("Генератор аналитических записок")
        self.master.geometry("400x300")
        self.combobox = Combobox(self.master)
        self.combobox2 = Combobox(self.master)
        self.combobox3 = Combobox(self.master)
        self.btn = Button(text="Получить отчет",  # высота шрифта
                     command=self.get_values)
        self.btn.pack()
        self.draw_element()

    def draw_element(self):
        self.combobox['values'] = self.list_regions
        self.combobox2['values'] = self.list_countries
        self.combobox3['values'] = self.list_years
        self.combobox.current(0)
        self.combobox2.current(0)
        self.combobox3.current(0)
        self.combobox.place(relx=.25, rely=.2, anchor="c", height=30, width=180, bordermode=OUTSIDE)
        self.combobox2.place(relx=.75, rely=.2, anchor="c", height=30, width=180, bordermode=OUTSIDE)
        self.combobox3.place(relx=.5, rely=.4, anchor="c", height=30, width=130, bordermode=OUTSIDE)
        self.master.configure(bg="LightBlue")
        mainloop()

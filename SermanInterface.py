from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle

from datetime import datetime

import reports
import finance
import sp_books

from kivy.config import Config
from kivy.core.window import Window
from kivy.base import EventLoop
EventLoop.window.clear_color = (.5, 0, 0, 1)
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', 840)
Config.set('graphics', 'height', 480)
Config.set('graphics', 'default_font_size', 20)
Config.write()
#Window.size = (900, 400)
Window.clearcolor = (.28, .09, .27, 1)

# Import kv files
#Builder.load_file("sermankv.kv")



class SermanApp(App):

    def SalesBookReport(self, instance):
        try:
            self.mangement_report_link = sp_books.fill_the_sales_book(self.start_date_text1.text, self.end_date_text1.text)
            sales_book_hiperlink = f'https://docs.google.com/spreadsheets/d/{str(self.mangement_report_link)}/edit#gid=0'
            self.label1.text = f'report from {self.start_date_text1.text} to {self.end_date_text1.text} was formed {str(datetime.now().strftime("%Y-%m-%d"))}!'
            self.info_text.text += f'GoogleTable link for SalesBook report is \n [ref=world][color=0000ff]{sales_book_hiperlink}[/color][/ref]\n'
            return self.mangement_report_link

        except:
            self.label1.text = "Unknown date format (mast be 2021-02-05)"
            return "Unknown date format (mast be 2021-02-05)"

    def PurchaseBookReport(self, instance):
        try:
            self.mangement_report_link = sp_books.fill_the_sales_book(self.start_date_text2.text, self.end_date_text2.text)
            sales_book_hiperlink = f'https://docs.google.com/spreadsheets/d/{str(self.mangement_report_link)}/edit#gid=0'
            self.label2.text = f'report from {self.start_date_text2.text} to {self.end_date_text1.text} was formed {str(datetime.now().strftime("%Y-%m-%d"))}!'
            self.info_text.text += f'GoogleTable link for PurchasesBook report is \n [ref=world][color=0000ff]{sales_book_hiperlink}[/color][/ref]\n'
            return self.mangement_report_link

        except:
            self.label2.text = "Unknown date format (mast be 2021-02-05)"
            return "Unknown date format (mast be 2021-02-05)"


    def MangementReport(self, instance):
        try:
            self.mangement_report_link = reports.monthly_report(self.start_date_text3.text, self.end_date_text3.text)
            profit_hiperlink = f'https://docs.google.com/spreadsheets/d/{str(self.mangement_report_link)}/edit#gid=0'
            self.label3.text = f'report from {self.start_date_text3.text} to {self.end_date_text3.text} was formed {str(datetime.now().strftime("%Y-%m-%d"))}!'
            self.info_text.text += f'GoogleTable link for Profit report is \n [ref=world][color=0000ff]{profit_hiperlink}[/color][/ref]\n'
            return self.mangement_report_link

        except:
            return "Unknown date format (mast be 2021-02-05)"

    def AccountSum(self, instance):
        self.label4.text = f'Acount balance on {str(datetime.now().strftime("%Y-%m-%d"))} is {str(round(finance.get_account_summ(), 2))} RUB.'

    def pop_up_menu1(self, pop_text):
        content = Label(text=str(self.start_date_text1.text ))
        popup1 = Popup(title='Test popup',
                      content=content,
                      size_hint=(None, None), size=(400, 400))
        self.text1.text = 'XXXXXXXX'
        popup1.open()

    def build(self):
        self.font_size = 20
        self.standard_label_width = 150
        self.standard_label_height = 30
        start_date = '2021-02-05'
        toda_y_date = str(datetime.now().strftime("%Y-%m-%d"))
        todayYear = datetime.now().year
        todayMonth = str(datetime.now().month)
        start_date = f'{todayYear}-{todayMonth}-01'
        end_date = toda_y_date
        bl = BoxLayout(orientation = 'vertical', padding=[20, 20, 20, 20], spacing=10)

        self.info_text = Label(text='Hello, welcome to Serman reports tool. Reports will be formed in Google Tables\n',
                               font_size=self.font_size,
                               halign='center',
                               valign='center',
                               markup=True)
        al = AnchorLayout()
        al.add_widget(self.info_text)
        bl.add_widget(al)
        gl = GridLayout(cols=5, row_force_default=True, row_default_height=self.standard_label_height, padding=[20, 20, 20, 20], spacing=10)
        # top names
        gl.add_widget(Label(text='start_date', size_hint_x=None, width=self.standard_label_width, font_size=self.font_size))
        gl.add_widget(Label(text='end_date', size_hint_x=None, width=self.standard_label_width, font_size=self.font_size))
        gl.add_widget(Label(text='Start button', size_hint_x=None, width=self.standard_label_width, font_size=self.font_size))
        gl.add_widget(Label(text='Type', size_hint_x=None, width=self.standard_label_width, font_size=self.font_size))
        gl.add_widget(Label(text='Google tags', size_hint_x=None, width=self.standard_label_width*2, font_size=self.font_size))

        #acountant outinvoices grid
        self.start_date_text1 = TextInput(text=start_date, size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size)
        self.end_date_text1 = TextInput(text=end_date, size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size)
        self.label1 = Label(text='Sales taxbook', height=self.standard_label_height, width=self.standard_label_width*2, font_size=self.font_size)
        gl.add_widget(self.start_date_text1)
        gl.add_widget(self.end_date_text1)
        gl.add_widget(Button(text='Start report', size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size, on_press = self.SalesBookReport))
        gl.add_widget(Label(text='Sales', size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size))
        gl.add_widget(self.label1)

        # acountant innerinvoices grid
        self.start_date_text2 = TextInput(text=start_date, size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size)
        self.end_date_text2 = TextInput(text=end_date,size_hint_x=None,  height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size)
        self.label2 = Label(text='Purchases taxbook', height=self.standard_label_height, width=self.standard_label_width*2, font_size=self.font_size)
        gl.add_widget(TextInput(text=start_date, size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size))
        gl.add_widget(TextInput(text=end_date, size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size))
        gl.add_widget(Button(text='Start report', size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size, on_press = self.PurchaseBookReport))
        gl.add_widget(Label(text='Purchases', size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size))
        gl.add_widget(self.label2)
        # profit grid
        self.start_date_text3 = TextInput(text=start_date, size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size)
        self.end_date_text3 = TextInput(text=end_date, size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size)
        self.label3 = Label(text='Profit in timeline', height=self.standard_label_height, width=self.standard_label_width*2, font_size=self.font_size) #, halign='right'
        gl.add_widget(self.start_date_text3)
        gl.add_widget(self.end_date_text3)
        gl.add_widget(Button(text='Start report', size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size, on_press = self.MangementReport))
        gl.add_widget(Label(text='Profit', size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size))
        gl.add_widget(self.label3)
        # money
        self.start_date_label4 = Label(text=start_date, size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size)
        self.end_date_label4 = Label(text=end_date, size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size)
        self.label4 = Label(text='Account summary', height=self.standard_label_height, width=self.standard_label_width*2, font_size=self.font_size)
        gl.add_widget(self.start_date_label4)
        gl.add_widget(self.end_date_label4)
        gl.add_widget(Button(text='Start report', size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size, on_press=self.AccountSum))
        gl.add_widget(Label(text='Account', size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size))
        gl.add_widget(self.label4)
        # agents grid
        gl.add_widget(TextInput(text=start_date, size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size))
        gl.add_widget(TextInput(text=end_date, size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size))
        gl.add_widget(Button(text='Start report', size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size))
        dropdown = DropDown()
        for index in ['Novosib', 'Saratov']:
            btn = Button(text=index, size_hint_y=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        mainbutton = Button(text='Agent', size_hint_x=None, height=self.standard_label_height, width=self.standard_label_width, font_size=self.font_size)
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        gl.add_widget(mainbutton)
        gl.add_widget(Label(text='Agents payments', height=self.standard_label_height, width=self.standard_label_width*2, font_size=self.font_size))
        bl.add_widget(gl)
        return bl

if __name__ == "__main__":
    SermanApp().run()

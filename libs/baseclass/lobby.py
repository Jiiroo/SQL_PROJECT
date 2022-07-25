from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.uix.button.button import MDRaisedButton
import pandas as pd
from kivymd_extensions.akivymd import *
import mysql
from xlsxwriter import worksheet
from xlsxwriter import workbook
from xlsxwriter.workbook import Workbook
from datetime import date
from libs.baseclass import db_conn
from kivy.uix.boxlayout import BoxLayout
import os
from kivy.properties import NumericProperty, ObjectProperty
import datetime
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast

Builder.load_file('./libs/kv/lobby.kv')

class Lobby(Screen):
    visitors = NumericProperty(25)

    def on_enter(self, *args):
        conn = db_conn.data_base()
        cur = conn.cursor()

        cur.execute("""SELECT COUNT(name) from customers where DATE_FORMAT(time_in, "%Y-%m-%d") = DATE_SUB(CURRENT_DATE(),INTERVAL 1 DAY)""")
        get = cur.fetchall()
        self.visitors = get[0][0]

class SetCustomer(BoxLayout):
    usr_int = ObjectProperty(None)

    def verify_entry(self):
        get = MDApp.get_running_app()
        try:
            int(self.usr_int.text)
        except ValueError:
            return False
        get.capacity = int(self.usr_int.text)
        self.usr_int.text = ''
        self.dialog.dismiss()
        get.root.current = 'scanner'
        return True


class RightSide(BoxLayout):
    dialog = None

    def scan_butt(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Set Customer Limit:",
                type="custom",
                content_cls=SetCustomer(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color='#35353F', on_release= self.closeDialog
                    ),
                    MDFlatButton(
                        text="OK", text_color='#35353F', on_release=self.grabText
                    ),
                ],
            )
            
        self.dialog.open()
            # self.dialog = MDDialog(title="Set Customer Limit", type="custom", content_cls=SetCustomer(),buttons=[MDRaisedButton(
            #                         text='Done',on_release=lambda x: self.done())])
        # self.dialog.open()

    def grabText(self, inst):
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                print(obj.text)
                get = MDApp.get_running_app()
                try:
                    int(obj.text)
                except ValueError:
                    obj.text = ''
                else:
                    get.capacity = int(obj.text)
                    obj.text = ''
                    self.dialog.dismiss()
                    get.root.current = 'scanner'
                
                    self.dialog.dismiss()

    def closeDialog(self, inst):
        self.dialog.dismiss()

    # def done(self, *args):
        # get = MDApp.get_running_app()
        # try:
        #     int(self.usr_int.text)
        # except ValueError:
        #     return False
        # get.capacity = int(self.usr_int.text)
        # self.usr_int.text = ''
        # self.dialog.dismiss()
        # get.root.current = 'scanner'
        # return True

    def show_toast(self):
        '''Displays a toast on the screen.'''
        toast('Export Successful!')

    def export_data(self):
        path = './Exports'

        # Check whether the specified path exists or not
        isExist = os.path.exists(path)

        if not isExist:
        
            # Create a new directory because it does not exist 
            os.makedirs(path)

        dates = []
        conn = db_conn.data_base()
        cur = conn.cursor()
        cur.execute("""SELECT name, age, address, number, DATE_FORMAT(time_in, "%H:%i"), DATE_FORMAT(time_out, "%H:%i"), DATE_FORMAT(time_in, "%M %D %Y")
                    from customers""")
        res = cur.fetchall()

        for i in res:
            if i[6] not in dates:
                dates.append(i[6])

        for d in dates:
            row_n = 1
            title = './Exports/TRACE ' + str(d) + '.xlsx'
            workbook = Workbook(title)
            worksheet = workbook.add_worksheet()
            
            # writes column names to spreadsheet
            worksheet.write('A1', 'Name')
            worksheet.write('B1', 'Age')
            worksheet.write('C1', 'Address')
            worksheet.write('D1', 'Contact Number')
            worksheet.write('E1', 'Time In')
            worksheet.write('F1', 'Time Out')
            worksheet.write('G1', 'Date')

            # writes values from database down to spreadsheet
            for i, row in enumerate(res, 1):
                for j, value in enumerate(row):
                    print(i, j)
                    if row[6] == d:
                        worksheet.write(i, j, value)

            workbook.close()
            
            # deletes all records from database
            # after exporting to spreadsheet
            # self.delete = "DELETE FROM records"
            # self.cur.execute(self.delete)
        conn.commit()
        conn.close()


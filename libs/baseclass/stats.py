from kivy.app import App
from kivymd_extensions.akivymd.uix.charts import AKBarChart
import mysql
from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder
from libs.baseclass import db_conn
from kivy.properties import ListProperty

Builder.load_file('./libs/kv/stats.kv')

class Statistics(MDScreen):

    def on_enter(self):
        date_time = []
        date = []

        conn = db_conn.data_base()
        cur = conn.cursor()
        cur.execute("""SELECT DATE_FORMAT(time_in, "%M %D %Y") as date, 
                    DATE_FORMAT(time_in, "%H")as time from customers""")
        get_data = cur.fetchall()
        
        for i in get_data:
            date_time.append(i)
            if i[0] not in date:
                date.append(i[0])

        for ver in date:
            blank = []
            for check in date_time:
                if check[0] == ver:
                    blank.append(check[1])
            get_widgets = MyBarChart(date=ver, time=check[1])
            self.ids.content.add_widget(get_widgets)
            print(ver, 'gg ', check)
        # chart1 = self.ids.chart1
        # chart1.x_values = [2, 8, 12, 35, 40, 43, 56]
        # chart1.y_values = [3, 2, 1, 20, 0, 1, 10]
        # chart1.update()

        # chart2 = self.ids.chart2
        # chart2.x_values = [2, 8, 12, 35, 40, 43, 56]
        # chart2.y_values = [3, 2, 1, 20, 0, 1, 10]
        # chart2.update()

        # chart3 = self.ids.chart3
        # chart3.x_labels = ["XYZ", "Second", "Third", "Last"]
        # chart3.y_labels = ["XYZ", "Second", "Third", "Last"]
        # chart3.update()

class MyBarChart(AKBarChart):
    date = ListProperty([])
    time = ListProperty([])
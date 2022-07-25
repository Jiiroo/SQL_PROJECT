from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd_extensions.akivymd import *
import mysql.connector
import datetime
Builder.load_file('./libs/kv/statistics.kv')

class Statistics(Screen):
    data_list = ListProperty([1,0,0,0,0,0])
    data_str = ListProperty(['1','3','4','9','8','7'])
    data_list2 = ListProperty([10,0,0,0,0,0,0])
    data_str2 = ListProperty(['10','10','15','18','16','16','14'])


    def on_enter(self):
        conn = mysql.connector.connect(host = '127.0.0.1',
                                    user = 'root',
                                    passwd = '1234',
                                    database = 'sql_project')

        cur = conn.cursor()

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)

        # customer count per 2hours
        # 10:00:00 - 11:59:00
        cur.execute(f"SELECT count(*) FROM customers WHERE time_in BETWEEN '{yesterday} 10:00:00' AND '{yesterday} 11:59:00'")
        count = cur.fetchall()
        get_count1 = count[0][0]
        
        # 12:00:00 - 13:59:00
        cur.execute(f"SELECT count(*) FROM customers WHERE time_in BETWEEN '{yesterday} 12:00:00' AND '{yesterday} 13:59:00'")
        count = cur.fetchall()
        get_count2 = count[0][0]

        # 14:00:00 - 15:59:00
        cur.execute(f"SELECT count(*) FROM customers WHERE time_in BETWEEN '{yesterday} 14:00:00' AND '{yesterday} 15:59:00'")
        count = cur.fetchall()
        get_count3 = count[0][0]

        # 16:00:00 - 17:59:00
        cur.execute(f"SELECT count(*) FROM customers WHERE time_in BETWEEN '{yesterday} 16:00:00' AND '{yesterday} 17:59:00'")
        count = cur.fetchall()
        get_count4 = count[0][0]

        # 18:00:00 - 19:59:00
        cur.execute(f"SELECT count(*) FROM customers WHERE time_in BETWEEN '{yesterday} 18:00:00' AND '{yesterday} 19:59:00'")
        count = cur.fetchall()
        get_count5 = count[0][0]

        # 20:00:00 - 21:59:00
        cur.execute(f"SELECT count(*) FROM customers WHERE time_in BETWEEN '{yesterday} 20:00:00' AND '{yesterday} 21:59:00'")
        count = cur.fetchall()
        get_count6 = count[0][0]

        cur.execute("""SELECT COUNT(name) from customers where DATE_FORMAT(time_in, "%Y-%m-%d") = DATE_SUB(CURRENT_DATE(),INTERVAL 1 DAY)""")
        num = cur.fetchall()
        get_num1 = num[0][0]
        
        cur.execute("""SELECT COUNT(name) from customers where DATE_FORMAT(time_in, "%Y-%m-%d") = DATE_SUB(CURRENT_DATE(),INTERVAL 2 DAY)""")
        num = cur.fetchall()
        get_num2 = num[0][0]

        cur.execute("""SELECT COUNT(name) from customers where DATE_FORMAT(time_in, "%Y-%m-%d") = DATE_SUB(CURRENT_DATE(),INTERVAL 3 DAY)""")
        num = cur.fetchall()
        get_num3 = num[0][0]

        cur.execute("""SELECT COUNT(name) from customers where DATE_FORMAT(time_in, "%Y-%m-%d") = DATE_SUB(CURRENT_DATE(),INTERVAL 4 DAY)""")
        num = cur.fetchall()
        get_num4 = num[0][0]

        cur.execute("""SELECT COUNT(name) from customers where DATE_FORMAT(time_in, "%Y-%m-%d") = DATE_SUB(CURRENT_DATE(),INTERVAL 5 DAY)""")
        num = cur.fetchall()
        get_num5 = num[0][0]

        cur.execute("""SELECT COUNT(name) from customers where DATE_FORMAT(time_in, "%Y-%m-%d") = DATE_SUB(CURRENT_DATE(),INTERVAL 6 DAY)""")
        num = cur.fetchall()
        get_num6 = num[0][0]

        cur.execute("""SELECT COUNT(name) from customers where DATE_FORMAT(time_in, "%Y-%m-%d") = DATE_SUB(CURRENT_DATE(),INTERVAL 7 DAY)""")
        num = cur.fetchall()
        get_num7 = num[0][0]

        if [get_count1, get_count2,get_count3,get_count4,get_count5,get_count6] != [0, 0, 0, 0, 0, 0]:
            self.data_list = [get_count1, get_count2,get_count3,get_count4,get_count5,get_count6]
            self.data_str = [str(get_count1), str(get_count2),str(get_count3),str(get_count4),str(get_count5),str(get_count6)]

            chart1 = self.ids.chartAF
            chart1.y_values = [get_count1, get_count2,get_count3,get_count4,get_count5,get_count6]
            chart1.y_labels = [str(get_count1), str(get_count2),str(get_count3),str(get_count4),str(get_count5),str(get_count6)]
            chart1.update()

        if [get_num1, get_num2,get_num3,get_num4,get_num5,get_num6,get_num7] != [0, 0, 0, 0, 0, 0, 0]:
            self.data_list2 = [get_num1, get_num2,get_num3,get_num4,get_num5,get_num6,get_num7]
            self.data_str2 = [str(get_num1), str(get_num2),str(get_num3),str(get_num4),str(get_num5),str(get_num6), str(get_num7)]

            chart2 = self.ids.chartAF2
            chart2.y_values = [get_num1, get_num2,get_num3,get_num4,get_num5,get_num6,get_num7]
            chart2.y_labels = [str(get_num1), str(get_num2),str(get_num3),str(get_num4),str(get_num5),str(get_num6), str(get_num7)]
            chart2.update()
        
        print(self.data_list)
        print(self.data_str)
        print(self.data_list2)
        print(self.data_str2)
        conn.close()


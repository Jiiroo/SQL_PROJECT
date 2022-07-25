import threading
import numpy as np
from pyzbar.pyzbar import decode
from functools import partial
import cv2
from kivy.app import App
from kivy.clock import Clock
import time
from kivy.graphics.texture import Texture
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
import mysql.connector
from kivymd_extensions.akivymd import *
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard
import requests
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog

Builder.load_file('./libs/kv/scanner.kv')



class Scanner(Screen):
    dialog = None
    visitor_count = StringProperty('0')
    capacity_limit = StringProperty('0')
    qr_reading = StringProperty('')
    url = "https://corona.lmao.ninja/v2/countries/philippines"

    json_data = requests.get(url).json()

    cases = ObjectProperty(str(json_data['cases']))
    cases_today = ObjectProperty(str(json_data['todayCases']))
    deaths = ObjectProperty(str(json_data['deaths']))
    deaths_today = ObjectProperty(str(json_data['todayDeaths']))
    recovered = ObjectProperty(str(json_data['recovered']))
    recovered_today = ObjectProperty(str(json_data['todayRecovered']))
    active = str(json_data['active'])
 
    def __init__(self, **kwargs):
        super(Scanner, self).__init__(**kwargs)
        self.record_scene = True

    def callback_function(self, dt):
        self.ids.board.load_next(mode='next')

        #time.sleep(3)
        Clock.schedule_once(self.callback_function, 3)

    def on_enter(self, *args):
        self.record_scene = True
        threading.Thread(target=self.start_cam, daemon=True).start()
        Clock.schedule_once(self.callback_function, 3)
        get = MDApp.get_running_app()
        self.capacity_limit = str(get.capacity)
   
    def start_cam(self):
        cam = cv2.VideoCapture(0)
        while (self.record_scene):
            ret, img = cam.read()
            img_flip = cv2.flip(img,1)
            if decode(img) == []:
                self.qr_reading = ''

            for barcode in decode(img_flip):
                data_ret = barcode.data.decode('utf-8')
                read_data = data_ret.split(';')

                # find_array = np.array([barcode.polygon],np.int32)
                # find_array = find_array.reshape((-1,1,2))
                # cv2.polylines(img_flip, [find_array], True, (255,0,255),5)
                # find_array2 = barcode.rect
                # cv2.putText(img_flip, read_data[0], (find_array2[0], find_array2[1]),
                #             cv2.FONT_HERSHEY_SIMPLEX, 2,(255,0,255),2)
                
                if len(read_data) == 4:
                    try:
                        int(read_data[1])
                        int(read_data[-1])
                    except (TypeError, ValueError):
                        self.qr_reading = 'Invalid QR Code'
                    else:
                        
                        self.qr_reading = 'Valid QR Code'
                        self.data_base(read_data)
                    time.sleep(3)

                else:
                    self.qr_reading = 'Invalid Qr Code'
                    time.sleep(3)

            Clock.schedule_once(partial(self.display_frame, img_flip))
            
            cv2.waitKey(1)

        cam.release()

    def on_leave(self):
        self.record_scene = False

    def display_frame(self, frame, dt):
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')
        texture.flip_vertical()
        self.ids.cam_respo.texture = texture

    def data_base(self, data):
        try:
            conn = mysql.connector.connect(
                            host = '127.0.0.1',
                            user = 'root',
                            passwd = '1234',
                            database="sql_project"
                            )
       
        except (mysql.connector.errors.ProgrammingError):
            conn = mysql.connector.connect(
                        host = '127.0.0.1',
                        user = 'root',
                        passwd = '1234'
                        )
            cur = conn.cursor()
            cur.execute("CREATE DATABASE sql_project")   

        cur = conn.cursor()   

        cur.execute("""CREATE TABLE IF NOT EXISTS customers (
                            id MEDIUMINT NOT NULL AUTO_INCREMENT,
                            PRIMARY KEY (id),
                            name varchar(255),
                            age int,
                            address varchar (255),
                            number text,
                            time_in datetime,
                            time_out datetime,
                            status text)
                            """)
        
        dt = time.strftime("%Y-%m-%d %H:%M:%S")
        
        cur.execute(f"SELECT name FROM customers WHERE name = '{data[0]}' AND status = 'In'")
        res = cur.fetchall()
        
        if len(res) == 1:
            cur.execute(f"UPDATE customers SET time_out = '{dt}', status = 'Out'")
            # self.ids.progress_relative.current_percent -= 1
            self.visitor_count = str(int(self.visitor_count)-1)
            
        else:
            if int(self.visitor_count) < int(self.capacity_limit):
                cur.execute(f"""INSERT INTO customers (name, age, address, number,
                                    time_in, time_out, status) VALUES 
                                    (%s, %s, %s, %s, '{dt}', NULL, 'In')
                                    """, data)
                                    
                # self.ids.progress_relative.current_percent += 1
                self.visitor_count = str(int(self.visitor_count)+1)
            else:
                if not self.dialog:
                    self.dialog = MDDialog(text="Limit Reached!", auto_dismiss=True)
                self.dialog.open()

        conn.commit()
        conn.close()


class OnBoarding(Screen):
    def on_enter(self):
        Clock.schedule_once(self.callback_function, 3)

    def callback_function(self, dt):
        self.root.ids.board.load_next(mode='next')
        #time.sleep(3)
        Clock.schedule_once(self.callback_function, 3)

    def finish_callback(self):
        pass



class MyCard(MDCard, RoundedRectangularElevationBehavior):
    text = StringProperty('')

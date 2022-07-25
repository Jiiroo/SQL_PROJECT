from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.properties import StringProperty, NumericProperty


Builder.load_file('./libs/kv/about.kv')

class About(Screen):
    text1 = StringProperty("""
    General Objectives
        • The primary objective of this project is to create a desktop 
        application that could contribute in assessing and tracing 
        people most specifically in this time of pandemic.
    
    Specific Objectives
        As a goal, this desktop application is designed as follows: 
        • Provides an information about the time of in and out of people such 
        as customers in every establishment. 
        • Provides a summary report about the daily covid cases, deaths, 
        recovered and other information 
        about the pandemic’s current situation in the form of excel.
        • To determine the count of people in a certain area in a specific time. 

    """)
    
    text2 = StringProperty("""
        You Trace Me App is a MySQL and Quick Response code-based 
    contact tracing app. QR codes are machine-readable codes made 
    up of an array of black and white squares that are typically 
    used for storing URLs or other information that the camera 
    can read. MySQL is an open-source relational database management 
    system. The QR codes contain information such as name, age, 
    phone number, and address, which can be requested from local 
    government units. The system can monitor people entering closed 
    establishments by recording their time entering and leaving when 
    these two works together. With the help of a Worldometer API, the 
    You Trace Me App can also keep track of COVID19 cases across the 
    country.
    """)
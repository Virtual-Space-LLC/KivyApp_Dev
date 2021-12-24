# import all the relevant classes
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
import pandas as pd
from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.garden.mapview.mapview import types, source, view, geojson, utils, mbtsource, downloader
from kivy.garden.graph import Graph, MeshLinePlot, HBar
from math import sin

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.collections import PolyCollection

# importing pyplot for graph plotting
from matplotlib import pyplot as plt
  
# importing numpy
import numpy as np
#from kivy.garden.matplotlib import FigureCanvasKivyAgg

import os, sys
from kivy.resources import resource_add_path, resource_find

# class to call the popup function
class PopupWindow(Widget):
    def btn(self):
        popFun()
  
# class to build GUI for a popup window
class P(FloatLayout):
    pass

class Pt(FloatLayout):
    pass
  
# function that displays the content
def popFun():
    show = P()
    window = Popup(title = "Alert", content = show,
                   size_hint = (None, None), size = (300, 300))
    window.open()

# function that displays the content
def popTech():
    show = Pt()
    window = Popup(title = "Tech Support", content = show,
                   size_hint = (None, None), size = (300, 300))
    window.open()
  
# class to accept user info and validate it
class loginWindow(Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)
    def validate(self):
        # validating if the email already exists 
        if self.email.text not in users['Email'].unique():
            popFun()
        else:
            # switching the current screen to display validation result
            sm.current = 'logdata'
  
            # reset TextInput widget
            self.email.text = ""
            self.pwd.text = ""
    
    def showPopup(self):
        popTech()
  
# class to accept sign up info  
class signupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)
    def signupbtn(self):
        # creating a DataFrame of the info
        user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text]],
                            columns = ['Name', 'Email', 'Password'])
        if self.email.text != "":
            if self.email.text not in users['Email'].unique():
  
                # if email does not exist already then append to the csv file
                # change current screen to log in the user now 
                user.to_csv('data/login.csv', mode = 'a', header = False, index = False)
                sm.current = 'login'
                self.name2.text = ""
                self.email.text = ""
                self.pwd.text = ""
        else:
            # if values are empty or invalid show pop up
            popFun()

class dataframeWindow(Screen):
    def showDataframe():  
        schedule = pd.read_excel('data/GnattChart_10.31.21.xlsx')
        data = []
        yticklabels = []
        yticks = []
        cats = {}
        #colormapping = {}
        for i in schedule.index:
           # colorCode = "C" + str(i)
            yticks.append(i+1) 
            splitDate = str(schedule['Start'][i]).split("-")
            day = splitDate[2].split(" ")
            endDay = int(day[0]) + int(schedule['Duration'][i])
            print(splitDate[2])
            field = dt.datetime(int(splitDate[0]), int(splitDate[1]), int(day[0]), 0, 15), dt.datetime(int(splitDate[0]), int(splitDate[1]), endDay, 0, 15), schedule['Work Type'][i].rstrip()
            data.append(field)

            yticklabels.append(schedule['Work Type'][i].rstrip())
            cats[schedule['Work Type'][i].rstrip()] = i+1
           # colormapping[schedule['Work Type'][i].rstrip()] = colorCode

        verts = []
        colors = []
        for d in data:
            v =  [(mdates.date2num(d[0]), cats[d[2]]-.4),
                (mdates.date2num(d[0]), cats[d[2]]+.4),
                (mdates.date2num(d[1]), cats[d[2]]+.4),
                (mdates.date2num(d[1]), cats[d[2]]-.4),
                (mdates.date2num(d[0]), cats[d[2]]-.4)]
            verts.append(v)
            colors.append('C0')

        bars = PolyCollection(verts, facecolors=colors)

        fig, ax = plt.subplots()
        ax.add_collection(bars)
        ax.autoscale()
        loc = mdates.DayLocator(interval=1)
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(loc))

        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
        plt.show()
        
class mapWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        lat = 33.506130
        lon = -112.351440
        addr1 = "1234 E Test St"
        addr2 = "Litchfield Park, AZ 89053"
        box = self.ids.box

        #Initialize map view
        map_view = MapView(lat=lat, lon=lon, zoom=13)
        map_view.map_source = "osm"

        mark1 = MapMarker(lat=lat, lon=lon, source="data/icons/marker.png")
        #mark1.bind(on_release=self.popupAddress)
        #address = Label(text='[color=000000]' + addr1 + ' [/color][color=000000] ' + addr2 + '[/color]',
    #markup = True, valign='middle', halign='center', pos=(350,285))
     #   mark1.add_widget(address)

        map_view.add_marker(mark1)
        box.add_widget(map_view)

    def showMap():
        sm.current = 'mapW'

class photoGallery(Screen):
    def showPhotos():
        sm.current = 'photo'

# class to display validation result
class logDataWindow(Screen):
    def runData(self):
        dataframeWindow.showDataframe()
    
    def runMap(self):
        mapWindow.showMap()

    def showGallery(self):
        photoGallery.showPhotos()
  
# class for managing screens
class windowManager(ScreenManager):
    pass
  
# kv file
kv = Builder.load_file('login.kv')
sm = windowManager()
  
# reading all the data stored
users=pd.read_csv('data/login.csv')

# adding screens
sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))
sm.add_widget(dataframeWindow(name='dfw'))
sm.add_widget(mapWindow(name='mapW'))
sm.add_widget(photoGallery(name='photo'))

# class that builds gui
class loginMain(App):
    def go_back(self):
        sm.current = 'logdata'
    def build(self):
        return sm

# driver function
if __name__=="__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    loginMain().run()
import kivy
from wetter import w as wetter
import ConfigParser
from kivy.app import App
import os
from kivy.uix.screenmanager import ScreenManager, Screen
from glob import glob
from os.path import join, dirname
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.label import Label
import time
from datetime import date
from datetime import datetime
kivy.require('1.9.1')

#owID 18623fdb375d1a3bde283a98f69bbd59

class Wetter(Screen):

    def dateToday(self):

        return str(date.today())

    def on_touch_down(self, touch):
        global SM
        SM.get_screen('menu')
        SM.transition.direction = 'down'
        SM.current = 'menu'
    def setLable(self):
        l = Label(text='Hello world')
        return l

    def getTemp(self,val):
        temp =wetter.getTemp('Heilbronn')
        return str(temp[val])


class GuestWLAN(Screen):
    pass
class MenuUI(Screen):
    pass
class Mopidy(Screen):

    def runMopedi(self):
        print ('Run Mopidy')


class FilenameList:
    filename = []
    i = 0

    def addDirectory(self, name):
        self.filename.extend(glob(join(name, '*')))

    def current(self):
        if self.i >= len(self.filename):
            return ''
        else:
            return self.filename[self.i]

    def next(self):
        if self.i+1 >= len(self.filename):
            self.i = 0
        else:
            self.i += 1
        return self.current()

class SlideShow(Screen):
    slide = ObjectProperty(None)
    list = FilenameList()

    def on_touch_down(self, touch):
        global SM
        SM.get_screen('menu')
        SM.transition.direction = 'left'
        SM.current = 'menu'

    def addDirectory(self, name):
        self.list.addDirectory(name)

    def update(self):
        self.slide.source = self.list.current()

    def next(self, dt):
        self.slide.source = self.list.next()

class WLAN(Screen):
    wlanssid = StringProperty(None)
    wlanpsk = StringProperty(None)
    android_qrcode = ObjectProperty(None)
    ios_qrcode = ObjectProperty(None)
    windows_qrcode = ObjectProperty(None)

    def updatesettings(self):
        wlancfg = ConfigParser.RawConfigParser()
        wlancfg.read('/var/guestwlan/wlan.cfg')
        self.wlanssid = wlancfg.get('WLAN', 'wlanssid')
        self.wlanpsk = wlancfg.get('WLAN', 'wlanpsk')
        self.android_qrcode.reload()
        self.ios_qrcode.reload()
        self.windows_qrcode.reload()

class ScreenManagement(ScreenManager):
    pass

class PowerOff(Screen):

    def rebootRPI(self):
        print "Reebooting .."
        os.system('sudo shutdown -r now')
        #reboot_statement = "sudo shutdown -r -f now"
        #popen_args = reboot_statement.split(" ")
        #Popen(popen_args, stdout=PIPE, stderr=PIPE)

    def shutdownRPI(self):
        print "ShutDOWN"
        os.system('sudo shutdown -h 0')


class Rasp(App):
    def build(self):
        global SM
        # the root is created in the KV file
        SM = self.root
        SlideShow = SM.get_screen('slideshow')
        SlideShow.addDirectory('/var/guestwlan/images')
        # Diashow starten
        SlideShow.update()
        Clock.schedule_interval(SlideShow.next, 10)
        return SM

if __name__ == "__main__":
    Rasp().run()
    #subprocess.call('mopidy')
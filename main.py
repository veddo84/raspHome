import kivy
import ConfigParser
import subprocess
from subprocess import Popen, PIPE
from kivy.app import App
import os
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from glob import glob
from os.path import join, dirname
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock
from datetime import datetime
kivy.require('1.9.1')


class GuestWLAN(Screen):
    pass
class MenuUI(Screen):
    pass
class Mopidy(Screen):

    def runMopedi(self):
        print ('Run Mopidy')
        subprocess.call('mopidy')



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
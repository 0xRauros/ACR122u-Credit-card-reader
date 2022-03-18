from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.graphics import Rectangle, Canvas, Line
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivymd.uix.card import MDSeparator
from kivymd.uix.list import TwoLineListItem

import CreditCardReader


class MainScreen(Screen):

    readers = None
    
    def scan_device(self, dt):
        
        
        readers = CreditCardReader.available_readers()
        
        if readers:
            self.ids.main_screen_msg.text = "Place the [b][color=3ee7dc]Credit[/color] Card[/b] in the terminal..."
            self.ids.device_label.text = "[b]Dev:\n " + str(readers[0]) + "[/b]"
            self.ids.scan_spinner.active = False
            
            self.scan_card()


        else:
            self.ids.main_screen_msg.text = "Connect the [b][color=3ee7dc]NFC[/color][/b] terminal..."
            self.ids.device_label.text = "[b]No device[/b]"
            self.ids.scan_spinner.active = True  
        

    def scan_card(self):
        if CreditCardReader.card_available()[0]: # If true
            self.manager.current = "info_screen"


    def on_enter(self):
        Clock.schedule_interval(self.scan_device, 0)
        


class InfoScreen(Screen):

    connection = None
    
    def on_enter(self):
        
        Clock.unschedule(MainScreen.scan_device)

        if CreditCardReader.card_available()[0]:
            self.set_credit_card_info()

        Clock.schedule_interval(self.scan_card, 0)


    def scan_card(self, dt):
        if not CreditCardReader.card_available()[0]:
            self.manager.current = "main_screen"
            Clock.unschedule(self.scan_card)
        
    
    def set_credit_card_info(self):
        '''
            For now only VISA type is available
        '''
        try:
            info = CreditCardReader.get_VISA_info() # Dictionary
        except Exception as e:
            print(e)
            self.manager.current = "main_screen"

        self.ids.card_name.text = "[b]" + info["[50] - Application Label"] + "[/b]"
        self.ids.pan.text = "[b]" + info["Primary Account Number (PAN)"] + "[/b]"
        self.ids.ed.text = "[b]Expiration Date > " + info["Expiration Date"] + "[/b]"
        
        for k, v in info.items():
            label = Label(text="[b][size=22][color=3ee7dc]"+ k +"[/size][/color]\n" + v + "[/b]", 
                           size_hint_y=None, height=60, 
                           font_size=14, halign="center")

            self.ids.info_list.add_widget(label)

            
            pass



class WarningScreen(Screen):
    pass


class CreditCardReaderApp(MDApp):

    def build(self):

        self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = "BlueGray"

        sm = ScreenManager()
        #sm.add_widget(WarningScreen(name="warning_screen"))
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(InfoScreen(name="info_screen"))
        
        return sm

    


def load_config():

    Config.set("graphics", "resizeable", True)

    LabelBase.register(name="Roboto",
                    fn_regular="assets/fonts/roboto/Roboto-Thin.ttf",
                    fn_bold="assets/fonts/roboto/Roboto-Medium.ttf")
    LabelBase.register(name="Slkscr",
                    fn_regular="assets/fonts/slkscr/slkscr.ttf",
                    fn_bold="assets/fonts/slkscr/slkscrb.ttf")
    LabelBase.register(name="ModernPictograms",
                    fn_regular="assets/fonts/modern_pictograms/modernpics.ttf")


if __name__ == "__main__":
    Window.clearcolor = get_color_from_hex("#454545")
    load_config()
    CreditCardReaderApp().run()
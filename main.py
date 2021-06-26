from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
import re
import json
import requests
from bs4 import BeautifulSoup

#from kivy.core.window import Window
#Window.size = (360, 640)



# example link:    http://loveread.ec/read_book.php?id=2317&p=1



class MainApp(MDApp):  
    
# LOADING BOOK
# ADAPTING TEXT
    def load_file(self, *args):
        try:
            if self.url_input.text[:36] != "http://loveread.ec/read_book.php?id=":
                return
            self.url_basic = self.url_input.text
            self.box.remove_widget(self.one_word)
            self.box.remove_widget(self.arrow_bottom)
            self.screen.remove_widget(self.box)
            self.page =1
            self.index=0
            self.url = self.url_basic[0:-1]+str(self.page)
            self.r = requests.get(self.url)
            soup = BeautifulSoup(self.r.content, 'html.parser')
            self.text_class = soup.find(True, class_="MsoNormal")
            self.text = self.text_class.get_text()
            self.text = self.text.lower()
            self.words_list = [re.sub(r"[^а-яА-Яa-zёЁA-Z0-9-]+", ' ', k) for k in self.text.split()]
            self.word = self.words_list[1:]
            self.button_next.text = f"page {self.page+1}"
            self.button_previous.text = f"page {self.page-1}"
            self.box.add_widget(self.one_word)
            self.box.add_widget(self.arrow_bottom)
            self.screen.add_widget(self.box)
            self.one_word.text = f"Page {self.page}"
            self.nav = soup.find(True, class_="navigation")
            self.pages_list = self.nav.get_text()
            self.i = self.pages_list.find("…")
            if self.i <0:
                self.j = self.pages_list.find("Вперед")
                if self.pages_list[self.j-2:self.j] == str(10):
                    self.last_page = self.pages_list[self.j-2:self.j]
                    self.write_json()
                else:
                    self.last_page = self.pages_list[self.j-1:self.j]
                    self.write_json()
            else:
                self.j = self.pages_list.find("Вперед")
                self.last_page = self.pages_list[self.i+1:self.j]
                self.write_json()
            self.page_input.helper_text = f"max: {self.last_page}"
            self.write_json()
        except:
            return
        
# BUILDING APLICATION   
    def build(self): 
        self.data = json.load(open('data.json','r'))
# TAKING DATA FROM JSON
        if bool(self.data) == True:
            self.url = self.data["book"]
            self.page = int(self.data["page"])
            self.last_page = int(self.data["last_page"])
            self.speed_words = int(self.data["speed"])
            for i in range(len(str(self.page))):
                    self.url = str(self.url)[:-1]
            self.url = self.url+str(self.page)
            self.write_json()
            self.r = requests.get(self.url)
            soup = BeautifulSoup(self.r.content, 'html.parser')
            self.text_class = soup.find(True, class_="MsoNormal")
            self.text = self.text_class.get_text()
            self.text = self.text.lower()
            self.words_list = [re.sub(r"[^а-яА-Яa-zёЁA-Z0-9-]+", ' ', k) for k in self.text.split()]
            self.word = self.words_list[1:]
            self.index=0
# TAKING DEFAULT DATA
        else:         
            self.page = 1
            self.last_page = 0
            self.index = 0
            self.speed_words = 180
        self.screen = Screen()
        self.theme_cls.theme_style = "Dark"
# INPUTS
        self.url_input = MDTextField(pos_hint={'center_x':.4, 'center_y':.9},size_hint_x= .6,hint_text = "link to the book",helper_text = "only from loveread.ec website",helper_text_mode = "on_focus")
        self.screen.add_widget(self.url_input)
        self.page_input = MDTextField(pos_hint={'center_x':.41, 'center_y':.5},size_hint_x= .15,hint_text = "to page:",helper_text = f"max: {self.last_page}",helper_text_mode = "on_focus")
        self.screen.add_widget(self.page_input)
# BUTTONS        
        self.button_load = MDFlatButton(text ="apply",on_press = self.load_file,pos_hint={'center_x':.85, 'center_y':.9},theme_text_color= "Custom",text_color =  (0, 0.7, 1, 1))
        self.screen.add_widget(self.button_load)
        self.button_start = MDFlatButton(text ="start",theme_text_color= "Custom",text_color =  (0, 0.7, 1, 1),on_press = self.btn_start,pos_hint={'center_x':.5, 'center_y':.6})
        self.screen.add_widget(self.button_start)
        self.button_next = MDFlatButton(text =f"page {self.page+1}",on_press = self.next_page,pos_hint={'center_x':.7, 'center_y':.6})
        self.screen.add_widget(self.button_next)
        self.button_previous = MDFlatButton(text =f"page {self.page-1}",on_press = self.previous_page,pos_hint={'center_x':.3, 'center_y':.6})
        self.screen.add_widget(self.button_previous)
        self.back_word_button = MDFlatButton(text = "<<",pos_hint={'center_x':.15, 'center_y':.7},font_size= "14sp",theme_text_color= "Custom",text_color =  (1, 1, 1, 1),on_release = self.back_word)
        self.screen.add_widget(self.back_word_button)
        self.plus_speed = MDFlatButton(text = "faster",pos_hint={'center_x':.7, 'center_y':.8},font_size= "14sp",theme_text_color= "Custom",text_color =  (1, 1, 1, 1),on_release = self.change_speed_plus)
        self.screen.add_widget(self.plus_speed)
        self.minus_speed = MDFlatButton(text = "slower",pos_hint={'center_x':.3, 'center_y':.8},font_size= "14sp",theme_text_color= "Custom",text_color =  (1, 1, 1, 1),on_release = self.change_speed_minus)
        self.screen.add_widget(self.minus_speed)
        self.button_page = MDFlatButton(text ="go",on_press = self.to_page,pos_hint={'center_x':.62, 'center_y':.5},theme_text_color= "Custom",text_color =  (0, 0.7, 1, 1))
        self.screen.add_widget(self.button_page)
# LABELS       
        self.box = MDBoxLayout(orientation="vertical",pos_hint={'center_x':.6, 'center_y':.7},size_hint_x= .7,size_hint_y = .11)      
        self.arrow_top = MDLabel(text=" "*8+"|", halign="left",pos_hint={'center_y':.95},theme_text_color= "Custom",text_color =  (1, 0, 0, 0.8))
        self.box.add_widget(self.arrow_top)
        self.arrow_bottom = MDLabel(text=" "*8+"|", halign="left",pos_hint={'center_y':.05},theme_text_color= "Custom",text_color =  (1, 0, 0, 0.8))
        self.speed = MDLabel(text=str(self.speed_words), halign="center",theme_text_color= "Custom",text_color =  (0, 0.7, 1, 1),pos_hint={'center_x':.5, 'center_y':.8} )
        self.screen.add_widget(self.speed)
# WORD
        self.one_word = MDLabel(text=f"Page {self.page}", halign="left",font_style="H5")
        self.box.add_widget(self.one_word)
        self.box.add_widget(self.arrow_bottom)
        self.screen.add_widget(self.box)
        self.write_json()
        return self.screen
    
# PRESS ON START        
    def btn_start(self, *args):
        if self.button_start.text == "start" or self.button_start.text == "restart page":
            self.button_start.text = "pause"
            self.screen.remove_widget(self.url_input)
            self.screen.remove_widget(self.button_load)
            self.screen.remove_widget(self.speed)
            self.screen.remove_widget(self.plus_speed)
            self.screen.remove_widget(self.minus_speed)
            self.screen.remove_widget(self.button_next)
            self.screen.remove_widget(self.button_previous)
            self.screen.remove_widget(self.back_word_button)
            self.screen.remove_widget(self.page_input)
            self.screen.remove_widget(self.button_page)
            self.interval = Clock.schedule_interval(self.word_change, 60/float(self.speed.text))
            self.write_json()
        elif self.button_start.text == "pause":
            self.button_start.text = "start"
            self.interval.cancel()
            self.screen.add_widget(self.speed)
            self.screen.add_widget(self.plus_speed)
            self.screen.add_widget(self.minus_speed)
            self.screen.add_widget(self.button_next)
            self.screen.add_widget(self.button_previous)
            self.screen.add_widget(self.url_input)
            self.screen.add_widget(self.button_load)
            self.screen.add_widget(self.back_word_button)
            self.screen.add_widget(self.page_input)
            self.screen.add_widget(self.button_page)
            self.write_json()
            
# CHANGING WORD  
    def word_change(self,*args):
        try:
            if len(self.word) == 0:
                self.button_start.text = "restart page"
                self.word = self.words_list[1:]
                self.interval.cancel()
                self.write_json()
            else:
                self.box.remove_widget(self.one_word)
                self.box.remove_widget(self.arrow_bottom)
                self.screen.remove_widget(self.box)
                self.one_word.text =  self.word[self.index]
                self.index = self.index +1
                self.box.add_widget(self.one_word)
                self.box.add_widget(self.arrow_bottom)
                self.screen.add_widget(self.box)
        except:
            self.btn_start(self,*args)
            
# CHANGING SPEED
    def change_speed_plus(self,*atgs):
        self.speed_words = int(self.speed.text)
        if self.speed_words >= 500:
            return
        self.speed_words += 10
        self.speed.text = str(self.speed_words)
        self.write_json()
    def change_speed_minus(self,*atgs):
        self.speed_words = int(self.speed.text)
        if self.speed_words <= 60:
            return
        self.speed_words -= 10
        self.speed.text = str(self.speed_words)
        self.write_json()
        
# SWIPE PAGE
    def next_page(self,*args):
        try:
            if int(self.last_page) == int(self.page):  
                return
            else:
                self.box.remove_widget(self.one_word)
                self.box.remove_widget(self.arrow_bottom)
                self.screen.remove_widget(self.box)
                self.page = self.page+1
                self.index=0
                try:
                    self.url = self.url_basic[0:-1]+str(self.page)
                    self.write_json()
                except:
                    self.url = self.data["book"]
                    for i in range(len(str(self.page))):
                        self.url = str(self.url)[:-1]
                    self.url = self.url+str(self.page)
                    self.write_json()
                self.r = requests.get(self.url)
                soup = BeautifulSoup(self.r.content, 'html.parser')
                self.text_class = soup.find(True, class_="MsoNormal")
                self.text = self.text_class.get_text()
                self.text = self.text.lower()
                self.words_list = [re.sub(r"[^а-яА-Яa-zёЁA-Z0-9-]+", ' ', k) for k in self.text.split()]
                self.word = self.words_list[1:]
                self.button_next.text = f"page {self.page+1}"
                self.button_previous.text = f"page {self.page-1}"
                self.box.add_widget(self.one_word)
                self.box.add_widget(self.arrow_bottom)
                self.screen.add_widget(self.box)
                self.one_word.text = f"Page {self.page}"
                self.write_json()
          
        except:
            self.page = 1
            self.btn_start(self,*args)  
            self.box.add_widget(self.one_word)
            self.box.add_widget(self.arrow_bottom)
            self.screen.add_widget(self.box)
            self.one_word.text = f"Page {self.page}"
        
    def previous_page(self,*args):
        try:
            if self.page <=1:
                return
            else:
                self.box.remove_widget(self.one_word)
                self.box.remove_widget(self.arrow_bottom)
                self.screen.remove_widget(self.box)
                self.page = self.page-1
                self.index=0
                try:
                    self.url = self.url_basic[0:-1]+str(self.page)
                    self.write_json()
                except:
                    self.url = self.data["book"]
                    for i in range(len(str(self.page))):
                        self.url = str(self.url)[:-1]
                    self.url = self.url+str(self.page)
                    self.write_json()
                self.r = requests.get(self.url)
                soup = BeautifulSoup(self.r.content, 'html.parser')
                self.text_class = soup.find(True, class_="MsoNormal")
                self.text = self.text_class.get_text()
                self.text = self.text.lower()
                self.words_list = [re.sub(r"[^а-яА-Яa-zёЁA-Z0-9-]+", ' ', k) for k in self.text.split()]
                self.word = self.words_list[1:]
                self.button_next.text = f"page {self.page+1}"
                self.button_previous.text = f"page {self.page-1}"
                self.box.add_widget(self.one_word)
                self.box.add_widget(self.arrow_bottom)
                self.screen.add_widget(self.box)
                self.one_word.text = f"Page {self.page}"
                self.write_json()
        except:
            self.page = 1
            self.btn_start(self,*args) 
            self.box.add_widget(self.one_word)
            self.box.add_widget(self.arrow_bottom)
            self.screen.add_widget(self.box)
            self.one_word.text = f"Page {self.page}"
            self.write_json()
            
# CHOOSING PAGE
    def to_page (self, *args):
        try:
            if int(self.page_input.text) > int(self.last_page) or int(self.page_input.text)<1:
                return
            self.box.remove_widget(self.one_word)
            self.box.remove_widget(self.arrow_bottom)
            self.screen.remove_widget(self.box)
            self.page = int(self.page_input.text)
            self.index=0
            try:
                self.url = self.url_basic[0:-1]+str(self.page)
                self.write_json()
            except:
                self.url = self.data["book"]
                for i in range(len(str(self.page))):
                    self.url = str(self.url)[:-1]
                self.url = self.url+str(self.page)
                self.write_json()
            self.r = requests.get(self.url)
            soup = BeautifulSoup(self.r.content, 'html.parser')
            self.text_class = soup.find(True, class_="MsoNormal")
            self.text = self.text_class.get_text()
            self.text = self.text.lower()
            self.words_list = [re.sub(r"[^а-яА-Яa-zёЁA-Z0-9-]+", ' ', k) for k in self.text.split()]
            self.word = self.words_list[1:]
            self.button_next.text = f"page {self.page+1}"
            self.button_previous.text = f"page {self.page-1}"
            self.box.add_widget(self.one_word)
            self.box.add_widget(self.arrow_bottom)
            self.screen.add_widget(self.box)
            self.one_word.text = f"Page {self.page}"
            self.write_json()
        except:
            return
            
# TO PREVIOUS WORD           
    def back_word (self, *args):
        if self.index == 0:
            return
        self.box.remove_widget(self.one_word)
        self.box.remove_widget(self.arrow_bottom)
        self.screen.remove_widget(self.box)
        self.index = self.index -1
        self.one_word.text =  self.word[self.index-1]
        self.box.add_widget(self.one_word)
        self.box.add_widget(self.arrow_bottom)
        self.screen.add_widget(self.box)
        self.write_json()
       
# WRITE TO JSON
    def write_json(self,*args):
        try:
            self.data["book"] = str(self.url)
            self.data["page"] = str(self.page)
            self.data["last_page"] = str(self.last_page)
            self.data["speed"] = str(self.speed_words)
            with open('data.json', 'w') as f:
                f.write(json.dumps(self.data))
            return
        except:
            return

MainApp().run()

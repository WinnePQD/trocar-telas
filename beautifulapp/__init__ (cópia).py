from beautifulapp.screens.main_screen import MainScreen
from kivy_reloader.app import App
from kivy_reloader.app import *
import os

import requests
import ssl
import certifi

import shutil
import trio
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.utils import platform
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.app import App
import urllib.request
from shutil import copyfile
from plyer import storagepath
from os.path import join, exists
from os import makedirs
from kivy.clock import Clock
from kivyauth.google_auth import initialize_google, login_google, logout_google
from kivyauth.utils import stop_login
from kivyauth.utils import login_providers, auto_login
import json

ssl._create_default_https_context = ssl._create_unverified_context




GOOGLE_CLIENT_ID = ("895349539092-rou61d94s6817ijaa3ka9d5ro90op0du.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = "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"


if platform != "android":

    Window.size = (406, 762)
    Window.always_on_top = True

class MainApp(MDApp, App):
    foto = NumericProperty(0)
    def build(self):

        #coloquei
        current_provider = ""
        camin = ''

#########começo####################
        if platform == 'android':
          #  self.picker = ImagePickerAndroid()
            print('self.picker.bind1')


        else:
            # Windows, Linux, MacOS, ios
           # self.picker = ImagePicker()


            print('self.picker.bind2')

      #  self.picker.bind(on_image_selected=self.on_image_selected)
        print('self.picker.bind3')

    @mainthread
    def open_file_manager(self):
        self.picker.choose(self.screen_manager.get_screen('Cadastro Screen').ids.user_photo)


    @mainthread
    def on_image_selected(self, inst, path: str):
       # print(path)
        self.screen_manager.get_screen('Cadastro Screen').ids.user_photo.source = path

        Clock.schedule_once(self.mudar_tela, 2)
       # Clock.schedule_interval(mudar_tela, 2)

    def mudar_tela(self, dt):
        downloads_dir = storagepath.get_downloads_dir()
        tmp_path = join(downloads_dir, "Price/")
        for nome in os.listdir(tmp_path):
            antesnome = tmp_path + nome
            novonome= tmp_path + '/user' + ".jpg"
            os.rename(antesnome,novonome)
            print(os.listdir(downloads_dir))
        #print(path)
        print('on image select')



        print('open file manager')

       # print(path)

    ##########fim######################
    def build_and_reload(self, initialize_server=True):
        self.kivy_reloader = App(initialize_server)
        self.screen_manager = self.App.screen_manager
        initial_screen = 'Main Screen'
       # initial_screen ='Lote Screen'
        try:
            link = "https://test-a6800-default-rtdb.firebaseio.com/"
            requisicao = requests.get(f"{link}/cadastro/.json")
            dic_requisicao = requisicao.json()

            with open(self.camin+'data.json', 'r') as data:
                print(self.camin)

                ver_json = json.load(data)
                print(self.camin)

            for id_venda in dic_requisicao:
                ver_senha = dic_requisicao[id_venda]["senha"]
                ver_email = dic_requisicao[id_venda]["email"]

                if ver_senha == ver_json['senha']:
                    print(id_venda)
                    self.id_senha = id_venda

            requisicao = requests.get(f"{link}/cadastro/{id_venda}.json")
            print(requisicao.json)
            print(requisicao.text)

            if ver_json['senha'] == ver_senha and ver_json['email'] == ver_email:
                print('deu certo')
                print(self.camin)
                #self.change_screen('Buscar Screen')
                #self.change_screen('Lote Screen')
                self.change_screen('Main Screen')
                print(self.camin)

            else:
                print('deu erradoo')
                self.change_screen(initial_screen)
                print(self.camin)

        except FileNotFoundError:
            self.change_screen(initial_screen)

        except Exception as e:
            print("Error while changing screen winne: \n")
            print(e)
            return False

        Clock.schedule_once(self.set_window_pos)
        return self.reloader

    def set_window_pos(self, *args):
        if platform != "android":
            Window._set_window_pos(4410, 470)

    def change_screen(self, screen_name, toolbar_title=None):
        #print(f"Changing screen to {screen_name}")
        if screen_name not in self.screen_manager.screen_names:
            screen_object = self.get_screen_object_from_screen_name(screen_name)
            self.screen_manager.add_widget(screen_object)

        self.screen_manager.current = screen_name

    def get_screen_object_from_screen_name(self, screen_name):
        # Parsing module 'my_screen.py' and object 'MyScreen' from screen_name 'My Screen'
        screen_module_in_str = "_".join([i.lower() for i in screen_name.split()])
        screen_object_in_str = "".join(screen_name.split())

        if platform == "android":
            self.unload_python_files_on_android(screen_module_in_str)

        # Importing screen object
        exec(f"from screens.{screen_module_in_str} import {screen_object_in_str}")

        # Instantiating the object
        screen_object = eval(f"{screen_object_in_str}()")

        return screen_object

    def on_start(self):
        self.camin = App.get_running_app().user_data_dir + '/'
        if platform == "android":
            print('teste')

            pass

        initialize_google(
            self.after_login,
            self.error_listener,
            GOOGLE_CLIENT_ID,
            GOOGLE_CLIENT_SECRET,
        )

    def Login(self):
        login_google()

    def Login2(self):
        pass

    def logout_(self):
        if self.current_provider == login_providers.google:
            logout_google(self.after_logout)


    @mainthread
    def after_login(self, name, email, photo_uri):

        self.update_ui(name, email, photo_uri)

    @mainthread
    def update_ui(self, name, email, photo_uri):

        App.get_running_app().change_screen("Cadastro Screen")

        self.screen_manager.get_screen('Cadastro Screen').ids.nome.text = ("{}".format(name))
        print(name)
        self.screen_manager.get_screen('Cadastro Screen').ids.user_photo.source = photo_uri
        self.screen_manager.get_screen('Cadastro Screen').ids.text_email.text = ("{}".format(email))

        # URL a ser baixada

        downloads_dir = storagepath.get_downloads_dir()
        new_folder_path = join(downloads_dir, "Price")

        # Create the directory if it doesn't exist
        if not exists(new_folder_path):
            makedirs(new_folder_path)

        # Baixando e armazenando a imagem no caminho especificado

        urllib.request.urlretrieve(photo_uri, str(new_folder_path + '/user.jpg'))

    def after_logout(self):
        pass

    def error_listener(self):
        pass




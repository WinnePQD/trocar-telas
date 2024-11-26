import os

from kivy.factory import Factory as F
import sys
from kivy.core.window import Window
from kivy.clock import Clock

from kivy_reloader.utils import load_kv_path
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen,ScreenManager

from kivy.uix.boxlayout import BoxLayout
from kivy import platform

#from kivyauth.google_auth import initialize_google, login_google, logout_google
#from kivyauth.utils import stop_login
#from kivyauth.utils import login_providers, auto_login
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
import certifi
import json
from kivy.app import App
#from screens.cadastro_screen import *


main_screen_kv = os.path.join("beautifulapp", "screens", "main_screen.kv")
load_kv_path(main_screen_kv)


GOOGLE_CLIENT_ID = ("895349539092-m7umj1ni4ac8damuq2j1gg9efl5e7s36.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = "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"


os.environ["SSL_CERT_FILE"] = certifi.where()
link = "https://test-a6800-default-rtdb.firebaseio.com/"

if platform == "android":
    from android.runnable import run_on_ui_thread
    from jnius import autoclass, cast

    Toast = autoclass("android.widget.Toast")
    String = autoclass("java.lang.String")
    CharSequence = autoclass("java.lang.CharSequence")
    Intent = autoclass("android.content.Intent")
    Uri = autoclass("android.net.Uri")
    LayoutParams = autoclass("android.view.WindowManager$LayoutParams")
    AndroidColor = autoclass("android.graphics.Color")

    PythonActivity = autoclass("org.kivy.android.PythonActivity")

    context = PythonActivity.mActivity


    @run_on_ui_thread
    def show_toast(text):
        t = Toast.makeText(
            context, cast(CharSequence, String(text)), Toast.LENGTH_SHORT
        )
        t.show()


    def set_statusbar_color():
        window = context.getWindow()
        window.addFlags(LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
        window.setStatusBarColor(AndroidColor.TRANSPARENT)


class MainScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def conect(self,*args):
        try:

            requisicao = requests.get(f"{link}/cadastro/.json")
            dic_requisicao = requisicao.json()


            for id_venda in dic_requisicao:

                self.password = dic_requisicao[id_venda]["senha"]
                self.email = dic_requisicao[id_venda]["email"]
                self.nomes = dic_requisicao[id_venda]["nome"]



            self.text_email = self.ids.text_email.text
            self.text_password = self.ids.text_password.text
            print(self.text_email)


            if self.email==self.text_email and self.password== self.text_password:
                if platform == "android":
                    show_toast(text="Bem vindo {}".format(self.nomes))
                    App.get_running_app().change_screen('Buscar Screen')



                else:
                    popup = Popup(title='CODIGO', title_color=[47 / 255., 167 / 255., 212 / 255., 1.],
                                  title_align='center',
                                  separator_color=[1, 1, 1, 1],
                                  background_color=[0, 0, 0, 1],

                                  content=Label(text="Bem vindo {}".format(self.nomes)),

                                  size_hint=(None, None), size=(dp(200), dp(200)))

                    popup.open()
                    App.get_running_app().change_screen('Buscar Screen')


            else:
                if platform == "android":
                    show_toast(text="email ou senha incorretos")

                else:


                    popup = Popup(title='CODIGO', title_color=[47 / 255., 167 / 255., 212 / 255., 1.],
                                  title_align='center',
                                  separator_color=[1, 1, 1, 1],
                                  background_color=[0, 0, 0, 1],

                                  content=Label(text="email ou senha incorretos"),

                                  size_hint=(None, None), size=(dp(200), dp(200)))

                    popup.open()
                    print(self.text_email)

        except requests.ConnectionError:
            if platform == "android":
                show_toast(text="sem internet")
            else:
                popup = Popup(title='CODIGO', title_color=[47 / 255., 167 / 255., 212 / 255., 1.],
                              title_align='center',
                              separator_color=[1, 1, 1, 1],
                              background_color=[0, 0, 0, 1],

                              content=Label(text="sem internet"),

                              size_hint=(None, None), size=(dp(200), dp(200)))

                popup.open()



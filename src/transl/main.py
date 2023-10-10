import flet as ft
import threading

from transl.translate import translate_en2ja, translate_ja2en

class CallIfNotCalled:
    def __init__(self, function, delay=1.0):
        self.function = function
        self.delay = delay
        self.timer = None

    def called(self):
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(self.delay, self.function)
        self.timer.start()

    def stop(self):
        if self.timer:
            self.timer.cancel()


def main(page: ft.Page):
    page.title = "transL"
    page.theme_mode = ft.ThemeMode.DARK

    def chg_lang(_e):
        c12.content = ft.Text("Japanese" if lang.value == "English" else "English")
        page.update()

    def text_change(_e):
        caller.called()

    def update_after():
        caller.stop()
        if lang.value == "English":
            tf2.value = translate_en2ja(tf1.value)
        else:
            tf2.value = translate_ja2en(tf1.value)
        page.update()

    caller = CallIfNotCalled(update_after, delay=1)

    lang = ft.Dropdown(
        label="Language",
        options=[
            ft.dropdown.Option("Japanese"),
            ft.dropdown.Option("English"),
        ],
        autofocus=True,
        on_change=chg_lang,
        value="Japanese",
    )

    c11 = ft.Container(
        content=lang,
        alignment=ft.alignment.center,
        expand=True,
    )
    c12 = ft.Container(
        content=ft.Text("English"),
        alignment=ft.alignment.center,
        expand=True,
    )
    c10 = ft.Row([c11, c12])

    tf1 = ft.TextField(
        label="before",
        hint_text="Please enter text here",
        border=ft.InputBorder.NONE,
        filled=True,
        multiline=True,
        on_change=text_change,
    )
    tf2 = ft.TextField(
        label="after",
        border=ft.InputBorder.NONE,
        filled=True,
        multiline=True,
        disabled=True,
    )
    
    c21 = ft.Container(
        content=tf1,
        alignment=ft.alignment.center,
        expand=True,
    )
    c22 = ft.Container(
        content=tf2,
        alignment=ft.alignment.center,
        expand=True,
    )
    c20 = ft.Row([c21, c22])

    c = ft.Column([c10, c20])

    page.add(c)

ft.app(target=main)

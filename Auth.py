from tkinter import *
from tkinter.font import Font
from tkinter.messagebox import showerror
from FileManager import FileManager


class Auth:
    AUTH: str = "auth.txt"  # файл аутентификации

    def __init__(self):
        self.logins = read_auth(Auth.AUTH)  # данные аутентификации

        self.window: Tk = Tk()
        self.top_frame = LabelFrame(self.window)
        self.bottom_frame = LabelFrame(self.window)
        self.login = Entry(self.top_frame)
        self.password = Entry(self.bottom_frame)

        self.configure_window()

    # настройка окна
    def configure_window(self):
        self.window.geometry("250x150")
        self.window.resizable(0, 0)
        self.window.title("Log in to your account")
        self.window.configure(padx=10, pady=10, bg="#20805E")
        self.window.bind("<Return>", self.auth)

        self.top_frame.configure(font=Font(size=9, weight="bold"), text="Login", pady=10, bg="#20805E")
        self.top_frame.pack(fill=BOTH)

        self.login.configure(font=Font(size=9, weight="bold"), bg="#000000", fg="#FFFFFF")
        self.login.pack()

        self.bottom_frame.configure(font=Font(size=9, weight="bold"), text="Password", pady=10, bg="#20805E")
        self.bottom_frame.pack(fill=BOTH)

        self.password.configure(show="*", font=Font(size=9, weight="bold"), bg="#000000", fg="#FFFFFF")
        self.password.pack()

        self.window.mainloop()

    # проверка логина и пароля
    def auth(self, event: Event):
        login: str = self.login.get()
        password: str = self.password.get()
        self.password.delete(0, END)
        if login != "" and password != "":
            if login in self.logins.keys():
                if password == self.logins[login]:
                    self.window.destroy()
                    FileManager()
                else:
                    showerror("Warning", "Неправильный логин или пароль")
            else:
                add_auth(Auth.AUTH, login, password)
                self.window.destroy()
                FileManager()


# получение данных об аутентификации
def read_auth(filename: str) -> dict:
    with open(filename, "r") as file:
        auth: dict = dict()
        for row in file:
            try:
                login: str = row.split(":")[0]
                password: str = row.split(":")[1][:-1]
                auth[login] = password
            except:
                pass
        else:
            return auth


# добавление данных аутентификации
def add_auth(filename: str, login: str, password: str):
    with open(filename, "a") as file:
        file.write(f"{login}:{password}\n")

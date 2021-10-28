import os
import shutil
from tkinter import *
from tkinter.font import Font
from tkinter.messagebox import showerror
from zipfile import ZipFile
from json import load


class FileManager:
    SETTINGS: str = "settings.json"

    def __init__(self):
        self.window: Tk = Tk()  # окно
        self.top_frame: Frame = Frame(self.window)  # верхнее поле для текстовых полей
        self.bottom_frame: Frame = Frame(self.window)  # нижнее поле для поля ввода и вывода текущего пути
        self.file_list: Listbox = Listbox(self.top_frame, width=30, height=20)  # доступные каталоги
        self.file_content: Listbox = Listbox(self.top_frame, width=70, height=20)  # содержимое файла
        self.text: StringVar = StringVar()  # переменная для хранения текущего пути для его вывода
        self.label: Label = Label(self.bottom_frame, width=96, textvariable=self.text)  # текущий путь
        self.console: Entry = Entry(self.bottom_frame, width=96)  # поле ввода
        self.commands: dict = {
            "createdir": self.create_dir,  # создать каталог: createdir dirname
            "removedir": self.remove_dir,  # удалить каталог: removedir dirname
            "changedir": self.change_dir,  # сменить каталог: changedir path
            "createfiles": self.create_files,  # создать пустые текстовые файлы: createfiles filename1 ... filenameN
            "writefile": self.write_file,  # добавить в файл текст: writefile filename text
            "readfile": self.read_file,  # вывести содержимое файла: readfile filename
            "removefiles": self.remove_files,  # создать каталог: removefiles filename1 ... filenameN
            "copyfiles": self.copy_files,  # создать каталог: copyfiles dirname
            "movefiles": self.move_files,  # создать каталог: movefiles filename1 ... filenameN dirname
            "renamefile": self.rename_file,  # создать каталог: renamefile old_name new_name
            "archive": self.archive,  # архифировать файлы: archive filename1 ... filenameN
            "extract": self.extract  # разархифировать архив: extract archive_name
        }
        self.root: str = self.set_root()  # текущий путь
        self.path: str = ""  # видимый для пользователя путь
        self.configure_window()  # настройка окна

    # установка корневого каталога
    @staticmethod
    def set_root():
        with open(FileManager.SETTINGS, "r") as settings:
            root_dir: str = load(settings)["directory"].replace("\\", "\\\\")
        os.chdir(root_dir)
        return os.getcwd()

    # настройка окна
    def configure_window(self):
        self.window.title("File manager")
        self.window.bind('<Return>', self.get_command)
        self.window.resizable(0, 0)
        self.top_frame.configure(bg="#20805E")
        self.bottom_frame.configure(bg="#20805E")
        self.top_frame.pack(fill=BOTH)
        self.bottom_frame.pack(fill=BOTH)
        self.file_list.pack(side=LEFT, padx=10, pady=10)
        self.file_list.configure(font=Font(size=9, weight="bold"), bg="#000000", fg="#FFFFFF",
                                 selectbackground="#FFFFFF", selectforeground="#000000")
        self.file_content.pack(side=RIGHT, padx=10, pady=10)
        self.file_content.configure(font=Font(size=9, weight="bold"), bg="#000000", fg="#FFFFFF",
                                    selectbackground="#FFFFFF", selectforeground="#000000")
        self.label.pack(side=TOP, padx=10)
        self.label.configure(font=Font(size=9, weight="bold"), bg="#000000", fg="#FFFFFF", anchor=W)
        self.console.pack(side=TOP, padx=10, pady=2)
        self.console.configure(font=Font(size=9, weight="bold"), bg="#000000", fg="#FFFFFF")
        self.display_dir_content()
        self.display_path()
        self.window.mainloop()

    # отображение каталогов и файлов в текущем каталоге
    def display_dir_content(self):
        self.file_list.delete(0, END)
        for file in os.listdir(os.getcwd()):
            self.file_list.insert(END, file)

    # отображение текущего пути
    def display_path(self):
        self.text.set(self.path)

    # отображение содержимого файла
    def display_content(self, content: list):
        self.file_content.delete(0, END)
        for line in content:
            self.file_content.insert(END, line)

    # считывание и выполнение команды из поля ввода
    def get_command(self, event: Event):
        line = self.console.get().split(" ")
        self.console.delete(0, END)
        if len(line) > 0:
            command, arguments = line[0], line[1:]
            if command in self.commands.keys():
                self.commands[command](*arguments)
            else:
                showerror("Warning", "There is no such command")
            self.display_path()

    # создание нового каталога
    def create_dir(self, *args):
        if len(args) > 1:
            showerror("Warning", "Too many arguments")
        else:
            dirName: str = args[0]
            try:
                os.mkdir(os.getcwd() + os.sep + dirName)
                self.display_dir_content()
            except Exception as e:
                showerror("Warning", str(e))

    # удаление каталога
    def remove_dir(self, *args):
        if len(args) > 1:
            showerror("Warning", "Too many arguments")
        else:
            dirName: str = args[0]
            try:
                shutil.rmtree(os.getcwd() + os.sep + dirName)
                self.display_dir_content()
            except Exception as e:
                showerror("Warning", str(e))

    # изменение текущего каталога
    def change_dir(self, *args):
        if len(args) > 1:
            showerror("Warning", "Too many arguments")
        else:
            try:
                temp_path: str = os.getcwd()
                os.chdir(args[0])
                if self.root not in os.getcwd():
                    showerror("Warning", "Incorrect path")
                    os.chdir(temp_path)
                else:
                    self.path = os.getcwd().replace(self.root, "")
                    self.display_dir_content()
            except Exception as e:
                showerror("Warning", str(e))

    # создание пустых текстовых файлов
    def create_files(self, *args):
        try:
            for file_name in args:
                if ".txt" not in file_name:
                    file_name += ".txt"
                open(file_name, 'a').close()
            self.display_dir_content()
        except Exception as e:
            showerror("Warning", str(e))

    # дозапись в текстовый файл
    def write_file(self, *args):
        if len(args) < 2:
            showerror("Warning", "Too few arguments")
        else:
            try:
                file_name: str = args[0]
                data: tuple = args[1:]
                with open(file_name, 'a') as file:
                    file.write(" ".join(data) + "\n")
                self.display_dir_content()
            except Exception as e:
                showerror("Warning", str(e))

    # вывод содержимого файла
    def read_file(self, *args):
        if len(args) > 1:
            showerror("Warning", "Too many arguments")
        else:
            try:
                file_name = args[0]
                with open(file_name, 'r') as file:
                    self.display_content(file.readlines())
            except Exception as e:
                showerror("Warning", str(e))

    # удаление файлов
    def remove_files(self, *file_names):
        try:
            for file_name in file_names:
                os.remove(file_name)
            self.display_dir_content()
        except Exception as e:
            showerror("Warning", str(e))

    # копирование файлов
    def copy_files(self, *args):
        file_names: tuple = args[:-1]
        dirPath: str = args[-1]
        try:
            for file_name in file_names:
                shutil.copy(file_name, dirPath)
            self.display_dir_content()
        except Exception as e:
            showerror("Warning", str(e))

    # перемещение файлов
    def move_files(self, *args):
        file_names: tuple = args[:-1]
        dirPath: str = args[-1]
        for file_name in file_names:
            shutil.move(file_name, dirPath)

        self.display_dir_content()

    # переименование файлов
    def rename_file(self, *args):
        if len(args) > 2:
            showerror("Warning", "Too many arguments")
        elif len(args) < 2:
            showerror("Warning", "Too few arguments")
        else:
            file_name: str = args[0]
            new_file_name: str = args[1]
            if ".txt" not in new_file_name:
                new_file_name += ".txt"
            os.rename(file_name, new_file_name)
        self.display_dir_content()

    def archive(self, *args):
        if len(args) < 1:
            showerror("Warning", "Too few arguments")
        else:
            try:
                with ZipFile(args[0].split(".")[0] + ".zip", "w") as zip_file:
                    for file_name in args:
                        zip_file.write(file_name)
                    self.display_dir_content()
            except Exception as e:
                showerror("Warning", str(e))

    def extract(self, *args):
        if len(args) > 1:
            showerror("Warning", "Too many arguments")
        else:
            try:
                with ZipFile(args[0]) as zip_file:
                    self.create_dir(args[0].replace(".zip", ""))
                    zip_file.extractall(args[0].replace(".zip", ""))
                    self.display_dir_content()
            except Exception as e:
                showerror("Warning", str(e))

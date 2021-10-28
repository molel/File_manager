from FileManager import *
import json


def main():
    with open("settings.json", "r") as settings:
        directory=json.load(settings)
    FileManager()


if __name__ == '__main__':
    main()

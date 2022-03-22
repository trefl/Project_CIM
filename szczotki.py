# Script to search for irregularities on the CIM, version: 1.0, author: Marek Trefler
import datetime
import os
import csv


class choice:

    def __init__(self):
        self.choice = 0

    def language(self):
        while self.choice != "1" and self.choice != "2":
            print("Wybierz jezyk / Choose Your language: \n\t1 - Polski / Polish \n\t2 - Angielski / English")
            self.choice = input("> ")

        list_pl = ["Data rozpoczęcia (dd.mm.rrrr)", "Data zakończenia (dd.mm.rrrr)",
                   "Wybór daty: \n\t1 - Calość \n\t2 - Zakres",
                   "Nieprawidłowa data lub format, wpisz datę w formacie dd.mm.rrrr", "Ilosc"]
        list_eng = ["Start date (dd.mm.yyyy)", "End date (dd.mm.yyyy)", "Date selection: \n\t 1 - All \n\t 2 - Range",
                    "Invalid date or format, please enter the date in the format dd.mm.yyyy", "Quantity"]
        if self.choice == "1":
            lang = list_pl
        else:
            lang = list_eng
        return lang

    def range(self):
        while self.choice != "1" and self.choice != "2":
            print(lang_list[2])
            self.choice = input("> ")
        if self.choice == "1":
            start_date = datetime.datetime.strptime("01.01.2000", '%d.%m.%Y')
            end_date = datetime.datetime.now()
        else:
            print(lang_list[0])
            start_date = addDate().my_date()
            print(lang_list[1])
            end_date = addDate().my_date()
        return start_date, end_date


class addDate:

    def __init__(self):
        self.date = input("> ")

    def my_date(self):
        while True:
            try:
                new_date = datetime.datetime.strptime(self.date, '%d.%m.%Y')
                break
            except:
                print(lang_list[3])
                self.date = input("> ")
        return new_date


# os.system('clear')
lang_list = choice().language()

dates = choice().range()

date_start = dates[0]
date_end = dates[1]


class search:

    def searchDirectory(self):
        dirname = "D:\Folder"
        folders = os.listdir(dirname)
        folderList = []
        for folder in folders:
            folderList.append(folder)
        return folderList

    def searchCCR(self, folder):
        # dirname = "/home/translog/plikiRM/"+folder
        dirname = "D:\Folder\\" + folder
        folders = os.listdir(dirname)
        CCRlist = []
        for folder in folders:
            if folder.find("CCR") == 0 and folder.find(".old") < 0:
                CCRlist.append(folder)
        return CCRlist


class retracking:

    def find_retracking(self, directory, file, data_start, data_end):
        flag = 0
        tempDict = {}
        cim = ""
        # with open("/home/translog/plikiRM/" + folder + "/" + file, "r") as read_obj:
        with open("D:\Folder" + "\\" + directory + "\\" + file, "r") as read_obj:
            for line in read_obj:
                if flag == 0:
                    if "for TE000" in line and datetime.datetime.strptime(line[:8],
                                                                          '%d.%m.%y') > data_start and datetime.datetime.strptime(
                        line[:8], '%d.%m.%y') < data_end:
                        s = line.find("for TE000")
                        cim = "CIM" + line[s + 9] + line[s + 10] + line[s + 11]
                        flag = 1
                else:
                    if "from CIM" in line:
                        flag = 1
                    elif "set_retracking" in line:
                        if cim not in tempDict:
                            tempDict[cim] = 1
                        else:
                            tempDict[cim] = tempDict[cim] + 1
                        flag = 0
                        cim = ""
                    else:
                        flag = 0
                        cim = ""
        return tempDict


def date_range(date_start, date_end):
    if str(date_start) == "2000-01-01 00:00:00":
        date_text = ""
    else:
        date_text = f'{date_start.strftime("%d.%m.%Y")} - {date_end.strftime("%d.%m.%Y")}'
    return date_text


# os.system('clear')

find_folders = search().searchDirectory()
now = datetime.datetime.now()
name_csv = "szczotki_" + str(now.year) + str(now.month) + str(now.day) + "_" + str(now.hour) + str(now.minute) + ".csv"
print(date_range(date_start, date_end))
with open(name_csv, 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([date_range(date_start, date_end)])
    writer.writerow(["RCE", "CCR", "CIM", lang_list[4]])
    for folder in find_folders:
        print(f'\n\033[33mRCE: {folder}\033[0;0m\n')
        find_ccr = search().searchCCR(folder)
        for ccr in find_ccr:
            retrackingDict = retracking().find_retracking(folder, ccr, date_start, date_end)
        sortDict = {k: v for k, v in sorted(retrackingDict.items(), key=lambda v: v[1], reverse=True)}
        for keys, values in sortDict.items():
            print(f'{keys}: {values}')
            writer.writerow([folder, ccr, keys, values])


# Script to search for irregularities on the CIM, version: 1.0, author: Marek Trefler

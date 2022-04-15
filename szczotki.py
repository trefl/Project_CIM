#!/usr/bin/python3
# Script to search for irregularities on the CIM, version: 1.0, author: Marek Trefler
# -*- coding: utf-8 -*-
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
                   "Wybór daty: \n\t1 - Calość \n\t2 - Zakres \n\t3 - Doba",
                   "Nieprawidłowa data lub format, wpisz datę w formacie dd.mm.rrrr", "Ilosc", "Plik ", " znajduje sie w ", "Nazwa"]
        list_eng = ["Start date (dd.mm.yyyy)", "End date (dd.mm.yyyy)", "Date selection: \n\t 1 - All \n\t 2 - Range \n\t 3 - 24h",
                    "Invalid date or format, please enter the date in the format dd.mm.yyyy", "Quantity", "File ", " located in ","Name"]
        if self.choice == "1":
            lang = list_pl
        else:
            lang = list_eng
        return lang

    def range(self):
        while self.choice != "1" and self.choice != "2" and self.choice != "3":
            print(lang_list[2])
            self.choice = input("> ")
        if self.choice == "1":
            start_date = datetime.datetime.strptime("01.01.2000", '%d.%m.%Y')
            end_date = datetime.datetime.now()
        elif self.choice == "2":
            print(lang_list[0])
            start_date = addDate().my_date()
            print(lang_list[1])
            end_date = addDate().my_date()
        else:
            print(lang_list[0])
            start_date = addDate().my_date()
            end_date = start_date + datetime.timedelta(days=1)
        
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


os.system('clear')
lang_list = choice().language()

dates = choice().range()

date_start = dates[0]
date_end = dates[1]


def rce():
    rce_list = []

    for i in range(1, 17):
        if i < 10:
            rce_list.append("00" + str(i))
        else:
            rce_list.append("0" + str(i))
    return rce_list


def searchCCR(folder):
    dirname = "/u/xpo/master/run/log/" + folder
    folders = os.listdir(dirname)
    CCRlist = []
    for folder in folders:
        if folder.find("CCR") == 0 and folder.find(".old") < 0 and folder.find(".save") < 0:
            CCRlist.append(folder)
    return CCRlist


class retracking:

    def find_retracking(self, directory, file, data_start, data_end):
        flag = 0
        tempDict = {}
        cim = ""
        with open("/u/xpo/master/run/log/" + directory + "/" + file, "r", encoding='latin-1') as read_obj:
            for line in read_obj:
                if flag == 0:
                    if "for TE000" in line and datetime.datetime.strptime(line[:8],'%d.%m.%y') >= data_start and datetime.datetime.strptime(line[:8], '%d.%m.%y') < data_end:
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
        
        rtDict = sorted(tempDict.items(), key=lambda x: x[1], reverse=True)
        return rtDict


def date_range(date_start, date_end):
    if str(date_start) == "2000-01-01 00:00:00":
        date_text = ""
    else:
        date_text = date_start.strftime("%d.%m.%Y") + "-" + date_end.strftime("%d.%m.%Y")
    return date_text
    
    
    
def findCIM(rce, key):
    name = ""
    with open("/home/translog/CimCom", "r") as read_obj:
        for line in read_obj:

            if rce == line[:3] and key[3:6] == line[4:7]:
                name = line[12:].replace('\n', '')
    return name

def addZero(nDate):
  if nDate < 10:
      nDate = "0"+ str(nDate)
  return nDate 


os.system('clear')

find_folders = rce()
now = datetime.datetime.now()

name_csv = "szczotki_" + str(now.year) + str(addZero(now.month)) + str(addZero(now.day)) + "_" + str(addZero(now.hour)) + str(addZero(now.minute)) + ".csv"
print(date_range(date_start, date_end))
with open("/home/translog/plikiRM/CSV/"+name_csv, 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([date_range(date_start, date_end)])
    writer.writerow(["RCE", "CCR", "CIM",lang_list[7], lang_list[4]])
    for folder in find_folders:
        print("\n\033[33mRCE: " + folder + "\033[0;0m\n")
        find_ccr = searchCCR(folder)
        #print(find_ccr)
        for ccr in find_ccr:
            retrackingList = retracking().find_retracking(folder, ccr, date_start, date_end)
            for i in retrackingList:
                name = findCIM(folder, i[0])
                print(ccr+" : " + str(i[0]) + " : \033[36m" +  name + (11-len(name))*" "+" " + "\033[m : \033[31m" + str(i[1]) + "\033[m")
                writer.writerow([folder, ccr, i[0], name, i[1]])
            
        
print("\n\033[35m" +lang_list[5] + name_csv + lang_list[6] + "/home/translog/plikiRM/CSV\033[0;0m\n")






# Script to search for irregularities on the CIM, version: 1.0, author: Marek Trefler

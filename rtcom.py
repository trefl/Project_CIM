#!/usr/bin/python3
# Script to search for irregularities on the COM, version: 1.0, author: Marek Trefler
# -*- coding: utf-8 -*-
import csv
import datetime
import os


def my_date():
    myDate = input("> ")
    while True:
        try:
            new_date = datetime.datetime.strptime(myDate, '%d.%m.%Y')
            break
        except:
            print("Nieprawidłowa data lub format, wpisz datę w formacie dd.mm.rrrr")
            myDate = input("> ")
    return new_date


def range_choice():
    choice = 0
    while choice != "1" and choice != "2" and choice != "3":
        print("Wybór daty: \n\t1 - Calość \n\t2 - Zakres \n\t3 - Doba")
        choice = input("> ")
    if choice == "1":
        start_date = datetime.datetime.strptime("01.01.2000", '%d.%m.%Y')
        end_date = datetime.datetime.now()
    elif choice == "2":
        print("Data rozpoczęcia (dd.mm.rrrr)")
        start_date = my_date()
        print("Data zakończenia (dd.mm.rrrr)")
        end_date = my_date()
    else:
        print("Data rozpoczęcia (dd.mm.rrrr)")
        start_date = my_date()
        end_date = start_date + datetime.timedelta(days=1)

    return start_date, end_date


dates = range_choice()

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
    #dirname = "D:\Folder\\" + folder
    folders = os.listdir(dirname)
    CCRlist = []
    for folder in folders:
        if folder.find("CCR") == 0 and folder.find(".old") < 0 and folder.find(".save") < 0:
            CCRlist.append(folder)
    return CCRlist


find_folders = rce()


def find_retracking(directory, file, start_date, end_date):
    tempDict = {}
    with open("/u/xpo/master/run/log/" + directory + "/" + file, "r", encoding='latin-1') as read_obj:
    #with open("D:\Folder" + "\\" + directory + "\\" + file, "r") as read_obj:
        for line in read_obj:
            data_row = datetime.datetime.strptime(line[:17], '%d.%m.%y %H:%M:%S')
            if "went out at slave" in line and "COM" in line and start_date <= data_row < end_date:
                s = line.find("COM")
                com = "COM" + line[s + 3] + line[s + 4] + line[s + 5]
                if com not in tempDict:
                    tempDict[com] = [1, 0]
                else:
                    tempDict[com][0] += 1
            if "didn't go out at exit COM" in line and start_date < data_row < end_date:
                s = line.find("COM")
                com = "COM" + line[s + 3] + line[s + 4] + line[s + 5]
                if com not in tempDict:
                    tempDict[com] = [0, 1]
                else:
                    tempDict[com][1] += 1
    return tempDict


def findC(rce, key):
    name = ""
    with open("/home/translog/CimCom", "r") as read_obj:
    #with open("D:\Folder\\CimCom.txt", "r") as read_obj:
        for line in read_obj:

            if rce == line[:3] and key == line[4:7]:
                name = line[12:].replace('\n', '')
    return name


def date_range(date_start, date_end):
    if str(date_start) == "2000-01-01 00:00:00":
        date_text = ""
    else:
        date_text = date_start.strftime("%d.%m.%Y") + "-" + date_end.strftime("%d.%m.%Y")
    return date_text

def addZero(nDate):
  if nDate < 10:
      nDate = "0"+ str(nDate)
  return nDate 


print(date_range(date_start, date_end))
now = datetime.datetime.now()
name_csv = "rtCOM_" + str(now.year) + str(addZero(now.month)) + str(addZero(now.day)) + "_" + str(addZero(now.hour)) + str(addZero(now.minute)) + ".csv"

with open("/home/translog/plikiRM/CSV/" + name_csv, 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([date_range(date_start, date_end)])
    writer.writerow(["RCE", "CCR", "C0M", "Nazwa", "Blad", "Ilosc"])
    for folder in find_folders:
        print("\n\033[33mRCE: " + folder + "\033[0;0m")
        find_ccr = searchCCR(folder)
        for ccr in find_ccr:
            retrackingDict = find_retracking(folder, ccr, date_start, date_end)
            for keys, values in retrackingDict.items():
                name = findC(folder, str(keys[3:]))
                print("\n\33[100mSUMA: " + str(keys) + " : " + name + " : " + str(sum(values)) + (
                            50 - len(name) - len(str(sum(values)))) * " " + "\33[m")
                if values[0] > 0:
                    print("\33[96mWorek wyjechal niespodziewanie na: " + str(keys) + " : " + str(values[0]) + "\33[m")
                    writer.writerow([folder, ccr, keys, name, "Worek wyjechal niespodziewanie na ", values[0]])
                if values[1] > 0:
                    print("\33[95mWorek nie wyjechal na: " + str(keys) + " : " + str(values[1]) + "\33[m")
                    writer.writerow([folder, ccr, keys, name, "Worek nie wyjechal na ", values[1]])


print("\n\033[35mPlik "+ name_csv + " znajduje sie w /home/translog/plikiRM/CSV\033[0;0m\n")
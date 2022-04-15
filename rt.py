#!/usr/bin/python3
# Script to search for retracking from the last 30 minutes, version: 1.0, author: Marek Trefler
# -*- coding: utf-8 -*-
import datetime
import io
import os
import sys

def startTime(arg):
    if len(arg)== 2:
        if arg[1].isdigit():
            find = datetime.datetime.now() - datetime.timedelta(hours=int(arg[1]))
        else:
            print("\033[31mNieprawidlowy parametr\033[m\n")
            find = datetime.datetime.now() - datetime.timedelta(hours=0.5)
    else:
        find = datetime.datetime.now() - datetime.timedelta(hours=0.5)
    return find
    
find_date = startTime(sys.argv)
print("\033[33mSTART: ", find_date )
print("\033[m\n")
rtDict = {}
#print(find_date)

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
now = datetime.datetime.now()

class retracking:

    def find_retracking(self, directory, file, start_date, tempDict):
        with open("/u/xpo/master/run/log/" + directory + "/" + file, "r", encoding='latin-1') as read_obj:
        #with open("D:\Folder" + "\\" + directory + "\\" + file, "r") as read_obj:
            for line in read_obj:
                if datetime.datetime.strptime(line[:17], '%d.%m.%y %H:%M:%S') > start_date:
                    if "went out at slave" in line:
                        if "COM" in line:
                            s = line.find("COM")
                            tempDict[line[:25]] = [directory, file[3:], "COM", line[s + 3] + line[s + 4] + line[s + 5], "Worek wyjechal niespodziewanie na  "]
                        elif "CIM" in line:
                            s = line.find("CIM")
                            tempDict[line[:25]] = [directory, file[3:], "CIM", line[s + 3] + line[s + 4] + line[s + 5], "Worek wyjechal niespodziewanie na  "]
                    elif "didn't go out at exit COM" in line:
                        s = line.find("COM")
                        tempDict[line[:25]] = [directory, file[3:], "COM", line[s + 3] + line[s + 4] + line[s + 5], "Worek nie wyjechal na              "]
                    elif "didn't go out at exit CIM" in line:
                        s = line.find("CIM")
                        tempDict[line[:25]] = [directory, file[3:], "CIM", line[s + 3] + line[s + 4] + line[s + 5], "Worek nie wyjechal na              "]


        return tempDict



for folder in find_folders:
    find_ccr = searchCCR(folder)
    for ccr in find_ccr:
        retracking().find_retracking(folder, ccr, find_date, rtDict)

def findC(rce, key):
    name = ""
    with open("/home/translog/CimCom", "r") as read_obj:
    #with open("D:\Folder\\CimCom.txt", "r") as read_obj:
        for line in read_obj:

            if rce == line[:3] and key == line[4:7]:
                name = line[12:].replace('\n', '')
    return name


sortList = sorted(rtDict.items(), key=lambda x: x[0], reverse=False)
for row in sortList:
    name = findC(str(row[1][0]), str(row[1][3]))
    print(row[0][:17] + "   \033[33m" + row[1][0] + "/" + row[1][1] + "\033[34m   " + row[1][2]+row[1][3] + "\033[m  " + row[1][4] + "  -->  \033[32m" + name +"\033[m")
    

# Script to search for retracking from the last 30 minutes, version: 1.0, author: Marek Trefler
    
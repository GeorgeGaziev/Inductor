
# coding: utf-8

# In[20]:


import urllib
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import pickle
from collections import Counter
from collections import namedtuple
import re
import xlwings as xw
import pandas as pd
import numpy as np


path_to_names = "D:/"
path_to_patronymics = "D:/"

with open(path_to_names + "NamesFromGufo.pickle", "rb") as f:
    tmpNames = pickle.load(f)
with open(path_to_patronymics + "PatronymicsFromGufo.pickle", "rb") as f:
    tmpPatronymics = pickle.load(f)

all_names = []
all_patronymics = []

for i in tmpNames:
    all_names.append(i)
for i in tmpPatronymics:
    all_patronymics.append(i)

def process():
    wb = xw.Book.caller()
    data = wb.selection
    sheetName = wb.sheets.active.name

    newSheetName = sheetName + "Changed"

    flag=False
    for i in wb.sheets:
        if i.name==newSheetName:
            flag=True

    newData = brute(data.value)

    if flag==False:
        xw.sheets.add(newSheetName, None, xw.sheets.active)

    wb.sheets[newSheetName].clear()
    wb.sheets[newSheetName].range('A1').options(transpose=True).value = newData
    wb.sheets[newSheetName].select()


def brute(tmp):
    res = []
    errs=[]
    for t in tmp:
        name = ""
        surname = ""
        patronymic = ""
        words = t.split(" ")
        for w in words:
            w = w.lower()
            w.strip()
            if (name == ""):
                for n in all_names:
                    if w == n:
                        name = n
                        break
            if (patronymic == ""):
                    for p in all_patronymics:
                        if w == p:
                            patronymic = p
                            break
            if (name != w and patronymic != w and surname == ""):
                surname = w

        if (name == ""):
            name = "N:'"+w+"'_Not_Found"
            #errs.append("name '" + w + "' in " + t)
        if (patronymic == ""):
            patronymic = "P:'"+w+"'_Not_Found"
            errs.append("patronymic '" + w + "' in " + t)
        name = name.title()
        surname = surname.title()
        patronymic = patronymic.title()
        res.append(surname + " " + name + " " + patronymic)

    if len(errs)!=0:
        res.append("----Ошибки----")
        for i in errs:
            res.append(i)
    return res





# # In[35]:
#
#
# with open("E:/test_changed.pickle","rb") as f:
#     tmp=pickle.load(f)
#
#
# # In[36]:
#
#
# print("Результат обработки:")
# testing_res=brute(tmp)
# for fio in testing_res:
#     print(fio)
#
#
# # In[37]:
#
#
# print("\nОшибочные:")
# errs=0
# for i in testing_res:
#     if i.find("Not_Found")!=-1:
#         print (i)
#         errs+=1
# print("Всего не определено: " + str(errs))

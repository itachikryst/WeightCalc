from typing import OrderedDict
from datetime import *
from pyexcel_ods import get_data
from dateutil.parser import parse, parserinfo
from pyexcel_ods import save_data


def get_valid_values_from_data(_data):
    days = []
    weights = []
    fatPercentages = []
    musclePercentages = []
    for i, day in enumerate(_data):
        if len(day) == 1:
            break
        days.append(i)
        weights.append(day[1])
        fatPercentages.append(day[2])
        musclePercentages.append(day[3])
    return days, weights, fatPercentages, musclePercentages


def get_data_from_ods_file(fileName="Waga.ods", raw=False, fast=False):
    _data = list(get_data(fileName).values())
    _data = _data[0]
    #print(_data)
    if not raw:
        _data.pop(0)
    if not fast:
        for i, day in enumerate(_data):
            if len(day) > 1:
                if not raw:
                    if day[0].__class__ == str:
                        _data[i][0] = parse(_data[i][0], dayfirst=True).date()
                elif raw and i > 0:
                    if day[0].__class__ == str:
                        _data[i][0] = parse(_data[i][0], dayfirst=True).date()
    #print(_data)
    return _data


def get_last_day(_data):
    lastDay = ""
    for i, day in enumerate(_data):
        if len(day) == 1:
            lastDay = _data[i - 1]
            break
    if lastDay == "":
        lastDay = _data[-1]
    return lastDay


def get_day_worse_than_percent(checkDay, _data):
    total = 0
    worse = 0
    for i, day in enumerate(_data):
        if len(day) == 1:
            break
        if day[1] >= checkDay[1]:
            worse += 1
        total += 1
    return worse / total


def get_best_day(_data):
    bestDay = _data[0]
    for i, day in enumerate(_data):
        if len(day) == 1:
            break
        if day[1] < bestDay[1]:
            bestDay = day
    return bestDay


def add_db_entry(date, weight, fat, muscle):
    list_data = get_data_from_ods_file(raw=True, fast=True)
    date = date.rstrip()
    parserinfo(dayfirst=True)
    date_datetime = parse(date, dayfirst=True).date()
    weight = float(weight)
    fat = float(fat)
    muscle = float(muscle)
    lastDay = get_last_day(list_data)
    #print(list_data)
    lastDayDate = lastDay[0]
    if lastDayDate.__class__ == str:
        lastDayDate = parse(lastDayDate, dayfirst=True).date()
        list_data[-1] = parse(list_data[-1], dayfirst=True).date()
    if lastDayDate + timedelta(days=1) == date_datetime:
        list_data.append([date, weight, fat, muscle])
    else:
        if lastDayDate >= date_datetime:
            #print("NOT IMPLEMENTED YET")
            raise Exception("Tried to add date which is already in use")
        else:
            temp = []
            genNum = (date_datetime - lastDayDate).days
            avg_weight = (lastDay[1] - weight) / genNum
            avg_fat = (lastDay[2] - fat) / genNum
            avg_muscle = (lastDay[3] - muscle) / genNum
            for _ in range(genNum - 1):
                temp.append(list_data[-1][0] + timedelta(days=1))
                temp.append(list_data[-1][1] - avg_weight)
                temp.append(list_data[-1][2] - avg_fat)
                temp.append(list_data[-1][3] - avg_muscle)
                list_data.append(temp)
                temp = []
            list_data.append([date, weight, fat, muscle])
    for day in list_data:
        if day[0].__class__ is not str:
            day[0] = day[0].strftime("%d.%m.%Y")
    data = OrderedDict()
    data.update({"Sheet 1": list_data})
    save_data("Waga.ods", data)

#!/usr/bin/env python3

import os
import re
import json
import difflib
import datetime

base_dir = os.path.dirname(os.path.realpath(__file__))

def subtrans(region, city):
    special_dict = {
        "乌兰察布市": "ulanqab",
        "云林县": "yunlin",
        "伊犁": "yili",
        "克孜勒苏": "kizilsu",
        "六盘水市": "liupanshui",
        "兴安盟": "xinganmeng",
        "南投县": "nantou",
        "博尔塔拉": "bortala",
        "台东县": "taidong",
        "台南": "tainan",
        "呼伦贝尔市": "hulunbeier",
        "嘉义县": "chiayi",
        "嘉义市": "chiayi",
        "基隆": "keelung",
        "宜兰县": "yilan",
        "屏东县": "pingtung",
        "巴彦淖尔市": "bayannaoer",
        "巴音郭楞": "bayinguoleng",
        "延边": "yanbian",
        "彰化县": "changhua",
        "新北": "New Taipei",
        "新竹县": "hsinchu",
        "新竹市": "hsinchu",
        "桃园": "taoyuan",
        "沙田": "shatin",
        "湘西": "xiangxi",
        "澎湖县": "penghu",
        "甘南": "gannan",
        "花莲县": "hualien",
        "苗栗县": "miaoli",
        "荃湾": "Tsuen Wan",
        "西双版纳": "xishuangbanna",
        "迪庆": "diqing",
        "金门县": "kinmen",
        "锡林郭勒": "xilinguole",
        "阿拉善": "alashan",
        "陇南市": "longnan",
        "黔东南": "qiandongnan",
        "黔南": "qiannan",
        "黔西南": "qianxinan"
    }
    city_json = os.path.join(base_dir, "chaincity.json")
    city_dict = None
    with open(city_json, "r") as f:
        city_dict = json.load(f)

    if region == "0":
        region, city = "", ""
    elif region in ["北京", "天津", "上海", "重庆"]:
        for r in city_dict:
            if region == r["name"]:
                region = r["name_en"]
                city = ""
    else:
        for r in city_dict:
            if region == r["name"]:
                region = r["name_en"]
                if city == "0":
                    break
                is_special = True
                for c in r["city"]:
                    if difflib.SequenceMatcher(None, c["name"], city).ratio() > 0.6:
                        for tmp in c["county"]:
                            if difflib.SequenceMatcher(None, tmp["name"], city).ratio() > 0.6:
                                city = tmp["name_en"]
                                is_special = False
                                break
                        break
                if is_special:
                    city = special_dict[city]
                if city == "taibeixian":
                    city = "Taipei"
                break

    return region.capitalize(), city.capitalize()


def maintrans():
    ip_merge_txt = os.path.join(base_dir, "ip.merge.txt")
    country_json = os.path.join(base_dir, "country.json")
    isp_json = os.path.join(base_dir, "isp.json")
    country_dict = None
    isp_dict = None
    with open(country_json, "r") as f:
        country_dict = json.load(f)
    with open(isp_json, "r") as f:
        isp_dict = json.load(f)
    lines = []
    with open(ip_merge_txt, "r") as f:
        lines = f.readlines()

    newlines = []
    country = ""
    region = ""
    city = ""
    isp = ""
    for line in lines:
        country = re.findall(r".*\|.*\|(.*)\|.*\|.*\|.*\|.*", line)[0]
        padding = re.findall(r".*\|.*\|.*\|(.*)\|.*\|.*\|.*", line)[0]
        region = re.findall(r".*\|.*\|.*\|.*\|(.*)\|.*\|.*", line)[0]
        city = re.findall(r".*\|.*\|.*\|.*\|.*\|(.*)\|.*", line)[0]
        isp = re.findall(r".*\|.*\|.*\|.*\|.*\|.*\|(.*)", line)[0]
        isp = isp_dict[isp]
        tmp = line.split("|")[0:2]
        tmpline = "{tmp0}|{tmp1}".format(tmp0=tmp[0], tmp1=tmp[1])
        if country == "中国":
            country = country_dict[country]
            region, city = subtrans(region, city)
            newlines.append("{line}|{country}|{padding}|{region}|{city}|{isp}\n".format(line=tmpline.rstrip(), country=country, padding=padding, region=region, city=city, isp=isp))
        elif country != "0":
            country = country_dict[country]
            newlines.append("{line}|{country}|{padding}|0|0|{isp}\n".format(line=tmpline.rstrip(), country=country, padding=padding, isp=isp))
        else:
            newlines.append("{line}|0|{padding}|0|0|{isp}\n".format(line=tmpline.rstrip(), padding=padding, isp=isp))

    with open("ip.merge.new.txt", "w+") as f:
        f.writelines(newlines)


if __name__=="__main__":
    s = datetime.datetime.now()
    maintrans()
    e = datetime.datetime.now()
    print("Total consume time: {}s".format((e-s).seconds))

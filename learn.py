# -*- coding: utf-8 -*-
import json
import re
import random
import Replymsg
import numpy as np
import requests
import urllib, urllib.request
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

appid = "WQ7PGU-A6Y6QKALPA"


def r2_gain(lis, a, b):
    y_avr = sum(lis[1]) / len(lis[1])
    p1, q1 = 0, 0
    for i in range(len(lis[0])):
        x = lis[0][i]
        y = lis[1][i]
        y_ = b * x + a
        p1 = p1 + (y - y_) ** 2
        q1 = q1 + (y - y_avr) ** 2
    r2 = 1 - p1 / q1
    return r2


def ab_gain(lis):
    n = len(lis[0])
    x_avr = sum(lis[0]) / len(lis[0])
    y_avr = sum(lis[1]) / len(lis[1])
    xy, xx = 0, 0
    for i in range(len(lis[0])):
        xy = xy + lis[0][i] * lis[1][i]
        xx = xx + lis[0][i] ** 2
    b = (xy - n * x_avr * y_avr) / (xx - n * x_avr * x_avr)
    a = y_avr - b * x_avr
    return a, b


def nonlinear_matrix(list, n):
    x_l = []
    for i in range(len(list[0])):
        xs = [list[0][i] ** j for j in range(n)]
        x_l.append(xs)
    A = np.array(x_l)
    Y = np.array(list[1])
    a = np.linalg.solve(np.dot(A.transpose(), A), np.dot(A.transpose(), Y))
    return a


async def data_handle(msg):
    x_place = re.search("X", msg["message"], 0)
    y_place = re.search("Y", msg["message"], 0)
    if re.match("统计", msg["message"], flags=0) is not None and x_place is not None and y_place is not None and \
            msg['message'][3].isdigit():
        try:
            xl = msg["message"][x_place.start() + 1:y_place.start()].split(' ')
            xl.remove('')
            xl.remove('')
            yl = msg["message"][(y_place.start() + 1)::].split(' ')
            yl.remove('')
            xl = [float(x) for x in xl]
            yl = [float(x) for x in yl]
            x_max = max(xl)
            x_min = min(xl)
            if len(xl) == len(yl):
                lis = [xl, yl]
                n = int(msg['message'][3])
                a = nonlinear_matrix(lis, n)
                xset = [0.05 * x + x_min for x in range(int((x_max - x_min) / 0.05))]
                x_ls = []
                for j in range(len(xset)):
                    x_ls.append([xset[j] ** num for num in range(n)])
                ar = np.array(x_ls)
                y_ls = np.dot(ar, a.transpose())
                print(len(y_ls))
                plt.scatter(xl, yl, marker='o', color='green', s=40, label='initial point')
                plt.plot(xset, y_ls, color='red', label='fitting curve')
                plt.legend(loc='best')
                plt.xlabel("x")
                plt.ylabel("y")
                plt.title("curve results")
                plt.savefig('./funcs.png')
                plt.cla()
                st = "统计非线性%d次回归： \n [CQ:image,file=file:///root/witch/funcs.png]" % n
                await Replymsg.send_msg(st, msg["group_id"], "group")
                if os.path.exists('funcs.png'):
                    os.remove('funcs.png')
        except Exception:
            pass

    if re.match("统计", msg["message"], flags=0) is not None and x_place is not None and y_place is not None and not \
            msg['message'][3].isdigit():
        try:
            xl = msg["message"][x_place.start() + 1:y_place.start()].split(' ')
            xl.remove('')
            xl.remove('')
            yl = msg["message"][(y_place.start() + 1)::].split(' ')
            yl.remove('')
            xl = [float(x) for x in xl]
            yl = [float(x) for x in yl]
            x_max = max(xl)
            x_min = min(xl)
            if len(xl) == len(yl):
                lis = [xl, yl]
                a, b = ab_gain(lis)
                r2 = r2_gain(lis, a, b)
                plt.scatter(xl, yl, marker='o', color='green', s=40, label='initial point')
                plt.plot([x_min, x_max], [b * x_min + a, b * x_max + a], color='red', label='fitting curve')

                plt.legend(loc='best')
                plt.xlabel("x")
                plt.ylabel("y")
                plt.title("curve result")
                plt.savefig('./funcs.png')
                plt.cla()
                st = "统计线性回归：\n" + "方程:%s" % ("Y = " + str(b) + " X ＋ " + str(a) + "\n") + "R方：" + str(
                    r2) + "[CQ:image,file=file:///root/witch/funcs.png]"
                await Replymsg.send_msg(st, msg["group_id"], "group")
                if os.path.exists('funcs.png'):
                    os.remove('funcs.png')
        except Exception:
            pass


async def data_error(msg):
    data_list = msg["message"][3::].split(" ")
    if re.match("误差", msg["message"], flags=0) and data_list is not None:
        nn = len(data_list)
        avr = 0
        for i in data_list:
            x = float(i)
            avr += x
        avr = avr / nn
        avr2, arr = 0, 0
        for i in data_list:
            x = float(i)
            arr += (x - avr) ** 2
            avr2 += x * x
        avr2 = avr2 / nn
        d2 = avr2 - avr * avr
        Da = arr / (nn * (nn - 1))
        rep = '数据为：'
        for i in data_list:
            rep += i + " "
        rep = rep + '\n均值为：' + str(avr) + '\n方差为：' + str(d2) + '\nA类误差为：' + str(Da)
        await Replymsg.send_msg(rep, msg["group_id"], "group")


prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
         109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
         233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
         367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
         499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
         643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
         797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
         947, 953, 967, 971, 977, 983, 991, 997, 1009]


async def primehandle(msg):
    if re.match("质数化", msg["message"]):

        try:
            with open("data/prime.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            compiles = re.compile(r'qq=([0-9]+)')
            sre = re.search(compiles, msg["message"])
            qq = msg["message"][(int(sre.start() + 3)):(int(sre.end()))]
            qq_num = int(qq)
            prilist = []
            count = len(prime)

            while count >= 1:
                for i in range(len(prime)):
                    count -= 1
                    if qq_num % prime[i] == 0:
                        prilist.append(prime[i])
                        qq_num = int(qq_num / prime[i])
                        break
            cos = 0
            for ss in range(5):
                for j in range(len(data)):
                    if int(qq_num) % int(data[j]) == 0:
                        prilist.append(data[j])
                        qq_num = int(qq_num / data[j])
                        break
                cos += 1
                if cos == 5:
                    prilist.append(qq_num)
                    break
            s = "一股魔力席卷至ta的身体，ta变成了："
            for num in prilist:
                s += str(num) + '*'
            s += '1=' + str(qq)
            await Replymsg.send_msg(s, msg["group_id"], "group")
        except Exception as e:
            print(e)


def wa_handle(key):
    findkey = str(key)
    url_find = 'http://api.wolframalpha.com/v1/simple?input=%s&appid=%s' % (urllib.parse.quote(findkey), appid)
    hand = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"
    }
    res = urllib.request.Request(url_find, headers=hand)
    response = urllib.request.urlopen(res)
    return response.read()


async def wa(msg):
    if re.match("math ", msg["message"]):
        try:
            key = msg["message"][5::]
            img = Image.open(BytesIO(wa_handle(key)))
            img.save('math.png')
            await Replymsg.send_msg("[CQ:image,file=file:///root/witch/math.png]", msg["group_id"], "group")
            if os.path.exists('math.png'):
                os.remove('math.png')
        except Exception as e:
            await Replymsg.send_msg(e, msg["group_id"], "group")


async def cats(msg):
    if re.match("cat", msg["message"]):
        try:
            if msg["message"] == "cat":
                url_cat = "https://thatcopy.pw/catapi/rest/"
            else:
                num = msg["message"][4::]
                url_cat = "https://thatcopy.pw/catapi/restId/" + num
            res = requests.get(url_cat)
            res = res.json()
            id = res["id"]
            img_id = res["url"]
            hand = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"
            }
            ress = urllib.request.Request(img_id, headers=hand)
            response = urllib.request.urlopen(ress).read()
            img = Image.open(BytesIO(response))
            img.save('cat.png')
            await Replymsg.send_msg("id=%d[CQ:image,file=file:///root/witch/cat.png]" % id, msg["group_id"], "group")
            if os.path.exists('cat.png'):
                os.remove('cat.png')
        except Exception as e:
            await Replymsg.send_msg(e, msg["group_id"], "group")


async def kksk(msg):
    if re.match("kksk", msg["message"]):
        try:
            url = "https://api.ixiaowai.cn/api/api.php"
            hand = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"
            }
            ress = urllib.request.Request(url, headers=hand)
            response = urllib.request.urlopen(ress).read()
            img = Image.open(BytesIO(response))
            img.save('kksk.png')
            await Replymsg.send_msg("[CQ:image,file=file:///root/witch/kksk.png]", msg["group_id"], "group")
            if os.path.exists('kksk.png'):
                os.remove('kksk.png')
        except Exception as e:
            await Replymsg.send_msg(e, msg["group_id"], "group")

st_data_path = 'data/stdata.json'


async def suki(msg):
    if re.match("suki", msg["message"]):
        with open(st_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            id = random.choice(data)
            url = 'https://pixiv.moeiris.com/pid.php?pid=%d&master=1' % id
            try:
                hand = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"
                }
                ress = urllib.request.Request(url, headers=hand)
                response = urllib.request.urlopen(ress).read()
                img = Image.open(BytesIO(response))
                img.save('SUKI.png')
                await Replymsg.send_msg("[CQ:image,file=file:///root/witch/SUKI.png]", msg["group_id"], "group")
                if os.path.exists('SUKI.png'):
                    os.remove('SUKI.png')
            except Exception as e:
                await Replymsg.send_msg(e, msg["group_id"], "group")

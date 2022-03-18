import Replymsg as r
import aiohttp
import urllib.parse
import time
import json
import dayly
import datetime
import re
from PIL import Image, ImageFont, ImageDraw
import random
import os

lesson_file = 'data/lesson.json'
day_time = ["first", "second", "third", "fourth", "fifth", "sixth", "weeks"]


def json_make(first, second, third, fourth, fifth, sixth, weeks):
    data = '[CQ:json,data={"app":"com.tencent.miniapp"&#44;"desc":""&#44;"view":"notification"&#44;"ver":"0.0.0.1"&#44;"prompt":"课表"&#44;"appID":""&#44;"sourceName":""&#44;"actionData":""&#44;"actionData_A":""&#44;"sourceUrl":""&#44;"meta":{"notification":{"appInfo":{"appName":"%s"&#44;"appType":4&#44;"appid":1109659848&#44;"iconUrl":"https:\/\/5b0988e595225.cdn.sohucs.com\/images\/20190910\/988f35964bc24f7391d2fed9d7d9f426.png"}&#44;"data":&#91;{"title":"第一节:"&#44;"value":"%s"}&#44;{"title":"第二节:"&#44;"value":"%s"}&#44;{"title":"第三节:"&#44;"value":"%s"}&#44;{"title":"第四节:"&#44;"value":"%s"}&#44;{"title":"晚一:"&#44;"value":"%s"}&#44;{"title":"晚二:"&#44;"value":"%s"}&#93;&#44;"title":"%s"&#44;"button":&#91;{"name":"本周"&#44;"action":"http:\/\/q1.qlogo.cn\/g?b=qq&amp;nk=1543366909&amp;s=640"}&#93;&#44;"emphasis_keyword":""}}&#44;"text":""&#44;"sourceAd":""&#44;"extra":""}]' % (
        "今日课表", first, second, third, fourth, fifth, sixth, weeks)
    return data


def lesson_time_handle(rank):
    if rank == "first":
        time_ = [8, 0, 0]
        return time_
    if rank == "second":
        time_ = [10, 0, 0]
        return time_
    if rank == "third":
        time_ = [14, 0, 0]
        return time_
    if rank == "fourth":
        time_ = [16, 0, 0]
        return time_
    if rank == "fifth":
        time_ = [18, 30, 0]
        return time_
    if rank == "sixth":
        time_ = [20, 30, 0]
        return time_


async def lesson_msg_send(msg):
    if msg["message"] == "今日课表":
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f1:
                data = json.load(f1)
                week_now = str(datetime.datetime.today().weekday())
                for i in range(len(data)):
                    if msg["sender"]["user_id"] == data[i]["user"]:
                        leslist = []
                        lesmsg = {}
                        for j in range(len(data[i]["data"][week_now])):
                            lesson = data[i]["data"][week_now][j]
                            leslist.append(lesson["rank"])
                            lesmsg[lesson["rank"]] = [lesson["lesson_name"], lesson["teacher"], lesson["place"]]
                        for k in day_time:
                            if k not in leslist:
                                lesmsg[k] = ["此时无课，做好预习和复习", "", ""]
                        weeks = str(datetime.datetime.today().strftime('%A'))
                        datas = json_make(lesmsg["first"][0] + " " + lesmsg["first"][1] + " " + lesmsg["first"][2],
                                          lesmsg["second"][0] + " " + lesmsg["second"][1] + " " + lesmsg["second"][2],
                                          lesmsg["third"][0] + " " + lesmsg["third"][1] + " " + lesmsg["third"][2],
                                          lesmsg["fourth"][0] + " " + lesmsg["fourth"][1] + " " + lesmsg["fourth"][2],
                                          lesmsg["fifth"][0] + " " + lesmsg["fifth"][1] + " " + lesmsg["fifth"][2],
                                          lesmsg["sixth"][0] + " " + lesmsg["sixth"][1] + " " + lesmsg["sixth"][2],
                                          weeks)
                        rep_msg = urllib.parse.quote(datas)
                        await r.send_msg(rep_msg, msg["group_id"], "group")
        except Exception as e:
            print(e)
            await r.send_msg("没有查询到相关课表嗷", msg["group_id"], "group")


async def lesson_msg_write(msg):
    if re.match("添加课表 ", msg["message"], flags=0) is not None:
        try:
            mes1 = msg["message"][5::]
            mesl1 = mes1.split(" ")
            if len(mesl1) == 5:
                with open(lesson_file, 'r', encoding='utf-8') as f1:
                    data = json.load(f1)
                    users = []
                    for i in range(len(data)):
                        users.append(data[i]["user"])
                    if msg["sender"]["user_id"] in users:
                        for i in range(len(data)):
                            if msg["sender"]["user_id"] == data[i]["user"]:
                                weekdays = True
                                for k in list(data[i]["data"].keys()):
                                    if k == mesl1[0]:
                                        weekdays = False
                                if int(mesl1[0]) in range(0, 7) and mesl1[1] in day_time and not weekdays:
                                    rere = True
                                    for j in range(len(data[i]["data"][mesl1[0]])):
                                        if mesl1[1] == data[i]["data"][mesl1[0]][j]["rank"]:
                                            await r.send_msg("已经写入过这节课了嗷~", msg["group_id"], "group")
                                            rere = False
                                    if rere:
                                        rank = mesl1[1]
                                        lesson_name = mesl1[2]
                                        teacher = mesl1[3]
                                        place = mesl1[4]
                                        dic_new = {"rank": rank, "lesson_name": lesson_name, "teacher": teacher,
                                                   "place": place}
                                        data[i]["data"][mesl1[0]].append(dic_new)
                                        with open(lesson_file, 'w', encoding='utf-8') as f2:
                                            json.dump(data, f2, ensure_ascii=False, sort_keys=True, indent=4)
                                            await r.send_msg("写入成功", msg["group_id"], "group")
                                if int(mesl1[0]) in range(0, 7) and mesl1[1] in day_time and weekdays:
                                    rank = mesl1[1]
                                    lesson_name = mesl1[2]
                                    teacher = mesl1[3]
                                    place = mesl1[4]
                                    dic_new = {"rank": rank, "lesson_name": lesson_name, "teacher": teacher,
                                               "place": place}
                                    data[i]["data"][mesl1[0]] = [dic_new]
                                    with open(lesson_file, 'w', encoding='utf-8') as f2:
                                        json.dump(data, f2, ensure_ascii=False, sort_keys=True, indent=4)
                                        await r.send_msg("写入成功", msg["group_id"], "group")

                    else:
                        rank = mesl1[1]
                        lesson_name = mesl1[2]
                        teacher = mesl1[3]
                        place = mesl1[4]
                        dic_new = {"rank": rank, "lesson_name": lesson_name, "teacher": teacher, "place": place}
                        lists = [dic_new]
                        data_ = {mesl1[0]: lists}
                        dic_newly = {"user": msg["sender"]["user_id"], "data": data_, "bool": True}
                        data.append(dic_newly)
                        with open(lesson_file, 'w', encoding='utf-8') as f2:
                            json.dump(data, f2, ensure_ascii=False, sort_keys=True, indent=4)
                            await r.send_msg("写入成功", msg["group_id"], "group")
            else:
                await r.send_msg("格式可能有误嗷~", msg["group_id"], "group")
        except Exception as e:
            print(e)


async def lesson_help(msg):
    if msg["message"] == "课表帮助":
        await r.send_msg(
            "课程使用说明：\n该功能为群聊功能，添加课程请按格式“课表 参数一 参数2 课程名 老师名 教室”\n参数一：0~6分别对应星期一到星期日\n参数二（以两节小课为一个单元）：first,second,third,fourth,fifth,sixth分别代表上午两节，下午两节，晚上两节课\n例：课表 0 first 大学英语 刘莹 天山堂A608\n代表星期一第1，2节课（8：30~10：10）",
            msg["group_id"], "group")


w_place_data = [221, 379, 538, 697, 855, 1015, 1174]
h_place_data = {"first": 63, "second": 162, "third": 349, "fourth": 445, "fifth": 540, "sixth": 632}
width = 150
height = 90
img_path = 'lesson.png'
color_list = [(251, 255, 242, 200), (192, 192, 192, 200), (255, 255, 0, 200), (244, 164, 95, 200), (127, 255, 0, 200),
              (218, 112, 214, 200),
              (153, 51, 250, 200), (34, 139, 34, 200), (255, 192, 203, 200), (255, 127, 80, 200), (237, 145, 33, 200)]


def lesson_img_make(user):
    with open(lesson_file, 'r', encoding='utf-8') as f1:
        data = json.load(f1)
        for sec in data:
            if int(sec["user"]) == user:
                data_class = sec
                break
        img = Image.open('lesson.png', 'r')
        font = ImageFont.truetype("font/萝莉体.ttf", 20)
        img.convert("RGBA")
        draw = ImageDraw.Draw(img, "RGBA")
        color_data = {}
        for weektime in range(7):
            try:
                class_ = data_class["data"][str(weektime)]
                for i in class_:
                    if i["lesson_name"] in list(color_data.keys()):
                        color = color_data[i["lesson_name"]]
                    else:
                        color = random.choice(list(set(color_list) - set(list(color_data.values()))))
                        color_data[i["lesson_name"]] = color
                    draw.rectangle((w_place_data[weektime], h_place_data[i["rank"]], w_place_data[weektime] + 160,
                                    h_place_data[i["rank"]] + 100), fill=color, outline=color)
                    draw.text((w_place_data[weektime] + 10, h_place_data[i["rank"]] + 12), text=i["lesson_name"],
                              font=font, fill=(0, 0, 0, 255))
                    draw.text((w_place_data[weektime] + 30, h_place_data[i["rank"]] + 42), text=i["teacher"], font=font,
                              fill=(0, 0, 0, 255))
                    draw.text((w_place_data[weektime] + 20, h_place_data[i["rank"]] + 72), text=i["place"], font=font,
                              fill=(0, 0, 0, 255))
            except Exception as e:
                print(e)
        img.save("les.png")


async def lesson_send(msg):
    if msg["message"] == "小巫课表":
        try:
            lesson_img_make(int(msg["sender"]["user_id"]))
            await r.send_msg("[CQ:image,file=file:///root/witch/les.png]", msg["group_id"], "group")
            if os.path.exists("les.png"):
                os.remove("les.png")
        except Exception as e:
            print(e)


def combine(key, text):
    num = len(text)
    text = [i for i in text]
    if num == 1:
        img = Image.new('RGBA', (320, 90), (255, 255, 255, 255))
        font = ImageFont.truetype("font/萝莉体.ttf", 20)
        img.convert("RGBA")
        draw = ImageDraw.Draw(img, "RGBA")
        draw.text((5, 45), text=key, font=font, fill=(0, 255, 0, 255))
        draw.text((125, 15), text=text[0], font=font, fill=(0, 255, 0, 255))


    else:

        max_high = 90 * num
        know_list = os.listdir('data/knowledge')
        know_list = [s.strip('.png') for s in know_list]
        knows_width = []
        knows = []
        for i in text:
            if i in know_list:
                knows.append(i)
                ims = Image.open("data/knowledge/" + i + '.png')
                size = ims.size
                max_high += size[1] - 90
                knows_width.append(size[0])
        if knows_width:
            max_width = 120 + max(knows_width)
        else:
            max_width = 320
        inner_list = []
        for k in text:
            if k in knows:
                pass
            else:
                inner_list.append(k)
        img = Image.new('RGBA', (max_width, max_high), (255, 255, 255, 255))
        fon1 = int(90 / len(key))
        font = ImageFont.truetype("font/萝莉体.ttf", fon1)
        img.convert("RGBA")
        draw = ImageDraw.Draw(img, "RGBA")
        draw.text((5, max_high / 2 - 20), text=key, font=font, fill=(0, 255, 0, 255))
        logg = Image.open('data/simp.png', 'r').resize((20, max_high))
        img.paste(logg, (100, 0, 120, max_high))
        font = ImageFont.truetype("font/萝莉体.ttf", 15)
        inner_list = [' · ' + i for i in inner_list]
        for i in range(len(inner_list)):
            if len(inner_list[i]) <= 12:
                font = ImageFont.truetype("font/萝莉体.ttf", int(190 / len(inner_list[i])))
                draw.text((125, 90 * i + 30), text=inner_list[i], font=font, fill=(0, 0, 0, 255))
            if 12 < len(inner_list[i]) <= 24:
                font = ImageFont.truetype("font/萝莉体.ttf", int(280 / len(inner_list[i])))
                draw.text((125, 90 * i + 15), text=inner_list[i][0:(int(len(inner_list[i]) / 2) + 4)], font=font,
                          fill=(0, 0, 0, 255))
                draw.text((140, 90 * i + 45),
                          text=inner_list[i][(len(inner_list[i]) - int(len(inner_list[i]) / 2) + 3)::], font=font,
                          fill=(0, 0, 0, 255))
            if 24 < len(inner_list[i]) <= 36:
                font = ImageFont.truetype("font/萝莉体.ttf", 15)
                draw.text((125, 90 * i + 15), text=inner_list[i][0:15], font=font, fill=(0, 0, 0, 255))
                draw.text((140, 90 * i + 40), text=inner_list[i][15:27], font=font, fill=(0, 0, 0, 255))
                draw.text((140, 90 * i + 65), text=inner_list[i][27::], font=font, fill=(0, 0, 0, 255))
            if len(inner_list[i]) > 36:
                font = ImageFont.truetype("font/萝莉体.ttf", int(500 / len(inner_list[i])))
                draw.text((125, 90 * i + 15), text=inner_list[i][0:(int(len(inner_list[i]) / 3) + 3)], font=font,
                          fill=(0, 0, 0, 255))
                draw.text((140, 90 * i + 40),
                          text=inner_list[i][(int(len(inner_list[i]) / 3) + 3):(2 * int(len(inner_list[i]) / 3) + 3)],
                          font=font, fill=(0, 0, 0, 255))
                draw.text((140, 90 * i + 65), text=inner_list[i][(2 * int(len(inner_list[i]) / 3) + 3)::], font=font,
                          fill=(0, 0, 0, 255))
        highmid = 90 * len(inner_list)
        for j in range(len(knows)):
            ps = Image.open("data/knowledge/" + knows[j] + '.png')
            size = ps.size
            img.paste(ps, (125, highmid, 125 + size[0], highmid + size[1]))
            highmid += size[1]
    img.save('data/knowledge/%s.png' % key)


async def knowledge(msg):
    know_list = os.listdir('data/knowledge')
    know_list = [s.strip('.png') for s in know_list]
    if re.match("知识 ", msg["message"], flags=0) is not None:
        msg_Text = msg["message"]
        try:
            read = str(msg_Text[3::])
            keystruct = read.split(' ')
            key = keystruct[0]
            text = keystruct[1::]
            if key in know_list:
                await r.send_msg("定义失败，已存在这一知识点", msg["group_id"], "group")
            else:
                combine(key, text)
                await r.send_msg("定义成功[CQ:image,file=file:///root/witch/data/knowledge/%s.png]" % key, msg["group_id"],
                                 "group")
        except Exception as e:
            await r.send_msg(e, msg["group_id"], "group")
    if re.match("删除知识 ", msg["message"], flags=0) is not None:
        key = msg["message"][5::]
        if key in know_list:
            if os.path.exists('data/knowledge/%s.png' % key):
                os.remove('data/knowledge/%s.png' % key)
                await r.send_msg("%s 知识已遗忘" % key, msg["group_id"],
                                 "group")
            else:
                await r.send_msg("记忆出错，删除失败呜呜~" % key, msg["group_id"], "group")
        else:
            await r.send_msg("小巫并不记得有这个知识点~", msg["group_id"], "group")
    if msg["message"] in know_list:
        key = msg["message"]
        await r.send_msg("[CQ:image,file=file:///root/witch/data/knowledge/%s.png]" % key, msg["group_id"],
                         "group")
    if msg["message"] == "知识列表":
        s = ""
        for s_ in know_list:
            s += s_ + "\n"
        await r.send_msg(s, msg["group_id"], "group")
    if re.match("查询知识 ", msg["message"], flags=0) is not None:
        key = msg["message"][5::]
        s = ""
        for i in know_list:
            if re.search(key, i, flags=0) is not None:
                s += i + '\n'
        await r.send_msg("%s 的查询结果如下：\n" % key+s, msg["group_id"], "group")

# -*- coding: utf-8 -*-
import re
import json
import Replymsg
import random
import aiohttp
import urllib
from lxml import etree
from bs4 import BeautifulSoup

defile = "data/define.json"
last_file = "data/last.json"
eat_file = "data/eat.json"


async def defgain(msg):
    if re.match("定义 ", msg["message"], flags=0) is not None:
        msg_Text = msg["message"]
        try:
            read = str(msg_Text[3::])
            keystruct = read.split(' ')
            eps = True
            with open(defile, 'r', encoding='utf-8-sig') as f:
                dic = json.load(f)
                item_list = []
                adds = {'group_id': msg["group_id"], 'keyword': keystruct[0], 'defman': msg["sender"]["nickname"],
                        'message': keystruct[1::]}
                for i in range(len(dic)):
                    if keystruct[0] == dic[i]["keyword"]:
                        if msg["group_id"] == dic[i]["group_id"]:
                            eps = False
                            await Replymsg.send_msg("该词已被定义过了哦~~请先删除后定义", msg["group_id"], "group")
                            print("[REPLY(%d)]:" % msg["group_id"], "defineded")
                            break
                if eps:
                    for k in range(len(dic)):
                        group_id = dic[k]["group_id"]
                        keyword = dic[k]["keyword"]
                        defman = dic[k]["defman"]
                        message = dic[k]["message"]
                        new_dic = {'group_id': group_id, 'keyword': keyword, 'defman': defman, 'message': message}
                        item_list.append(new_dic)
                    item_list.append(adds)
                    with open(defile, 'w', encoding='utf-8') as f2:
                        json.dump(item_list, f2, ensure_ascii=False, sort_keys=True, indent=4)
                        await Replymsg.send_msg("小巫记住了！", msg["group_id"], "group")
                        print("[REPLY(%d)]:" % msg["group_id"], "小巫记住了！")
        except:
            await Replymsg.send_msg("格式可能有些错误呢~", msg["group_id"], "group")
            print("[REPLY(%d)]:" % msg["group_id"], "定义格式错误")


async def defreply(msg):
    try:
        with open(defile, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            for i in range(len(data)):
                if msg["message"] == data[i]["keyword"]:
                    if msg["group_id"] == data[i]["group_id"]:
                        s = ''
                        for k in range(0, len(data[i]["message"])):
                            s += data[i]["message"][k] + " "
                        await Replymsg.send_msg(s, msg["group_id"], "group")
                        print("[REPLY(%d)]:" % msg["group_id"], "回复定义%s" % data[i]["keyword"])
    except Exception as e:
        print(e)


async def defrm(msg):
    if re.match("删除定义 ", msg["message"], flags=0) is not None:
        msgdata = str(msg["message"][5::])
        key_rm = msgdata.split(' ')
        lip = True
        item_list = []
        with open(defile, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i in range(len(data)):
                if key_rm[0] == data[i]["keyword"]:
                    if msg["group_id"] == data[i]["group_id"]:
                        lip = False
                        try:
                            for j in range(len(data)):
                                if j != i:
                                    group_id = data[j]["group_id"]
                                    keyword = data[j]["keyword"]
                                    defman = data[j]["defman"]
                                    message = data[j]["message"]
                                    new_dic = {'group_id': group_id, 'keyword': keyword, 'defman': defman,
                                               'message': message}
                                    item_list.append(new_dic)
                            f.close()
                            with open(defile, 'w', encoding='utf-8') as f2:
                                json.dump(item_list, f2, ensure_ascii=False, sort_keys=True, indent=4)
                                await Replymsg.send_msg("小巫不记得什么是%s了~" % key_rm[0], msg["group_id"], "group")
                                print("[REPLY(%d)]:" % msg["group_id"], "小巫不记得什么是%s了~" % key_rm[0])
                        except Exception as e:
                            raise e
            if lip:
                await Replymsg.send_msg("格式可能出错嗷，当然也可能是小巫不记得%s了~" % key_rm[0], msg["group_id"], "group")
                print("[REPLY(%d)]:" % msg["group_id"], "格式可能出错嗷，当然也可能是小巫不记得%s了~" % key_rm[0])


async def get_coser_image():
    # 推次元
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' + '(KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    rand_int = random.randint(1, 19)
    if rand_int == 1:
        url = "https://t2cy.com/acg/cos/index.html"
    else:
        url = "https://t2cy.com/acg/cos/index_%d.html" % rand_int
    async with aiohttp.ClientSession() as session:
        async with await session.get(url=url, headers=headers) as response:
            url_text = await response.text()
        tree = etree.HTML(url_text)
        url_list = tree.xpath('//ul[@class="cy2-coslist clr"]/li/h3/a/@href')
        target_url = "https://t2cy.com" + url_list[random.randint(0, len(url_list) - 1)]
        async with await session.get(url=target_url, headers=headers) as response:
            target_text = await response.text()
        target_tree = etree.HTML(target_text)
        img_src = target_tree.xpath('//div/p/img/@src')
        if len(img_src) == 0:
            img_src = target_tree.xpath('//div/p/img/@data-loadsrc')
            return "https://t2cy.com" + img_src[random.randint(0, len(img_src) - 1)]
        else:
            src = img_src[random.randint(0, len(img_src) - 1)]
            if src.startswith("/"):
                src = "https://t2cy.com" + src
            return src


async def defman(msg):
    if re.match("定义人 ", msg["message"], flags=0):
        msgdata = str(msg["message"][4::])
        key_man = msgdata.split(' ')
        lip = True
        with open(defile, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i in range(len(data)):
                if key_man[0] == data[i]["keyword"]:
                    if msg["group_id"] == data[i]["group_id"]:
                        lip = False
                        reply_man = data[i]["defman"]
                        await Replymsg.send_msg("教给小巫‘%s’定义的人是:%s" % (key_man[0], reply_man), msg["group_id"], "group")
                        print("[REPLY(%d)]:" % msg["group_id"], "小巫不记得什么是%s了~" % key_man[0])
        if lip:
            await Replymsg.send_msg("格式可能出错嗷，当然也可能是小巫不记得%s了~" % key_man[0], msg["group_id"], "group")
            print("[REPLY(%d)]:" % msg["group_id"], "格式可能出错嗷，当然也可能是小巫不记得%s了~" % key_man[0])


def jrrp_rate(jr):
    if jr <= 20:
        return "大凶"
    if 20 < jr <= 40:
        return "凶"
    if 40 < jr <= 50:
        return "小凶"
    if 50 < jr <= 60:
        return "末吉"
    if 60 < jr <= 80:
        return "中吉"
    if jr > 80:
        return "大吉"



async def baidu_zhidao(keyword, group_id):
    find_key = urllib.parse.quote(keyword)
    url_find = 'https://baike.baidu.com/search?word=%s&pn=0&rn=0&enc=utf8' % find_key
    hand = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"
    }
    res = urllib.request.Request(url_find, headers=hand)
    try:
        response = urllib.request.urlopen(res)
        html = response.read().decode('utf-8')
        bs = BeautifulSoup(html, "html.parser")
        first_find = bs.select("a[class='result-title']", limit=1)
        rule = re.compile(r'href="(.*?)"')
        https = re.findall(rule, str(first_find))[0]
        await Replymsg.send_msg(urllib.parse.quote(https), group_id, 'group')
    except Exception as e:
        await Replymsg.send_msg("小巫查不到%s呜呜呜~" % keyword, group_id, "group")


async def weather_reply(keyword, group_id):
    key = "8a2e37318173402a592e410d38e6c56e"
    keyword_handle = urllib.parse.quote(keyword)
    url_request = 'http://apis.juhe.cn/simpleWeather/query?city=%s&key=%s' % (keyword_handle, key)
    try:
        response = urllib.request.urlopen(url_request)
        info = json.load(response)
        await Replymsg.send_msg("%s的天气是：%s \n温度为：%s℃ \n风向为：%s \n风速为：%s " % (
            keyword, info["result"]["realtime"]["info"], info["result"]["realtime"]["temperature"],
            info["result"]["realtime"]["direct"], info["result"]["realtime"]["power"]), group_id, "group")
    except Exception as e:
        await Replymsg.send_msg("小巫没有查到相关城市的天气嗷", group_id, "group")
        print(e)


async def eat_gain(msg):
    if re.match("小巫中餐 ", msg["message"], flags=0) is not None and ["message"][5::] != "":
        try:
            read = str(msg["message"][5::])
            eps = True
            with open(eat_file, 'r', encoding='utf-8-sig') as f:
                dic = json.load(f)
                item_list = []
                adds = {"type": "中餐", "name": read, "group_id": msg["group_id"]}
                for i in range(len(dic)):
                    if read == dic[i]["name"]:
                        if msg["group_id"] == dic[i]["group_id"] and dic[i] == "中餐":
                            eps = False
                            await Replymsg.send_msg("该该菜已经在菜谱中了嗷~", msg["group_id"], "group")
                            print("[REPLY(%d)]:" % msg["group_id"], "defineded")
                            break
                if eps:
                    for k in range(len(dic)):
                        group_id = dic[k]["group_id"]
                        type = dic[k]["type"]
                        name = dic[k]["name"]
                        new_dic = {'group_id': group_id, 'type': type, 'name': name}
                        item_list.append(new_dic)
                    item_list.append(adds)
                    with open(eat_file, 'w', encoding='utf-8') as f2:
                        json.dump(item_list, f2, ensure_ascii=False, sort_keys=True, indent=4)
                        await Replymsg.send_msg("小巫学会这道菜了！", msg["group_id"], "group")
                        print("[REPLY(%d)]:" % msg["group_id"], "小巫学菜")
        except:
            await Replymsg.send_msg("菜的格式可能有些错误呢~", msg["group_id"], "group")
            print("[REPLY(%d)]:" % msg["group_id"], "定义格式错误")
    if re.match("小巫早餐 ", msg["message"], flags=0) is not None and ["message"][5::] != "":
        try:
            read = str(msg["message"][5::])
            eps = True
            with open(eat_file, 'r', encoding='utf-8-sig') as f:
                dic = json.load(f)
                item_list = []
                adds = {"type": "早餐", "name": read, "group_id": msg["group_id"]}
                for i in range(len(dic)):
                    if read == dic[i]["name"]:
                        if msg["group_id"] == dic[i]["group_id"] and dic[i] == "早餐":
                            eps = False
                            await Replymsg.send_msg("该该菜已经在菜谱中了嗷~", msg["group_id"], "group")
                            print("[REPLY(%d)]:" % msg["group_id"], "defineded")
                            break
                if eps:
                    for k in range(len(dic)):
                        group_id = dic[k]["group_id"]
                        type = dic[k]["type"]
                        name = dic[k]["name"]
                        new_dic = {'group_id': group_id, 'type': type, 'name': name}
                        item_list.append(new_dic)
                    item_list.append(adds)
                    with open(eat_file, 'w', encoding='utf-8') as f2:
                        json.dump(item_list, f2, ensure_ascii=False, sort_keys=True, indent=4)
                        await Replymsg.send_msg("小巫学会这道菜了！", msg["group_id"], "group")
                        print("[REPLY(%d)]:" % msg["group_id"], "小巫学菜")
        except:
            await Replymsg.send_msg("菜的格式可能有些错误呢~", msg["group_id"], "group")
            print("[REPLY(%d)]:" % msg["group_id"], "定义格式错误")
    if re.match("小巫晚餐 ", msg["message"], flags=0) is not None and ["message"][5::] != "":
        try:
            read = str(msg["message"][5::])
            eps = True
            with open(eat_file, 'r', encoding='utf-8-sig') as f:
                dic = json.load(f)
                item_list = []
                adds = {"type": "晚餐", "name": read, "group_id": msg["group_id"]}
                for i in range(len(dic)):
                    if read == dic[i]["name"]:
                        if msg["group_id"] == dic[i]["group_id"] and dic[i] == "晚餐":
                            eps = False
                            await Replymsg.send_msg("该该菜已经在菜谱中了嗷~", msg["group_id"], "group")
                            print("[REPLY(%d)]:" % msg["group_id"], "defineded")
                            break
                if eps:
                    for k in range(len(dic)):
                        group_id = dic[k]["group_id"]
                        type = dic[k]["type"]
                        name = dic[k]["name"]
                        new_dic = {'group_id': group_id, 'type': type, 'name': name}
                        item_list.append(new_dic)
                    item_list.append(adds)
                    with open(eat_file, 'w', encoding='utf-8') as f2:
                        json.dump(item_list, f2, ensure_ascii=False, sort_keys=True, indent=4)
                        await Replymsg.send_msg("小巫学会这道菜了！", msg["group_id"], "group")
                        print("[REPLY(%d)]:" % msg["group_id"], "小巫学菜")
        except:
            await Replymsg.send_msg("菜的格式可能有些错误呢~", msg["group_id"], "group")
            print("[REPLY(%d)]:" % msg["group_id"], "定义格式错误")


async def eat_out(msg):
    with open(eat_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if msg["message"] == "小巫早餐":
            cai = []
            try:
                for i in range(len(data)):
                    if data[i]["type"] == "早餐" and data[i]["group_id"] == msg["group_id"]:
                        cai.append(data[i]["name"])
                await Replymsg.send_msg(random.choice(cai), msg["group_id"], "group")
            except Exception:
                await Replymsg.send_msg("菜谱里可能还没有菜嗷~", msg["group_id"], "group")
        if msg["message"] == "小巫中餐":
            cai = []
            try:
                for i in range(len(data)):
                    if data[i]["type"] == "中餐" and data[i]["group_id"] == msg["group_id"]:
                        cai.append(data[i]["name"])
                await Replymsg.send_msg(random.choice(cai), msg["group_id"], "group")
            except Exception:
                await Replymsg.send_msg("菜谱里可能还没有菜嗷~", msg["group_id"], "group")
        if msg["message"] == "小巫晚餐":
            cai = []
            try:
                for i in range(len(data)):
                    if data[i]["type"] == "晚餐" and data[i]["group_id"] == msg["group_id"]:
                        cai.append(data[i]["name"])
                await Replymsg.send_msg(random.choice(cai), msg["group_id"], "group")
            except Exception:
                await Replymsg.send_msg("菜谱里可能还没有菜嗷~", msg["group_id"], "group")


async def defmsg(msg):
    if re.match("定义列表", msg["message"], flags=0) is not None:
        try:
            with open(defile, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                list_return = []
                s = ""
                for i in data:
                    if i["group_id"] == int(msg["group_id"]):
                        list_return.append(i["keyword"])
                for j in list_return:
                    s += j + "\n"
                await Replymsg.send_msg(f"小巫在这个群的定义有：\n{s}", msg["group_id"], "group")
        except:
            await Replymsg.send_msg("小巫记忆出错了，唔", msg["group_id"], "group")


arrage_file = 'data/time_arrange.json'


async def times_arrage(msg):
    if re.match("定时 ", msg["message"], flags=0) is not None:
        try:
            messy = msg["message"].split(' ')
            print(1)
            time = [messy[2], messy[3], messy[4]]
            times = messy[1]
            note = messy[-1]
            group_id = msg["group_id"]
            def_man = msg["sender"]['user_id']

            dic = {"time": time, "times": times, 'note': note, "def_man": def_man, "group_id": group_id}
            with open(arrage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                data.append(dic)
            with open(arrage_file, 'w', encoding='utf-8') as f1:
                json.dump(data, f1, ensure_ascii=False, sort_keys=True, indent=4)
            await Replymsg.send_msg("定时成功[CQ:at,qq=%d]" % def_man, msg["group_id"], "group")
        except Exception as e:
            print(e)

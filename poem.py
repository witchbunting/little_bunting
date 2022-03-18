# -*- coding: utf-8 -*-
import json
import sys
import re
import random
import Replymsg
from time import time

store_file = 'data/CET6/store.json'




def chs_to_cht(line):
    for i in range(0, len(line)):
        if line[i] in zh2Hans.keys():
            line.replace('%s' % line[i], '%s' % zh2Hans["%s" % line[i]])
    return line

async def songshi_reply(msg):
    if re.match('小巫宋诗', msg["message"]):
        try:
            with open("data/poem/poet.song.%d.json" % (1000 * random.randint(0, 254)), 'r', encoding='utf-8-sig') as f:
                dic = json.load(f)
                dsr = random.choice(dic)
                title = chs_to_cht(line=dsr["title"])
                author = chs_to_cht(line=dsr["author"])
                paragraph = ''
                for j in range(0, len(dsr["paragraphs"])):
                    paragraph += dsr["paragraphs"][j] + '\n'
                await Replymsg.send_msg("%s\n  %s\n%s" % (title, author, paragraph), msg["group_id"], "group")
                print("[REPLY(%d)]:" % msg["group_id"], "宋诗")
        except Exception as e:
            raise e


async def tangshi_reply(msg):
    if re.match('小巫唐诗', msg["message"]):
        try:
            with open("data/poem/poet.tang.%d.json" % (1000 * random.randint(0, 57)), 'r', encoding='utf-8-sig') as f:
                dic = json.load(f)
                dsr = random.choice(dic)
                title = chs_to_cht(line=dsr["title"])
                author = chs_to_cht(line=dsr["author"])
                paragraph = ''
                for j in range(0, len(dsr["paragraphs"])):
                    paragraph += dsr["paragraphs"][j]+ '\n'
                await Replymsg.send_msg("%s\n  %s\n%s" % (title, author, paragraph), msg["group_id"], "group")
                print("[REPLY(%d)]:" % msg["group_id"], "唐诗")
        except Exception as e:
            raise e


async def songci_reply(msg):
    if re.match('小巫宋词', msg["message"]):
        try:
            with open("data/ci/ci.song.%d.json" % (1000 * random.randint(0, 21)), 'r', encoding='utf-8-sig') as f:
                dic = json.load(f)
                dsr = random.choice(dic)
                rhythmic = chs_to_cht(line=dsr["rhythmic"])
                author = chs_to_cht(line=dsr["author"])
                paragraph = ''
                for j in range(0, len(dsr["paragraphs"])):
                    paragraph += chs_to_cht(line=dsr["paragraphs"][j]) + '\n'
                await Replymsg.send_msg("%s\n  %s\n%s" % (rhythmic, author, paragraph), msg["group_id"], "group")
                print("[REPLY(%d)]:" % msg["group_id"], "宋词")
        except Exception as e:
            raise e


async def shijing_reply(msg):
    if re.match('小巫诗经', msg["message"]):
        try:
            with open("data/shijing/shijing.json", 'r', encoding='utf-8-sig') as f:
                dic = json.load(f)
                dsr = random.choice(dic)
                title = chs_to_cht(line=dsr["title"])
                chapter = chs_to_cht(line=dsr["chapter"])
                section = chs_to_cht(line=dsr["section"])
                paragraph = ''
                for j in range(0, len(dsr["content"])):
                    paragraph += chs_to_cht(line=dsr["content"][j]) + '\n'
                await Replymsg.send_msg("%s·%s·%s\n%s" % (chapter, section, title, paragraph), msg["group_id"], "group")
                print("[REPLY(%d)]:" % msg["group_id"], "诗经")
        except Exception as e:
            raise e


async def lunyu_reply(msg):
    if re.match('小巫论语', msg["message"]):
        try:
            with open("data/lunyu/lunyu.json", 'r', encoding='utf-8-sig') as f:
                dic = json.load(f)
                dsr = random.choice(dic)
                chapter = chs_to_cht(line=dsr["chapter"])
                paragraph = chs_to_cht(line=random.choice(dsr["paragraphs"]))
                await Replymsg.send_msg("%s\n%s" % (chapter, paragraph), msg["group_id"], "group")
                print("[REPLY(%d)]:" % msg["group_id"], "论语")
        except Exception as e:
            raise e


async def yuanqu_reply(msg):
    if re.match('小巫元曲', msg["message"]):
        try:
            with open("data/yuanqu/yuanqu.json", 'r', encoding='utf-8-sig') as f:
                dic = json.load(f)
                dsr = random.choice(dic)
                title = chs_to_cht(line=dsr["title"])
                author = chs_to_cht(line=dsr["author"])
                paragraph = ''
                for j in range(0, len(dsr["paragraphs"])):
                    paragraph += chs_to_cht(line=dsr["paragraphs"][j]) + '\n'
                await Replymsg.send_msg("%s\n  %s\n%s" % (title, author, paragraph), msg["group_id"], "group")
                print("[REPLY(%d)]:" % msg["group_id"], "元曲")
        except Exception as e:
            raise e


async def youmeng_reply(msg):
    if re.match('小巫幽梦影', msg["message"]):
        try:
            with open("data/youmengying/youmengying.json", 'r', encoding='utf-8-sig') as f:
                dic = json.load(f)
                dsr = random.choice(dic)
                content = dsr["content"]
                comment = ''
                for j in range(0, len(dsr["comment"])):
                    comment += dsr["comment"][j] + '\n'
                await Replymsg.send_msg("%s\n论曰：%s" % (content, comment), msg["group_id"], "group")
                print("[REPLY(%d)]:" % msg["group_id"], "元曲")
        except Exception as e:
            raise e


async def daxue_reply(msg):
    if re.match('小巫大学', msg["message"]):
        try:
            with open("data/sishuwujing/daxue.json", 'r', encoding='utf-8-sig') as f:
                dic = json.load(f)
                dsr = random.choice(dic["message"])
                await Replymsg.send_msg("大学\n%s" % dsr, msg["group_id"], "group")
                print("[REPLY(%d)]:" % msg["group_id"], "大学")
        except Exception as e:
            raise e


async def CET_random(msg):
    if msg["message"] == "cet":
        with open("data/CET6/CET6.json", 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            s = random.choice(data)
            ms = s["word"] + '\n' + s["mean"] + "\n编号为：" + str(s["rank"])
            await Replymsg.send_msg(ms, msg['group_id'], "group")


async def CET_ranket(msg):
    if re.match('cet ', msg["message"]) and msg["message"][4::].isnumeric():
        try:
            with open("data/CET6/CET6.json", 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                for s in data:
                    if s["rank"] == int(msg["message"][4::]):
                        ms = s["word"] + '\n' + s["mean"] + "\n编号为：" + str(s["rank"])
                        await Replymsg.send_msg(ms, msg['group_id'], "group")
        except Exception as e:
            await Replymsg.send_msg("输入可能有误嗷~", msg['group_id'], "group")


async def CET(msg):
    if msg["message"] == "CET":
        try:
            with open("data/CET6/CETgroup.json", 'r', encoding='utf-8-sig') as f:
                ref = json.load(f)
                bool_open = True
                for part in ref:
                    if part["group_id"] == msg["group_id"] and part["user"] == msg["sender"]["user_id"]:
                        await Replymsg.send_msg("游戏已经开始了嗷！[CQ:at,qq=%s]" % str(msg["sender"]["user_id"]),
                                                msg["group_id"],
                                                "group")
                        bool_open = False
                if bool_open:
                    with open("data/CET6/CET6.json", 'r', encoding='utf-8-sig') as f1:
                        data = json.load(f1)
                        ideal = random.choice(data)
                        word = ideal["word"]
                        mean = ideal["mean"]
                        unknow = "_ " * len(word)
                        start_time = time()
                        have_gain = []
                        life = len(word) + 3
                        dic = {"word": word, "mean": mean, "unknow": unknow, "time": start_time,
                               "group_id": msg["group_id"], "user": msg["sender"]["user_id"],
                               "have_gain": have_gain, "life": life}
                        ref.append(dic)
                        await Replymsg.send_msg(
                            "游戏开始，请输入猜的字母或单词[CQ:at,qq=%s]" % str(msg["sender"]["user_id"]) + '\n现在的单词是：' + dic[
                                'unknow'] + '\n' + '排除字母为：' + ''.join(
                                dic["have_gain"]) + '\n现在您的生命值为：' + str(dic["life"]),
                            msg["group_id"],
                            "group")
                        with open("data/CET6/CETgroup.json", 'w', encoding='utf-8-sig') as f2:
                            json.dump(ref, f2, ensure_ascii=False, sort_keys=True, indent=4)
        except Exception as e:
            print(e)
    with open("data/CET6/CETgroup.json", 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
        for part in data:
            if part["group_id"] == msg["group_id"] and part["user"] == msg["sender"]["user_id"]:
                if len(msg["message"]) == 1 and msg["message"].isalpha():
                    if msg["message"] in part["word"] and msg["message"] not in part["have_gain"]:
                        part["have_gain"].append(msg["message"])
                        iters = re.finditer(msg["message"], part["word"])
                        for i in iters:
                            part["unknow"] = part["unknow"][:(i.start() * 2)] + msg["message"] + part["unknow"][
                                                                                                 (i.start() * 2 + 1):]
                        rep = '猜对字母加一\n现在的单词是：' + part["unknow"] + '\n' + '排除字母为：' + ''.join(
                            part["have_gain"]) + '\n现在您的生命值为：' + str(part["life"])
                        await Replymsg.send_msg(rep, msg["group_id"], "group")
                        with open("data/CET6/CETgroup.json", 'w', encoding='utf-8-sig') as f3:
                            json.dump(data, f3, ensure_ascii=False, sort_keys=True, indent=4)
                    elif msg["message"] in part["have_gain"]:
                        await Replymsg.send_msg("你已经猜过这个字母了，不要浪费生命嗷！", msg["group_id"], "group")
                    else:
                        part["have_gain"].append(msg["message"])
                        part["life"] = part["life"] - 1
                        rep = '很遗憾，该字母不在这个单词里面\n现在的单词是：' + part["unknow"] + '\n' + '排除字母为：' + ''.join(
                            part["have_gain"]) + '\n现在您的生命值为：' + str(part["life"])
                        await Replymsg.send_msg(rep, msg["group_id"], "group")
                        with open("data/CET6/CETgroup.json", 'w', encoding='utf-8-sig') as f3:
                            json.dump(data, f3, ensure_ascii=False, sort_keys=True, indent=4)
                        if part["life"] <= 0:
                            res = '游戏结束' + '\n单词为：' + part["word"] + '\n释义为：' + part["mean"]
                            await Replymsg.send_msg(res, msg["group_id"], "group")
                            data.remove(part)
                            with open("data/CET6/CETgroup.json", 'w', encoding='utf-8-sig') as f4:
                                json.dump(data, f4, ensure_ascii=False, sort_keys=True, indent=4)
                                break
                if msg["message"] == part["word"] or '_' not in list(part["unknow"]):
                    rep = '恭喜你猜对了\n' + '单词为：' + part["word"] + '\n释义为：' + part["mean"]
                    await Replymsg.send_msg(rep, msg["group_id"], "group")
                    data.remove(part)
                    with open("data/CET6/CETgroup.json", 'w', encoding='utf-8-sig') as f4:
                        json.dump(data, f4, ensure_ascii=False, sort_keys=True, indent=4)
                        break
    with open("data/CET6/CETgroup.json", 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
        t_now = time()
        for part in data:
            if t_now - part["time"] >= 600:
                data.remove(part)
                await Replymsg.send_msg("游戏超时", part["group_id"], "group")
                with open("data/CET6/CETgroup.json", 'w', encoding='utf-8-sig') as f4:
                    json.dump(data, f4, ensure_ascii=False, sort_keys=True, indent=4)
                    break


async def cet_store(msg):
    if re.match('收藏 ', msg["message"]) and msg["message"][3::].isnumeric():
        try:
            with open(store_file, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                nu = False
                for line in data:
                    if line["sender"] == msg["sender"]["user_id"]:
                        line["ranks"].append(msg["message"][3::])
                        with open(store_file, 'w', encoding='utf-8-sig') as f3:
                            json.dump(data, f3, ensure_ascii=False, sort_keys=True, indent=4)
                        await Replymsg.send_msg("添加成功", msg["group_id"], "group")
                        nu = True
                        break
                if not nu:
                    data.append({"sender": msg["sender"]["user_id"], "ranks": [msg["message"][3::]]})
                    with open(store_file, 'w', encoding='utf-8-sig') as f3:
                        json.dump(data, f3, ensure_ascii=False, sort_keys=True, indent=4)
                        await Replymsg.send_msg("添加成功", msg["group_id"], "group")
        except:
            pass


async def cet_s(msg):
    if msg["message"] == "收藏":
        with open(store_file, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            nus = False
            for line in data:
                if line["sender"] == msg["sender"]["user_id"]:
                    rep = ''
                    for j in line["ranks"]:
                        with open("data/CET6/CET6.json", 'r', encoding='utf-8-sig') as f2:
                            words = json.load(f2)
                            for s in words:
                                if int(j) == int(s["rank"]):
                                    rep += str(j) + " " + s["word"] + " " + s["mean"] + '\n'
                    await Replymsg.send_msg(rep, msg["group_id"], "group")
                    nus = True
                    break
            if not nus:
                await Replymsg.send_msg("您还没有收藏词汇嗷", msg["group_id"], "group")


async def rm_store(msg):
    if re.match('删除收藏 ', msg["message"]) and msg["message"][5::].isnumeric():
        try:
            with open(store_file, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                nu = True
                for line in data:
                    if line["sender"] == msg["sender"]["user_id"]:
                        line["ranks"].remove(msg["message"][5::])
                        with open(store_file, 'w', encoding='utf-8-sig') as f3:
                            json.dump(data, f3, ensure_ascii=False, sort_keys=True, indent=4)
                        await Replymsg.send_msg("删除成功", msg["group_id"], "group")
                        nu = False
                        break
                if nu:
                    await Replymsg.send_msg("该单词不在你的收藏列表嗷~", msg["group_id"], "group")
        except:
            pass

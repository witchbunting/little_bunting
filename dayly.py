import time
import re
import json
import Replymsg
from datetime import datetime

jrrp_file = "data/jrrp.json"

dayly_file_data = 'data/dayly.json'

history_list = [702599462, 774261838]
arrage_file = 'data/time_arrange.json'


def daily_init():
    if time_boole(0, 0, 1) or time_boole(1, 00, 00):
        try:
            with open(jrrp_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, sort_keys=True, indent=4)
        except Exception:
            pass


def time_boole(hour, minute, second):
    now = datetime.now()
    arranged = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
    delta = arranged - now
    delta_skip = int(delta.total_seconds())
    if 0 <= delta_skip <= 3:
        return True
    else:
        return False


async def dayly_send():
    daily_init()
    with open(arrage_file, 'r', encoding='utf-8') as f4:
        data = json.load(f4)
        for i in data:
            time_ = i["time"]
            if time_boole(int(time_[0]), int(time_[1]), int(time_[2])) and int(i["times"]) > 0:
                try:
                    await Replymsg.send_msg("[CQ:at,qq=%d]\n%s" % (i["def_man"], i["note"]), i["group_id"], "group")
                    i["times"] = int(i["times"])-1
                    time.sleep(3)
                except Exception as e:
                    pass
        with open(arrage_file, 'w', encoding='utf-8') as f5:
            json.dump(data, f5, ensure_ascii=False, sort_keys=True, indent=4)


async def dayly_save(msg):
    if re.match("小巫定时 ", msg["message"], flags=0) is not None:

        dil1 = msg["message"][5::]
        dil2 = dil1.split(" ")
        item_list = []
        if dil2[1].isnumeric() and dil2[2].isnumeric() and dil2[3].isnumeric():
            try:
                dic_new = {"group_id": int(dil2[0]), "hour": int(dil2[1]), "minute": int(dil2[2]), "second": int(dil2[3]),
                           "message": dil2[4]}
                with open(dayly_file_data, 'r', encoding='utf-8') as f1:
                    total = json.load(f1)
                    for i in range(len(total)):
                        group_id = total[i]["group_id"]
                        hour = total[i]["hour"]
                        minute = total[i]["minute"]
                        second = total[i]["second"]
                        message = total[i]["message"]
                        dic_old = {"group_id": group_id, "hour": hour, "minute": minute, "second": second,
                                   "message": message}
                        item_list.append(dic_old)
                    item_list.append(dic_new)
                with open(dayly_file_data, 'w', encoding='utf-8') as f2:
                    json.dump(item_list, f2, ensure_ascii=False, sort_keys=True, indent=4)
                await Replymsg.send_msg("定时成功", 845986940, "private")
            except Exception:
                    pass


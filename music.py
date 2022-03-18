import requests
import re
import json
import Replymsg
import array
from sympy import Matrix
from sympy.matrices import dense
import numpy as np

# -*- coding: utf-8 -*-
url_Muc = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?aggr=1&cr=1&flag_qc=0&p=1&n=1&w='


async def music(msg):
    msg_Text = msg["message"]
    if re.match('点歌 ', msg_Text):
        Song_Val = ''
        Song_list = msg_Text.split("点歌 ")
        Song_Len = len(Song_list)
        for i in range(Song_Len):
            Song_Val = Song_Val + Song_list[i]
        Song_url = url_Muc + Song_Val
        data_text = requests.get(Song_url).text
        data_json = json.loads(data_text[9:-1])
        SongID = int(data_json["data"]["song"]["list"][0]["songid"])
        await Replymsg.send_msg('[CQ:music,id=%d,type=qq]' % SongID, msg["group_id"], "group")
        print("[REPLY(%d)]:" % msg["group_id"], "音乐")


async def matrix_my(msg):
    msg_Text = msg["message"]
    if re.match('化简 ', msg_Text):
        try:
            read = str(msg_Text[3::])
            row_number = read.count('/')
            line = read.split('/')
            i = 0
            for i in range(0, row_number):
                line[i] = line[i].split(' ')
                i = i + 1
            line_handle = list(filter(None, line))
            arry = np.array(line_handle)
            matrx = Matrix(arry)
            result = matrx.rref()
            result_line = list(result)
            resl = str(result_line)
            await Replymsg.send_msg('矩阵化简为：%s' % resl, msg["group_id"], "group")
            print("[REPLY(%d)]:" % msg["group_id"], "矩阵")
        except:
            await Replymsg.send_msg('小巫觉得这个矩阵无法化简', msg["group_id"], "group")
            print("[REPLY(%d)]:" % msg["group_id"], "矩阵")
    if re.match('行列式 ', msg_Text):
        try:
            read = str(msg_Text[4::])
            row_number = read.count('/')
            line = read.split('/')
            i = 0
            for i in range(0, row_number):
                line[i] = line[i].split(' ')
                i = i + 1
            line_handle = list(filter(None, line))
            arry = np.array(line_handle)
            matrx = Matrix(arry)
            result = matrx.det()
            resd = str(result)
            await Replymsg.send_msg('矩阵的行列式为：%s' % resd, msg["group_id"], "group")
            print("[REPLY(%d)]:" % msg["group_id"], "矩阵")
        except:
            await Replymsg.send_msg('小巫只会求方阵的行列式嗷！', msg["group_id"], "group")
            print("[REPLY(%d)]:" % msg["group_id"], "矩阵")
    if re.match('逆矩阵 ', msg_Text):
        try:
            read = str(msg_Text[4::])
            row_number = read.count('/')
            line = read.split('/')
            i = 0
            for i in range(0, row_number):
                line[i] = line[i].split(' ')
                i = i + 1
            line_handle = list(filter(None, line))
            arry = np.array(line_handle)
            matrx = Matrix(arry)
            result = matrx.inv()
            resi = str(result)
            await Replymsg.send_msg('该矩阵的矩阵为：%s' % resi, msg["group_id"], "group")
            print("[REPLY(%d)]:" % msg["group_id"], "矩阵")
        except:
            await Replymsg.send_msg('该矩阵好像不可逆~', msg["group_id"], "group")
            print("[REPLY(%d)]:" % msg["group_id"], "矩阵")

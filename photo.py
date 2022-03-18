# -*- coding: utf-8 -*-
import os
import re
import json
import Replymsg
import random
import aiohttp
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from urllib import request
import Replymsg as R


async def xiangsu(msg):
    m = re.compile("url=(.*)]")
    if re.match("像素化", msg["message"]) is not None and m.search(msg["message"]) is not None:
        r = m.search(msg["message"]).span()
        img_url = msg["message"][r[0] + 4:r[1] - 1]
        request.urlretrieve(img_url, "photo.png")
        block_size = 10
        img = Image.open("photo.png")
        width, height = img.size
        img_array = img.load()
        max_width = width + block_size
        max_height = height + block_size
        for x in range(block_size - 1, max_width, block_size):
            for y in range(block_size - 1, max_height, block_size):
                if x == max_width - max_width % block_size - 1:
                    x = width - 1
                if y == max_height - max_height % block_size - 1:
                    y = height - 1
                change_block(x, y, block_size, img_array)
                y += block_size
            x += block_size
        img.save('result.png')
        await R.send_msg("[CQ:image,file=file:///root/witch/result.png]", msg["group_id"], "group")
        if os.path.exists('photo.png'):
            os.remove('photo.png')
            os.remove('result.png')


def change_block(x, y, black_size, img_array):
    color_dist = {}
    block_pos_list = []
    for pos_x in range(-black_size + 1, 1):
        for pos_y in range(-black_size + 1, 1):
            # todo print(x + pos_x,y + pos_y)
            block_pos_list.append([x + pos_x, y + pos_y])
    for pixel in block_pos_list:
        if not str(img_array[pixel[0], pixel[1]]) in color_dist.keys():
            color_dist[str(img_array[pixel[0], pixel[1]])] = 1
        else:
            color_dist[str(img_array[pixel[0], pixel[1]])] += 1
    # key-->value => value-->key
    new_dict = {v: k for k, v in color_dist.items()}
    max_color = new_dict[max(color_dist.values())]
    # 将区块内所有的颜色值设置为颜色最多的颜色
    for a in block_pos_list:
        img_array[a[0], a[1]] = tuple(list(map(int, max_color[1:len(max_color) - 1].split(","))))


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]


async def ocr(msg):
    if re.match("ocr", msg["message"]) is not None:
        try:
            img_id = msg["message"].split('=')[1]
            id = img_id.split('.')[0]
            url = 'http://127.0.0.1:5700/ocr_image?image=%s.image' % id
            rep = json.loads(requests.get(url).text)
            texts = rep["data"]["texts"]
            end = ''
            for i in texts:
                end += i["text"] + '\n'
            await Replymsg.send_msg(end, msg["group_id"], "group")
        except Exception as e:
            print(e)


async def saying_lu(msg):
    if re.match("鲁迅说 ", msg["message"]) is not None:
        ms = msg['message'][4::]
        img_file = 'data/image/lx.png'
        img = Image.open(img_file)
        fontpath = "font/word1.ttf"
        font = ImageFont.truetype(fontpath, 40)
        draw = ImageDraw.Draw(img)
        draw.text((100, 300), ms, font=font, fill=(255, 255, 255))
        draw.text((500, 380), '鲁迅说', font=font, fill=(255, 255, 255))
        img.save('lu.png')
        await R.send_msg("[CQ:image,file=file:///root/witch/lu.png]", msg["group_id"], "group")
        if os.path.exists('lu.png'):
            os.remove('lu.png')


async def saying_me(msg):
    if re.match("小巫说 ", msg["message"]) is not None:
        ms = msg['message'][4::]
        img_file = 'data/image/me.png'
        img = Image.open(img_file)
        fontpath = "font/word1.ttf"
        font = ImageFont.truetype(fontpath, 100)
        draw = ImageDraw.Draw(img)
        draw.text((300, 800), ms, font=font, fill=(255, 255, 255))
        draw.text((1300, 900), '小巫说', font=font, fill=(255, 255, 255))
        img.save('me.png')
        await R.send_msg("[CQ:image,file=file:///root/witch/me.png]", msg["group_id"], "group")
        if os.path.exists('me.png'):
            os.remove('me.png')

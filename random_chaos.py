import matplotlib.pyplot as plt
import random
from math import *
import Replymsg
import os
from mpl_toolkits.mplot3d import Axes3D


# 几个非线性函数
# 形式：(d/dt)^2x+a*(d/dt)x+sum(kn*x^n)+b*cos(c*x)
# 取值 -1<=a,kn,γ,b<=1  x=1,y=1 steps=0.002,times=200
def duffing_gain():
    try:
        x_l = []
        y_l = []
        steps = 0.002
        times = 40000
        x = 1
        y = 1
        a = random.randint(-1000, 1000) / 10
        b = random.randint(0, 1000) / 1000
        s = '[(d/dt)^2]x(t)＋(%f)(d/dt)-x＋x^3=(%f)cos(t)' % (a, b)
        for i in range(times):
            dx = y * steps
            dy = (a * cos(i * steps) - b * y + x - x ** 3) * steps
            x += dx
            y += dy
            x_l.append(x)
            y_l.append(y)
        return s, x_l, y_l
    except Exception:
        return duffing_gain()

def points_gain():
    try:
        s = "[(d/dt)^2]*x＋"
        x_l = []
        y_l = []
        steps = 0.002
        times = 40000
        x = 1
        y = 1
        a = random.randint(-100, 100) / 100
        b = random.randint(-100, 100) / 100
        c = random.randint(-100, 100) / 100
        n = random.choice(range(3, 6))
        k = []
        for i in range(1, n):
            kn = random.randint(-100, 100) / 100
            k.append(kn)
            s += "(" + str(kn) + ")*x^" + str(i) + "＋"
        for j in range(times):
            dx = y * steps
            dy = (b * cos(c * x) - sum([k[i] * x ** (i + 1) for i in range(len(k))]) - a * y) * steps
            x += dx
            y += dy
            x_l.append(x)
            y_l.append(y)
        s += "(" + str(a) + ")*(d/dt)x＋%f*cos(%f*x)=0" % (b, c)
        if y_l[-1] > 10 ** 10:
            return points_gain()
        else:
            return s, x_l, y_l
    except Exception:
        return points_gain()


def lorenz_gain():
    x_l = []
    y_l = []
    z_l = []
    steps = 0.001
    times = 80000
    x = 1
    y = 1
    z = 1
    a = 10
    b = random.randint(200, 1000) / 10
    c = 8 / 3
    s = "dx/dt=-%f(x-y)\ndy/dt=%fx-y-xz\ndz/dt=-%fz＋xy" % (a, b, c)
    for i in range(times):
        dx = -a * (x - y) * steps
        dy = (b * x - y - x * z) * steps
        dz = (-c * z + x * y) * steps
        x += dx
        y += dy
        z += dz
        x_l.append(x)
        y_l.append(y)
        z_l.append(z)
    if max(z_l) > 10 ** 3 or max(y_l) > 10 ** 3:
        return lorenz_gain()
    else:
        return s, x_l, y_l, z_l


async def chaos_send(msg):
    if msg["message"] == "随机相图":
        try:
            s, xl, yl = points_gain()
            plt.plot(xl, yl, c='g')
            plt.xlabel("x")
            plt.ylabel("(d/dt)x")
            plt.title("random chaos")
            plt.savefig("./chaos.png")
            plt.cla()
            st = "随机方程：%s [CQ:image,file=file:///root/witch/chaos.png]" % s
            await Replymsg.send_msg(st, msg["group_id"], "group")
            if os.path.exists('chaos.png'):
                os.remove('chaos.png')
        except Exception as e:
            await Replymsg.send_msg(str(e), msg["group_id"], "group")
    if msg["message"] == "duffing":
        try:
            s, xl, yl = duffing_gain()
            plt.plot(xl, yl, 'red')
            plt.xlabel("x")
            plt.ylabel("(d/dt)x")
            plt.title("random duffing oscillators")
            plt.savefig("./duffing.png")
            plt.cla()
            st = "随机参数杜芬振子：%s [CQ:image,file=file:///root/witch/duffing.png]" % s
            await Replymsg.send_msg(st, msg["group_id"], "group")
            if os.path.exists('duffing.png'):
                os.remove('duffing.png')
        except Exception as e:
            await Replymsg.send_msg(str(e), msg["group_id"], "group")
    if msg["message"] == "lorenz":
        try:
            s, xl, yl, zl = lorenz_gain()
            fig = plt.figure()
            fig = Axes3D(fig)
            ax = plt.axes(projection='3d')
            ax.plot(xl, yl, zl,linewidth=1)
            plt.title("lorenz oscillator")
            plt.savefig("./lorenz.png")
            plt.cla()
            st = "%s \n[CQ:image,file=file:///root/witch/lorenz.png]" % s
            await Replymsg.send_msg(st, msg["group_id"], "group")
            if os.path.exists('lorenz.png'):
                os.remove('lorenz.png')
        except Exception as e:
            await Replymsg.send_msg(str(e), msg["group_id"], "group")

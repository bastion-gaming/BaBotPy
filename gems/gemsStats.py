import csv
import datetime as dt
from core import gestion as ge
from gems import gemsFonctions as GF
import matplotlib.pyplot as plt
import gg_lib as gg
from languages import lang as lang_P


def create_graphbourse(ctx, item, yearStart, monthStart, yearEnd, monthEnd):
    ID = ctx.author.id
    now = dt.datetime.now()
    param = dict()
    param["ID"] = ID
    param["item"] = item
    param["yearStart"] = yearStart
    param["monthStart"] = monthStart
    param["yearEnd"] = yearEnd
    param["monthEnd"] = monthEnd

    ge.socket.send_string(gg.std_send_command("csv_read", ID, ge.name_pl, param))
    msg = GF.msg_recv()

    if msg[0] == "NOK":
        return ["404", msg[2]]
    else:
        dataitem = msg[2]
        lang = msg[1]
    axeX = []
    axeY1 = []
    axeY2 = []
    for data in dataitem:
        date_time_obj = dt.datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S.%f')
        axeX.append("{day}\n{h}:{m}".format(day=date_time_obj.day, h=date_time_obj.hour, m=date_time_obj.minute))
        axeY1.append(int(data[1]))
        axeY2.append(int(data[2]))
    namegraph = "bourse_{item} {year}-{month}-{day} {h}_{m}_{s}.png".format(item=item, year=now.year, month=now.month, day=now.day, h=now.hour, m=now.minute, s=now.second)
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(axeX, axeY2, color='tab:blue', label=lang_P.forge_msg(lang, "graphbourse", None, False, 0), marker='8')
    if int(monthStart) == int(monthEnd) and int(yearStart) == int(yearEnd):
        plt.title("{i}  ▌ {m} {y}".format(i=item, m=lang_P.forge_msg(lang, "month", None, False, int(monthStart)-1), y=yearStart))
    else:
        plt.title("{i}  ▌ {m} {y} ▶ {nowM} {nowY}".format(i=item, m=lang_P.forge_msg(lang, "month", None, False, int(monthStart)-1), y=yearStart, nowM=lang_P.forge_msg(lang, "month", None, False, int(monthEnd)-1), nowY=yearEnd))
    plt.margins(x=0.02, y=0.1)
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(axeX, axeY1, color='tab:red', label=lang_P.forge_msg(lang, "graphbourse", None, False, 1), marker='8')
    plt.margins(x=0.02, y=0.1)
    plt.legend()
    plt.savefig("cache/{}".format(namegraph))
    plt.clf()
    return [namegraph, lang]

# -*- coding=utf-8 -*-
import requests_html as rh
import time
import threading as tr


def flu():
    global sss
    while sss < thr:
        fw.flush()
        time.sleep(60)


def load():
    global dictch
    while True:
        line = fr.readline().split()
        if not line:
            break
        else:
            dictch[int(line[0])] = int(line[1])
        #    print((line[0], line[1]))
        #    print(dictch[int(line[0])])
    fr.close()


def finished():
    global sss
    sss = 0
    for stat in lst:
        if not stat:
            sss = 0
        else:
            sss += 1
    if sss == thr:
        fw.close()
        print("Finished.")
    else:
        sss = 0


def sub(j):
    global hexie
    i = j
    sel1 = 'body > section > div > div.manga-desc > div.manga-author > a'
    sel2 = 'body > section > div > div.manga-desc > div.manga-author > span'
    sel3 = 'body > section > div > div.manga-desc > p'
    sel4 = 'body > section > div > div.manga-title > div > h1'
    while i <= times:
        flag3 = 0
        flag4 = 0
        flag2 = 0
        #    print(dictch[i])
        try:
            flag2 = dictch[i] == 3  # 判断是否为和谐，我也不知道为什么这么写，but it just works.
            flag = dictch[i] != 0 and (hexie or not flag2)
            flag4 = dictch[i] == 1
        #        print(dictch[i] != 0, " ", not (hexie and dictch[i] != 3), " ", hexie, " ", dictch[i] != 3)
        except KeyError:
            flag = 1
        #    print(i, " ", flag)
        if flag:
            url = urlo + str(i)
            resp = sess.get(url)
            res1 = resp.html.find(sel1)
            res2 = resp.html.find(sel2)
            res3 = resp.html.find(sel3)
            res4 = resp.html.find(sel4)
            ls1 = []
            t3 = None
            #    print("Test1")
            for r1, r2, r3, r4 in zip(res1, res2, res3, res4):
                t1 = r1.text
                t2 = r2.text
                t3 = r3.text
                t4 = r4.text
                if t3 == "为了坚持正确的价值导向、构建健康的网络环境，本漫画正在进行内容自审，暂时下线，多谢大家的谅解与及支持。":
                    t3 = "自审中"
                    t4 += "(自审中)"
                ls1.append(t4)
                ls1.append(t1)
                ls1.append(t2)
                ls1.append(t3)
            #    print("Test2")
            if hexie or t3 != "自审中":
                if ls1:
                    if not flag4:
                        fw.write(str(i) + " 1\n")
                    for item in ls1:
                        #                print("Test4")
                        print(item)
                    print(url)
                    #        print("Test5")
                    #        print(j)
                    print("\n")
                #        time.sleep(0.1)
                else:
                    fw.write(str(i) + " 0\n")
            #        print("Test6")
            if t3 == "自审中":
                flag3 = 1
        if not flag2 and flag3:
            fw.write(str(i) + " 3\n")
        #    print("Test7")
        i += thr
    lst[j - 1] = 1
    finished()


times = int(input("Range:"))
thr = int(input("Thread:"))
hexie = bool(int(input("Show \"自审中\"?")))
sess = rh.HTMLSession()
urlo = 'http://www.buka.cn/detail/'
fw = open("buka2cache.txt", "a+")
fr = open("buka2cache.txt", "r")
lst = [0] * thr
dictch = {}
sss = 0
load()
tr.Thread(target=flu).start()
for k in range(thr):
    new_thread = tr.Thread(target=sub, args=(k + 1,))
    new_thread.start()

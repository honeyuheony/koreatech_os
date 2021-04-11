import tkinter
import tkinter.font
import tkinter.ttk
import time
import threading
import random
import process
import algorithms
from multiprocessing import Process as mp

plist = []
at_start = 0
for i in range(1, 16):
    globals()['p{}'.format(i)] = process.Process(at_start, random.randrange(1,7))
    plist.append(globals()['p{}'.format(i)])
    at_start += random.randrange(1,3)

al = algorithms.Algorithm(plist, 2)

# var
execution_speed = 1000 # 진행속도
time_tick = 0 # 틱
#ready_queue = []
gantt_queue = []

window=tkinter.Tk()
window.title("운영체제 8조")
window.geometry("960x1080+100+100")
window.resizable(False, False)

#font
label_font = tkinter.font.Font(family="맑은 고딕", size=10, weight='bold')
button_font = tkinter.font.Font(family="맑은 고딕", size=20, slant="italic", )
table_font = ""

# default setting
# Ready queue (for realtime)
title_readyqueue = tkinter.Label(window, text="Ready Queue", width=12, height=4, font = label_font)
canvas_readyqueue = tkinter.Canvas(window, relief="solid", width = 930, height = 60, bd=3)

# Gantt Chart (for realtime)
title_ganttchart = tkinter.Label(window, text="Gantt Chart  |", width=12, height=4, font = label_font)
text_runtime = tkinter.StringVar()
text_runtime.set('  RUNTIME : ' + str(execution_speed * time_tick) + ' ms')
title_runtime = tkinter.Label(window, textvariable = text_runtime, width=20, height=4, anchor = 'w', font = label_font)
canvas_ganttchart = tkinter.Canvas(window, relief="solid", width = 930, height = 60, bd=3)

# Result Table
title_resulttable = tkinter.Label(window, text="Result Table", width=12, height=4, font = label_font)
table_resulttable = tkinter.ttk.Treeview(window, columns = ["AT", "BT", "WT", "TT", "NTT"])
table_resulttable.column("#0", width = '65', anchor = tkinter.CENTER)
table_resulttable.heading("#0", text="Process Name")
table_resulttable.column("AT", width = '130', anchor = 'center')
table_resulttable.heading("AT", text="Arrival Time(AT)")
table_resulttable.column("BT", width = '130', anchor = 'center')
table_resulttable.heading("BT", text="Burst Time(BT)")
table_resulttable.column("WT", width = '130', anchor = 'center')
table_resulttable.heading("WT", text="Waiting Time(WT)")
table_resulttable.column("TT", width = '130', anchor = 'center')
table_resulttable.heading("TT", text="Turnaround Time(TT)")
table_resulttable.column("NTT", width = '130', anchor = 'center')
table_resulttable.heading("NTT", text="Normalized TT(NTT)")

# Ready queue (for realtime)
title_readyqueue.place(x=10, y = 350)
canvas_readyqueue.place(x=10, y = 400, width=940)

# Gantt Chart (for realtime)
title_ganttchart.place(x=10, y = 500)
title_runtime.place(x=125, y = 500)
canvas_ganttchart.place(x=10, y = 550, width=940)

# Result Table
title_resulttable.place(x=10, y=620)
table_resulttable.place(x=10, y=670, width=940, height=350)
# #0 space 6개, table default setting
iid_num = 1
for p in plist :
    table_resulttable.insert('', 'end', text = "      " + p.name
    , values=(p.at, p.bt, p.wt, p.tt, p.ntt), iid = "p" + str(iid_num))
    iid_num += 1


def renew_resulttable(process) :
    return

def show_ready_queue(*queue) :
    canvas_readyqueue.delete("all")
    count = 1
    for p in queue :
        if p == None :
            continue
        fill_color = p.color
        x1 = 5 + 60 * (count - 1) # min = 5
        y1 = 5
        x2 = 5 + 60 * count # max = 935
        y2 = 70
        # (60, 65)의 사각형으로 ready_queue 채우기 
        rectangle = canvas_readyqueue.create_rectangle(x1, y1, x2, y2, fill = fill_color, width = 2)
        text = canvas_readyqueue.create_text(x2-30, 35, text = p.name, font = label_font)
        count = count + 1
    canvas_readyqueue.place(x=10, y = 400)
def put_gantt_chart(*timeLine) :  
    count = 1
    canvas_ganttchart.delete("all")   
    for p in timeLine :
        fill_color = p.color
        x1 = 5 + 30 * (count - 1) # min = 5
        y1 = 5
        x2 = 5 + 30 * count # max = 935
        y2 = 70
        # (30, 65)의 사각형으로 gantt_chart 채우기 
        rectangle = canvas_ganttchart.create_rectangle(x1, y1, x2, y2, fill = fill_color, width = 2)
        text = canvas_ganttchart.create_text(x2-15, 35, text = p.name, font = label_font)
        count = count + 1
    canvas_ganttchart.place(x=10, y=550, width=940)
    

def main() :
    thread1 = None
    thread2 = None
    for i in range(0, 5000) :
        start_time = time.time()
        queue, timeLine, finished, isEnd = al.srtn(i)
        text_runtime.set('RUNTIME : ' + str(execution_speed * i) + ' ms')
        if len(queue) != 0 :
            thread1= threading.Thread(target=show_ready_queue, args=queue)
            thread1.start()
        else : 
            canvas_readyqueue.delete("all")
        # readyqueue와 ganttchart 시간간격
        if (execution_speed/1000) / 2 > (time.time() - start_time) :
            time.sleep((execution_speed/1000) / 2 - (time.time() - start_time))
        if timeLine != None :
            thread2= threading.Thread(target=put_gantt_chart, args=timeLine)
            thread2.start()
        if finished != None :
            table_resulttable.item(finished.name.lower(), text = "      " + finished.name
        , values=(finished.at, finished.bt, finished.wt, finished.tt, finished.ntt))
        if thread1 != None :
            thread1.join()
        if thread2 != None :
            thread2.join()
        # accurate time
        if (execution_speed/1000) > (time.time() - start_time) :
            time.sleep(execution_speed/1000 - (time.time() - start_time))
        if isEnd :
            break
# 라스트출력 문제있음

#show_gantt_chart()
ttt = threading.Thread(target=main)
ttt.start()

window.mainloop()
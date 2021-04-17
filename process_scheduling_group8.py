import tkinter
import tkinter.font
import tkinter.ttk
import time
import threading
import random
import process
import algorithms

process_num = 1 # process 객체 번호매기기
plist = [] # processList
execution_speed = 1000 
running_algorithm = None
selected_algorithm = None

window = tkinter.Tk()
window.title("운영체제 8조")
window.geometry("1460x780+100+100")
window.resizable(False, False)
# 부가적으로 추가할 수 있는 기능 :
# try catch 를 이용한 입력값 제어, 중복시작방지
# delete 시 processname을 순서대로 재배치해주는 작업

# clicked insert button
def insert(event) :
    #global로 선언하여 treeview에 남아있게끔 선언한다.
    global plist
    subp1 = 0
    subp2 = 0
    subp1 = int(entry_at.get())
    subp2 = int(entry_bt.get())
    globals()['p{}'.format(len(plist)+1)] = process.Process((len(plist)+1), subp1, subp2)
    plist.append(globals()['p{}'.format(len(plist)+1)])
    treeview.insert('','end',text=plist[len(plist)-1].name,
        values=(plist[len(plist)-1].at,plist[len(plist)-1].bt),iid="p" + str(len(plist)))

# clicked start button
def start_event(event) :
    global plist
    global execution_speed
    global running_algorithm
    global selected_algorithm
    timeQuntuam = None
    countOfProcessor = 1
    if ent_es.get() != '' :
        execution_speed = int(ent_es.get()) # execution speed
    selected_algorithm = combobox_algorithm.get() # selected_algorithm
    countOfProcessor = int(combobox_processNumber.get())
    if selected_algorithm == 'RR' :
        timeQuntuam = int(entry_rr.get()) # timeQuntuam
    # default setting
    canvas_readyqueue.delete("all") # clean canvas
    canvas_ganttchart.delete("all") # clean canvas
    for t in table_resulttable.get_children() : # clean table
        table_resulttable.delete(t)
    iid_num = 1
    for p in plist: # table set
        # Process data reset
        p.reset()
        table_resulttable.insert('', 'end', text="      " + p.name,
            values=(p.at, p.bt, p.wt, p.tt, p.ntt), iid="p" + str(iid_num))
        iid_num += 1
    running_algorithm = algorithms.Algorithm(plist, countOfProcessor, timeQuntuam)
    # start
    main_event = threading.Thread(target=main)
    main_event.start()

# clicked delete button
def delete_event(event) :
    global plist
    selected_item = treeview.selection()[0]
    del_process = plist.pop(treeview.index(selected_item))
    del del_process
    for t in treeview.get_children() : 
        treeview.delete(t)
    i = 1
    for p in plist :
        p.process_id = i
        p.name = 'p' + str(i)
        p.color = p.color_list[i-1]
        treeview.insert('','end',text=plist[i-1].name,
            values=(plist[i-1].at,plist[i-1].bt),iid="p" + str(i))
        i += 1

# clicked randomset button
def randomset_event(event) :
    # delete
    global plist
    if len(plist) != 0 :
        for t in treeview.get_children() : 
            treeview.delete(t)
        for p in plist :
            del p
    # random set
    plist = []
    at_start = 0
    for i in range(1, 16):
        globals()['p{}'.format(i)] = process.Process(
            i, at_start, random.randrange(3, 10))
        plist.append(globals()['p{}'.format(i)])
        at_start += random.randrange(1, 3)
        treeview.insert('','end',text=plist[i-1].name,
        values=(plist[i-1].at,plist[i-1].bt),iid="p" + str(i))

# default setting
# font
label_font = tkinter.font.Font(family="맑은 고딕", size=10, weight='bold')
button_font = tkinter.font.Font(family="맑은 고딕", size=20, slant="italic", )  
table_font = ""

# algorithm List
algo_label=tkinter.Label(window) 
algo_label.config(text="Algorithm List",font=label_font)
AlgorithmList=["FCFS","RR","SPN","SRTN","HRRN","ours"]
values=[AlgorithmList[i] for i in range(0,6)]
combobox_algorithm = tkinter.ttk.Combobox(window,width="17",values=values)
combobox_algorithm.set("알고리즘 선택")

# RR timequantum
RRtime=tkinter.Label(window) #RRtime
RRtime.config(text="RR Time quantum",font=label_font)
seconds = tkinter.Label(window) #seconds
seconds.config(text="seconds(s)",font=label_font)
entry_rr=tkinter.Entry(window,width="20")

# Arrival time
arr_label=tkinter.Label(window) #Arrival time
arr_label.config(text="Arrival time",font=label_font)
entry_at=tkinter.Entry(window,width="20")

# Burst time
bt_label=tkinter.Label(window) #Burst time
bt_label.config(text="Burst time",font=label_font)
entry_bt=tkinter.Entry(window,width="20")

# Process Number
processnum_label=tkinter.Label(window) #Processor Number
processnum_label.config(text="Processor Number",font=label_font)
value2=[str(i) for i in range(1,5)]
combobox_processNumber = tkinter.ttk.Combobox(window,width="17",values=value2)
combobox_processNumber.set("프로세스 개수")

#Execution Speed
es_label=tkinter.Label(window) 
es_label.config(text="Execution Speed",font=label_font)
ms=tkinter.Label(window) #ms
ms.config(text="ms",font=label_font)
ent_es=tkinter.Entry(window,width="20")

# insert treeview
treeview_label=tkinter.Label(window) #treeview label
treeview_label.config(text="Time table",font=label_font)
treeview = tkinter.ttk.Treeview(window, columns=["one","two"])
treeview.column("#0",width="150")
treeview.heading("#0",text="Process Name",anchor="center")
treeview.column("#1",width="150")
treeview.heading("one",text="Arrival Time(AT)",anchor="center")
treeview.column("#2",width="150")
treeview.heading("two",text="Burst Time(BT)",anchor="center")

# Button set
add=tkinter.Button(window,text="ADD",font=button_font,overrelief="solid",width="9",height="1",bg="white",fg="blue")
delete=tkinter.Button(window,text="DELETE",font=button_font,overrelief="solid",width="9",height="1",bg="white",fg="blue")
start=tkinter.Button(window,text="START",font=button_font,overrelief="solid",width="30",height="2",bg="white",fg="blue")
randomset=tkinter.Button(window,text="TEST SET",font=button_font,overrelief="solid",width="9",height="1",bg="white",fg="blue")
# Button mapping
add.bind("<Button-1>",insert)
start.bind("<Button-1>",start_event)
randomset.bind("<Button-1>", randomset_event)
delete.bind("<Button-1>",delete_event)

# Ready queue (for realtime)
title_readyqueue = tkinter.Label(
    window, text="Ready Queue", width=12, height=4, font=label_font)
canvas_readyqueue = tkinter.Canvas(
        window, relief="solid", width=930, height=60, bd=3)

# Gantt Chart (for realtime)
title_ganttchart = tkinter.Label(
    window, text="Gantt Chart  |", width=12, height=4, font=label_font)
text_runtime = tkinter.StringVar()
text_runtime.set('  RUNTIME : 0 ms')
title_runtime = tkinter.Label(
    window, textvariable=text_runtime, width=20, height=4, anchor='w', font=label_font)
canvas_ganttchart = tkinter.Canvas(
    window, relief="solid", width=930, height=60, bd=3)

# Result Table
title_resulttable = tkinter.Label(
    window, text="Result Table", width=12, height=4, font=label_font)
table_resulttable = tkinter.ttk.Treeview(
    window, columns=["AT", "BT", "WT", "TT", "NTT"])
table_resulttable.column("#0", width='65', anchor=tkinter.CENTER)
table_resulttable.heading("#0", text="Process Name")
table_resulttable.column("AT", width='130', anchor='center')
table_resulttable.heading("AT", text="Arrival Time(AT)")
table_resulttable.column("BT", width='130', anchor='center')
table_resulttable.heading("BT", text="Burst Time(BT)")
table_resulttable.column("WT", width='130', anchor='center')
table_resulttable.heading("WT", text="Waiting Time(WT)")
table_resulttable.column("TT", width='130', anchor='center')
table_resulttable.heading("TT", text="Turnaround Time(TT)")
table_resulttable.column("NTT", width='130', anchor='center')
table_resulttable.heading("NTT", text="Normalized TT(NTT)")

def defaultGui():
    # insert algorithm List
    algo_label.place(x=20,y=40)
    combobox_algorithm.place(x=150,y=40)

    # insert RR timequantum
    RRtime.place(x=20,y=70)
    seconds.place(x=300,y=70)
    entry_rr.place(x=150,y=70)

    # insert Arrival time
    arr_label.place(x=20,y=100)
    entry_at.place(x=150,y=100)

    # insert Burst time
    bt_label.place(x=20,y=130)
    entry_bt.place(x=150,y=130)

    # insert Process Number
    processnum_label.place(x=20,y=240)
    combobox_processNumber.place(x=150,y=240)
    
    # insert Execution Speed
    es_label.place(x=20,y=270)
    ent_es.place(x=150,y=270)
    ms.place(x=300,y=270)

    # insert treeview
    treeview_label.place(x=20,y=385)
    treeview.place(x=20,y=410,height=350)

    # insert Button 
    add.place(x=20,y=165)
    start.place(x=20,y=300)
    delete.place(x=170,y=165)
    randomset.place(x=320,y=165)
    
    # Ready queue (for realtime)
    title_readyqueue.place(x=510, y=50)
    canvas_readyqueue.place(x=510, y=100, width=940)

    # Gantt Chart (for realtime)
    title_ganttchart.place(x=510, y=200)
    title_runtime.place(x=625, y=200)
    canvas_ganttchart.place(x=510, y=250, width=940, height=110)

    # Result Table
    title_resulttable.place(x=510, y=360)
    table_resulttable.place(x=510, y=410, width=940, height=350)


def show_ready_queue(*queue):
    canvas_readyqueue.delete("all")  
    count = 1
    for p in queue:
        if p == None:
            continue
        fill_color = p.color
        x1 = 5 + 60 * (count - 1)  # min = 5
        y1 = 5
        x2 = 5 + 60 * count  # max = 935
        y2 = 70
        rectangle = canvas_readyqueue.create_rectangle(
            x1, y1, x2, y2, fill=fill_color, width=2)
        text = canvas_readyqueue.create_text(
            x2-30, 35, text=p.name, font=label_font)
        count = count + 1
    canvas_readyqueue.place(x=510, y=100)

def show_gantt_chart(*timeLine):
    canvas_ganttchart.delete("all")
    for mp in timeLine:
        count = 1
        for p in mp:
            if p == None :
                count = count + 1
                continue
            fill_color = p.color
            x1 = 5 + 30 * (count - 1)  # min = 5
            y1 = 5 + timeLine.index(mp) * (100/len(timeLine))
            x2 = 5 + 30 * count  # max = 935
            y2 = 5 + (100/len(timeLine)) + timeLine.index(mp) * (100/len(timeLine))
            rectangle = canvas_ganttchart.create_rectangle(
                x1, y1, x2, y2, fill=fill_color, width=2)
            text = canvas_ganttchart.create_text(
                x2-15, y2-((100/len(timeLine))/2), text=p.name, font=label_font)
            count = count + 1
    canvas_ganttchart.place(x=510, y=250, width=940, height=110)

def main():
    global selected_algorithm
    defaultGui()
    thread1 = None
    thread2 = None
    i = 0
    while True:
        start_time = time.time()
        # insert ready_process
        if selected_algorithm == 'FCFS' :
            return_queue, return_timeLine, return_finished, isEnd = running_algorithm.fcfs(i)
        if selected_algorithm == 'RR' :
            return_queue, return_timeLine, return_finished, isEnd = running_algorithm.rr(i)
        if selected_algorithm == 'SPN' :
            return_queue, return_timeLine, return_finished, isEnd = running_algorithm.spn(i)
        if selected_algorithm == 'SRTN' :
            return_queue, return_timeLine, return_finished, isEnd = running_algorithm.srtn(i)
        if selected_algorithm == 'HRRN' :
            return_queue, return_timeLine, return_finished, isEnd = running_algorithm.hrrn(i)
        if selected_algorithm == 'ours' :
            return_queue, return_timeLine, return_finished, isEnd = running_algorithm.rr_test(i)
        i += 1
        text_runtime.set('RUNTIME : ' + str(execution_speed * i) + ' ms')
        if len(return_queue) != 0:
            thread1 = threading.Thread(
                target=show_ready_queue, args=(return_queue))
            thread1.start()
        else :
            canvas_readyqueue.delete("all") 
        if return_timeLine != None:
            thread2 = threading.Thread(
                target=show_gantt_chart, args=return_timeLine)
            thread2.start()
        for finish in return_finished :
            if finish != None:
                table_resulttable.item(finish.name.lower(), text="      " + finish.name, values=(
                    finish.at, finish.bt, finish.wt, finish.tt, finish.ntt))
        if thread1 != None:
            thread1.join()
        if thread2 != None:
            thread2.join()
        # accurate time
        if (execution_speed/1000) > (time.time() - start_time):
            time.sleep(execution_speed/1000 - (time.time() - start_time))
        if isEnd:
            break

defaultGui()
window.mainloop()

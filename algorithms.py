import process
import threading
import random


class Algorithm :
    # class var
    plist = []
    timeLine = []
    queue = []
    index = 0
    timeQ = 0 
    last_gantt_chart = None
    currentProcess = None
    currentProcessTime = 0 
    end_line = False

    
      
    def fcfs(self, t) :
        # reset
        plist = self.plist
        queue = self.queue
        timeLine = self.timeLine
        index = self.index
        currentProcess = self.currentProcess
        finishProcess = None

        # ready queue(queue)
        if index < len(plist) and plist[index].at == t:
            queue.append(plist[index])
            index += 1
        if currentProcess == None:
            if len(queue)!=0:
                currentProcess = queue.pop(0)
            #else :
        # gantt chart(timeLine)
        if currentProcess != None:
            if len(timeLine) > 31 : # Gantt Chart Max Length
                timeLine.pop(0)
            timeLine.append(currentProcess)
            currentProcess.decrease_rt()
            if currentProcess.rt==0:
                currentProcess.set_tt()
                currentProcess.set_ntt()
                finishProcess = currentProcess
                # 임시
                print(currentProcess.process_id, currentProcess.tt)
                currentProcess=None

        if(len(queue)!=0):
            for p in queue:
                p.wt+=1
        if(currentProcess == None and len(queue)==0 and index == len(plist)):
            self.end_line = True
        # apply
        self.index = index
        self.queue = queue
        self.timeLine = timeLine
        self.index = index 
        self.currentProcess = currentProcess
        self.finishProcess = finishProcess
        return (queue, timeLine, finishProcess, self.end_line)


    def rr(self, t) :
        # reset
        plist = self.plist
        queue = self.queue
        timeLine = self.timeLine
        index = self.index
        timeQ = self.timeQ
        currentProcess = self.currentProcess
        currentProcessTime = self.currentProcessTime
        finishProcess = None

        if currentProcess != None and currentProcessTime == timeQ:
            queue.append(currentProcess)
            currentProcess = None
            currentProcessTime = 0

        # ready queue(queue)
        if index < len(plist) and plist[index].at == t:
            queue.append(plist[index])
            index += 1
        
        # launch
        if currentProcess == None:
            if len(queue)!=0:
                currentProcess = queue.pop(0) 
            
        if currentProcess != None:
            if len(timeLine) > 31 : # Gantt Chart Max Length
                timeLine.pop(0) # 타임라인 꽉 차면 앞에꺼 삭제??
            timeLine.append(currentProcess)
            currentProcess.decrease_rt()
            currentProcessTime += 1
            if currentProcess.rt==0:
                currentProcess.set_tt()
                currentProcess.set_ntt()
                finishProcess = currentProcess
                # 임시
                print(currentProcess.process_id, currentProcess.tt)
                currentProcess=None
                currentProcessTime = 0

        if(len(queue)!=0):
            for p in queue:
                p.wt+=1
        if(currentProcess == None and len(queue)==0 and index == len(plist)):
            self.end_line = True
        # apply
        self.index = index
        self.queue = queue
        self.timeLine = timeLine
        self.index = index 
        self.currentProcess = currentProcess
        self.currentProcessTime = currentProcessTime
        self.finishProcess = finishProcess
        return (queue, timeLine, finishProcess, self.end_line)
        

    def spn(self, t) :
        # reset
        plist = self.plist
        queue = self.queue
        timeLine = self.timeLine
        index = self.index
        currentProcess = self.currentProcess
        finishProcess = None

        # ready queue(queue)
        if index < len(plist) and plist[index].at == t:
            queue.append(plist[index])
            index += 1
            # sort by bt
            queue = sorted(queue, key=lambda process : process.bt)

        if currentProcess == None:
            if len(queue)!=0:
                currentProcess = queue.pop(0)
            #else :
        # gantt chart(timeLine)
        if currentProcess != None:
            if len(timeLine) > 31 : # Gantt Chart Max Length
                timeLine.pop(0)
            timeLine.append(currentProcess)
            currentProcess.decrease_rt()
            if currentProcess.rt==0:
                currentProcess.set_tt()
                currentProcess.set_ntt()
                finishProcess = currentProcess
                # 임시
                print(currentProcess.process_id, currentProcess.tt)
                currentProcess=None

        if(len(queue)!=0):
            for p in queue:
                p.wt+=1
        if(currentProcess == None and len(queue)==0 and index == len(plist)):
            self.end_line = True
        # apply
        self.index = index
        self.queue = queue
        self.timeLine = timeLine
        self.index = index 
        self.currentProcess = currentProcess
        self.finishProcess = finishProcess
        return (queue, timeLine, finishProcess, self.end_line)


    def srtn(self, t) :
        # reset
        plist = self.plist
        queue = self.queue
        timeLine = self.timeLine
        index = self.index
        currentProcess = self.currentProcess
        finishProcess = None

        # 한 사이클 끝난 프로세스 아직 시간 남았으면 큐에 다시 집어넣기
        if (currentProcess != None):
            queue.append(currentProcess)
            currentProcess = None

        # ready queue(queue)
        if index < len(plist) and plist[index].at == t:
            queue.append(plist[index])
            index += 1

        # sort by rt
        queue = sorted(queue, key=lambda process : process.rt)

        if len(queue)!=0:
            currentProcess = queue.pop(0)

            #else :
        # gantt chart(timeLine)
        if currentProcess != None:
            if len(timeLine) > 31 : # Gantt Chart Max Length
                timeLine.pop(0)
            timeLine.append(currentProcess)
            currentProcess.decrease_rt()
            if currentProcess.rt==0:
                currentProcess.set_tt()
                currentProcess.set_ntt()
                finishProcess = currentProcess
                # 임시
                print(currentProcess.process_id, currentProcess.tt)
                currentProcess=None

        if(len(queue)!=0):
            for p in queue:
                p.wt += 1


        if(currentProcess == None and len(queue)==0 and index == len(plist)):
            self.end_line = True
        # apply
        self.index = index
        self.queue = queue
        self.timeLine = timeLine
        self.index = index
        self.currentProcess = currentProcess
        self.finishProcess = finishProcess
        return (queue, timeLine, finishProcess, self.end_line)


    def hrrn(self, t):
        # reset
        plist = self.plist
        queue = self.queue
        timeLine = self.timeLine
        index = self.index
        timeQ = self.timeQ
        currentProcess = self.currentProcess
        finishProcess = None


        # ready queue(queue)
        if index < len(plist) and plist[index].at == t:
            queue.append(plist[index])
            index += 1

        # sort by response ratio
        queue = sorted(queue, reverse=True, key=lambda process: process.getResponseR())

        # launch
        if currentProcess == None:
            if len(queue) != 0:
                currentProcess = queue.pop(0)

        if currentProcess != None:
            if len(timeLine) > 31:  # Gantt Chart Max Length
                timeLine.pop(0)  # 타임라인 꽉 차면 앞에꺼 삭제??
            timeLine.append(currentProcess)
            currentProcess.decrease_rt()
            if currentProcess.rt == 0:
                currentProcess.set_tt()
                currentProcess.set_ntt()
                finishProcess = currentProcess
                # 임시
                print(currentProcess.process_id, currentProcess.tt)
                currentProcess = None

        if (len(queue) != 0):
            for p in queue:
                p.wt += 1
        if (currentProcess == None and len(queue) == 0 and index == len(plist)):
            self.end_line = True
        # apply
        self.index = index
        self.queue = queue
        self.timeLine = timeLine
        self.index = index
        self.currentProcess = currentProcess
        self.finishProcess = finishProcess
        return (queue, timeLine, finishProcess, self.end_line)


    def __init__(self, plist, timeQ = None) :
        if timeQ != None:
            self.timeQ = timeQ
        self.plist = plist


    def resetIndex(self):
        self.index = 0
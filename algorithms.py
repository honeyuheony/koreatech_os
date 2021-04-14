import process

class Algorithm :
    # class var
    plist = [] # Process list
    queue = [] # Readyqueue data
    timeLine = [] # Ganttchart data
    index = 0 # Process check
    timeQ = 0 # Time quantum
    multiProcessor = [] # 프로세서 리스트로
    multiProcessorTime = [] # RR때 쓸 시간
    countOfProcessor = 0 # 프로세서 개수
    end_line = False # End

    
    def fcfs(self, t) :
        # reset
        plist = self.plist
        queue = self.queue
        timeLine = self.timeLine
        index = self.index
        finishProcess = [] # 리스트로 수정
        multiProcessor = self.multiProcessor
        countOfProcessor = self.countOfProcessor

        # ready queue(queue)
        while(index < len(plist) and plist[index].at == t) :
            queue.append(plist[index])
            index += 1

        while len(queue) != 0 and multiProcessor.count(None):
            multiProcessor[multiProcessor.index(None)] = queue.pop(0)

            #else :
        # gantt chart(timeLine)
        for i in range(countOfProcessor):
            if len(timeLine[i]) > 31 : # Gantt Chart Max Length
                timeLine[i].pop(0)
            if multiProcessor[i] == None:
                timeLine[i].append(None)
            if multiProcessor[i] != None:
                timeLine[i].append(multiProcessor[i]) 
                multiProcessor[i].decrease_rt()
                if multiProcessor[i].rt == 0:
                    multiProcessor[i].set_tt()
                    multiProcessor[i].set_ntt()
                    finishProcess.append(multiProcessor[i])
                    print(multiProcessor[i].name, multiProcessor[i].wt)
                    multiProcessor[i] = None
                        # 임시

        if(len(queue)!=0):
            for p in queue:
                p.wt+=1

        if (multiProcessor.count(None) == countOfProcessor and len(queue) == 0 and index == len(plist)):
            self.end_line = True
        # apply
        self.index = index
        self.queue = queue
        self.timeLine = timeLine
        self.index = index
        self.multiProcessor = multiProcessor
        return (queue, timeLine, finishProcess, self.end_line)


    def rr(self, t) :
        # reset
        plist = self.plist
        queue = self.queue
        timeLine = self.timeLine
        index = self.index
        timeQ = self.timeQ
        finishProcess = []
        multiProcessor = self.multiProcessor
        countOfProcessor = self.countOfProcessor
        multiProcessorTime = self.multiProcessorTime

        for i in range(countOfProcessor):
            if multiProcessor[i] != None and multiProcessorTime[i] == timeQ:
                queue.append(multiProcessor[i])
                multiProcessor[i] = None
                multiProcessorTime[i] = 0


        # ready queue(queue)
        while (index < len(plist) and plist[index].at == t):
            queue.append(plist[index])
            index += 1

        while len(queue) != 0 and multiProcessor.count(None):
            multiProcessor[multiProcessor.index(None)] = queue.pop(0)

        # launch
        for i in range(countOfProcessor):
            if len(timeLine[i]) > 30:  # Gantt Chart Max Length
                timeLine[i].pop(0)
            if multiProcessor[i] == None:
                timeLine[i].append(None)
            if multiProcessor[i] != None:
                timeLine[i].append(multiProcessor[i])  
                multiProcessor[i].decrease_rt()
                multiProcessorTime[i] += 1
                if multiProcessor[i].rt == 0:
                    multiProcessor[i].set_tt()
                    multiProcessor[i].set_ntt()
                    finishProcess.append(multiProcessor[i])
                    print(multiProcessor[i].name, multiProcessor[i].wt)
                    multiProcessor[i] = None
                    multiProcessorTime[i] = 0

        if(len(queue)!=0):
            for p in queue:
                p.wt+=1

        if (multiProcessor.count(None) == countOfProcessor and len(queue) == 0 and index == len(plist)):
            self.end_line = True
        # apply
        self.index = index
        self.queue = queue
        self.timeLine = timeLine
        self.index = index
        self.multiProcessor = multiProcessor
        self.multiProcessorTime = multiProcessorTime
        return (queue, timeLine, finishProcess, self.end_line)

    def rr_test(self, t) :
        # reset
        plist = self.plist
        queue = self.queue
        timeLine = self.timeLine
        index = self.index
        timeQ = self.timeQ
        finishProcess = []
        multiProcessor = self.multiProcessor
        countOfProcessor = self.countOfProcessor
        multiProcessorTime = self.multiProcessorTime

        total_bt = 0
        for p in queue :
            total_bt += p.bt
        if len(queue) == 0 :
            timeQ = 0
        else :
            timeQ = (total_bt / len(queue))

        for i in range(countOfProcessor):
            if multiProcessor[i] != None and multiProcessorTime[i] == timeQ:
                queue.append(multiProcessor[i])
                multiProcessor[i] = None
                multiProcessorTime[i] = 0


        # ready queue(queue)
        while (index < len(plist) and plist[index].at == t):
            queue.append(plist[index])
            index += 1

        while len(queue) != 0 and multiProcessor.count(None):
            multiProcessor[multiProcessor.index(None)] = queue.pop(0)

        # launch
        for i in range(countOfProcessor):
            if len(timeLine[i]) > 30:  # Gantt Chart Max Length
                timeLine[i].pop(0)
            if multiProcessor[i] == None:
                timeLine[i].append(None)
            if multiProcessor[i] != None:
                timeLine[i].append(multiProcessor[i])  
                multiProcessor[i].decrease_rt()
                multiProcessorTime[i] += 1
                if multiProcessor[i].rt == 0:
                    multiProcessor[i].set_tt()
                    multiProcessor[i].set_ntt()
                    finishProcess.append(multiProcessor[i])
                    print(multiProcessor[i].name, multiProcessor[i].wt)
                    multiProcessor[i] = None
                    multiProcessorTime[i] = 0

        if(len(queue)!=0):
            for p in queue:
                p.wt+=1

        if (multiProcessor.count(None) == countOfProcessor and len(queue) == 0 and index == len(plist)):
            self.end_line = True
        # apply
        self.index = index
        self.queue = queue
        self.timeLine = timeLine
        self.index = index
        self.multiProcessor = multiProcessor
        self.multiProcessorTime = multiProcessorTime
        return (queue, timeLine, finishProcess, self.end_line)
        

    def spn(self, t) :
        # reset
        plist = self.plist
        queue = self.queue
        timeLine = self.timeLine
        index = self.index
        finishProcess = []  # 리스트로 수정
        multiProcessor = self.multiProcessor
        countOfProcessor = self.countOfProcessor

        # ready queue(queue)
        while index < len(plist) and plist[index].at == t:
            queue.append(plist[index])
            index += 1
            # sort by bt
            queue = sorted(queue, key=lambda process : process.bt)

        while len(queue) != 0 and multiProcessor.count(None):
            multiProcessor[multiProcessor.index(None)] = queue.pop(0)


            #else :
        # gantt chart(timeLine)
        for i in range(countOfProcessor):
            if len(timeLine[i]) > 30:  # Gantt Chart Max Length
                timeLine[i].pop(0)
            if multiProcessor[i] == None:
                timeLine[i].append(None)
            if multiProcessor[i] != None:
                timeLine[i].append(multiProcessor[i])  
                multiProcessor[i].decrease_rt()
                if multiProcessor[i].rt == 0:
                    multiProcessor[i].set_tt()
                    multiProcessor[i].set_ntt()
                    finishProcess.append(multiProcessor[i])
                    print(multiProcessor[i].name, multiProcessor[i].wt)
                    multiProcessor[i] = None

        if(len(queue)!=0):
            for p in queue:
                p.wt+=1

        if (multiProcessor.count(None) == countOfProcessor and len(queue) == 0 and index == len(plist)):
            self.end_line = True
        # apply
        self.index = index
        self.queue = queue
        self.timeLine = timeLine
        self.index = index
        self.multiProcessor = multiProcessor
        return (queue, timeLine, finishProcess, self.end_line)


    def srtn(self, t) :
        # reset
        plist = self.plist
        queue = self.queue
        timeLine = self.timeLine
        index = self.index
        finishProcess = []  # 리스트로 수정
        multiProcessor = self.multiProcessor
        countOfProcessor = self.countOfProcessor

        # 한 사이클 끝난 프로세스 아직 시간 남았으면 큐에 다시 집어넣기
        for i in range(countOfProcessor):
            if (multiProcessor[i] != None):
                queue.append(multiProcessor[i])
                multiProcessor[i] = None

        # ready queue(queue)
        while index < len(plist) and plist[index].at == t:
            queue.append(plist[index])
            index += 1

        # sort by rt
        queue = sorted(queue, key=lambda process : process.rt)

        while len(queue) != 0 and multiProcessor.count(None):
            multiProcessor[multiProcessor.index(None)] = queue.pop(0)

            #else :
        # gantt chart(timeLine)
        for i in range(countOfProcessor):
            if len(timeLine[i]) > 30:  # Gantt Chart Max Length
                timeLine[i].pop(0)
            if multiProcessor[i] == None:
                timeLine[i].append(None)
            if multiProcessor[i] != None:
                timeLine[i].append(multiProcessor[i])  
                multiProcessor[i].decrease_rt()
                if multiProcessor[i].rt == 0:
                    multiProcessor[i].set_tt()
                    multiProcessor[i].set_ntt()
                    finishProcess.append(multiProcessor[i])
                    print(multiProcessor[i].name, multiProcessor[i].wt)
                    multiProcessor[i] = None


        if(len(queue)!=0):
            for p in queue:
                p.wt += 1

        if (multiProcessor.count(None) == countOfProcessor and len(queue) == 0 and index == len(plist)):
            self.end_line = True
        # apply
        self.index = index
        self.queue = queue
        self.timeLine = timeLine
        self.multiProcessor = multiProcessor
        return (queue, timeLine, finishProcess, self.end_line)

    
    def hrrn(self, t):
        # reset
        plist = self.plist
        queue = self.queue
        timeLine = self.timeLine
        index = self.index
        finishProcess = []  # 리스트로 수정
        multiProcessor = self.multiProcessor
        countOfProcessor = self.countOfProcessor


        # ready queue(queue)
        while index < len(plist) and plist[index].at == t:
            queue.append(plist[index])
            index += 1

        # sort by response ratio
        queue = sorted(queue, reverse=True, key=lambda process: process.getResponseR())

        # launch
        while len(queue) != 0 and multiProcessor.count(None):
            multiProcessor[multiProcessor.index(None)] = queue.pop(0)

        for i in range(countOfProcessor):
            if len(timeLine[i]) > 30:  # Gantt Chart Max Length
                timeLine[i].pop(0)
            if multiProcessor[i] == None:
                timeLine[i].append(None)
            if multiProcessor[i] != None:
                timeLine[i].append(multiProcessor[i])  
                multiProcessor[i].decrease_rt()
                if multiProcessor[i].rt == 0:
                    multiProcessor[i].set_tt()
                    multiProcessor[i].set_ntt()
                    finishProcess.append(multiProcessor[i])
                    print(multiProcessor[i].name, multiProcessor[i].wt)
                    multiProcessor[i] = None

        if (len(queue) != 0):
            for p in queue:
                p.wt += 1

        if (multiProcessor.count(None) == countOfProcessor and len(queue) == 0 and index == len(plist)):
            self.end_line = True
        # apply
        self.index = index
        self.queue = queue
        self.timeLine = timeLine
        self.index = index
        self.multiProcessor = multiProcessor
        return (queue, timeLine, finishProcess, self.end_line)


    def __init__(self, plist, countOfProcessor, timeQ = None ) :
        if timeQ != None:
            self.timeQ = timeQ
        self.plist = plist
        self.countOfProcessor = countOfProcessor
        for i in range(countOfProcessor):
            self.multiProcessor.append(None)
            self.multiProcessorTime.append(0)
            self.timeLine.append([])


    def resetIndex(self):
        self.index = 0
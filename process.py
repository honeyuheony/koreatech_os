# Process 입력
class Process :
    at, bt = 0, 0
    wt = 0
    tt = 0 # BT+WT
    ntt = 0 # TT/BT
    rt = 0 # remainTime
    name = ""
    process_id = 0
    color_list = ['red', 'blue', 'yellow', 'green', 'magenta', 'cyan', 'coral', 'gold', 'grey', 'steelBlue4', 'deep pink', 'khaki3', 'seaGreen1', 'LightBlue1', 'tan4']
    color = ""
    #fade_color = 'eee9e9'

    def increase_wt(self) :
        self.wt = self.wt + 1
    def decrease_rt(self) :
        self.rt = self.rt - 1
    def set_tt(self) :
        self.tt = self.bt + self.wt
    def set_ntt(self) :
        self.ntt = self.tt/self.bt

    def __init__(self, id, at, bt):
        self.process_id = id
        self.color = Process.color_list[self.process_id-1]
        self.name = "P" + str(self.process_id)
        self.at = at
        self.bt = bt
        self.rt = bt
    
    def reset(self):
        self.wt = 0
        self.tt = 0
        self.ntt = 0
        self.rt = self.bt

    def getResponseR(self):
        return (self.wt + self.bt) / self.bt
        
    def state(self):
        state = (self.name, self.at, self.bt, self.wt, self.tt, self.ntt)
        return state
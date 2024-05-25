class Decoder:
    beat = []
    lt = []

    # (pitch,tone)
    def __init__(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            self.lt = f.readlines()
        for i in range(len(self.lt)):
            self.lt[i] = self.lt[i].strip('\n')

        t = 0
        while t < len(self.lt):
            t = self.singleBeat(t)
        # print(self.beat)

    def singleBeat(self, t: int):
        bt = []
        while not self.lt[t] == '{':
            print("Decode Error, Panic Mode", t)
            t += 1
        t += 1
        nts = [[] for i in range(16)]
        for i in range(t, t + 16):
            notes = self.lt[i].strip("$").split("|")
            for note in notes:
                if len(note) != 0:
                    nts[i - t].append(list(map(int, note.split(","))))
        self.beat.append(nts)
        return t + 17

    def get_beat(self):
        ans = []
        for x in self.beat:
            for j in x:
                ans.append(j)
        return ans
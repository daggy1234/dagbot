import time


class bword:
    def __init__(self):
        self.bord = set()

    def loadbword(self):
        with open("dagbot/data/dirtywords.txt", "r") as file:
            l = file.readlines()
            for i in l:
                i = i.strip("\n")
                self.bord.add(i)

    async def setcheck(self, nset):
        f = nset.intersection(self.bord)
        if len(f) == 0:
            return (False, "nothing")
        else:
            return (True, f)

    async def constructwordset(self, sent):
        l = sent.split(" ")
        nset = set()
        for w in l:
            w = w.lower()
            nset.add(w)
        return nset

    async def itercheck(self, sent):
        sent = sent.lower()
        sent = sent.strip(" ")
        sent = sent.replace(" ", "")
        for word in self.bord:
            if word in sent:
                return (True, word)
            else:
                continue
        return (False, "nothing")

    async def bwordcheck(self, sent):
        start = time.perf_counter()
        s = await self.constructwordset(sent)
        r, f = await self.setcheck(s)
        if r:
            return (True, f"NSFW: {f}")
        else:
            rt, w = await self.itercheck(sent)
            if rt:
                return (True, f"NSFW word: {w}")
            else:
                return (False, "PASSED SFW")

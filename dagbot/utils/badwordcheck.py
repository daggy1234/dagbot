from typing import Set, Tuple, Union

class bword:
    def __init__(self):
        self.bord: Set[str] = set()

    def loadbword(self):
        with open("dagbot/data/dirtywords.txt", "r") as file:
            lines = file.readlines()
            for i in lines:
                i = i.strip("\n")
                self.bord.add(i)

    async def setcheck(self, nset: Set[str]) -> Tuple[bool, Union[str, Set[str]]]:
        f = nset.intersection(self.bord)
        if len(f) == 0:
            return (False, "nothing")
        else:
            return (True, f)

    async def constructwordset(self, sent: str) -> Set[str]:
        split = sent.split(" ")
        nset = set()
        for w in split:
            w = w.lower()
            nset.add(w)
        return nset

    async def itercheck(self, sent: str) -> Tuple[bool, str]:
        sent = sent.lower()
        sent = sent.strip(" ")
        sent = sent.replace(" ", "")
        for word in self.bord:
            if word in sent:
                return (True, word)
            else:
                continue
        return (False, "nothing")

    async def bwordcheck(self, sent: str) -> Tuple[bool, str]:
        s = await self.constructwordset(sent)
        r, f = await self.setcheck(s)
        if r:
            return (True, f"NSFW: {f}")
        rt, w = await self.itercheck(sent)
        if rt:
            return (True, f"NSFW word: {w}")
        else:
            return (False, "PASSED SFW")

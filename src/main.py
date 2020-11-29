from FG import FG
from TM import TM


if __name__ == '__main__':
  tm = TM()
  tm.read("../TM.txt")
  fg = FG()
  fg.from_TM(tm)
  fg.write("../FG.txt")
  fg.generates("#1*1=1$", tm)
  fg.generates("11", tm)
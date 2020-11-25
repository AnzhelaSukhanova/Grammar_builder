from FG import FG
from TM import TM


if __name__ == '__main__':
  tm = TM()
  tm.read("../TM.txt")
  fg = FG()
  fg.from_TM(tm)
  fg.write("../FG.txt")
  #word = input()
  #print(tm.compute('#' + word + '$'))

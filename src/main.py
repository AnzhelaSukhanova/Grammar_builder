from FG import FG
from TM import TM
from CSG import CSG


if __name__ == '__main__':
  tm = TM()
  tm.read("../TM.txt")
  fg = FG()
  fg.from_TM(tm)
  fg.write("../FG.txt")
  csg = CSG()
  csg.from_lba(tm)
  word = input()
  while word != ":q":
    print("\nFree grammar generation:")
    fg.generates('#' + word + '$', tm)
    print("\nContext-sensitive grammar generation:")
    csg.generates(word)
    print()
    word = input()

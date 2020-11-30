import time


class TM:
  def __init__(self):
    self.states = []
    self.in_sym = []
    self.tape_sym = []
    self.trans = dict()
    self.fin_states = []
    self.start = '0'
    self.blank = 'B'

  def read(self, filename):
    f = open(filename, 'r')
    self.start = f.readline().rstrip()
    self.blank = f.readline().rstrip()
    self.tape_sym = [self.blank]
    self.in_sym = f.readline().rstrip().split()
    self.fin_states = f.readline().rstrip().split()

    for line in f:
      q1, s1, q2, s2, way = line.rstrip().split()
      if q1 not in self.states:
        self.states.append(q1)
      if q2 not in self.states:
        self.states.append(q2)
      if s1 not in self.tape_sym:
        self.tape_sym.append(s1)
      if s2 not in self.tape_sym:
        self.tape_sym.append(s2)
      self.trans[(q1, s1)] = [q2, s2, way]

  def compute(self, word):
    if len(word) < 2:
      return False
    for sym in word:
      if sym not in self.in_sym:
        return False
    cur_state = self.start
    index = 0
    start_time = time.time()
    while cur_state not in self.fin_states:
      if time.time() - start_time > 5:
        return False
      sym = word[index]
      if (cur_state, sym) in self.trans:
        trans = self.trans[(cur_state, sym)]
        print(word[:index] + "|" + trans[1] + "|" + word[index + 1:])
        word = word[:index] + trans[1] + word[index + 1:]
        if trans[2] == 'r':
          index += 1
        elif trans[2] == 'l':
          index -= 1
          if index < 0:
            word = self.blank + word
            index = 0
        else:
          if trans[0] == cur_state and trans[1] == sym:
            return False
        cur_state = trans[0]
    return True

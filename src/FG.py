from pyformlang.cfg import Variable


class FG:
  def __init__(self):
    self.var = []
    self.term = []
    self.prod = dict()
    self.start = Variable('S')
    self.var_names = dict()

  def from_TM(self, TM):
    self.term = TM.in_sym + ['']
    self.var = TM.states + ['S', 'S1', 'S2', 'S3']
    for X in self.term:
      for Y in TM.tape_sym:
        self.var.append(Variable(f'[{X},{Y}]'))
    self.var = list(map(Variable, self.var))

    self.prod[(Variable('S'),)] = [
      Variable('S1'),
      TM.start,
      Variable('S2')
    ]
    self.prod[(Variable('S1'),)] = [Variable('S1'), Variable(f'[,{TM.blank}]')]
    self.prod[(Variable('S2'),)] = [Variable('S3')]
    self.prod[(Variable('S1'),)] = [Variable(f'[,{TM.blank}]'), Variable('S3')]
    self.prod[(Variable('S1'),)] = ['']
    self.prod[(Variable('S3'),)] = ['']
    self.var_names[Variable('S')] = 'S'
    self.var_names[Variable('S1')] = 'S1'
    self.var_names[Variable('S2')] = 'S2'
    self.var_names[Variable('S3')] = 'S3'
    self.var_names[Variable(f'[,{TM.blank}]')] = 'N'
    N_num = 1
    for term in self.term:
      self.prod[(Variable('S2'),)] = [Variable(f'[{term},{term}]'), Variable('S3')]
      self.var_names[Variable(f'[{term},{term}]')] = 'N' + str(N_num)
      N_num += 1

    for C in TM.tape_sym:
      for q in TM.states:
        if (q, C) in TM.trans:
          trans = TM.trans[(q, C)]
          if trans[2] == 'r':
            for a in self.term:
              self.prod[(Variable(q), Variable(f'[{a},{C}]'))] =\
                [Variable(f'[{a},{trans[1]}]'), Variable(trans[0])]
              self.var_names[Variable(f'[{a},{C}]')] = 'N' + str(N_num)
              self.var_names[Variable(f'[{a},{trans[1]}]')] = 'N' + str(N_num + 1)
              self.var_names[Variable(q)] = 'Q' + str(q)
              self.var_names[Variable(trans[0])] = 'Q' + str(trans[0])
              N_num += 2
          elif trans[2] == 'l':
            for a in self.term:
              for b in self.term:
                for E in TM.tape_sym:
                  self.prod[(Variable(f'[{b},{E}]'), Variable(q), Variable(f'[{a},{C}]'))] = \
                    [Variable(trans[0]), Variable(f'[{b},{E}]'), Variable(f'[{a},{trans[1]}]')]
                  self.var_names[Variable(f'[{a},{C}]')] = 'N' + str(N_num)
                  self.var_names[Variable(f'[{a},{trans[1]}]')] = 'N' + str(N_num + 1)
                  self.var_names[Variable(f'[{b},{E}]')] = 'N' + str(N_num + 2)
                  self.var_names[Variable(q)] = 'Q' + str(q)
                  self.var_names[Variable(trans[0])] = 'Q' + str(trans[0])
                  N_num += 3

      for q in TM.fin_states:
        for a in self.term:
          self.prod[(Variable(q),)] = ['']
          self.prod[(Variable(q), Variable(f'[{a},{C}]'))] = [Variable(q), Variable(a), Variable(q)]
          self.prod[(Variable(q), Variable(f'[{a},{C}]'))] = [Variable(q), Variable(a), Variable(q)]
          self.var_names[Variable(f'[{a},{C}]')] = 'N' + str(N_num)
          self.var_names[Variable(q)] = 'Q' + str(q)
          N_num += 1

  def write(self, filename):
    f = open("../FG.txt", 'w')
    f.close()
    f = open(filename, 'a')
    for head in self.prod:
      for elem in head:
        f.write(self.var_names[elem] + " ")
      f.write("->")
      for elem in self.prod[head]:
        if elem in self.term:
          f.write(" " + str(elem))
        else:
          f.write(" " + self.var_names[elem])
      f.write("\n")
    f.close()

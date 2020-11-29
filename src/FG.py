class FG:
  def __init__(self):
    self.var = []
    self.term = []
    self.prod = []
    self.start = ['S']
    self.var_names = dict()

  def from_TM(self, TM):
    self.term = TM.in_sym
    self.var = TM.states + ['S', 'S1', 'S2']
    for X in self.term + ['']:
      for Y in TM.tape_sym:
        self.var.append(f'[{X},{Y}]')

    self.prod.append((['S'], [tuple(TM.start), 'S1']))
    self.prod.append((['S1'], ['S2']))
    self.prod.append((['S2'], [f'[{""},{TM.blank}]', 'S2']))
    self.prod.append((['S2'], ['']))
    self.var_names[tuple(TM.start)] = 'Q' + str(TM.start)
    self.var_names['S'] = 'S'
    self.var_names['S1'] = 'S1'
    self.var_names['S2'] = 'S2'
    self.var_names[f'[{""},{TM.blank}]'] = 'N'
    N_num = 1
    for term in self.term + ['']:
      self.prod.append((['S1'], [f'[{term},{term}]', 'S1']))
      self.var_names[f'[{term},{term}]'] = 'N' + str(N_num)
      N_num += 1

    for C in TM.tape_sym:
      for q in TM.states:
        if (q, C) in TM.trans:
          trans = TM.trans[(q, C)]
          if trans[2] == 'r':
            for a in self.term + ['']:
              self.prod.append(([tuple(q), f'[{a},{C}]'], \
                                [f'[{a},{trans[1]}]', tuple(trans[0])]))
              self.var_names[f'[{a},{C}]'] = 'N' + str(N_num)
              self.var_names[f'[{a},{trans[1]}]'] = 'N' + str(N_num + 1)
              self.var_names[tuple(q)] = 'Q' + str(q)
              self.var_names[tuple(trans[0])] = 'Q' + str(trans[0])
              N_num += 2
          elif trans[2] == 'l':
            for a in self.term + ['']:
              for b in self.term + ['']:
                for E in TM.tape_sym:
                  self.prod.append(([f'[{b},{E}]', tuple(q), f'[{a},{C}]'], \
                                    [tuple(trans[0]), f'[{b},{E}]', f'[{a},{trans[1]}]']))
                  self.var_names[f'[{a},{C}]'] = 'N' + str(N_num)
                  self.var_names[f'[{a},{trans[1]}]'] = 'N' + str(N_num + 1)
                  self.var_names[f'[{b},{E}]'] = 'N' + str(N_num + 2)
                  self.var_names[tuple(q)] = 'Q' + str(q)
                  self.var_names[tuple(trans[0])] = 'Q' + str(trans[0])
                  N_num += 3

      for q in TM.fin_states:
        for a in self.term + ['']:
          self.prod.append(([tuple(q)], ''))
          self.prod.append(([tuple(q), f'[{a},{C}]'], [tuple(q), a, tuple(q)]))
          self.prod.append(([f'[{a},{C}]', tuple(q)], [tuple(q), a, tuple(q)]))
          self.var_names[f'[{a},{C}]'] = 'N' + str(N_num)
          self.var_names[tuple(q)] = 'Q' + str(q)
          N_num += 1

  def write(self, filename):
    f = open("../FG.txt", 'w')
    for prod in self.prod:
      for head in prod[0]:
        if head in self.term:
          f.write(f'{head} ')
        else:
          f.write(f'{self.var_names[head]} ')
      for body in prod[1]:
        if body in self.term + [""]:
          f.write(f' {body}')
        else:
          f.write(f' {self.var_names[body]}')
      f.write("\n")
    f.close()

  def generates(self, word, TM):
    if len(word) == 0 and "" not in self.term:
      return False
    cur_sent = self.prod[0][1]
    output = ["S"]
    self.add_sent(output, cur_sent)

    for sym in word:
      if sym not in self.term:
        return False
      i = self.prod_index(f'[{sym},{sym}]', 1)
      cur_sent = cur_sent[:len(cur_sent) - 1] + self.prod[i][1]
      self.add_sent(output, cur_sent)
    cur_sent = cur_sent[:len(cur_sent) - 1] + self.prod[1][1]
    self.add_sent(output, cur_sent)
    cur_sent = cur_sent[:len(cur_sent) - 1] + self.prod[2][1]
    self.add_sent(output, cur_sent)
    cur_sent = cur_sent[:len(cur_sent) - 1]
    self.add_sent(output, cur_sent)
    i = 0
    max_changed = 1
    while max_changed < len(word):
      j = self.prod_index(cur_sent[i:i + 2], 0)
      if j is None:
        i -= 1
        j = self.prod_index(cur_sent[i:i + 3], 0)
        if j is None:
          print("Implementation error")
        cur_sent[i:i + 3] = self.prod[j][1]
        self.add_sent(output, cur_sent)
        max_changed = i + 2
      else:
        cur_sent[i:i + 2] = self.prod[j][1]
        self.add_sent(output, cur_sent)
        i += 1
        max_changed = i

    if cur_sent[i] in list(map(tuple, TM.fin_states)):
      for k in range(i, len(cur_sent) - 1):
        j = self.prod_index(cur_sent[k:k + 2], 0)
        cur_sent[k:k + 2] = self.prod[j][1]
        self.add_sent(output, cur_sent)
      for k in reversed(range(i)):
        j = self.prod_index(cur_sent[k:k + 2], 0)
        cur_sent[k:k + 2] = self.prod[j][1]
        self.add_sent(output, cur_sent)
      for k in range(len(cur_sent)):
        if cur_sent[k] in list(map(tuple, TM.fin_states)):
          j = self.prod_index(cur_sent[k], 0)
          cur_sent[k] = self.prod[j][1]
          self.add_sent(output, cur_sent)
      if ''.join(cur_sent) == word:
        print("\n", ' '.join(output))
        return True
      else:
        print("\nThe word '" + word + "' is not generated by free grammar")
        return False
    else:
      print("\nThe word '" + word + "' is not generated by free grammar")
      return False

  def prod_index(self, part, type):
    i = 0
    while i != len(self.prod) \
            and part not in self.prod[i][type] \
            and part != self.prod[i][type]:
      i += 1
    if i == len(self.prod):
      return None
    else:
      return i

  def add_sent(self, output, sent):
    output.append("->")
    for elem in sent:
      if elem != "":
        if elem in self.var_names:
          output.append(self.var_names[elem])
        else:
          output.append(elem)

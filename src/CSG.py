from TM import TM


class CSG:
  def __init__(self):
    self.var = []
    self.term = []
    self.prod = []
    self.lba_start = 0
    self.start = 'S'
    self.var_names = dict()

  def from_lba(self, lba: TM):
    self.var.append('S')
    self.var.append('S1')
    self.var_names['S'] = 'S'
    self.var_names['S1'] = 'S1'
    self.term = lba.in_sym
    self.lba_start = lba.start

    for a in set(lba.in_sym) - {'#', '$'}:
      # (1)
      self.prod.append(([self.start], [f'[{tuple(lba.start)},#,{a},{a},$]']))
      # (4.1), (4.2), (4.3)
      self.prod.append(([self.start], [f'[{tuple(lba.start)},#,{a},{a}]', 'S1']))
      self.prod.append((['S1'], [f'[{a},{a}]', 'S1']))
      self.prod.append((['S1'], [f'[{a},{a},$]']))

    for a in set(lba.in_sym) - {'#', '$'}:
      for x in set(lba.tape_sym) - {'#', '$'}:
        q = lba.fin_states[0]  # there is only one final state
        # (3.1), (3.2), (3.2)
        self.prod.append(([f'[{tuple(q)},#,{x},{a},$]'], [a]))
        self.prod.append(([f'[#,{tuple(q)},{x},{a},$]'], [a]))
        self.prod.append(([f'[#,{x},{a},{tuple(q)},$]'], [a]))

        # (8.1), (8.2), (8.3)
        self.prod.append(([f'[{tuple(q)},#,{x},{a}]'], [a]))
        self.prod.append(([f'[#,{tuple(q)},{x},{a}]'], [a]))
        self.prod.append(([f'[#,{x},{a},{tuple(q)}]'], [a]))

        # (8.4), (8.5)
        self.prod.append(([f'[{tuple(q)},{x},{a},$]'], [a]))
        self.prod.append(([f'[{x},{a},{tuple(q)},$]'], [a]))

        for b in set(lba.in_sym) - {'#', '$'}:
          # (9.1), (9.2)
          self.prod.append(([a, f'[{x},{b}]'], [a, b]))
          self.prod.append(([a, f'[{x},{b},$]'], [a, b]))

          # (9.3), (9.4)
          self.prod.append(([f'[{x},{a}]', b], [a, b]))
          self.prod.append(([f'[#,{x},{a}]', b], [a, b]))

          for y in set(lba.tape_sym) - {'#', '$'}:
            for p in lba.states:
              for z in set(lba.tape_sym) - {'#', '$'}:
                for q in set(lba.states) - set(lba.fin_states):
                  # (2.1), (5.1)
                  if (q, '#') in lba.trans and lba.trans[(q, '#')] == [p, '#', 'r']:
                    self.prod.append(([f'[{tuple(q)},#,{x},{a},$]'], [f'[#,{tuple(p)},{x},{a},$]']))
                    self.prod.append(([f'[{tuple(q)},#,{x},{a}]'], [f'[#,{tuple(p)},{x},{a}]']))
                  # (2.2), (5.2), (6.2), (6.4), (7.3)
                  if (q, x) in lba.trans and lba.trans[(q, x)] == [p, y, 'l']:
                    self.prod.append(([f'[#,{tuple(q)},{x},{a},$]'], [f'[{tuple(p)},#,{y},{a},$]']))
                    self.prod.append(([f'[#,{tuple(q)},{x},{a}]'], [f'[{tuple(p)},#,{y},{a}]']))
                    self.prod.append(([f'[{z},{b}]', f'[{tuple(q)},{x},{a}]'], [
                      f'[{tuple(p)},{z},{b}]',
                      f'[{y},{a}]'
                    ]))
                    self.prod.append(([f'[#,{z},{b}]', f'[{tuple(q)},{x},{a}]'], [
                      f'[#,{tuple(p)},{z},{b}]',
                      f'[{y},{a}]'
                    ]))
                    self.prod.append(([f'[{z},{b}]', f'[{tuple(q)},{x},{a},$]'], [
                      f'[{tuple(p)},{z},{b}]',
                      f'[{y},{a},$]'
                    ]))
                  # (2.3), (5.3), (6.1), (6.3), (7.1)
                  if (q, x) in lba.trans and lba.trans[(q, x)] == [p, y, 'r']:
                    self.prod.append(([f'[#,{tuple(q)},{x},{a},$]'], [f'[#,{y},{a},{tuple(p)},$]']))
                    self.prod.append(([f'[#,{tuple(q)},{x},{a}]', f'[{z},{b}]'], [
                      f'[#,{y},{a}]',
                      f'[{tuple(p)},{z},{b}]'
                    ]))
                    self.prod.append(([f'[{tuple(q)},{x},{a}]', f'[{z},{b}]'], [
                      f'[{y},{a}]',
                      f'[{tuple(p)},{z},{b}]'
                    ]))
                    self.prod.append(([f'[{tuple(q)},{x},{a}]', f'[{z},{b},$]'], [
                      f'[{y},{a}]',
                      f'[{tuple(p)},{z},{b},$]'
                    ]))
                    self.prod.append(([f'[{tuple(q)},{x},{a},$]'], [f'[{y},{a},{tuple(p)},$]']))
                  # (2.4), (7.2)
                  if (q, '$') in lba.trans and lba.trans[(q, '$')] == [p, '$', 'l']:
                    self.prod.append(([f'[#,{x},{a},{tuple(q)},$]'], [f'[#,{tuple(p)},{x},{a},$]']))
                    self.prod.append(([f'[{x},{a},{tuple(q)},$]'], [f'[{tuple(p)},{x},{a},$]']))
                  # 7.2 for 'n'
                  if (q, '$') in lba.trans and lba.trans[(q, '$')] == [p, '$', 'n']:
                    self.prod.append(([f'[{x},{a},{tuple(q)},$]'], [f'[{tuple(p)},{x},{a},$]']))
    for prod in self.prod:
      for h in prod[0]:
        if h not in self.term and h not in self.var:
          self.var.append(h)
          n = len(self.var)
          self.var_names[h] = 'S' + str(n)
      for b in prod[1]:
        if b not in self.term and b not in self.var:
          self.var.append(b)
          n = len(self.var)
          self.var_names[b] = 'S' + str(n)

  def generates(self, word):
    if len(word) < 2:
      return False

    if word[0] not in self.term:
      return False
    output = [self.start]
    # 4.1
    cur_sent = self.prod_by_part(f'[{tuple(self.lba_start)},#,{word[0]},{word[0]}]')
    if not cur_sent:
      print("\nError in modeling start configuration")
      print(cur_sent, 0)
      return False

    self.add_sent(output, cur_sent)
    for c in word[1:-1]:
      if c not in self.term:
        return False
      # 4.2
      body = [f'[{c},{c}]', 'S1']
      if self.in_prod(body):
        cur_sent = cur_sent[:-1] + body
        self.add_sent(output, cur_sent)
      else:
        print("\nError in modeling start configuration")
        print(cur_sent, 'center')
        return False

    if word[-1] not in self.term:
      return False

    if self.in_prod([f'[{word[-1]},{word[-1]},$]']):
      # 4.3
      cur_sent = cur_sent[:-1] + [f'[{word[-1]},{word[-1]},$]']
      self.add_sent(output, cur_sent)
    else:
      print("\nError in modeling start configuration")
      print(cur_sent, -1)
      return False
    changes = True
    i = 0
    while changes:
      changes = False
      i = 0
      while i < len(cur_sent) - 1:
        if self.prod_by_head([cur_sent[i]]):
          cur_sent = cur_sent[:i] + self.prod_by_head([cur_sent[i]]) + cur_sent[i + 1:]
          self.add_sent(output, cur_sent)
          changes = True
        else:
          i += 1
      if self.prod_by_head([cur_sent[-1]]):
        cur_sent = cur_sent[:-1] + self.prod_by_head([cur_sent[-1]])
        self.add_sent(output, cur_sent)
        changes = True
      i = 0
      while i < (len(cur_sent) - 2):
        if self.prod_by_head([cur_sent[i], cur_sent[i + 1]]):
          cur_sent = cur_sent[:i] + self.prod_by_head([cur_sent[i], cur_sent[i + 1]]) + cur_sent[i + 2:]
          self.add_sent(output, cur_sent)
          changes = True
        else:
          i += 1
      if self.prod_by_head([cur_sent[-2], cur_sent[-1]]):
        cur_sent = cur_sent[:-2] + self.prod_by_head([cur_sent[-2], cur_sent[-1]])
        self.add_sent(output, cur_sent)
        changes = True

    res = ''
    for t in cur_sent:
      res += t

    if res != word:
      print('\nThe word is not generated by context-sensitive grammar')
      return False
    print("\n", ' '.join(output))
    return True

  def add_sent(self, output, sent):
    output.append("->")
    for elem in sent:
      if elem in self.var_names:
        output.append(self.var_names[elem])
      else:
        output.append(elem)

  def prod_by_head(self, head):
    for p in self.prod:
      if p[0] == head:
        return p[1]
    return []

  def prod_by_part(self, body):
    for p in self.prod:
      if body in p[1] or body == p[1]:
        return p[1]
    return []

  def in_prod(self, body):
    for p in self.prod:
      if body == p[1]:
        return True
    return False

  def print_to_file(self, filename):
    f = open(filename, 'w')
    for prod in self.prod:
      for h in prod[0]:
        if h in self.term:
          f.write(f'{h} ')
        else:
          f.write(f'{self.var_names[h]} ')
      f.write("->")
      for b in prod[1]:
        if b in self.term:
          f.write(f' {b}')
        else:
          f.write(f' {self.var_names[b]}')
      f.write("\n")
    f.close()

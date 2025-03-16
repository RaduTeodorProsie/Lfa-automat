from logging import raiseExceptions

class AFD:
    def __init__(self, Q, E, d, q0, finals):
        self.Q = Q
        self.sig = E
        self.trans = d
        self.start = q0
        self.finals = finals

        for transition in d.items() :
            print(transition)
            self.check_transition(transition)
        for stare in finals:
            self.check_state(stare)
        if q0 != None:
            self.check_state(q0)

    def check_state(self, state):
        if state not in self.Q:
            raise Exception("Stare invalida")

    def set_start_state(self, state):
        self.check_state(state)
        if self.start != None:
            raise Exception("Ai mai multe stari initiale")
        self.start = state

    def set_end_state(self, state):
        self.check_state(state)
        self.finals.add(state)

    def check_transition(self, transition):
        self.check_state(transition[0][0])
        if transition[0][1] not in self.sig:
            raise Exception("Simbolul nu e in alfabet")
        self.check_state(transition[1])

    def add_state(self, state):
        self.Q.add(state)

    def add_sym(self, symbol):
        self.sig.add(symbol)

    def add_transition(self, transition):
        self.check_transition(transition)
        if transition[0] in self.trans:
            raise Exception("Automatul nu e determinist")
        self.trans[transition[0]] = transition[1]

    def accepta(self, word):
        for c in word:
            if c not in self.sig:
                return "Cuvant invalid"
        nod = self.start
        for c in word:
            if (nod, c) not in self.trans.keys():
                return "Cuvantul nu e acceptat"
            nod = self.trans[(nod, c)]

        if nod in self.finals:
            return "Cuvantul e acceptat"
        return "Cuvantul nu e acceptat"

with open("config.txt", "r") as file:
    sections = dict(); section_name = None
    automat = AFD(set(), set(), dict(), None, set())
    for line in file:
        line = line.strip()
        if line == "" or line[0] == '#' :
            continue
        if line == 'End' :
            section_name = None
        else:
            if section_name != None:
                sections[section_name].append(line)
            else :
                section_name = line
                sections[line] = []
    for litera in sections["Sigma:"]:
        automat.add_sym(litera)
    for line in sections["States:"]:
        line = line.split(',')
        automat.add_state(line[0])
        if 'F' in line:
            automat.set_end_state(line[0])
        if 'S' in line:
            automat.set_start_state(line[0])

    for line in sections["Transitions:"]:
        a, l, b = line.split(',')
        automat.add_transition(((a, l), b))

    print(automat.accepta("abcd"))

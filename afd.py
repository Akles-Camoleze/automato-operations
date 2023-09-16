def load(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        automaton = AFD(lines[0].strip()[1:])

        for state, line in enumerate(lines[1:], start=1):
            line = line.strip()
            automaton.new_state(state)
            if line.startswith(">"):
                automaton.set_initial_state(state)
            elif line.startswith("*"):
                automaton.set_initial_state(state)
                automaton.set_final_state(state)
            elif line.startswith("."):
                automaton.set_final_state(state)

            for i, symbol in enumerate(automaton.alphabet):
                end_state = int(line[i + 1])
                automaton.new_state(end_state)
                automaton.new_transition(state, end_state, symbol)

        print(f"'{filename}' carregado com sucesso.")
        return automaton

    except Exception as e:
        print(f"Erro ao carregar o autômato: {str(e)}")


class AFD:

    def __init__(self, alphabet) -> None:
        self.states = set()
        self.finalStates = set()
        self.initialState = None
        self.transitions = dict()
        self.alphabet = alphabet
        self.__error = False
        self.__currState = None

    def __str__(self):
        states_str = f"Estados: {', '.join(map(str, self.states))}\n"
        initial_str = f"Estado Inicial: {self.initialState}\n"
        final_str = f"Estados Finais: {', '.join(map(str, self.finalStates))}\n"
        transitions_str = "Transições:\n"
        for (start_id, symbol), end_id in self.transitions.items():
            transitions_str += f"{start_id} --({symbol})--> {end_id}\n"
        return states_str + initial_str + final_str + transitions_str

    def init(self) -> None:
        self.__error = False
        self.__currState = self.initialState

    def state_exists(self, id) -> bool:
        return id in self.states

    def state_is_final(self, id) -> bool:
        return id in self.finalStates

    def new_state(self, id, initial=False, final=False) -> bool:
        id = int(id)
        if self.state_exists(id):
            return False
        self.states.add(id)
        if initial:
            self.initialState = id
        if final:
            self.finalStates.add(id)
        return True

    def set_initial_state(self, id) -> bool:
        if not self.state_exists(id):
            return False
        self.initialState = id
        return True

    def set_final_state(self, id) -> bool:
        if not self.state_exists(id) or self.state_is_final(id):
            return False
        self.finalStates.add(id)
        return True

    def remove_final_state(self, id) -> bool:
        if not self.state_exists(id) or not self.state_is_final(id):
            return False
        self.finalStates.remove(id)
        return True

    def transition_exists(self, start_id, symbol):
        return (start_id, symbol) in self.transitions

    def new_transition(self, start_id, end_id, symbol):
        start_id, end_id, symbol = int(start_id), int(end_id), str(symbol)
        if not self.state_exists(start_id) or not self.state_exists(end_id):
            return False
        if len(symbol) != 1 or symbol not in self.alphabet:
            return False
        self.transitions[(start_id, symbol)] = end_id
        return True

    def remove_transition(self, start_id, symbol):
        if not self.transition_exists(start_id, symbol):
            return False
        self.transitions.pop((start_id, symbol))
        return True

    def start(self, word):
        for symbol in word:
            if symbol not in self.alphabet:
                self.__error = True
                break
            if not self.transition_exists(self.__currState, symbol):
                self.__error = True
                break
            self.__currState = self.transitions[(self.__currState, symbol)]
        return self.__currState

    def error(self):
        return self.__error

    def curr_state(self):
        return self.__currState

    def save(self, filename='afd.txt'):
        try:
            with open(filename, 'w') as file:
                alphabet_line = "#" + "".join(self.alphabet) + "\n"
                file.write(alphabet_line)

                for state in self.states:
                    if state == self.initialState and self.state_is_final(state):
                        state_type = "*"
                    elif state == self.initialState:
                        state_type = ">"
                    elif self.state_is_final(state):
                        state_type = "."
                    else:
                        state_type = "#"

                    state_line = f"{state_type}"
                    for symbol in self.alphabet:
                        transition = self.transitions.get((state, symbol), "")
                        state_line += str(transition)
                    state_line += "\n"

                    file.write(state_line)

            print(f"Autômato salvo em '{filename}' com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar o autômato: {str(e)}")

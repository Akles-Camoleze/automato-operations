import afd
from afd import AFD

if __name__ == '__main__':
    automaton = afd.load('afd.txt')
    # automaton = AFD('ab')
    # for i in range(1, 5):
    #     automaton.new_state(i)
    # automaton.set_initial_state(1)
    automaton.set_final_state(1)
    automaton.remove_final_state(4)
    #
    # automaton.new_transition(1, 2, 'a')
    # automaton.new_transition(2, 1, 'a')
    # automaton.new_transition(3, 4, 'a')
    # automaton.new_transition(4, 3, 'a')
    # automaton.new_transition(1, 3, 'b')
    # automaton.new_transition(3, 1, 'b')
    # automaton.new_transition(2, 4, 'b')
    # automaton.new_transition(4, 2, 'b')
    # automaton.save()
    print(automaton)

    word = ''
    automaton.init()
    state = automaton.start(word)

    if automaton.state_is_final(state) and not automaton.error():
        print(f'Aceita {word}')
    else:
        print(f'Rejeita {word}')


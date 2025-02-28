class DFA:
    def init(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def is_accepting(self, state):
        return state in self.accept_states

    def process_string(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol '(symbol)' is not in the alphabet")
            current_state = self.transitions.get((current_state, symbol))
            if current_state is None:
                raise ValueError(f"No transition deined for state '{current_state}'")
        return self.is_accepting(current_state)

states = {'q0', 'q1', 'q2'}
alphabet = {'1', '0'}

transitions = {
        ('q0', '1') : 'q1',
        ('q0', '0') : 'q0',
        ('q1', '1') : 'q2',
        ('q1', '0'): 'q2',
        ('q2' , '1') : 'q2',
        ('q2', '1') : 'q2'
}

start_state = 'q0'
accept_state = {'q2'}

dfa = DFA(states, alphabet, transitions, start_state, accept_states)

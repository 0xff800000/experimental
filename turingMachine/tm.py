class Tape(object):

    blank_symbol = " "

    def __init__(self,
                 tape_string = ""):
        self.__tape = dict((enumerate(tape_string)))
        # last line is equivalent to the following three lines:
        #self.__tape = {}
        #for i in range(len(tape_string)):
        #    self.__tape[i] = input[i]

    def __str__(self):
        s = ""
        min_used_index = min(self.__tape.keys())
        max_used_index = max(self.__tape.keys())
        for i in range(min_used_index, max_used_index):
            s += self.__tape[i]
        return s

    def __getitem__(self,index):
        if index in self.__tape:
            return self.__tape[index]
        else:
            return Tape.blank_symbol

    def __setitem__(self, pos, char):
        self.__tape[pos] = char


class TuringMachine(object):

    def __init__(self,
                 tape = "",
                 blank_symbol = " ",
                 initial_state = "",
                 final_states = None,
                 transition_function = None):
        self.__tape = Tape(tape)
        self.__head_position = 0
        self.__blank_symbol = blank_symbol
        self.__current_state = initial_state
        if transition_function == None:
            self.__transition_function = {}
        else:
            self.__transition_function = transition_function
        if final_states == None:
            self.__final_states = set()
        else:
            self.__final_states = set(final_states)

    def get_tape(self):
        return str(self.__tape)

    def step(self):
        char_under_head = self.__tape[self.__head_position]
        x = (self.__current_state, char_under_head)
        if x in self.__transition_function:
            y = self.__transition_function[x]
            self.__tape[self.__head_position] = y[1]
            if y[2] == "R":
                self.__head_position += 1
            elif y[2] == "L":
                self.__head_position -= 1
            self.__current_state = y[0]
        else:
            raise Exception("Turing Machine crashed : No transition found")

    def final(self):
        if self.__current_state in self.__final_states:
            print('The machine stopped in the {} state'.format(self.__current_state))
            return True
        else:
            return False

    def print_state(self):
        print(self.get_tape())
        char_under_head = self.__tape[self.__head_position]
        x = (self.__current_state, char_under_head)
        print(' '*(self.__head_position)+'^'+' {}'.format(x[0]))

## Invert tape
# tape_str = "010011 "
# initial_state = "init"
# transition_function = {
#     ("init","0"):("init", "1", "R"),
#     ("init","1"):("init", "0", "R"),
#     ("init"," "):("final"," ", "N"),
# }
# final_states = {"final"}

# Match 2 strings separated by #
tape_str = "010011#010011 "
initial_state = "match"
transition_function = {
    ("match","0"):("matchz_next", ".", "R"),
    ("matchz_next","1"):("matchz_next", "1", "R"),
    ("matchz_next","0"):("matchz_next", "0", "R"),
    ("matchz_next","#"):("matchz", "#", "R"),
    ("matchz","#"):("matchz", "#", "R"),
    ("matchz","."):("matchz", ".", "R"),
    ("matchz","1"):("Reject", "0", "N"),
    ("matchz","0"):("return_#start", ".", "L"),

    ("match","1"):("matcho_next", ".", "R"),
    ("matcho_next","1"):("matcho_next", "1", "R"),
    ("matcho_next","0"):("matcho_next", "0", "R"),
    ("matcho_next","#"):("matcho", "#", "R"),
    ("matcho","#"):("matcho", "#", "R"),
    ("matcho","."):("matcho", ".", "R"),
    ("matcho","0"):("Reject", "0", "N"),
    ("matcho","1"):("return_#start", ".", "L"),

    ("return_#start","0"):("return_#start", "0", "L"),
    ("return_#start","1"):("return_#start", "1", "L"),
    ("return_#start","#"):("return_start", "#", "L"),
    ("return_#start","."):("return_#start", ".", "L"),

    ("return_start","0"):("return_start", "0", "L"),
    ("return_start","1"):("return_start", "1", "L"),
    ("return_start","#"):("return_start", "#", "L"),
    ("return_start","."):("match", ".", "R"),

    ("match","#"):("Accept", "#", "N"),
}
final_states = {"Accept",'Reject'}


t = TuringMachine(tape_str,
                  initial_state = initial_state,
                  final_states = final_states,
                  transition_function=transition_function)

print("Input on Tape:\n" + t.get_tape())

while not t.final():
    t.print_state()
    t.step()


print("Result of the Turing machine calculation:")
print(t.get_tape())

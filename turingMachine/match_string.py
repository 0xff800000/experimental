from turingmachine import TuringMachine

# Match 2 strings separated by #
tape_str = "0100111#0100111 "
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

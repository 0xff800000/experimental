from turingmachine import TuringMachine

# Invert tape
tape_str = "010011 "
initial_state = "init"
transition_function = {
    ("init","0"):("init", "1", "R"),
    ("init","1"):("init", "0", "R"),
    ("init"," "):("final"," ", "N"),
}
final_states = {"final"}

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

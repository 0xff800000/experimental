from turingmachine import TuringMachine


## Add two numbers a + b, Note : LSB on the left side !
tape_str = "1110000#1110000#"+10*' '
initial_state = "start"
transition_function = {
    # Select first digit of a
    ("start","0"):("zero+", ".", "R"),
    ("start","1"):("one+", ".", "R"),
    ("start","."):("start", ".", "R"),
    ("start","#"):("Accept", "#", "N"),

    # Skip a
    ("zero+","1"):("zero+", "1", "R"),
    ("zero+","0"):("zero+", "0", "R"),
    ("zero+","#"):("zero+?", "#", "R"),

    ("one+","1"):("one+", "1", "R"),
    ("one+","0"):("one+", "0", "R"),
    ("one+","#"):("one+?", "#", "R"),

    # Select first digit of b
    ("zero+?","."):("zero+?", ".", "R"),
    ("one+?","."):("one+?", ".", "R"),

    ("zero+?","0"):("zero+zero", ".", "R"),
    ("zero+?","1"):("zero+one", ".", "R"),
    ("one+?","0"):("zero+one", ".", "R"),
    ("one+?","1"):("one+one", ".", "R"),

    # Skip b
    ("zero+zero","0"):("zero+zero", "0", "R"),
    ("zero+zero","1"):("zero+zero", "1", "R"),
    ("zero+zero","."):("zero+zero", ".", "R"),
    ("zero+zero","#"):("zero+zero=", "#", "R"),

    ("zero+one","0"):("zero+one", "0", "R"),
    ("zero+one","1"):("zero+one", "1", "R"),
    ("zero+one","."):("zero+one", ".", "R"),
    ("zero+one","#"):("zero+one=", "#", "R"),

    ("one+one","0"):("one+one", "0", "R"),
    ("one+one","1"):("one+one", "1", "R"),
    ("one+one","."):("one+one", ".", "R"),
    ("one+one","#"):("one+one=", "#", "R"),

    ("one+one+one","0"):("one+one+one", "0", "R"),
    ("one+one+one","1"):("one+one+one", "1", "R"),
    ("one+one+one","."):("one+one+one", ".", "R"),
    ("one+one+one","#"):("one+one+one=", "#", "R"),

    # Find digit of answer
    ("zero+zero=","0"):("zero+zero=", "0", "R"),
    ("zero+zero=","1"):("zero+zero=", "1", "R"),
    ("zero+zero="," "):("return_start", "0", "L"),

    ("zero+one=","0"):("zero+one=", "0", "R"),
    ("zero+one=","1"):("zero+one=", "1", "R"),
    ("zero+one="," "):("return_start", "1", "L"),

    ("one+one=","0"):("one+one=", "0", "R"),
    ("one+one=","1"):("one+one=", "1", "R"),
    ("one+one="," "):("return_start_c", "0", "L"),

    ("one+one+one=","0"):("one+one+one=", "0", "R"),
    ("one+one+one=","1"):("one+one+one=", "1", "R"),
    ("one+one+one="," "):("return_start_c", "1", "L"),

    # Return to start and carry
    ("return_start_c","0"):("return_start_c", "0", "L"),
    ("return_start_c","1"):("return_start_c", "1", "L"),
    ("return_start_c","#"):("return_start_c#", "#", "L"),
    ("return_start_c#","0"):("return_start_c#", "0", "L"),
    ("return_start_c#","0"):("return_start_c#", "0", "L"),
    ("return_start_c#","1"):("return_start_c#", "1", "L"),
    ("return_start_c#","."):("return_start_c#", ".", "L"),
    ("return_start_c#","#"):("return_start_c##", "#", "L"),
    ("return_start_c##","0"):("return_start_c##", "0", "L"),
    ("return_start_c##","1"):("return_start_c##", "1", "L"),
    ("return_start_c##","."):("carry+?", ".", "R"),

    # Carry + 0
    ("carry+?","0"):("carry+0", ".", "R"),
    ("carry+?","1"):("carry+1", ".", "R"),
    ("carry+1","0"):("carry+1", "0", "R"),
    ("carry+1","1"):("carry+1", "1", "R"),
    ("carry+1","#"):("carry+1+?", "#", "R"),
    ("carry+0","0"):("carry+0", "0", "R"),
    ("carry+0","1"):("carry+0", "1", "R"),
    ("carry+0","#"):("carry+0+?", "#", "R"),
    ("carry+0+?","."):("carry+0+?", ".", "R"),
    ("carry+1+?","."):("carry+1+?", ".", "R"),
    ("carry+1+?","0"):("zero+one", ".", "R"),
    ("carry+1+?","1"):("one+one+one", ".", "R"),
    ("carry+0+?","1"):("one+one", ".", "R"),
    ("carry+0+?","0"):("zero+one", ".", "R"),

    # Return to start
    ("return_start","0"):("return_start", "0", "L"),
    ("return_start","1"):("return_start", "1", "L"),
    ("return_start","#"):("return_start#", "#", "L"),

    ("return_start#","0"):("return_start#", "0", "L"),
    ("return_start#","1"):("return_start#", "1", "L"),
    ("return_start#","."):("return_start#", ".", "L"),
    ("return_start#","#"):("return_start##", "#", "L"),

    ("return_start##","0"):("return_start##", "0", "L"),
    ("return_start##","1"):("return_start##", "1", "L"),
    ("return_start##","."):("start", ".", "R"),

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

# Unit test
for a in range(-10,10):
    for b in range(-10,10):
        print('a(dec:{},bin:{}) + b(dec:{},bin:{})'.format(a,a,b,b))

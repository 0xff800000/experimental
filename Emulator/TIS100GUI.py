from tkinter import *
from tkinter.filedialog import askopenfilename

# Registers
registers={
'r1':0,
'r2':0,
'r3':0,
'r4':0,
'pc':0,
'acc':0,
'bak':0
}

program=[]

# Reads a the prog form a file
def readProg():
    file = askopenfilename()
    f = open(file,'r')
    for line in f:
        if '#' in line: continue
        line = line.lower()
        line = line.split()
        for i in range(len(line)):
            if line[i].isdigit():
                line[i]=int(line[i])
        program.append(line)

################## Instruction set ######################

def nop():
    registers['pc']+=1

def mov(src,dst):
    if src in registers:
        registers[dst]=registers[src]
    else:
        registers[dst]=src
    registers['pc']+=1

def add(src):
    if src in registers:
        registers['acc']+=registers[src]
    else:
        registers['acc']+=src
    registers['pc']+=1

def sub(src):
    if src in registers:
        registers['acc']-=registers[src]
    else:
        registers['acc']-=src
    registers['pc']+=1

def neg():
    registers['acc']= ~registers['acc']
    registers['pc']+=1

def sav():
    registers['bak']=registers['acc']
    registers['pc']+=1

def swp():
    tmp=registers['bak']
    registers['bak']=registers['acc']
    registers['acc']=tmp
    registers['pc']+=1

def jmp(dst):
    registers['pc']=dst-1

def jez(dst):
    if registers['acc'] == 0:
        registers['pc']=dst-1
    else:
        registers['pc']+=1

def jnz(dst):
    if registers['acc'] != 0:
        registers['pc']=dst-1
    else:
        registers['pc']+=1

def jgz(dst):
    if registers['acc'] > 0:
        registers['pc']=dst-1
    else:
        registers['pc']+=1

def jlz(dst):
    if registers['acc'] < 0:
        registers['pc']=dst-1
    else:
        registers['pc']+=1

instrTable={
    'nop':(nop,0),
    'mov':(mov,2),
    'add':(add,1),
    'sub':(sub,1),
    'neg':(neg,1),
    'sav':(sav,0),
    'swp':(swp,0),
    'jmp':(jmp,1),
    'jez':(jez,1),
    'jnz':(jnz,1),
    'jgz':(jgz,1),
    'jlz':(jlz,1)
    }
def step():
    # Intruction fetch
    func,var = instrTable[program[registers['pc']][0]]
    # Exec
    if var == 0:
        func()
    elif var == 1:
        func(program[registers['pc']][1])
    elif var == 2:
        func(program[registers['pc']][1],program[registers['pc']][2])
    #print(registers)

def showState():
    #pcvar.set(registers['pc'])
    #w.pack()
    i=0
    for reg in registers:
        labelsStr[i].set('{} : {}'.format(reg.upper(),registers[reg]))
        labels[i].pack()
        i+=1
    stepBut.pack()
    autoStepBut.pack()
    root.update()

# Buttons
autoStep=False

def cb_step():
    step()

def cb_autoStep():
    global autoStep
    autoStep = ~autoStep

# GUI
root = Tk()
pcvar= StringVar()
labels=[]
labelsStr=[]
stepBut = Button(root, text="Step", command=cb_step)
autoStepBut = Button(root, text="Run", command=cb_autoStep)
for reg in range(len(registers)):
    labelsStr.append(StringVar())
    labels.append(Label(root, textvariable=labelsStr[reg])) 
# Main
readProg()

while True:
    showState()
    if autoStep: step()
    

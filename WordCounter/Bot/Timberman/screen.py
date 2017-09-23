import pyautogui

isRight = False
branchColor = (126,100,76)

class coord():
	leftClick = (760,701)
	rightClick = (991,704)
	
	leftBranch = (766,595)
	rightBranch = (984,594)

def isBranch():
	if isRight==True:
		color=pyautogui.pixel(coord.rightBranch[0],coord.rightBranch[1])
	else:
		color=pyautogui.pixel(coord.leftBranch[0],coord.leftBranch[1])
	if color==branchColor:
		return True
	else:
		return False


x=coord.leftClick[0]
y=coord.leftClick[1]

while True:
        if isBranch():
                # Change side
                if isRight:
                        x=coord.leftClick[0]
                        y=coord.leftClick[1]
                else:
                        x=coord.rightClick[0]
                        y=coord.rightClick[1]
                isRight=not isRight
        else:
                # Click
                pyautogui.click(x,y)

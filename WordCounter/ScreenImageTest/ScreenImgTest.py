import pyautogui

coords=list(pyautogui.locateAllOnScreen('Iexplorer.png'),grayscale=True)

for i in range(len(coords)):
	x,y=pyautogui.center(coords[i])
	pyautogui.moveTo(x,y,1)
import pyautogui
import msvcrt

while True:
	if msvcrt.kbhit():
		if ord(msvcrt.getch())=='q':
			quit()
		pos=pyautogui.position()
		print('Position : {}'.format(pos))
		print('Pixel color : {}\n'.format(pyautogui.pixel(pos[0],pos[1])))
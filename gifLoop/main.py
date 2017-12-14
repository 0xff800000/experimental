from moviepy.editor import *
import math,random,sys

def time_symetrize(clip):
	return concatenate([clip,clip.fx(vfx.time_mirror)])

def random_loop(clip):
	time = random.random()*clip.duration
	front = clip.subclip(t_start=time,t_end=clip.duration)
	back = clip.subclip(t_start=0,t_end=time)
	return concatenate([front,back])

def loop(clip,time):
	front = clip.subclip(t_start=time,t_end=clip.duration)
	back = clip.subclip(t_start=0,t_end=time)
	return concatenate([front,back])

def sqare_matrix(c,n):
	c = c.fx( vfx.resize, width=c.w/n)
	line = [c for i in range(n)]
	square = [line for i in range(n)]
	return square

def sqare_matrix_loop_rand(c,n):
	c = c.fx( vfx.resize, width=c.w/n)
	square = []
	for j in range(n):
		line = [random_loop(c) for i in range(n)]
		square.append(line)
	return square

def sqare_matrix_loop_spread(c,n):
	c = c.fx( vfx.resize, width=c.w/n)
	square = []
	for j in range(n):
		line = []
		for i in range(n):
			time=c.duration*(1.0-(j*n+i)/(n*n))
			line.append(loop(c,time))
		square.append(line)
	return square

in_name = str(sys.argv[1])
out_name = in_name.split('.')[0]
clip = VideoFileClip(in_name,audio=False)
clip = clip.subclip(t_start=1,t_end=clip.duration-1)
# clip = concatenate([clip,clip.fx(vfx.time_mirror)])
# clip = clip.fx( vfx.speedx, 5)
# clip = clip.fx(vfx.supersample, 0,40)
print(clip.duration)
# final_clip = clips_array(sqare_matrix_loop_rand(clip,5))
final_clip = clips_array(sqare_matrix_loop_spread(clip,20))
clip = clip.fx( vfx.resize, width=360)
# clip.preview()
final_clip.write_gif(out_name+".gif",fps=5)

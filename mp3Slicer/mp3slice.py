import sys, os
from pydub import AudioSegment

# Extract the names of the music and the timings
# Format of flie : start time; song name
# Metadata : #tag,attrubute
def getInfo(path):
	f = open(path,'r')
	times = []
	names = []
	metadata = {}
	for line in f:
		line = line.replace('\n','')
		# Extract metadata
		if line[0] == '#':
			line = ''.join([x for x in line][1:])
			line = line.split(',')
			metadata[line[0]] = line[1]
			continue

		line = line.split(',')
		#print(line)

		# Convert to miliseconds
		time_str = line[0].split(':')
		t = 0
		if len(time_str) == 3: # (h:m:s)
			t = float(time_str[0]) * 60 * 60 * 1000
			t += float(time_str[1]) * 60 * 1000
			t += float(time_str[2]) * 1000
		elif len(time_str) == 2: # (m:s)
			t = float(time_str[0]) * 60 * 1000
			t += float(time_str[1]) * 1000
		else:
			print("Error : time format")
			exit(-1)
		times.append(t)
		names.append(line[1])
	return times,names,metadata

# Extract possible delimiters of the music based on the zeroes
def predictTime(music):
	f = music.frame_rate
	music = music.raw_data
	#print(music[0:10])
	zeroes_regions = []
	newRegion = True
	start = 0
	stop = 0
	i = 0
	for s in music:
		#print(s)
		if newRegion and s == 0:
			#print('Hit at %i' % i)
			start = i
			newRegion = False
		if not newRegion and s != 0:
			newRegion = True
			stop = i-1
			if stop-start>1000:
				zeroes_regions.append((start/f*1000,stop/f*1000))
		i+=1
		#print(zeroes_regions)
	return zeroes_regions


time = []
name = []
if len(sys.argv) != 3:
	print("Usage : " + sys.argv[0] + " timing_file mp3_file")
else:
	output_dir = 'out'
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	time, name, meta = getInfo(sys.argv[1])
	start_time = time

	print("Opening music file...")
	music_file = AudioSegment.from_mp3(sys.argv[2])

	# Check the time
	for t in time:
		if t > len(music_file):
			print("The timings does not correspond to the mp3 file")
			exit(-1)

	# Predict the time
	print('Predict the timings...')
	predicted_time = predictTime(music_file)
	final_time = []
	for t in time:
		distance = []
		found_in = False
		# If t is between one of the predicted state
		for pt in predicted_time:
			distance.append((abs(t-pt[0]),pt[0]))
			distance.append((abs(t-pt[1]),pt[1]))
			if t >= pt[0] and t <= pt[1]:
				final_time.append(pt[1])
				found_in = True
				break
		# If t is 2 seconds away from one predicted
		if not found_in:
			distance.sort()
			if(distance[0][0]<2000):
				final_time.append(distance[0][1])
				found_in = True
			else:
				final_time.append(t)
		if found_in:
			print('Time selected from predicted value.')

	print(time)
	print(final_time)
	print(predicted_time)
	stop_time = time[1:]
	stop_time.append(len(music_file))
	

	for start,stop,name in zip(start_time,stop_time,name):
		print("Converting %s..." % name)
		file_name = "out/%s.mp3" % name
		if os.path.exists(file_name):
			print("File %s already exists." % file_name)
			continue
		out = open(file_name, 'wb')
		song = music_file[start:stop]
		song.export(out, format='mp3', tags=meta)
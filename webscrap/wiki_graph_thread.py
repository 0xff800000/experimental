import urllib.request, random, datetime
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool

found = False

def get_links(path):
	global found
	global initial_link
	global explored_links
	if found:
		return
	print("Exploring : %s" % path)
	try:
		url = urllib.request.urlopen( "https://en.wikipedia.org" + path)
	except:
		print("Failed to explore : %s" % path)
		return []
	explored_links += 1
	page = BeautifulSoup( url ,"lxml")
	url.close()

	links = []
	for p in page.findAll("a"):
		if "class" not in p.attrs:
			if "href" in p.attrs:
				if "/wiki/" in p.attrs["href"] and p.attrs["href"] not in links and ":" not in p.attrs["href"] and "wikimediafoundation" not in p.attrs:
					links.append(p.attrs["href"])
	if target_link in links:
		found = True
	return (links, path)

def get_steps(start,stop,tree):
	path = [start]
	while start != stop:
		path.append(tree[start])
		start = tree[start]
	return path

# Random link
#initial_link = urllib.request.urlopen( "https://en.wikipedia.org" + "/wiki/Special:Random").geturl().split('.org')[1]
initial_link = "/wiki/Quaternion"
target_link = "/wiki/Adolf_Hitler"

current_link = initial_link
previous_link = initial_link
explored_links = 0
# link : coming from
tree = {}
print("Searching path from {} to {}.".format(initial_link,target_link))
start_time = datetime.datetime.now()

# Build frontier
current_frontier = get_links(initial_link)
frontier = []
layer = 1
tree[initial_link] = ''

for f in current_frontier[0]:
	tree[f] = current_frontier[1]
current_frontier = current_frontier[0]

pool = ThreadPool(processes=2)
while not found:
	if len(current_frontier) == 0:
		print("Path between {} and {} could not be found...".format(initial_link,target_link))
		exit(0)

	print('#'*10 + 'layer {}'.format(layer) + '#'*10)
	layer += 1
	discovered = pool.map(get_links, current_frontier)

	# Add to tree
	current_frontier = []
	for d in discovered:
		if d == None:
			continue
		if len(d) == 0:
			continue
		links = d[0]
		current_link = d[1]
		for l in links:
			if l not in tree:
				tree[l] = current_link
				if l not in current_frontier:
					current_frontier.append(l)
				if l == target_link:
					print("@"*100)
					break

pool.close()

stop_time = datetime.datetime.now()

print("********************")
print("Path found after exploring {} links.".format(explored_links))
print("Time of execution : %s" % str(stop_time-start_time))
print("Size of graph : {}".format(len(tree)))
steps = get_steps(target_link,initial_link,tree)
print("There is %i steps:" %len(steps))
for x in steps:
	print(x)

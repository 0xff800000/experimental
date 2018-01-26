import urllib.request, random, datetime
from bs4 import BeautifulSoup

def get_links(path):
	try:
		url = urllib.request.urlopen( "https://en.wikipedia.org" + path)
	except:
		print("Failed to explore : %s" % path)
		return []
	page = BeautifulSoup( url ,"lxml")
	url.close()

	links = []
	for p in page.findAll("a"):
		if "class" not in p.attrs:
			if "href" in p.attrs:
				if "/wiki/" in p.attrs["href"] and p.attrs["href"] not in links and ":" not in p.attrs["href"] and "wikimediafoundation" not in p.attrs:
					links.append(p.attrs["href"])

	return links

def get_steps(start,stop,tree):
	path = [start]
	while start != stop:
		path.append(tree[start])
		start = tree[start]
	return path

# Random link
initial_link = urllib.request.urlopen( "https://en.wikipedia.org" + "/wiki/Special:Random").geturl().split('.org')[1]
#initial_link = "/wiki/Special:Random"
target_link = "/wiki/Adolf_Hitler"

current_link = initial_link
previous_link = initial_link
explored_links = 0
# link : coming from
tree = {}
print("Searching path from {} to {}.".format(initial_link,target_link))
start_time = datetime.datetime.now()

# Build frontier
frontier = get_links(initial_link)
for f in frontier:
	tree[f] = previous_link

while target_link not in frontier:
	if len(frontier) == 0:
		print("Path between {} and {} could not be found...".format(initial_link,target_link))
		exit(0)

	# Take the first link and explore the page
	current_link = frontier.pop(0) # Shortest path
	#current_link = frontier.pop(random.randint(0,len(frontier))) # Not shortest path but faster convergence

	#print("*INFO* Size of frontier : {}, Links in graph : {}".format(len(frontier),len(tree)))
	print("Exploring : %s" % current_link)
	discovered = get_links(current_link)
	explored_links += 1

	# Add to tree
	next_in_front = []
	for d in discovered:
		if d not in tree:
			tree[d] = current_link
			if d not in frontier:
				next_in_front.append(d)

	frontier += next_in_front
stop_time = datetime.datetime.now()

print("********************")
print("Path found after exploring {} links.".format(explored_links))
print("Time of execution : %s" % str(stop_time-start_time))
print("Size of graph : {}".format(len(tree)))
steps = get_steps(target_link,initial_link,tree)
print("There is %i steps:" %len(steps))
for x in steps:
	print(x)

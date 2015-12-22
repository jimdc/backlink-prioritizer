import json, sys, urllib.request, ast, codecs
from urllib.parse import quote 

list_o_links = []

#this function from Jelle Fransen of StackOverflow to handle Windows' limited console output
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

def getbacklinks (blc):
	fullurl = "http://en.wikipedia.org/w/api.php?action=query&list=backlinks&bltitle=" + sys.argv[1] + "&blnamespace=0&blfilterredir=nonredirects&bllimit=500&format=json"
	if blc is not None:
		fu = fullurl + "&blcontinue=" + blc
	else:
		fu = fullurl
		
	response = urllib.request.urlopen(fu).read().decode('utf-8')
	data = json.loads(response)
	backlinks = data["query"]["backlinks"]
	for backlink in backlinks:
		list_o_links.append([backlink["title"], -1])

	try: 
		blcontinue = data["continue"]["blcontinue"]
		getbacklinks(blcontinue)
	except KeyError as K:
		return

def last90views (article):
	response = urllib.request.urlopen('http://stats.grok.se/json/en/latest90/' + quote(article)).read().decode()
	data = json.loads(response)
	totalviews = 0
	for dates in data["daily_views"]:
		totalviews = totalviews + data["daily_views"][dates]
	return totalviews
	
workinglistname = sys.argv[1] + "_(wlh).txt"
try:
	workinglist = codecs.open(workinglistname, "rb", "utf-8")
	for wlline in workinglist:
		list_o_links.append(ast.literal_eval(wlline.strip()))
		
	workinglist.close()
except FileNotFoundError:
	pass

lol_incomplete = []
lolinc_len = 0
lol_complete = []
	
if not list_o_links:
	getbacklinks(None)
	lol_incomplete = list_o_links
	lol_complete = []
	lolinc_len = len(lol_incomplete)
	print("No existing backlinks recorded for " + sys.argv[1] + ": created " + str(lolinc_len) + " new ones")
else:
	lol_incomplete = [x for x in list_o_links if x[1] == -1]
	lol_complete = [x for x in list_o_links if x[1] != -1]
	lolinc_len = len(lol_incomplete)
	print("Found records for " + sys.argv[1] + ": trying to fill in " + str(lolinc_len) + " incomplete entries");
	
try:
	counter = 0 
	for lolindv in lol_incomplete:
		counter += 1
		uprint(str(int(counter/lolinc_len*100)) + "% complete: finding views for " + lolindv[0])
		lolindv[1] = last90views(lolindv[0])
finally:
	merged = lol_incomplete + lol_complete
	sorted_by_views = sorted(merged, key=lambda tup: tup[1], reverse=True)
	with codecs.open(workinglistname, "w+", "utf-8") as workinglist_w:
		for sbv in sorted_by_views:
			print(sbv, file=workinglist_w)
		print("Wrote " + str(len(sbv)) + " entries")

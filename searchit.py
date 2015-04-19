def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0,numloops):
		newranks={}
		for page in graph:
			newrank=(1-d)/npages
			for node in graph:
				if page in graph[node]:
					newrank=newrank+d*ranks[node]/len(graph[node])
			newranks[page]=newrank
		ranks=newranks
    return ranks


def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    depth = {}
    depth[seed] = 1
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled and depth[page] <= 5:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            for outlink in outlinks :
                depth[outlink] = depth[page] + 1
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph


def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""
    
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
        
def add_to_index(index, keyword, url):
    if keyword in index:
        if not url in index[keyword] :
            index[keyword].append(url)
    else:
        index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None
        
def result(index,keyword,ranks) :
    pages = lookup(index, keyword)
    if pages == None :
        print "Searched Keyword not found"
    else :
        lin = {}
        for page in pages :
            lin[page] = ranks[page]
        for each in  sorted(lin, key = lin.get) :
            print each
    return

print "Enter the seed page"
seed = raw_input()
print "Enter a keyword to search"
s = raw_input()
index, graph = crawl_web(seed)
ranks = compute_ranks(graph)
result(index,s,ranks)

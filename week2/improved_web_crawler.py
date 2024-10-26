def basicwebcrawler(seedpage_url,maxpages):
    # Store URLs crawled and their text content
    num_pages_crawled=0
    crawled_urls=[]
    crawled_texts=[]

    # urls which has already been visited
    crawled_urls_set = set()

    # Remaining pages to crawl: start from a seed page URL
    pagestocrawl=[seedpage_url]

    MAX_LINKS_PER_PAGE = 10

    # Process remaining pages until a desired number
    # of pages have been found or until there's no pages to crawl
    while num_pages_crawled<maxpages and len(pagestocrawl)>0:
        # Retrieve the topmost remaining page and parse it
        pagetocrawl_url=pagestocrawl[0]
        print('Getting page:')
        print(pagetocrawl_url)
        pagetocrawl_html=requests.get(pagetocrawl_url)
        pagetocrawl_parsed=bs4.BeautifulSoup(pagetocrawl_html.content,'html.parser')
        
        # Get the text and URLs of the page
        pagetocrawl_text=getpagetext(pagetocrawl_parsed)
        pagetocrawl_urls=getpageurls(pagetocrawl_parsed)

        # Store the URL and content of the processed page
        num_pages_crawled+=1
        crawled_urls.append(pagetocrawl_url)
        crawled_texts.append(pagetocrawl_text)
        crawled_urls_set.add(pagetocrawl_url)

        num_links_to_add = min(len(pagetocrawl_urls), MAX_LINKS_PER_PAGE)
        selected_links = random.sample(pagetocrawl_urls, num_links_to_add)

        # Remove the processed page from remaining pages,
        # but add the new URLs
        pagestocrawl.pop(0)
        for url in selected_links:
            if url not in crawled_urls_set:
                pagestocrawl.append(url)

    return(crawled_urls,crawled_texts)

mycrawled_urls, mycrawled_texts = basicwebcrawler('https://www.sis.uta.fi/~tojape/',10)
from newspaper import Article

class archive:

    def __init__(self, urls):
        self.articles = []
        unique_urls = set(urls)

        i = 1
        f = 0
        for url in unique_urls:
            print("Downloading and parsing article {} of {}... ".format(i, len(unique_urls)), end='\r')
            i += 1
            article = Article(url)
            try:
                article.download()
                article.parse()
                self.articles.append(article)
            except:
                f += 1
        print("Downloading and parsing article {} of {}... Done!".format(i-1, len(unique_urls)))
        print("Skipped {} articles.".format(f))


    def filter(self, sources_path=None, keywords_path=None, do_sources=False, do_keywords=False, scan_text=False):
        if not do_keywords and not do_sources:
            return
        articles_f = []

        if do_sources:
            try:
                sources = []
                for s in open(sources_path, 'r').readlines():
                    sources.append(s[:-1])
                if len(sources) == 0:
                    print("Error: No sources in sources.txt.")
                    exit()
                print("Keeping articles from these sources:")
                for s in sources:
                    print('  ' + s)
            except:
                print("Error: Could not open sources.txt")
                exit()
        if do_keywords:
            try:
                keywords = []
                for kw in open(keywords_path, 'r').readlines():
                    keywords.append(kw[:-1])
                if len(keywords) == 0:
                    print("Error: No keywords in keywords.txt")
                print("Keeping articles with these keywords:")
                for kw in keywords:
                    print('  ' + kw)
            except:
                print("Error: Could not open keywords.txt")
                exit()

        for i in self.articles:
            added = False
            # check sources
            if do_sources:
                for s in sources:
                    if s in i.url and not added:
                        articles_f.append(i)
                        added = True
                        continue
            # if not yet added
            if do_keywords and not added:
                for kw in keywords:
                    if (kw in i.url or kw in i.title) and not added:
                        articles_f.append(i)
                        added = True
                        continue
                    elif scan_text and not added and kw in i.text:
                        articles_f.append(i)
                        added = True
                        continue

        if do_sources or do_keywords:
            print("Kept {} articles.".format(len(articles_f)))
            self.articles = articles_f


    def to_csv(self, filename):
        with open(filename, 'w') as f:

            f.write("title,date,authors,url\n")

            for article in self.articles:
                f.write("\"" + article.title.replace('\"', '\'') + "\",")

                if article.publish_date is not None:
                    f.write(\
                        str(article.publish_date.month) + "/" +\
                        str(article.publish_date.day) + "/" +\
                        str(article.publish_date.year) + ",\"")
                else:
                    f.write(",\"")

                for j in range(0, len(article.authors)):
                    f.write(article.authors[j])
                    if len(article.authors) > 1 and j < len(article.authors)-1:
                        f.write(", ")
                f.write("\",")

                f.write(article.url + "\n")
            print("Output saved to " + filename + ".")

try:
    from newspaper import Article
except:
    ("Newspaper not installed. Try: pip3 install newspaper3k")

class article_archive:

    def __init__(self, urls):
        self.articles = []
        unique_urls = set(urls)
        for url in unique_urls:
            self.articles.append(Article(url))

    def filter_sources(self, allowed_sources_path):
        with open(allowed_sources_path, 'r') as f:
            sources = f.read().splitlines()
            print("Selecting articles from:")
            for source in sources:
                print("\t" + source)
            filtered_articles = []
            for article in self.articles:
                for source in sources:
                    if source in article.url:
                        filtered_articles.append(article)
            self.articles = filtered_articles

    def to_csv(self, filename):
        with open(filename, 'w') as f:
            i = 1
            print("Downloading and parsing " + str(len(self.articles)) + " articles. This may take a while...")

            f.write("title,date,authors,url\n")

            for article in self.articles:

                percent = i/len(self.articles)
                print("{:.1%} complete".format(percent), end='\r')
                i = i + 1

                try:
                    article.download()
                    article.parse()
                except:
                    f.write(",,," + article.url + "\n")
                    continue

                title = article.title
                for char in title:
                    if ord(char) > 127 or ord(char) < 32:
                        title = title.replace(char, "")
                title = title.replace(",", "")
                f.write(title + ",")

                if article.publish_date is not None:
                    f.write(\
                        str(article.publish_date.month) + "/" +\
                        str(article.publish_date.day) + "/" +\
                        str(article.publish_date.year) + ",")
                else:
                    f.write(",")

                for j in range(0, len(article.authors)):
                    f.write(article.authors[j])
                    if len(article.authors) > 1 and j < len(article.authors)-1:
                        f.write("; ")
                f.write(",")

                f.write(article.url + "\n")
            print("\nDone! Output saved to " + filename + ".")

